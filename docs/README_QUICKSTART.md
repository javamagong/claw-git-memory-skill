# Git Memory Skill - 快速开始

> 🧠 AI 记忆自动版本管理 - **一句话安装，零配置使用**

---

## 🚀 一句话安装

```bash
bash skills/git-memory/quick-install.sh
```

**就这么简单！** 无需任何配置，立即可用。

---

## ✅ 安装后

### 重启 OpenClaw

```bash
sh /workspace/projects/scripts/restart.sh
```

### 正常使用

**无需任何操作！** 记忆会自动版本化保存：

- ✅ 会话开始 → 自动创建分支
- ✅ 对话中 → 自动保存记忆
- ✅ 会话结束 → 自动提交

---

## 📦 可选：配置远程同步

**仅当需要多设备同步时才配置**

### 🎯 方式 1：对话配置（推荐）⭐

**直接告诉我：**
- "帮我配置 Git Memory"
- "启用远程同步"
- "启用多设备同步"

**我会引导你完成配置！** ✅

---

### 📱 方式 2：交互式引导

```bash
python3 skills/git-memory/guide-config.py
```

按提示选择使用场景即可。

---

### ⌨️ 方式 3：命令行向导

```bash
python3 skills/git-memory/config-wizard.py
```

分步配置选项。

---

**不配置也能用！** 本地版本控制完全正常。

---

## 📊 查看状态

```bash
# Git 提交历史
git log --oneline -10

# 同步状态（如果配置了远程）
python3 -c "
from skills.git-memory.lib.git_memory import GitMemorySkill
skill = GitMemorySkill('.')
print(skill.get_sync_status())
"
```

---

## 🎯 功能特性

### 已包含

- ✅ **自动版本控制** - 所有记忆自动 Git 提交
- ✅ **会话隔离** - 每个会话独立分支
- ✅ **历史回溯** - 随时查看/恢复历史版本
- ✅ **智能合并** - 自动处理冲突
- ✅ **零配置** - 安装即用

### 可选（需配置远程）

- ⭐ **多设备同步** - 云端 + 本地自动同步
- ⭐ **远程备份** - GitHub/GitLab 备份
- ⭐ **设备标识** - commit 包含设备名

---

## ⚠️ 常见问题

### Q: 必须配置 GitHub 吗？

**A:** 不！本地使用完全没问题，Git 版本控制正常工作。

### Q: 配置远程复杂吗？

**A:** 不！运行 `python3 skills/git-memory/config-wizard.py`，按提示操作即可。

### Q: 会影响性能吗？

**A:** 几乎无影响！Git 操作在后台异步执行。

### Q: 多个会话会冲突吗？

**A:** 不会！每个会话独立分支，自动合并。

---

## 📖 详细文档

- `README.md` - 本文档（快速开始）
- `skills/git-memory/README.md` - 完整说明
- `GIT_MEMORY_MULTI_DEVICE_SYNC.md` - 多设备同步指南
- `config/git-memory.yaml` - 配置文件

---

## 💡 极简使用流程

```
1. 安装
   bash skills/git-memory/quick-install.sh

2. 重启
   sh /workspace/projects/scripts/restart.sh

3. 使用
   正常对话，记忆自动保存

4. （可选）配置远程
   python3 skills/git-memory/config-wizard.py
```

**就这么简单！** 🫡

---

*版本：1.1.0 | 最后更新：2026-03-21*
