# Git Memory 配置助手 - OpenClaw Skill

> 通过对话引导用户完成 Git Memory 配置

---

## 🎯 激活时机

当用户提到以下关键词时激活：

- "配置 Git Memory"
- "启用远程同步"
- "开启多设备同步"
- "怎么设置 Git Memory"
- "帮我配置远程仓库"
- "云端和本地同步"
- "Git Memory 怎么用"

---

## 📋 配置流程（对话式）

### 阶段 1：确认需求

**用户：** "帮我配置 Git Memory"

**AI：**
```
好的！我来帮你配置 Git Memory。

首先，你打算如何使用？

1️⃣  单设备使用（就这一台电脑）
    - 零配置，本地自动保存
    
2️⃣  云端 + 本地双设备同步
    - 两个设备自动同步记忆
    
3️⃣  只需要远程备份
    - 自动推送到 GitHub 备份
```

---

### 阶段 2：根据场景配置

#### 场景 A：单设备使用

**用户：** "1" 或 "单设备"

**AI：**
```
✅ 好的！已为你配置为单设备模式。

配置内容：
- 远程同步：❌ 不启用
- 多设备同步：❌ 不启用
- 自动提交：✅ 已启用

记忆会自动保存到本地 Git 仓库，可以直接使用了！

需要我帮你重启 OpenClaw 吗？
```

**执行操作：**
```python
# 调用 Tool 更新配置
update_config('remote.enabled', False)
update_config('multi_device.enabled', False)
```

---

#### 场景 B：云端 + 本地双设备同步

**用户：** "2" 或 "多设备"

**AI：**
```
好的！多设备同步需要先配置远程仓库。

📦 请创建一个 GitHub 私有仓库：

1. 访问 https://github.com/new
2. 创建私有仓库（名称如：openclaw-memory）
3. 复制仓库地址（如：git@github.com:username/repo.git）

创建好后告诉我仓库地址。
```

**用户提供地址后：**

**用户：** "git@github.com:erming/openclaw-memory.git"

**AI：**
```
✅ 远程同步已启用！仓库地址：
   git@github.com:erming/openclaw-memory.git

接下来，这是哪个设备？

1️⃣  local - 本地电脑（Mac/Windows/Linux）
2️⃣  cloud - 云端服务器（vefaas/VPS）
3️⃣  mobile - 移动设备
```

**执行操作：**
```python
# 配置远程同步
result = enable_remote_sync('git@github.com:erming/openclaw-memory.git')
```

**用户选择设备类型后：**

**用户：** "local" 或 "1"

**AI：**
```
✅ 多设备同步已启用！

当前设备配置：
- 设备类型：local（本地电脑）
- 设备名称：macbook-pro（自动获取）
- 冲突解决：本地优先（保留本地版本）

📝 下一步：
在云端设备上也运行配置，选择 cloud 类型。

需要我帮你重启 OpenClaw 吗？
```

**执行操作：**
```python
# 配置多设备同步
result = enable_multi_device_sync('local', 'macbook-pro')
```

---

#### 场景 C：只需要远程备份

**用户：** "3" 或 "备份"

**AI：**
```
好的！配置远程备份。

📦 GitHub 仓库地址是？
（格式：git@github.com:username/repo.git）

如果还没有仓库，可以：
1. 访问 https://github.com/new
2. 创建私有仓库
3. 复制地址
```

**用户提供地址后：**

**AI：**
```
✅ 远程备份已启用！

配置内容：
- 远程同步：✅ 已启用
- 自动推送：✅ 已启用
- 多设备同步：❌ 不启用

记忆会自动推送到 GitHub 备份，本地优先。

需要我帮你重启 OpenClaw 吗？
```

**执行操作：**
```python
# 启用远程同步
result = enable_remote_sync(repo_url)
# 禁用多设备同步
disable_multi_device_sync()
```

---

## 🛠️ 支持的对话命令

### 配置相关

**用户：** "启用远程同步"

**AI：**
```
好的！请提供 GitHub 仓库地址：
格式：git@github.com:username/repo.git
```

**执行：** `enable_remote_sync(repo_url)`

---

**用户：** "启用多设备同步"

**AI：**
```
好的！这是哪个设备？

1️⃣  local - 本地电脑
2️⃣  cloud - 云端服务器
3️⃣  mobile - 移动设备
```

