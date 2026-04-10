# Git Memory Skill

> 🧠 AI 记忆自动版本管理 - 支持 OpenClaw 和 Hermes

## 描述

用 Git 版本控制管理 AI 记忆系统，解决 AI 失忆问题。
支持全局记忆、子系统记忆、会话隔离、自动提交、远程同步。

## 支持平台

| 平台 | 实现方式 | 工具 |
|------|---------|------|
| OpenClaw | TypeScript Hooks | 自动触发 |
| Hermes | Python Provider | gitmemory_* tools |

## 激活时机

### OpenClaw
- 会话开始时自动激活（读取最新记忆）
- 用户提到"记住这个"、"别忘了"、"记忆"等关键词
- 交易/操作完成后自动记录
- 会话结束时自动合并

### Hermes
- 配置 `memory.provider: gitmemory` 后自动激活
- 提供 `gitmemory_status/commit/push/pull` 工具
- 会话结束时自动 commit + push

## 核心功能

1. **记忆版本控制** - 所有记忆变更可追溯
2. **会话隔离** - 每个会话独立分支
3. **自动提交** - AI 自动写 commit message
4. **冲突检测** - 多会话冲突显式提示
5. **远程同步** - 推送到 GitHub/Gitee 备份
6. **多设备同步** - 共享记忆仓库

## 安装方法

### OpenClaw
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/javamagong/claw-git-memory-skill/main/quick-install.sh)
```

### Hermes
```bash
git clone git@github.com:javamagong/claw-git-memory-skill.git
cd claw-git-memory-skill
bash hermes/install.sh ~/my-claw-memory
```

## 配置

### OpenClaw (TOOLS.md)
```yaml
git-memory:
  repo: /workspace/projects/workspace
  remote: git@github.com:yourname/repo.git
  auto-commit: true
```

### Hermes (~/.hermes/config.yaml)
```yaml
memory:
  provider: gitmemory
  repo: ~/my-claw-memory
  auto_commit: true
  auto_push: true
```

## Hermes 工具

| 工具 | 说明 |
|------|------|
| `gitmemory_status` | 检查同步状态 |
| `gitmemory_commit` | 提交记忆变更 |
| `gitmemory_push` | 推送到远程 |
| `gitmemory_pull` | 拉取最新记忆 |

## 作者

JavaMaGong & A小二

## 版本

2.1.0

## 许可证

MIT
