# Git Memory Skill

🧠 基于 Git 的 AI 记忆管理 - **支持 OpenClaw 和 Hermes**

![](https://camo.githubusercontent.com/dd1b51eac051b316a3173585bc64d36e19fa2d4e90a4581734cc292c175130f1/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f76657273696f6e2d322e312e302d626c75652e737667)
![](https://camo.githubusercontent.com/8bb50fd2278f18fc326bf71f6e88ca8f884f72f179d3e555e20ed30157190d0d/68747470733a2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d4d49542d677265656e2e737667)

## 🚀 快速安装

### OpenClaw 用户

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/javamagong/claw-git-memory-skill/main/quick-install.sh)
```

### Hermes Agent 用户

```bash
# 克隆仓库
git clone git@github.com:javamagong/claw-git-memory-skill.git
cd claw-git-memory-skill

# 运行安装脚本
bash hermes/install.sh ~/my-claw-memory

# 重启 Hermes
hermes gateway restart
```

## 📋 功能特性

| 功能 | OpenClaw | Hermes |
|------|----------|--------|
| 自动版本控制 | ✅ Hooks | ✅ Provider |
| 会话隔离 | ✅ | ✅ |
| 自动提交 | ✅ | ✅ |
| 自动推送 | ✅ | ✅ |
| 远程同步 | ✅ | ✅ |
| 工具接口 | ❌ | ✅ gitmemory_* |

## 🏗️ 项目结构

```
claw-git-memory-skill/
├── .openclaw/hooks/     # OpenClaw 钩子 (TypeScript)
│   ├── git-memory-session-start.ts
│   └── git-memory-session-end.ts
├── hermes/              # Hermes 提供器 (Python)
│   ├── __init__.py
│   ├── provider.py
│   └── install.sh
└── docs/                # 文档
```

## 📖 使用说明

### OpenClaw

全自动，无需手动操作：
- 会话开始 → 自动拉取最新记忆
- 对话过程 → 自动保存记忆
- 会话结束 → 自动提交 + 推送

### Hermes

**可用工具：**

| 工具 | 说明 |
|------|------|
| `gitmemory_status` | 检查同步状态 |
| `gitmemory_commit` | 提交记忆变更 |
| `gitmemory_push` | 推送到远程 |
| `gitmemory_pull` | 拉取最新记忆 |

**使用示例：**
```
你: 检查记忆同步状态
Hermes: *调用 gitmemory_status*
当前状态：
- 仓库: ~/my-claw-memory
- 分支: master
- 待提交: 3 个文件
- 最后提交: session: abc123 at 2026-04-10 12:00
```

## 🔧 配置说明

### OpenClaw (TOOLS.md)

```yaml
git-memory:
  repo: /workspace/projects/workspace
  remote: git@github.com:yourname/repo.git
  auto-commit: true
  auto-push: false
```

### Hermes (~/.hermes/config.yaml)

```yaml
memory:
  provider: gitmemory
  repo: ~/my-claw-memory
  auto_commit: true
  auto_push: true
```

或设置环境变量：
```bash
export GIT_MEMORY_REPO=~/my-claw-memory
```

## 📁 记忆仓库结构

```
my-claw-memory/
├── MEMORY.md          # 全局记忆
├── USER.md            # 用户档案
├── SOUL.md            # 人格设定
├── TOOLS.md           # 环境配置
├── SECRET.example.md  # 敏感信息模板
├── memory/            # 日常记忆
│   ├── 2026-04-10.md
│   └── ...
├── subsystems/        # 子系统记忆
│   ├── trading/
│   └── conversation/
└── .git/              # Git 仓库
```

## 🔄 多设备同步

```
┌─────────────────┐
│  Git 远程仓库    │  (GitHub/Gitee)
│                 │
└────────┬────────┘
         │ git push/pull
    ┌────┴────┬──────────┐
    ↓         ↓          ↓
┌───────┐ ┌────────┐ ┌──────────┐
│ 扣子   │ │ 腾讯云  │ │ OpenClaw │
│ 云电脑 │ │ Hermes │ │ (原环境)  │
└───────┘ └────────┘ └──────────┘
```

所有设备共享同一个记忆仓库，保持记忆同步。

## 📋 更新日志

### v2.1.0 (2026-04-10)
- ✅ 添加 Hermes Agent 支持
- ✅ Python Provider 及 gitmemory_* 工具
- ✅ 统一记忆仓库结构
- ✅ 多设备同步支持

### v2.0.0 (2026-03-22)
- 自动触发机制
- 子系统记忆
- Schema-Driven Merge
- 冲突检测
- OpenClaw Hook 集成

详见 [CHANGELOG.md](CHANGELOG.md)

## 📚 文档

- [English README](README.md)
- [中文文档](README_zh.md)
- [子系统指南](docs/subsystems.md)
- [冲突解决](docs/conflict-resolution.md)
- [多设备同步](docs/git-memory/GIT_MEMORY_MULTI_DEVICE_SYNC.md)

## 🤝 参与贡献

欢迎贡献代码：
1. Fork 本仓库
2. 创建特性分支
3. 添加测试
4. 提交 Pull Request

## 📄 许可证

MIT License

---

*版本: 2.1.0 | 由 JavaMaGong & A小二 构建*