**执行：** `enable_multi_device_sync(device_type)`

---

**用户：** "禁用远程同步"

**AI：**
```
✅ 远程同步已禁用。

本地版本控制仍然可用：
- 记忆自动保存
- 历史版本可查
- 会话隔离正常

只是不再同步到远程了。
```

**执行：** `disable_remote_sync()`

---

### 状态查询

**用户：** "查看 Git Memory 配置"

**AI：**
```
当前配置：

✅ 远程同步：已启用
   仓库地址：git@github.com:erming/openclaw-memory.git

✅ 多设备同步：已启用
   设备类型：local
   设备名称：macbook-pro
   冲突解决：本地优先

✅ 自动提交：已启用

需要修改配置吗？
```

**执行：** `get_config()`

---

**用户：** "查看同步状态"

**AI：**
```
同步状态：

📊 远程仓库：✅ 已连接
📊 设备类型：local
📊 设备名称：macbook-pro

📈 同步情况：
- 领先远程：0 个提交
- 落后远程：2 个提交

需要拉取远程最新记忆吗？
```

**执行：** `get_sync_status()`

---

### 同步操作

**用户：** "同步记忆" / "拉取远程" / "推送记忆"

**AI：**
```
📥 正在拉取远程最新记忆...
✅ 已拉取 2 个新提交

📤 正在推送本地记忆...
✅ 推送成功

当前与远程同步。
```

**执行：** `manual_sync('both')` 或 `manual_sync('pull')` / `manual_sync('push')`

---

## 🎯 对话示例

### 示例 1：完整配置流程

```
用户：帮我配置 Git Memory

AI：好的！你打算如何使用？
    1️⃣  单设备使用（就这一台电脑）
    2️⃣  云端 + 本地双设备同步
    3️⃣  只需要远程备份

用户：2

AI：好的！多设备同步需要先配置远程仓库。
    📦 请创建一个 GitHub 私有仓库：
    1. 访问 https://github.com/new
    2. 创建私有仓库
    3. 告诉我仓库地址

用户：创建好了，git@github.com:erming/openclaw-memory.git

AI：✅ 远程同步已启用！
    这是哪个设备？
    1️⃣  local - 本地电脑
    2️⃣  cloud - 云端服务器
    3️⃣  mobile - 移动设备

用户：local

AI：✅ 多设备同步已启用！
    当前设备：local（本地电脑）
    冲突解决：本地优先
    
    📝 下一步：
    在云端设备上也运行配置，选择 cloud 类型。
    
    需要我帮你重启 OpenClaw 吗？

用户：好的，重启

AI：🔄 正在重启 OpenClaw...
    ✅ 重启完成！Git Memory 已生效。
```

---

### 示例 2：查看配置

```
用户：Git Memory 配置好了吗？

AI：让我检查一下...
    
    当前配置：
    ✅ 远程同步：已启用
    ✅ 多设备同步：已启用
    ✅ 设备类型：local
    ✅ 设备名称：macbook-pro
    
    同步状态：
    📊 领先远程：0 个提交
    📊 落后远程：0 个提交
    
    一切正常！
```

---

### 示例 3：故障排查

```
用户：启用远程同步

AI：好的！请提供 GitHub 仓库地址：
    格式：git@github.com:username/repo.git

用户：git@github.com:erming/openclaw-memory.git

AI：⚠️  配置失败：Permission denied (publickey)
    
    检测到 SSH Key 未配置。
    
    需要：
    1. 生成 SSH Key：
       ssh-keygen -t ed25519 -C "your@email.com"
    
    2. 添加到 GitHub：
       cat ~/.ssh/id_ed25519.pub
       复制到：https://github.com/settings/keys
    
    3. 测试：
       ssh -T git@github.com
    
    配置好后告诉我，我帮你重试。
```

---

## 🔧 Tools 调用

### 配置管理

```python
# 启用远程同步
enable_remote_sync(repo_url: str)
→ {
    'success': True,
    'enabled': True,
    'url': repo_url,
    'message': '远程同步已启用'
}

# 启用多设备同步
enable_multi_device_sync(device_type: str, device_name: str = None)
→ {
    'success': True,
    'enabled': True,
    'device_type': 'local',
    'device_name': 'macbook-pro',
    'conflict_resolution': 'local_wins'
}

# 禁用远程同步
disable_remote_sync()
→ {
    'success': True,
    'disabled': True,
    'message': '远程同步已禁用'
}

# 查看配置
get_config(key: str = None)
→ {
    'success': True,
    'config': {
        'remote': {'enabled': True, 'url': '...'},
        'multi_device': {'enabled': True, 'device_type': 'local'},
        'auto_commit': {'enabled': True}
    }
}
```

