"""GitMemoryProvider — Git-backed memory with auto-sync for Hermes.

A Hermes memory provider that stores memory in a Git repository
and automatically commits/pushes changes.

Usage:
    1. Configure in ~/.hermes/config.yaml:
       memory:
         provider: gitmemory
         repo: ~/my-claw-memory

    2. Or set environment variable:
       export GIT_MEMORY_REPO=~/my-claw-memory

    3. Restart Hermes - memory will be auto-synced via git
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from agent.memory_provider import MemoryProvider

logger = logging.getLogger(__name__)


class GitMemoryProvider(MemoryProvider):
    """Git-backed memory with automatic version control.

    Uses a Git repository (like my-claw-memory) as the memory store.
    Auto-commits on memory writes and pushes on session end.
    """

    def __init__(self, hermes_home: str = None):
        self._hermes_home = hermes_home
        self._repo_path: Optional[str] = None
        self._branch: str = "master"
        self._has_remote: bool = False
        self._remote_url: str = ""
        self._pending_changes: List[str] = []
        self._session_id: str = ""
        self._initialized: bool = False
        self._auto_commit: bool = True
        self._auto_push: bool = True

    @property
    def name(self) -> str:
        return "gitmemory"

    def is_available(self) -> bool:
        """Check if gitmemory is configured."""
        repo_path = self._get_repo_path()
        return bool(repo_path) and os.path.isdir(repo_path)

    def _get_repo_path(self) -> str:
        """Get repo path from config or environment."""
        # Priority: env var > config file > default
        repo_path = os.environ.get("GIT_MEMORY_REPO", "")
        if repo_path:
            return os.path.expanduser(repo_path)

        # Try hermes config
        if self._hermes_home:
            config_path = os.path.join(self._hermes_home, "config.yaml")
        else:
            config_path = os.path.expanduser("~/.hermes/config.yaml")

        if os.path.exists(config_path):
            try:
                import yaml
                with open(config_path, "r") as f:
                    config = yaml.safe_load(f) or {}
                repo_path = config.get("memory", {}).get("repo", "")
                if repo_path:
                    return os.path.expanduser(repo_path)
            except Exception as e:
                logger.debug(f"Failed to read config: {e}")

        # Default
        return os.path.expanduser("~/my-claw-memory")

    def initialize(self, session_id: str, **kwargs) -> None:
        """Initialize gitmemory provider for a session."""
        self._session_id = session_id
        self._hermes_home = kwargs.get("hermes_home", os.path.expanduser("~/.hermes"))

        # Get repo path
        self._repo_path = self._get_repo_path()
        logger.info(f"GitMemory: Using repo at {self._repo_path}")

        # Verify it's a git repo
        git_dir = os.path.join(self._repo_path, ".git")
        if not os.path.exists(git_dir):
            logger.warning(f"GitMemory: {self._repo_path} is not a git repository")
            logger.info("GitMemory: Run 'git init' in the directory first")
            return

        # Detect branch
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self._repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                self._branch = result.stdout.strip()
        except Exception:
            pass

        # Check for remote
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=self._repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                self._has_remote = True
                self._remote_url = result.stdout.strip()
                logger.info(f"GitMemory: Remote configured: {self._remote_url}")
        except Exception as e:
            logger.debug(f"Failed to check remote: {e}")

        # Fetch latest from remote (non-blocking)
        if self._has_remote:
            self._fetch_async()

        self._initialized = True
        logger.info(f"GitMemory: Initialized successfully")

    def _fetch_async(self) -> None:
        """Fetch from remote (fire and forget)."""
        try:
            subprocess.run(
                ["git", "fetch", "origin"],
                cwd=self._repo_path,
                capture_output=True,
                timeout=60
            )
            logger.debug("GitMemory: Fetched from remote")
        except Exception as e:
            logger.debug(f"GitMemory: Fetch failed: {e}")

    def system_prompt_block(self) -> str:
        """Return info about gitmemory in system prompt."""
        if not self._initialized:
            return ""
        return f"""
