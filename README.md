# Git Memory Skill

> 🧠 AI 记忆自动版本管理 - 让 AI 不再失忆

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://clawhub.com/skills/git-memory)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 快速开始

### 安装

```bash
cd /workspace/projects/workspace
bash skills/git-memory/scripts/install.sh
```

### 重启 OpenClaw

```bash
sh /workspace/projects/scripts/restart.sh
```

### 使用

**无需任何操作！** 记忆会自动版本化保存。

---

## 核心特性

- ✅ **自动版本控制** - 所有记忆变更自动 Git 提交
- ✅ **会话隔离** - 每个会话独立分支，互不干扰
- ✅ **历史回溯** - 随时查看/恢复到任意历史版本
- ✅ **远程备份** - 可选同步到 GitHub/GitLab
- ✅ **智能合并** - Schema 驱动的 JSON 合并
- ✅ **精准检索** - 多维度过滤搜索

---

## 可选命令

```bash
# 查看记忆历史
git log --oneline

# 搜索记忆
git grep "关键词"

# 查看某子系统的历史
git log -- subsystems/trading/

# 恢复到历史版本
git checkout <commit-hash> -- MEMORY.md
```

---

## 目录结构

```
/workspace/
├── MEMORY.md                    # 全局记忆
├── memory/                      # 每日记忆
├── subsystems/                  # 子系统记忆
│   ├── trading/                 # 股票交易
│   ├── conversation/            # 对话
│   ├── skills/                  # 技能学习
│   └── tools/                   # 工具配置
└── .git/                        # Git 仓库
```

---

## 配置

### 自定义合并策略

在子系统目录下创建 `.mergerc.yaml`：

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

### 配置远程备份（可选）

```bash
git remote add origin https://github.com/yourname/memory.git
git push -u origin main
```

---

## 架构设计

详见 [飞书设计文档](https://feishu.cn/docx/...)

### 核心决策

1. **Schema-Driven Merge** - 配置驱动的 JSON 合并
2. **Worktree Lifecycle** - 自动清理残留 worktree
3. **Pure Git Search** - 纯 Git 检索，不引入 SQLite

---

## FAQ

### Q: 需要懂 Git 吗？

**A:** 不需要！所有 Git 操作自动完成。

### Q: 会丢数据吗？

**A:** 不会！Git 版本控制，所有历史都可恢复。

### Q: 需要配置远程仓库吗？

**A:** 可选！本地使用完全没问题。

### Q: 会影响性能吗？

**A:** 几乎无影响！Git 操作在后台异步执行。

### Q: 多个会话会冲突吗？

**A:** 不会！每个会话独立分支，自动合并。

---

## 开发

### 运行测试

```bash
cd skills/git-memory
pytest tests/
```

### 查看日志

```bash
tail -f logs/git-memory.log
```

---

## 参考资源

- [TaG (Trading as Git)](https://www.traderalice.com/blog/trading-as-git-intro)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [Git Documentation](https://git-scm.com/docs)

---

## License

MIT License

---

*版本：1.0.0 | 最后更新：2026-03-19*
