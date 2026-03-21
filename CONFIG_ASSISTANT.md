# Git Memory 配置助手 Skill

> 通过对话引导用户完成配置

## 激活时机

- 用户提到"配置 Git Memory"、"启用远程同步"、"配置多设备"等
- 用户询问如何使用 Git Memory
- 用户安装后首次使用

## 配置流程

### 阶段 1：检查安装状态

```python
# 检查 Skill 是否已安装
if not skill_installed('git-memory'):
    return "Git Memory Skill 还未安装，要我帮你安装吗？"
```

### 阶段 2：了解使用场景

**询问用户：**
```
你打算如何使用 Git Memory？

1) 单设备使用（就这一台电脑）
2) 云端 + 本地双设备同步
3) 只需要远程备份
```

### 阶段 3：根据场景配置

#### 场景 A：单设备使用

**配置：**
```yaml
remote:
  enabled: false

multi_device:
  enabled: false
```

**回复：**
```
✅ 已为你配置为单设备模式！

- 记忆会自动保存到本地 Git 仓库
- 可以随时查看历史版本
- 不需要远程同步

可以直接使用了！
```

#### 场景 B：云端 + 本地双设备

**步骤 1：询问 GitHub 仓库**
```
好的！需要你先创建一个 GitHub 私有仓库：

1. 访问 https://github.com/new
2. 创建私有仓库（名称如：openclaw-memory）
3. 告诉我仓库地址（如：git@github.com:username/repo.git）
```

**步骤 2：配置远程同步**
```python
enable_remote_sync(repo_url)
```

**步骤 3：询问设备类型**
```
远程同步已启用！

这是哪个设备？
- local（本地电脑，如 Mac/Windows）
- cloud（云端服务器，如 vefass）
```

**步骤 4：配置多设备同步**
```python
enable_multi_device_sync(device_type='local')
```

**回复：**
```
✅ 多设备同步已配置完成！

当前设备：local（本地电脑）
冲突解决：本地优先（保留本地版本）

下一步：
1. 在云端设备上也运行配置
2. 选择 device_type: cloud
3. 冲突解决：远程优先

这样两个设备就会自动同步记忆了！
```

#### 场景 C：只需要远程备份

**步骤 1：配置远程**
```python
enable_remote_sync(repo_url)
```

**步骤 2：禁用多设备**
```python
disable_multi_device_sync()
```

**回复：**
```
✅ 远程备份已启用！

- 记忆会自动推送到 GitHub
- 不会启用多设备同步
- 本地优先，不会自动拉取远程

适合只需要备份的场景！
```

## 常用命令（用户可对话触发）

### 查看配置

**用户：** "查看 Git Memory 配置"

**执行：**
```python
get_config()
```

**回复：**
```
当前配置：

远程同步：❌ 未启用
多设备同步：❌ 未启用
自动提交：✅ 已启用

需要启用远程同步吗？
```

### 启用远程同步

**用户：** "启用远程同步"

**执行：**
```python
enable_remote_sync()
```

**回复：**
```
好的！请提供你的 GitHub 仓库地址：

格式：git@github.com:username/repo.git

如果还没有仓库，可以：
1. 访问 https://github.com/new
2. 创建私有仓库
3. 复制仓库地址
```

### 启用多设备同步

**用户：** "启用多设备同步"

**执行：**
```python
enable_multi_device_sync()
```

**回复：**
```
好的！这是哪个设备？

1) local - 本地电脑（Mac/Windows/Linux）
2) cloud - 云端服务器（vefaas/VPS）
3) mobile - 移动设备
```

### 禁用远程同步

**用户：** "禁用远程同步"

**执行：**
```python
disable_remote_sync()
```

**回复：**
```
✅ 远程同步已禁用

本地版本控制仍然可用：
- 记忆自动保存
- 历史版本可查
- 会话隔离正常

只是不再同步到远程了。
```

### 查看同步状态

**用户：** "查看同步状态"

**执行：**
```python
get_sync_status()
```