<gitmemory>
Memory is stored in a Git repository at {self._repo_path}.
Branch: {self._branch}
Remote: {self._remote_url or 'not configured'}
Changes are automatically versioned and synced.
</gitmemory>
"""

    def prefetch(self, query: str, *, session_id: str = "") -> str:
        """No query-based recall for gitmemory (handled by builtin memory)."""
        return ""

    def sync_turn(self, user_content: str, assistant_content: str, *, session_id: str = "") -> None:
        """No auto-sync per turn (too noisy)."""
        pass

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Return tool schemas for gitmemory."""
        return [
            {
                "name": "gitmemory_status",
                "description": "Check git memory status - pending changes, sync state, branch info",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "gitmemory_commit",
                "description": "Commit pending memory changes to git. Use this after important memory updates.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Optional commit message. Auto-generated if not provided."
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "gitmemory_push",
                "description": "Push committed changes to remote repository. Requires remote to be configured.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "gitmemory_pull",
                "description": "Pull latest changes from remote repository. Useful for multi-device sync.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]

    def handle_tool_call(self, tool_name: str, args: Dict[str, Any], **kwargs) -> str:
        """Handle gitmemory tool calls."""
        if tool_name == "gitmemory_status":
            return json.dumps(self._get_status(), indent=2)
        elif tool_name == "gitmemory_commit":
            return json.dumps(self._commit(args.get("message", "")), indent=2)
        elif tool_name == "gitmemory_push":
            return json.dumps(self._push(), indent=2)
        elif tool_name == "gitmemory_pull":
            return json.dumps(self._pull(), indent=2)
        else:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})

    def on_memory_write(self, action: str, target: str, content: str) -> None:
        """Called when built-in memory tool writes an entry.

        Auto-stage the changed files and optionally commit.
        """
        if not self._initialized:
            return

        logger.info(f"GitMemory: Memory write - {action} on {target}")

        # Stage the relevant files
        try:
            subprocess.run(
                ["git", "add", "-A"],
                cwd=self._repo_path,
                capture_output=True,
                timeout=10
            )
            self._pending_changes.append(f"{action}:{target}")

            # Auto commit if enabled and significant change
            if self._auto_commit and len(self._pending_changes) >= 3:
                self._commit(f"auto: memory updates")
                self._pending_changes = []

        except Exception as e:
            logger.warning(f"GitMemory: Failed to stage files: {e}")

    def on_session_end(self, messages: List[Dict[str, Any]]) -> None:
        """Called when session ends - auto commit and push."""
        if not self._initialized:
            return

        logger.info("GitMemory: Session end - syncing...")

        # Check for uncommitted changes
        status = self._get_status()
        if not status.get("has_changes", False):
            logger.info("GitMemory: No uncommitted changes")
            return

        # Generate commit message with session summary
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        commit_msg = f"session: {self._session_id[:8]} at {timestamp}"

        # Auto commit
        commit_result = self._commit(commit_msg)
        if not commit_result.get("success", False):
            logger.warning(f"GitMemory: Commit failed: {commit_result.get('error')}")
            return

        # Auto push if remote configured
        if self._has_remote and self._auto_push:
            push_result = self._push()
            if push_result.get("success", False):
                logger.info("GitMemory: Successfully pushed to remote")
            else:
                logger.warning(f"GitMemory: Push failed: {push_result.get('error')}")

    def shutdown(self) -> None:
        """Clean shutdown - flush pending changes."""
        if self._pending_changes:
            logger.info(f"GitMemory: Shutdown with {len(self._pending_changes)} pending changes")
            self._commit("shutdown: final sync")

    # -- Helper methods -------------------------------------------------------

    def _get_status(self) -> Dict[str, Any]:
        """Get git status."""
        if not self._initialized:
            return {"error": "Not initialized", "initialized": False}

        try:
            # Get porcelain status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self._repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            changes = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]

            # Get branch info
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self._repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            current_branch = branch_result.stdout.strip() or self._branch

            # Get last commit
            log_result = subprocess.run(
                ["git", "log", "-1", "--oneline"],
                cwd=self._repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            last_commit = log_result.stdout.strip() if log_result.returncode == 0 else "N/A"

            return {
                "initialized": True,
                "repo_path": self._repo_path,
                "branch": current_branch,
                "has_remote": self._has_remote,
                "remote_url": self._remote_url,
                "has_changes": len(changes) > 0,
                "changes": changes,
                "last_commit": last_commit,
                "pending_writes": len(self._pending_changes)
            }
        except Exception as e:
            return {"error": str(e), "initialized": self._initialized}

    def _commit(self, message: str = "") -> Dict[str, Any]:
        """Commit all changes."""
        if not self._initialized:
            return {"success": False, "error": "Not initialized"}

        try:
            # Check if there's anything to commit
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self._repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if not result.stdout.strip():
                return {"success": True, "message": "No changes to commit"}

            # Generate commit message if not provided
            if not message:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = f"auto: memory update at {timestamp}"

            # Stage all changes
            subprocess.run(
                ["git", "add", "-A"],
                cwd=self._repo_path,
                capture_output=True,
                timeout=10
            )

            # Commit
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self._repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                self._pending_changes = []
                return {
                    "success": True,
                    "message": message,
                    "output": result.stdout.strip()
                }
            else:
                # Check if it's "nothing to commit"
                if "nothing to commit" in result.stdout:
                    return {"success": True, "message": "Nothing to commit"}
                return {"success": False, "error": result.stderr or result.stdout}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _push(self) -> Dict[str, Any]:
        """Push to remote."""
        if not self._initialized:
            return {"success": False, "error": "Not initialized"}
        if not self._has_remote:
            return {"success": False, "error": "No remote configured"}

        try:
            result = subprocess.run(
                ["git", "push", "origin", self._branch],
                cwd=self._repo_path,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                return {"success": True, "output": result.stdout.strip()}
            else:
                return {"success": False, "error": result.stderr or "Push failed"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _pull(self) -> Dict[str, Any]:
        """Pull from remote."""
        if not self._initialized:
            return {"success": False, "error": "Not initialized"}
        if not self._has_remote:
            return {"success": False, "error": "No remote configured"}

        try:
            result = subprocess.run(
                ["git", "pull", "origin", self._branch],
                cwd=self._repo_path,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                return {"success": True, "output": result.stdout.strip()}
            else:
                return {"success": False, "error": result.stderr or "Pull failed"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_config_schema(self) -> List[Dict[str, Any]]:
        """Return config fields for hermes memory setup."""
        return [
            {
                "key": "repo",
                "description": "Path to the git memory repository",
                "secret": False,
                "required": True,
                "default": "~/my-claw-memory"
            },
            {
                "key": "auto_commit",
                "description": "Automatically commit memory changes",
                "secret": False,
                "required": False,
                "default": True
            },
            {
                "key": "auto_push",
                "description": "Automatically push to remote on session end",
                "secret": False,
                "required": False,
                "default": True
            }
        ]

    def save_config(self, values: Dict[str, Any], hermes_home: str) -> None:
        """Save config to hermes config.yaml."""
        import yaml

        config_path = os.path.join(hermes_home, "config.yaml")
        config = {}

        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = yaml.safe_load(f) or {}

        if "memory" not in config:
            config["memory"] = {}

        config["memory"]["provider"] = "gitmemory"
        config["memory"]["repo"] = values.get("repo", "~/my-claw-memory")
        config["memory"]["auto_commit"] = values.get("auto_commit", True)
        config["memory"]["auto_push"] = values.get("auto_push", True)

        os.makedirs(hermes_home, exist_ok=True)
        with open(config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False)

        logger.info(f"GitMemory: Config saved to {config_path}")
