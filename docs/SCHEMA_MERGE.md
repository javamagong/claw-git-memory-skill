# Schema-Driven Merge 详解

> 配置驱动的 JSON 智能合并，框架层零膨胀

---

## 问题背景

传统硬编码合并规则的问题：

```python
# ❌ 错误设计：硬编码
SPECIAL_MERGE_RULES = {
    'transactions': 'union',
    'holdings': 'local',
    'count': 'max'
}
# 违反开闭原则，新增字段需要修改核心代码
```

---

## 解决方案

每个子系统通过 `.mergerc.yaml` 自定义合并策略：

```yaml
# subsystems/trading/.mergerc.yaml
version: 1
fields:
  transactions:
    type: array
    merge_strategy: union
    id_fields: ['transaction_id']
    dedup: true
  
  holdings:
    type: object
    merge_strategy: deep_merge
    conflict_resolution: local
  
  count:
    type: scalar
    merge_strategy: max

_default:
  merge_strategy: local
```

---

## 支持的合并策略

### 1. union - 数组并集 + 去重

```yaml
transactions:
  type: array
  merge_strategy: union
  id_fields: ['transaction_id']
```

**合并逻辑**：
- BASE: `[{'id': '1'}]`
- REMOTE: `[{'id': '1'}, {'id': '2'}]`
- LOCAL: `[{'id': '1'}, {'id': '3'}]`
- **结果**: `[{'id': '1'}, {'id': '2'}, {'id': '3'}]`

---

### 2. deep_merge - 对象深度合并

```yaml
holdings:
  type: object
  merge_strategy: deep_merge
  conflict_resolution: local
```

**合并逻辑**：
- 递归合并所有字段
- 冲突时以 `conflict_resolution` 为准（local/remote）

---

### 3. max - 标量取最大值

```yaml
count:
  type: scalar
  merge_strategy: max
```

**合并逻辑**：
- REMOTE: `15`
- LOCAL: `12`
- **结果**: `15`

---

### 4. latest - 标量取最新值

```yaml
last_updated:
  type: scalar
  merge_strategy: latest
  key: 'timestamp'
```

**合并逻辑**：
- 比较 `timestamp` 字段
- 取最新的时间戳

---

### 5. local - 以本地为准（默认）

```yaml
_default:
  merge_strategy: local
```

**合并逻辑**：
- 直接使用 LOCAL 的值
- 适用于配置类字段

---

### 6. remote - 以远程为准

```yaml
config_version:
  type: scalar
  merge_strategy: remote
```

**合并逻辑**：
- 直接使用 REMOTE 的值
- 适用于全局配置

---

## 框架层实现

```python
# lib/git_memory/merger.py

class SchemaDrivenMerger:
    """Schema 驱动的合并引擎（框架层，零业务知识）"""
    
    def merge(self, subsystem_path, base, remote, local):
        # 1. 加载 schema（框架层不关心内容）
        schema = self._load_schema(subsystem_path)
        
        # 2. 按 schema 执行合并（框架层通用逻辑）
        result = {}
        for key in set(remote.keys()) | set(local.keys()):
            field_schema = schema['fields'].get(key, schema['_default'])
            result[key] = self._apply_strategy(
                field_schema['merge_strategy'],
                base.get(key), remote.get(key), local.get(key),
                field_schema
            )
        
        return result
```

**框架层零膨胀**：
- ✅ 不硬编码任何业务规则
- ✅ 只负责读取 schema 并执行
- ✅ 新增子系统无需修改核心代码

---

## 配置示例

### 股票交易系统

```yaml
# subsystems/trading/.mergerc.yaml
version: 1
fields:
  transactions:
    merge_strategy: union
    id_fields: ['transaction_id']
  
  holdings:
    merge_strategy: deep_merge
    conflict_resolution: local
  
  total_pnl:
    merge_strategy: max

_default:
  merge_strategy: local
```

---

### 对话系统

```yaml
# subsystems/conversation/.mergerc.yaml
version: 1
fields:
  preferences:
    merge_strategy: deep_merge
  
  important_facts:
    merge_strategy: union
    id_fields: ['fact_id']

_default:
  merge_strategy: local
```

---

### 技能学习系统

```yaml
# subsystems/skills/.mergerc.yaml
version: 1
fields:
  learned_skills:
    merge_strategy: union
    id_fields: ['skill_name']
  
  experience_points:
    merge_strategy: max

_default:
  merge_strategy: local
```

---

## 最佳实践

### 1. 为数组字段定义唯一 ID

```yaml
transactions:
  merge_strategy: union
  id_fields: ['transaction_id']  # ✅ 明确 ID 字段
```

### 2. 为对象字段指定冲突策略

```yaml
holdings:
  merge_strategy: deep_merge
  conflict_resolution: local  # ✅ 冲突时以本地为准
```

### 3. 使用_default 兜底

```yaml
_default:
  merge_strategy: local  # ✅ 未配置的字段使用默认策略
```

### 4. 文档化 schema

```yaml
version: 1
description: "股票交易系统合并配置"  # ✅ 添加描述
fields:
  transactions:
    description: "交易记录列表"
    merge_strategy: union
```

---

## 测试验证

```python
from git_memory.merger import SchemaDrivenMerger

merger = SchemaDrivenMerger()

# 测试数据
base = {'transactions': [{'id': '1'}]}
remote = {'transactions': [{'id': '1'}, {'id': '2'}]}
local = {'transactions': [{'id': '1'}, {'id': '3'}]}

# 合并
result = merger.merge('subsystems/trading', base, remote, local)

# 验证
assert len(result['transactions']) == 3
assert result['transactions'][1]['id'] == '2'
assert result['transactions'][2]['id'] == '3'
```

---

*版本：1.0.0 | 最后更新：2026-03-19*