### 同步操作

```python
# 会话开始同步
sync_start()
→ {'success': True, 'synced': True, 'message': '已拉取最新记忆'}

# 会话结束同步
sync_end()
→ {'success': True, 'synced': True, 'message': '记忆已保存并推送'}

# 手动同步
manual_sync(direction: str = 'both')
→ {'success': True, 'operations': [...]}

# 查看同步状态
get_sync_status()
→ {
    'remote_enabled': True,
    'device_type': 'local',
    'sync_delta': {'ahead': 0, 'behind': 2}
}
```

---

## ⚠️ 故障处理

### 问题 1：远程仓库未配置

**检测：** `remote.enabled = false`

**回复：**
```
远程同步还未启用。

需要我帮你启用吗？
1. 创建 GitHub 私有仓库
2. 告诉我仓库地址
3. 我帮你配置
```

---

### 问题 2：SSH Key 未配置

**检测：** `Permission denied (publickey)`

**回复：**
```
⚠️  SSH Key 未配置。

需要：
1. 生成 SSH Key：
   ssh-keygen -t ed25519 -C "your@email.com"

2. 添加到 GitHub：
   cat ~/.ssh/id_ed25519.pub
   复制到：https://github.com/settings/keys

3. 测试：
   ssh -T git@github.com

配置好后告诉我，我帮你重试。
```

---

### 问题 3：合并冲突

**检测：** `merge conflict`

**回复：**
```
⚠️  检测到合并冲突！

冲突文件：
- memory/2026-03-21.md

需要我帮你解决吗？

选项：
1️⃣  保留本地版本（覆盖远程）
2️⃣  保留远程版本（覆盖本地）
3️⃣  手动解决（我告诉你怎么弄）
```

---

### 问题 4：多设备同步未启用远程

**检测：** `multi_device.enabled = true` 但 `remote.enabled = false`

**回复：**
```
多设备同步需要先启用远程同步。

需要我帮你启用远程同步吗？
1. 创建 GitHub 私有仓库
2. 告诉我仓库地址
3. 我帮你配置
```

---

## 📖 配置建议

### 新手用户

**推荐：** 单设备模式

```
配置：
- remote.enabled: false
- multi_device.enabled: false

优点：
- 零配置
- 本地使用
- 无需 GitHub
```

---

### 进阶用户

**推荐：** 远程备份

```
配置：
- remote.enabled: true
- multi_device.enabled: false
- auto_push: true

优点：
- 自动备份
- 本地优先
- 简单可靠
```

---

### 高级用户

**推荐：** 多设备同步

```
云端配置：
- remote.enabled: true
- multi_device.enabled: true
- device_type: cloud
- conflict_resolution: remote_wins

本地配置：
- remote.enabled: true
- multi_device.enabled: true
- device_type: local
- conflict_resolution: local_wins

优点：
- 自动同步
- 智能冲突解决
- 设备标识清晰
```

---

## 🎯 实现细节

### Skill 导出

```python
# OpenClaw Skill 导出
tools = {
    # 配置管理
    'enable_remote_sync': enable_remote_sync,
    'enable_multi_device_sync': enable_multi_device_sync,
    'disable_remote_sync': disable_remote_sync,
    'get_config': get_config,
    
    # 同步操作
    'sync_start': sync_start,
    'sync_end': sync_end,
    'get_sync_status': get_sync_status,
    'manual_sync': manual_sync,
}
```

### 配置验证

```python
def validate_config():
    """验证配置是否有效"""
    config = get_config()
    
    if config['remote']['enabled'] and not config['remote']['url']:
        return False, "远程同步已启用但未配置地址"
    
    if config['multi_device']['enabled'] and not config['remote']['enabled']:
        return False, "多设备同步需要远程同步"
    
    return True, "配置有效"
```

---

**版本：** 1.1.0  
**日期：** 2026-03-21  
**状态：** ✅ 生产就绪
