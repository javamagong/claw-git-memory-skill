# Git Memory Skill

🧠 Git-based Memory Management for AI Agents - **Supports OpenClaw and Hermes**

![](https://camo.githubusercontent.com/dd1b51eac051b316a3173585bc64d36e19fa2d4e90a4581734cc292c175130f1/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f76657273696f6e2d322e312e302d626c75652e737667)
![](https://camo.githubusercontent.com/8bb50fd2278f18fc326bf71f6e88ca8f884f72f179d3e555e20ed30157190d0d/68747470733a2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d4d49542d677265656e2e737667)

## 🚀 Quick Install

### For OpenClaw

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/javamagong/claw-git-memory-skill/main/quick-install.sh)
```

### For Hermes Agent

```bash
# Clone the repository
git clone git@github.com:javamagong/claw-git-memory-skill.git
cd claw-git-memory-skill

# Run installer
bash hermes/install.sh ~/my-claw-memory

# Restart Hermes
hermes gateway restart
```

## 📋 Features

| Feature | OpenClaw | Hermes |
|---------|----------|--------|
| Auto version control | ✅ Hooks | ✅ Provider |
| Session isolation | ✅ | ✅ |
| Auto commit | ✅ | ✅ |
| Auto push | ✅ | ✅ |
| Remote sync | ✅ | ✅ |
| Tool access | ❌ | ✅ gitmemory_* |

## 🏗️ Architecture

```
claw-git-memory-skill/
├── .openclaw/hooks/     # OpenClaw hooks (TypeScript)
│   ├── git-memory-session-start.ts
│   └── git-memory-session-end.ts
├── hermes/              # Hermes provider (Python)
│   ├── __init__.py
│   ├── provider.py
│   └── install.sh
└── docs/                # Documentation
```

## 📖 Usage

### OpenClaw

Automatic - no manual operations needed:
- Session start → Auto-pull latest memory
- During conversation → Auto-save memory
- Session end → Auto-commit + push

### Hermes

**Tools available:**

| Tool | Description |
|------|-------------|
| `gitmemory_status` | Check git memory status |
| `gitmemory_commit` | Commit pending changes |
| `gitmemory_push` | Push to remote |
| `gitmemory_pull` | Pull from remote |

**Example in Hermes chat:**
```
You: Check memory sync status
Hermes: *uses gitmemory_status*
Current status:
- Repo: ~/my-claw-memory
- Branch: master
- Changes: 3 pending
- Last commit: session: abc123 at 2026-04-10 12:00
```

## 🔧 Configuration

### OpenClaw

Add to `TOOLS.md`:
```yaml
git-memory:
  repo: /workspace/projects/workspace
  remote: git@github.com:yourname/repo.git
  auto-commit: true
  auto-push: false
```

### Hermes

Add to `~/.hermes/config.yaml`:
```yaml
memory:
  provider: gitmemory
  repo: ~/my-claw-memory
  auto_commit: true
  auto_push: true
```

Or set environment variable:
```bash
export GIT_MEMORY_REPO=~/my-claw-memory
```

## 📁 Memory Repository Structure

```
my-claw-memory/
├── MEMORY.md          # Global memory
├── USER.md            # User profile
├── SOUL.md            # Agent personality
├── TOOLS.md           # Environment config
├── SECRET.example.md  # Secrets template
├── memory/            # Daily memory
│   ├── 2026-04-10.md
│   └── ...
├── subsystems/        # Subsystem memory
│   ├── trading/
│   └── conversation/
└── .git/              # Git repository
```

## 🔄 Multi-Device Sync

```
┌─────────────────┐
│  Git Remote      │  (GitHub/Gitee)
│  Repository      │
└────────┬────────┘
         │ git push/pull
    ┌────┴────┬──────────┐
    ↓         ↓          ↓
┌───────┐ ┌────────┐ ┌──────────┐
│ 扣子   │ │ 腾讯云  │ │ OpenClaw │
│ 云电脑 │ │ Hermes │ │ (原环境)  │
└───────┘ └────────┘ └──────────┘
```

All devices share the same memory repository, keeping memories in sync.

## 📋 Changelog

### v2.1.0 (2026-04-10)
- ✅ Added Hermes Agent support
- ✅ Python provider with gitmemory_* tools
- ✅ Unified memory repository structure
- ✅ Multi-device sync support

### v2.0.0 (2026-03-22)
- Auto-trigger mechanism
- Subsystem memory
- Schema-Driven Merge
- Conflict detection
- OpenClaw Hook Integration

See [CHANGELOG.md](CHANGELOG.md) for full history.

## 📚 Documentation

- [English README](README.md)
- [中文文档](README_zh.md)
- [Subsystem Guide](docs/subsystems.md)
- [Conflict Resolution](docs/conflict-resolution.md)
- [Multi-Device Sync](docs/git-memory/GIT_MEMORY_MULTI_DEVICE_SYNC.md)

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 📄 License

MIT License

---

*Version: 2.1.0 | Built by JavaMaGong & A小二 (OpenClaw/Hermes assistant)*
