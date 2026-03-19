# Git Memory Skill 使用示例

本文档提供 Git Memory Skill 的实际使用示例。

---

## 示例 1：自动保存用户偏好

```python
# 用户说："记住，我不吃辣"
skill.save_memory(
    content="用户饮食偏好：不吃辣",
    subsystem="conversation",
    reason="用户饮食偏好"
)

# 生成的 commit:
# mem(conversation): 用户饮食偏好
#
# ## Metadata
# session: abc123
# timestamp: 2026-03-19T21:50:00
# ai: A 小二
#
# ## Details
# 用户饮食偏好：不吃辣
```

---

## 示例 2：记录交易操作

```python
# 交易完成
skill.save_memory(
    content=json.dumps({
        'stock': 'AAPL',
        'action': 'SELL',
        'quantity': 100,
        'price': 180.5,
        'pnl': 500
    }),
    subsystem="trading",
    reason="AAPL 止盈离场"
)
```

---

## 示例 3：搜索历史对话

```python
# 用户问："我之前说过什么关于饮食的？"
results = skill.search_memory(
    query="饮食",
    subsystem="conversation",
    limit=10
)

for result in results['results']:
    print(f"{result['timestamp']}: {result['message']}")
```

---

## 示例 4：查看交易历史

```python
# 查看 AAPL 的所有交易
results = skill.search_memory(
    query="AAPL",
    subsystem="trading",
    commit_type="trade",
    limit=50
)

print(f"AAPL 交易历史：{results['count']} 条")
for r in results['results']:
    print(f"  {r['timestamp']}: {r['message']}")
```

---

## 示例 5：回滚错误记忆

```python
# 发现记忆错误，回滚
result = skill.rollback_memory(
    commit_id="abc1234567",
    dry_run=True  # 先预览
)

print("将要回滚的文件:")
for f in result['changed_files']:
    print(f"  - {f}")

# 确认回滚
result = skill.rollback_memory(
    commit_id="abc1234567",
    dry_run=False
)
print(f"回滚成功：{result['message']}")
```

---

## 示例 6：查看记忆状态

```python
status = skill.get_memory_status()

print(f"Git 状态：{status['git_status']}")
print(f"未提交变更：{status['uncommitted_changes']}")
print(f"最后提交：{status['last_commit'][:7]}")
print(f"当前分支：{status['branch']}")
```

---

## 示例 7：智能合并子系统数据

```python
# 两个会话同时修改了交易记录
base = {'transactions': [{'id': '1', 'stock': 'AAPL'}]}
remote = {'transactions': [{'id': '1', 'stock': 'AAPL'}, {'id': '2', 'stock': 'TSLA'}]}
local = {'transactions': [{'id': '1', 'stock': 'AAPL'}, {'id': '3', 'stock': 'MSFT'}]}

# 使用 Schema-Driven Merge 智能合并
merged = skill.merge_subsystem_data('trading', base, remote, local)

# 结果：包含所有 3 条交易记录
# [{'id': '1', 'stock': 'AAPL'}, {'id': '2', 'stock': 'TSLA'}, {'id': '3', 'stock': 'MSFT'}]
```

---

## 示例 8：按时间范围查询

```python
# 查询今日交易
today = datetime.now().strftime('%Y-%m-%d')
results = skill.search_memory(
    commit_type='trade',
    since=today,
    limit=100
)

print(f"今日交易：{results['count']} 笔")
```

---

## 示例 9：按会话 ID 查询

```python
# 查询特定会话的所有操作
results = skill.search_memory(
    session_id='abc123',
    limit=50
)

print(f"会话 abc123 的操作：{results['count']} 条")
```

---

## 示例 10：批量保存记忆

```python
# 批量保存多个记忆
memories = [
    ("用户喜欢蓝色", "preference"),
    ("用户住在上海", "location"),
    ("用户是程序员", "occupation"),
]

for content, category in memories:
    skill.save_memory(
        content=content,
        subsystem="conversation",
        reason=category
    )
```

---

## 命令行示例

```bash
# 查看记忆历史
git log --oneline

# 搜索记忆
git grep "饮食"

# 查看交易系统历史
git log -- subsystems/trading/

# 恢复到历史版本
git checkout abc1234 -- MEMORY.md

# 查看统计
git count-objects -v
```

---

*版本：1.0.0 | 最后更新：2026-03-19*
