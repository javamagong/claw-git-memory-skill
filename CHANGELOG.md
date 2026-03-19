# Git Memory Skill - 变更日志

## [1.0.0] - 2026-03-19

### ✨ 新增

#### 核心功能
- **Schema-Driven Merge** - 配置驱动的 JSON 智能合并
- **Worktree 生命周期管理** - startup recovery + 注册表双保险
- **纯 Git 检索** - 多维度过滤搜索，不引入 SQLite
- **跨平台锁** - 支持 Linux/macOS/Windows
- **结构化 Commit** - 自动格式化 commit message

#### OpenClaw Tools
- `search_memory()` - 搜索记忆
- `save_memory()` - 保存记忆
- `get_memory_history()` - 获取历史
- `rollback_memory()` - 回滚记忆
- `get_memory_status()` - 获取状态

#### 文档
- README.md - 项目文档
- SKILL.md - OpenClaw Skill 描述
- examples/usage-examples.md - 使用示例
- docs/SCHEMA_MERGE.md - Schema-Driven Merge 详解
- docs/WORKTREE_LIFECYCLE.md - Worktree 生命周期详解

### 🔧 技术实现

#### 核心模块
- `lib/git_memory/merger.py` - Schema-Driven Merge 引擎
- `lib/git_memory/worktree.py` - Worktree 管理器 + 注册表
- `lib/git_memory/tools.py` - Git 检索工具
- `lib/git_memory/lock.py` - 跨平台锁管理器
- `lib/git_memory/formatter.py` - Commit 格式化

#### 脚本
- `scripts/install.sh` - 一键安装
- `scripts/publish.sh` - 打包发布

### ✅ 测试

- 核心功能测试：4/4 通过
  - Schema-Driven Merge ✅
  - Commit Formatter ✅
  - Lock Manager ✅
  - Git 检索 ✅

### 📋 架构决策

1. **Schema-Driven Merge** - 框架层零膨胀，业务知识完全解耦
2. **Worktree Lifecycle** - startup recovery + 注册表，自动清理残留
3. **Pure Git Search** - 纯 Git 检索，不引入 SQLite（MVP）

### 🎯 已知限制

- Worktree 方案默认关闭（v2.0 开启）
- 语义搜索未实现（v2.0 向量数据库）
- SQLite 索引未实现（v2.0 可选）

### 📝 下一步（v2.0）

- [ ] Worktree 方案（高并发场景）
- [ ] 向量数据库集成（语义搜索）
- [ ] SQLite 索引（快速查询）
- [ ] 分层存储（冷热分离）
- [ ] 自动 GC（定期清理）

---

## 版本说明

**1.0.0** - MVP 版本，核心功能完成

- ✅ 所有 P0 风险已解决
- ✅ 核心功能测试通过
- ✅ 文档完整
- ✅ 可发布到 ClawHub

---

*最后更新：2026-03-19*
