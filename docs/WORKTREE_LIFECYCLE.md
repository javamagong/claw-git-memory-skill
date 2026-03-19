# Worktree 生命周期管理

> startup recovery + 注册表双保险，自动清理残留 worktree

---

## 问题背景

Git Worktree 方案的风险：

1. **进程 Crash** → worktree 目录残留
2. **未清理** → 磁盘空间浪费
3. **手动清理** → 容易遗漏

---

## 解决方案

### 双保险机制

```
┌─────────────────────────────────────────────────────┐
│              Worktree 生命周期管理                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. 创建时注册                                       │
│     └─→ 记录 PID + 路径 + 时间                      │
│                                                     │
│  2. 启动时恢复                                       │
│     └─→ 扫描注册表 → 检查 PID → 清理死进程         │
│                                                     │
│  3. 删除时注销                                       │
│     └─→ 从注册表移除                                │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 注册表设计

### 注册表文件

```json
// /tmp/gm-registry.json
{
  "version": 1,
  "worktrees": [
    {
      "path": "/workspace/.git/worktrees/session-abc123",
      "session_id": "abc123",
      "pid": 12345,
      "created_at": "2026-03-19T21:00:00",
      "status": "active"
    }
  ],
  "last_cleanup": "2026-03-19T21:30:00"
}
```

### 字段说明

| 字段 | 说明 |
|------|------|
| `path` | worktree 绝对路径 |
| `session_id` | 会话唯一标识 |
| `pid` | 创建进程 ID |
| `created_at` | 创建时间（ISO8601） |
| `status` | 状态（active/cleanup） |

---

## 实现细节

### 1. 创建时注册

```python
# lib/git_memory/worktree.py

class WorktreeRegistry:
    def register(self, worktree_path: str, session_id: str):
        """注册 worktree（创建时调用）"""
        registry = self._load_registry()
        
        registry['worktrees'].append({
            'path': str(worktree_path),
            'session_id': session_id,
            'pid': os.getpid(),
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        })
        
        self._save_registry(registry)
```

---

### 2. 启动时恢复

```python
def startup_recovery(self) -> int:
    """启动时恢复（清理残留 worktree）"""
    registry = self._load_registry()
    cleaned = 0
    
    for wt in registry['worktrees'][:]:
        if not self.is_pid_alive(wt['pid']):
            # PID 已死，清理 worktree
            print(f"🧹 清理残留 worktree: {wt['path']}")
            
            # 删除 worktree 目录
            wt_path = Path(wt['path'])
            if wt_path.exists():
                subprocess.run(
                    ['git', 'worktree', 'remove', str(wt_path), '--force'],
                    cwd=self.repo_path
                )
                shutil.rmtree(wt_path, ignore_errors=True)
            
            # 从注册表注销
            registry['worktrees'].remove(wt)
            cleaned += 1
    
    registry['last_cleanup'] = datetime.now().isoformat()
    self._save_registry(registry)
    
    return cleaned
```

---

### 3. 删除时注销

```python
def unregister(self, worktree_path: str):
    """注销 worktree（删除时调用）"""
    registry = self._load_registry()
    
    registry['worktrees'] = [
        wt for wt in registry['worktrees']
        if wt['path'] != str(worktree_path)
    ]
    
    self._save_registry(registry)
```

---

## 完整生命周期

```python
# lib/git_memory/worktree.py

class WorktreeManager:
    @contextmanager
    def session_worktree(self, session_id: str):
        """会话 worktree 上下文管理器（完整生命周期）"""
        worktree_path = None
        
        try:
            # 1. 启动恢复（清理残留）
            self.registry.startup_recovery()
            
            # 2. 创建 worktree
            worktree_path = self._create_worktree(session_id)
            
            # 3. 注册（记录 PID）
            self.registry.register(worktree_path, session_id)
            
            # 4. 使用 worktree
            yield worktree_path
            
            # 5. 提交 + 合并
            commit_hash = self._commit_and_merge(worktree_path, session_id)
            
        finally:
            # 6. 清理（无论成功失败）
            if worktree_path:
                self._cleanup_worktree(worktree_path)
                self.registry.unregister(worktree_path)
```

---

## PID 检查

```python
def is_pid_alive(self, pid: int) -> bool:
    """检查 PID 是否存活"""
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False  # 进程已死
    except PermissionError:
        return True   # 权限不足，假设存活
```

---

## 异常处理

### 场景 1：进程 Crash

```
进程创建 worktree → 注册 → Crash
↓
下次启动时
↓
startup_recovery 扫描注册表
↓
发现 PID 已死 → 清理 worktree + 注销
↓
✅ 自动恢复
```

---

### 场景 2：正常退出

```
进程创建 worktree → 注册 → 使用 → 提交 → 清理 → 注销
↓
✅ 正常生命周期
```

---

### 场景 3：并发冲突

```
进程 A 创建 worktree-A → 注册
进程 B 创建 worktree-B → 注册
↓
两个 worktree 独立运行
↓
各自清理各自的
↓
✅ 无冲突
```

---

## 性能优化

### 1. 延迟清理

```python
# 不是每次启动都清理，检查最后清理时间
if last_cleanup > 1 小时前:
    return 0  # 跳过清理
```

### 2. 批量清理

```python
# 一次性清理所有死进程 worktree
for wt in registry['worktrees'][:]:
    if not is_pid_alive(wt['pid']):
        cleanup(wt)
```

### 3. 异步清理

```python
# 清理操作后台执行，不阻塞启动
threading.Thread(target=cleanup_thread).start()
```

---

## 监控与调试

### 查看注册表

```bash
cat /tmp/gm-registry.json
```

### 手动清理

```python
from git_memory.worktree import WorktreeRegistry

registry = WorktreeRegistry('/workspace')
cleaned = registry.startup_recovery()
print(f"清理了 {cleaned} 个残留 worktree")
```

### 查看活跃 worktree

```python
active = registry.get_active_worktrees()
for wt in active:
    print(f"{wt['session_id']}: PID {wt['pid']}")
```

---

## 最佳实践

### 1. 注册表文件权限

```python
# 设置只允许所有者读写
os.chmod(registry_path, 0o600)
```

### 2. 定期清理

```python
# 每天清理一次
if last_cleanup < 24 小时前:
    startup_recovery()
```

### 3. 日志记录

```python
import logging

logging.info(f"清理 worktree: {wt['path']} (PID {wt['pid']} 已死)")
```

### 4. 错误处理

```python
try:
    cleanup(wt)
except Exception as e:
    logging.error(f"清理失败：{e}")
    # 不中断，继续清理下一个
```

---

## 测试验证

```python
def test_worktree_lifecycle():
    manager = WorktreeManager('/workspace')
    
    # 创建
    worktree = manager.create_worktree('test123')
    
    # 验证注册
    info = manager.registry.get_worktree_info(str(worktree))
    assert info['session_id'] == 'test123'
    assert info['pid'] == os.getpid()
    
    # 清理
    manager.cleanup(worktree)
    
    # 验证注销
    info = manager.registry.get_worktree_info(str(worktree))
    assert info is None
```

---

*版本：1.0.0 | 最后更新：2026-03-19*
