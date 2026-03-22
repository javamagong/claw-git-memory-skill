# Git Memory Skill

> 🧠 Git-based Memory Management for OpenClaw - **One-command install, zero-config usage**

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://clawhub.com/skills/git-memory)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🚀 Quick Install

### One-Command Install

```bash
bash skills/git-memory/quick-install.sh
```

**That's it!** No configuration needed, ready to use immediately.

### Restart OpenClaw

```bash
sh /workspace/projects/scripts/restart.sh
```

### Usage

**No manual operations needed!** Memory is automatically versioned:

- ✅ Session start → Auto-create branch
- ✅ During conversation → Auto-save memory
- ✅ Session end → Auto-commit
- ✅ History → View/restore anytime

---

## 📦 Optional: Configure Remote Sync

**Only needed for multi-device sync**

```bash
python3 skills/git-memory/config-wizard.py
```

Follow the prompts:
1. Device type (local/cloud)
2. Device name
3. GitHub repository URL

**Works without config!** Local version control works perfectly.

---

## ⚡ Auto-Trigger Mechanism

Git Memory automatically activates in these scenarios:

| Trigger | Action |
|---------|--------|
| **Session Start** | Pull latest memory from main branch |
| **User says "remember this"** | Save to current session branch |
| **Trading/Operation Complete** | Auto-commit transaction record |
| **Session End** | Merge to main + push (if remote configured) |
| **Conflict Detected** | Explicit prompt with merge options |

### Manual Commands

```bash
# Save memory manually
git-memory save "Remember to review trading rules before market open"

# View memory history
git-memory log

# Search memory
git-memory search "trading"

# Initialize (first-time only)
git-memory init
```

---

## 📊 Check Status

```bash
# Git commit history
git log --oneline -10

# Sync status (if remote configured)
python3 -c "
import sys
sys.path.insert(0, 'skills/git-memory/lib')
from git_memory import GitMemorySkill
skill = GitMemorySkill('.')
print(skill.get_sync_status())
"
```

---

## User Experience

### Installation (40 seconds)

1. One-command install (30 sec)
2. Restart OpenClaw (10 sec)
3. ✅ Done

### Daily Usage (Invisible)

- ❌ **No** manual git add
- ❌ **No** manual git commit
- ❌ **No** manual branch management
- ✅ **Auto** save memory
- ✅ **Auto** versioning
- ✅ **Auto** merge conflicts

### Use Cases

| User Type | Operations Needed | Time |
|-----------|------------------|------|
| New install | Install + restart | 40 sec |
| Existing memory | Install + restart + confirm migration | 1 min |
| Daily use | None (fully automatic) | 0 sec |

---

## Core Features

- ✅ **Auto Version Control** - All memory changes auto-committed to Git
- ✅ **Session Isolation** - Each session has independent branch
- ✅ **History Tracking** - View/restore to any historical version
- ✅ **Remote Backup** - Optional sync to GitHub/GitLab
- ✅ **Smart Merge** - Schema-driven JSON merge
- ✅ **Precise Search** - Multi-dimensional filtering
- ✅ **Conflict Detection** - Explicit prompts for multi-session conflicts

---

## 📁 Directory Structure

```
/workspace/
├── MEMORY.md                    # Global memory
├── memory/                      # Daily memory
│   ├── 2026-03-22.md           # Today's log
│   └── 2026-03-21.md           # Yesterday's log
├── subsystems/                  # Subsystem memory
│   ├── trading/                 # Stock trading (cost, holdings, transactions)
│   ├── conversation/            # Conversation context
│   ├── skills/                  # Skills learning
│   └── tools/                   # Tool configuration
└── .git/                        # Git repository
```

### Subsystems

| Subsystem | Purpose | Example |
|-----------|---------|---------|
| `trading/` | Stock transactions, holdings, P/L | Cost basis, buy/sell records |
| `conversation/` | Long-running conversation context | Project preferences, user info |
| `skills/` | Learned skills and patterns | Tool usage, workflows |
| `tools/` | Environment-specific config | SSH hosts, camera names, TTS voices |

See [docs/subsystems.md](docs/subsystems.md) for details.

---

## 🔧 Configuration

### Custom Merge Strategy

Create `.mergerc.yaml` in subsystem directory:

```yaml
version: 1
fields:
  transactions:
    merge_strategy: union
    id_fields: ['id']
  
  holdings:
    merge_strategy: deep_merge

_default:
  merge_strategy: local
```

### Configure Remote Backup (Optional)

```bash
git remote add origin https://github.com/yourname/memory.git
git push -u origin main
```

### TOOLS.md Configuration

```yaml
git-memory:
  repo: /workspace/projects/workspace
  remote: git@github.com:yourname/repo.git  # Optional
  auto-commit: true
  auto-push: false  # Optional, default: no force push
```

---

## ⚠️ Conflict Resolution

When multiple sessions modify memory simultaneously:

1. **Detection** - Git Memory detects divergent branches
2. **Schema-Aware Merge** - Attempts automatic merge using `.mergerc.yaml`
3. **Explicit Prompt** - If auto-merge fails, shows conflict with options:
   - Accept incoming changes
   - Keep local changes
   - Manual merge

See [docs/conflict-resolution.md](docs/conflict-resolution.md) for detailed workflow.

---

## Architecture Design

See [Feishu Design Doc](https://feishu.cn/docx/...)

### Core Decisions

1. **Schema-Driven Merge** - Configuration-driven JSON merge
2. **Worktree Lifecycle** - Auto-cleanup of stale worktrees
3. **Pure Git Search** - Git-based search, no SQLite

---

## FAQ

### Q: Do I need to know Git?

**A:** No! All Git operations are automatic.

### Q: Will I lose data?

**A:** No! Git version control, all history is recoverable.

### Q: Do I need to configure remote repository?

**A:** Optional! Local usage works perfectly fine.

### Q: Will it affect performance?

**A:** Minimal impact! Git operations run asynchronously in background.

### Q: Will multiple sessions conflict?

**A:** No! Each session has independent branch, auto-merged with conflict detection.

---

## Development

### Run Tests

```bash
cd skills/git-memory
pytest tests/
```

### View Logs

```bash
tail -f logs/git-memory.log
```

---

## References

- [TaG (Trading as Git)](https://www.traderalice.com/blog/trading-as-git-intro)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Git Documentation](https://git-scm.com/docs)

---

## License

MIT License

---

*Version: 1.1.0 | Last updated: 2026-03-22 | Built by 张明春 & A 小二 (OpenClaw assistant) via vibe coding 🫡*