**回复：**
```
同步状态：

远程仓库：✅ 已连接
仓库地址：git@github.com:user/repo.git
设备类型：local
设备名称：macbook-pro

同步情况：
- 领先远程：0 个提交
- 落后远程：2 个提交

需要拉取远程最新记忆吗？
```

### 手动同步

**用户：** "同步记忆" / "拉取远程" / "推送记忆"

**执行：**
```python
manual_sync(direction='both')  # 或 'pull' / 'push'
```

**回复：**
```
✅ 同步完成！

已拉取远程最新记忆
已推送本地记忆到远程

当前与远程同步。
```

## 故障排查

### 问题：远程仓库未配置

**用户：** "启用远程同步"但未提供地址

**回复：**
```
需要先配置远程仓库地址。

请告诉我你的 GitHub 仓库地址：
git@github.com:username/repo.git

如果还没有，可以：
1. https://github.com/new 创建私有仓库
2. 复制仓库地址
3. 告诉我
```

### 问题：SSH Key 未配置

**检测到：** `Permission denied (publickey)`

**回复：**
```
检测到 SSH Key 未配置。

需要：
1. 生成 SSH Key：
   ssh-keygen -t ed25519 -C "your@email.com"

2. 添加到 GitHub：
   cat ~/.ssh/id_ed25519.pub
   # 复制到：https://github.com/settings/keys

3. 测试：
   ssh -T git@github.com

配置好后告诉我，我帮你重试。
```

### 问题：合并冲突

**检测到：** 合并冲突

**回复：**
```
⚠️ 检测到合并冲突！

冲突文件：
- memory/2026-03-21.md

需要我帮你解决吗？

选项：
1) 保留本地版本（覆盖远程）
2) 保留远程版本（覆盖本地）
3) 手动解决（我告诉你怎么弄）
```

## 配置建议

### 新手用户
```
推荐：单设备模式
- 零配置
- 本地使用
- 无需 GitHub
```

### 进阶用户
```
推荐：远程备份
- 启用远程同步
- 不启用多设备
- 自动推送备份
```

### 高级用户
```
推荐：多设备同步
- 启用远程同步
- 启用多设备同步
- 云端：conflict_resolution=remote_wins
- 本地：conflict_resolution=local_wins
```

## 对话示例

### 示例 1：单设备配置

```
用户：帮我配置 Git Memory

助手：好的！你打算如何使用？
     1) 单设备使用（就这一台电脑）
     2) 云端 + 本地双设备同步
     3) 只需要远程备份

用户：1

助手：✅ 已为你配置为单设备模式！
     记忆会自动保存到本地 Git 仓库。
     可以直接使用了！
```

### 示例 2：多设备配置

```
用户：我想在云端和本地都用 Git Memory

助手：好的！需要你先创建一个 GitHub 私有仓库：
     1. 访问 https://github.com/new
     2. 创建私有仓库（如：openclaw-memory）
     3. 告诉我仓库地址

用户：git@github.com:erming/openclaw-memory.git

助手：✅ 远程同步已启用！
     这是哪个设备？
     - local（本地电脑）
     - cloud（云端服务器）

用户：local

助手：✅ 多设备同步已启用！
     设备类型：local
     冲突解决：本地优先
     
     下一步：在云端设备上也配置，选择 cloud 类型。
```

### 示例 3：查看状态

```
用户：Git Memory 配置好了吗？

助手：让我检查一下...
     
     当前配置：
     - 远程同步：✅ 已启用
     - 多设备同步：✅ 已启用
     - 设备类型：local
     - 设备名称：macbook-pro
     
     同步状态：
     - 领先远程：0 个提交
     - 落后远程：0 个提交
     
     一切正常！
```

## 实现细节

### Tools 导出

```python
# OpenClaw Tools
tools = {
    'enable_remote_sync': enable_remote_sync,
    'enable_multi_device_sync': enable_multi_device_sync,
    'disable_remote_sync': disable_remote_sync,
    'get_config': get_config,
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
