# 记忆迁移指南

> 将现有记忆文件迁移到 Git Memory 系统

---

## 适用场景

### ✅ 需要迁移

- 已经使用 OpenClaw 一段时间
- 已有 `MEMORY.md` 文件
- 已有 `memory/` 目录
- 已有 `subsystems/` 目录

### ❌ 无需迁移

- 全新安装
- 没有任何记忆文件
- 已经在使用 Git Memory

---

## 迁移方式

### 方式 1：自动检测（推荐）

安装时自动检测并提示迁移：

```bash
bash skills/git-memory/scripts/install.sh

# 如果检测到现有记忆文件：
# 🔄 检测到现有记忆文件，是否迁移？(y/N)
# 输入 y 确认迁移
```

---

### 方式 2：手动迁移

```bash
cd /workspace/projects/workspace

# 预览模式（不实际执行）
python3 skills/git-memory/lib/git_memory/migrator.py --dry-run

# 实际执行
python3 skills/git-memory/lib/git_memory/migrator.py
```

---

### 方式 3：迁移脚本

安装后会自动创建迁移脚本：

```bash
# 使用迁移脚本
bash migrate-memory.sh
```

---

## 迁移流程

```
1. 检查前置条件
   └─→ Git 仓库已初始化
   
2. 扫描现有文件
   └─→ MEMORY.md
   └─→ memory/*.md
   └─→ subsystems/**/*
   
3. 用户确认
   └─→ 显示文件列表
   └─→ 确认迁移
   
4. 添加到 Git
   └─→ git add MEMORY.md memory/ subsystems/
   
5. 创建提交
   └─→ commit: migrate: 迁移现有记忆到 Git Memory 系统
   
6. 完成
   └─→ 创建迁移脚本（方便以后使用）
```

---

## 迁移示例

### 示例 1：标准迁移

```bash
$ python3 skills/git-memory/lib/git_memory/migrator.py

============================================================
🔄 Git Memory - 记忆迁移工具
============================================================
🔍 检查前置条件...
✅ 检测到现有记忆:
   - MEMORY.md
   - memory/ 目录
   - subsystems/ 目录

📋 扫描现有记忆文件...
   MEMORY.md: 15.2 KB
   memory/2026-03-19.md: 3.5 KB
   subsystems/trading/holdings.json: 2.1 KB
   subsystems/trading/transactions/: 5.3 KB
   
   总计：15 个文件

============================================================
🔄 开始迁移记忆到 Git 管理
============================================================

❓ 确认迁移？
   这将把所有现有记忆文件添加到 Git 管理
   并创建初始提交

   继续？(y/N): y

📦 添加文件到 Git...
   ✅ 已添加 15 个文件

📝 创建初始提交...
   ✅ 提交成功：abc1234

============================================================
✅ 迁移完成！
============================================================

📝 创建迁移脚本：./migrate-memory.sh
   以后可以使用：bash migrate-memory.sh
```

---

### 示例 2：预览模式

```bash
$ python3 skills/git-memory/lib/git_memory/migrator.py --dry-run

============================================================
🔄 Git Memory - 记忆迁移工具
============================================================

⚠️  预览模式（不会实际执行）

🔍 检查前置条件...
✅ 检测到现有记忆:
   - MEMORY.md
   - memory/ 目录

📋 扫描现有记忆文件...
   MEMORY.md: 15.2 KB
   memory/2026-03-19.md: 3.5 KB
   
   总计：5 个文件

============================================================
🔄 开始迁移记忆到 Git 管理
============================================================

⚠️  预览模式（不会实际执行）

📦 添加文件到 Git...
   将要添加 5 个文件
   - MEMORY.md
   - memory/2026-03-19.md
   - memory/2026-03-18.md
   - memory/2026-03-17.md
   - memory/2026-03-16.md

============================================================
✅ 预览完成（未实际执行）
============================================================
```

---

## 迁移后的 Git 历史

```bash
$ git log --oneline

abc1234 migrate: 迁移现有记忆到 Git Memory 系统
def5678 feat: 完成 Git Memory MVP 核心实现
```

迁移会创建一个专门的 commit，标记为 `migrate:` 前缀。

---

## 迁移内容

### 会迁移的文件

| 文件/目录 | 说明 |
|----------|------|
| `MEMORY.md` | 全局长期记忆 |
| `memory/*.md` | 每日记忆 |
| `subsystems/trading/` | 股票交易记忆 |
| `subsystems/conversation/` | 对话记忆 |
| `subsystems/skills/` | 技能学习记忆 |
| `subsystems/tools/` | 工具配置记忆 |

### 不会迁移的文件

| 文件/目录 | 原因 |
|----------|------|
| `.git/` | Git 仓库本身 |
| `.gitignore` | 已存在 |
| `logs/` | 日志文件 |
| `__pycache__/` | Python 缓存 |

---

## 常见问题

### Q: 迁移会覆盖现有文件吗？

**A:** 不会！迁移只是将现有文件添加到 Git 管理，不会修改文件内容。

---

### Q: 迁移失败会丢失数据吗？

**A:** 不会！迁移只执行 `git add` 和 `git commit`，不会删除或修改文件。

---

### Q: 可以取消迁移吗？

**A:** 可以！在确认提示时输入 `N` 即可取消。

---

### Q: 迁移后可以回滚吗？

**A:** 可以！使用 Git 回滚：

```bash
# 回滚迁移提交
git reset --hard HEAD~1

# 或者恢复到迁移前的状态
git checkout <commit-hash> -- .
```

---

### Q: 迁移需要多长时间？

**A:** 通常 10-30 秒，取决于文件数量和大小。

---

### Q: 迁移后 Git 仓库会变大吗？

**A:** 会，但这是正常的。Git 会存储文件的历史版本。

示例：
- 迁移前：MEMORY.md 15 KB
- 迁移后：.git/ 目录约 50-100 KB

---

## 最佳实践

### 1. 迁移前备份（可选）

```bash
# 备份现有记忆文件
cp -r MEMORY.md memory/ subsystems/ /tmp/memory-backup/
```

### 2. 使用预览模式

```bash
# 先预览，确认无误后再执行
python3 skills/git-memory/lib/git_memory/migrator.py --dry-run
python3 skills/git-memory/lib/git_memory/migrator.py
```

### 3. 检查迁移结果

```bash
# 查看 Git 状态
git status

# 查看提交历史
git log --oneline -5

# 查看仓库大小
du -sh .git/
```

### 4. 保留迁移脚本

```bash
# 迁移脚本会保存在工作目录
ls -la migrate-memory.sh

# 以后可以使用
bash migrate-memory.sh
```

---

## 技术细节

### 迁移原理

```python
# 1. 扫描现有文件
files = scan_existing_files()

# 2. 添加到 Git
git add MEMORY.md memory/ subsystems/

# 3. 创建提交
git commit -m "migrate: 迁移现有记忆到 Git Memory 系统"
```

### Commit Message 格式

```
migrate: 迁移现有记忆到 Git Memory 系统

## Metadata
migration: true
timestamp: 2026-03-19T22:15:00
ai: A 小二

## Details
迁移的文件:
- MEMORY.md: 15.2 KB
- memory/: 10 个文件
- subsystems/: 5 个文件

总计：15 个文件
```

---

*版本：1.0.0 | 最后更新：2026-03-19*
