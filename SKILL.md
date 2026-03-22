# Git Memory Skill

> 🧠 AI 记忆自动版本管理

## 描述

用 Git 版本控制管理 OpenClaw 记忆系统，解决 AI 失忆问题。
支持全局记忆、子系统记忆、会话隔离、自动提交、远程同步。

## 激活时机

- 会话开始时自动激活（读取最新记忆）
- 用户提到"记住这个"、"别忘了"、"记忆"等关键词
- 交易/操作完成后自动记录
- 会话结束时自动合并

## 核心功能

1. **记忆版本控制** - 所有记忆变更可追溯
2. **会话隔离** - 每个会话独立分支
3. **自动提交** - AI 自动写 commit message
4. **冲突检测** - 多会话冲突显式提示
5. **远程同步** - 推送到 GitHub/GitLab 备份

## 使用方法

### 基础命令

- `git-memory init` - 初始化记忆仓库
- `git-memory save "消息"` - 手动保存记忆
- `git-memory log` - 查看记忆历史
- `git-memory search "关键词"` - 搜索记忆

### 自动触发

- 会话开始 → 自动 pull 最新记忆
- 会话结束 → 自动 merge + push
- 交易完成 → 自动 commit 交易记录

## 配置

在 TOOLS.md 中添加：

```yaml
git-memory:
  repo: /workspace/projects/workspace
  remote: git@github.com:yourname/repo.git  # 可选
  auto-commit: true
  auto-push: false  # 可选，默认不强制推送
```

## 依赖

- Git 2.0+
- Python 3.8+
- PyYAML

## 安装

```bash
bash scripts/install.sh
```

## 作者

JavaMaGong & A 小二

## 版本

2.0.0

## 许可证

MIT
