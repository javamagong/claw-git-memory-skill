"""GitMemory provider for Hermes Agent - File-based memory with Git sync."""
from __future__ import annotations
import os
import subprocess
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from agent.memory_provider import MemoryProvider

logger = logging.getLogger(__name__)


class GitMemoryProvider(MemoryProvider):
    """Git-backed memory provider that reads/writes markdown files and syncs via git."""
    
    def __init__(self):
        self.repo_path: Optional[Path] = None
        self.session_id: str = ""
        self._initialized = False
    
    @property
    def name(self) -> str:
        return "gitmemory"
    
    def is_available(self) -> bool:
        """Check if repo path exists and is a git repo."""
        return True  # Will be checked in initialize()
    
    def initialize(self, session_id: str, **kwargs) -> None:
        """Initialize the provider."""
        self.session_id = session_id
        hermes_home = kwargs.get("hermes_home", "~/.hermes")
        
        # Read config from hermes config
        import yaml
        config_path = Path(hermes_home).expanduser() / "config.yaml"
        if config_path.exists():
            with open(config_path) as f:
                config = yaml.safe_load(f)
                repo_path = config.get("memory", {}).get("repo", "~/my-claw-memory")
                self.repo_path = Path(repo_path).expanduser()
        else:
            self.repo_path = Path("~/my-claw-memory").expanduser()
        
        # Ensure repo exists
        if not self.repo_path.exists():
            logger.warning(f"GitMemory repo not found: {self.repo_path}")
            return
        
        # Pull latest
        try:
            subprocess.run(["git", "pull"], cwd=self.repo_path, capture_output=True, check=False)
            logger.info(f"GitMemory initialized: {self.repo_path}")
            self._initialized = True
        except Exception as e:
            logger.error(f"GitMemory init failed: {e}")
    
    def system_prompt_block(self) -> str:
        """Return instructions for using this memory."""
        if not self._initialized:
            return ""
        return "You have access to persistent memory stored in markdown files. Use the memory tool to read/write."
    
    def prefetch(self, query: str, *, session_id: str = "") -> str:
        """Recall relevant context from memory files."""
        if not self._initialized:
            return ""
        
        results = []
        for md_file in self.repo_path.rglob("*.md"):
            try:
                content = md_file.read_text()
                if query.lower() in content.lower():
                    results.append(f"--- {md_file.name} ---\n{content[:500]}\n")
            except:
                continue
        
        if results:
            return f"[Memory Context]\n{''.join(results[:3])}\n"
        return ""
    
    def sync_turn(self, user_content: str, assistant_content: str, *, session_id: str = "") -> None:
        """Sync after turn - commit if there are changes."""
        if not self._initialized:
            return
        
        try:
            result = subprocess.run(["git", "status", "--porcelain"], cwd=self.repo_path, capture_output=True, text=True)
            if result.stdout.strip():
                subprocess.run(["git", "add", "-A"], cwd=self.repo_path, check=True)
                subprocess.run(["git", "commit", "-m", f"Memory update: {session_id[:8]}"], cwd=self.repo_path, check=False)
                subprocess.run(["git", "push"], cwd=self.repo_path, check=False)
                logger.info("GitMemory synced")
        except Exception as e:
            logger.error(f"GitMemory sync failed: {e}")
    
    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Return tool schemas for memory operations."""
        if not self._initialized:
            return []
        
        return [
            {
                "name": "memory",
                "description": "Read or write persistent memory files. Use 'read' to get content, 'write' to save.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["read", "write", "search"],
                            "description": "Action to perform"
                        },
                        "filename": {
                            "type": "string",
                            "description": "File to read/write (e.g., 'MEMORY.md', 'USER.md')"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write (for write action)"
                        },
                        "query": {
                            "type": "string",
                            "description": "Search query (for search action)"
                        }
                    },
                    "required": ["action"]
                }
            }
        ]
    
    def handle_tool_call(self, tool_name: str, args: Dict[str, Any], **kwargs) -> str:
        """Handle memory tool calls."""
        import json
        if tool_name != "memory":
            return json.dumps({"error": "Unknown tool"})
        
        action = args.get("action", "read")
        
        if action == "read":
            filename = args.get("filename", "MEMORY.md")
            filepath = self.repo_path / filename
            if filepath.exists():
                return json.dumps({"content": filepath.read_text()})
            return json.dumps({"error": "File not found"})
        
        elif action == "write":
            filename = args.get("filename", "MEMORY.md")
            content = args.get("content", "")
            filepath = self.repo_path / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(content)
            return json.dumps({"success": True})
        
        elif action == "search":
            query = args.get("query", "")
            results = []
            for md_file in self.repo_path.rglob("*.md"):
                try:
                    content = md_file.read_text()
                    if query.lower() in content.lower():
                        results.append(str(md_file.relative_to(self.repo_path)))
                except:
                    continue
            return json.dumps({"files": results})
        
        return json.dumps({"error": "Unknown action"})
    
    def shutdown(self) -> None:
        """Final sync on shutdown."""
        self.sync_turn("", "", session_id=self.session_id)


# ---------------------------------------------------------------------------
# Plugin entry point
# ---------------------------------------------------------------------------

def register(ctx) -> None:
    """Register GitMemory as a memory provider plugin."""
    ctx.register_memory_provider(GitMemoryProvider())
