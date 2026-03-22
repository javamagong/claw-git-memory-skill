# Git Memory OpenClaw 集成指南

> 在 OpenClaw 中配置和使用 Git Memory 记忆管理系统

**版本：** 2.0.0  
**最后更新：** 2026-03-23  
**作者：** JavaMaGong & A 小二

---

## 📋 目录

1. [快速开始](#快速开始)
2. [安装步骤](#安装步骤)
3. [配置说明](#配置说明)
4. [使用示例](#使用示例)
5. [故障排查](#故障排查)
6. [高级配置](#高级配置)

---

## 快速开始

### 一句话安装

```bash
bash skills/git-memory/quick-install.sh
```

### 重启 OpenClaw

```bash
sh /workspace/projects/scripts/restart.sh
```

### 开始使用

**无需任何操作！** Git Memory 会自动：

- ✅ 会话开始 → 拉取最新记忆
- ✅ 对话中 → 自动保存记忆
- ✅ 会话结束 → 自动提交并推送

---

## 安装步骤

### 前置要求

| 要求 | 版本 | 检查命令 |
|------|------|---------|
| Git | 2.0+ | `git --version` |
| Python | 3.8+ | `python3 --version` |
| OpenClaw | 最新版 | `openclaw --version` |
| PyYAML | 任意 | `python3 -c "import yaml"` |

### 步骤 1：运行安装脚本

```bash
cd /workspace/projects/workspace
bash skills/git-memory/quick-install.sh
```

**安装脚本会：**
1. ✅ 检查依赖（Git/Python/PyYAML）
2. ✅ 初始化 Git 仓库（如果未初始化）
3. ✅ 创建目录结构（memory/, subsystems/, config/）
4. ✅ 创建默认配置文件
5. ✅ 注册 OpenClaw Hooks（如果检测到 OpenClaw）

### 步骤 2：验证安装

```bash
# 检查 Git 状态
git status

# 检查配置文件
cat config/git-memory.yaml

# 检查 Hooks 是否注册
ls -la ~/.openclaw/hooks/ | grep git-memory
```

### 步骤 3：重启 OpenClaw

```bash
sh /workspace/projects/scripts/restart.sh
```

---

## 配置说明

### 配置文件位置

```
/workspace/projects/workspace/config/git-memory.yaml
```

### 配置项详解

#### 1. 远程同步配置

```yaml
remote:
  enabled: true          # 是否启用远程同步
  url: "git@github.com:user/repo.git"  # 仓库地址
  auto_pull: true        # 会话开始自动拉取
  auto_push: true        # 会话结束自动推送
```

**配置远程仓库：**

```bash
python3 skills/git-memory/config-wizard.py
```

按提示输入：
1. 设备类型（local/cloud）
2. 设备名称
3. GitHub 仓库地址

#### 2. 多设备同步

```yaml
multi_device:
  enabled: true
  device_type: local     # local | cloud | mobile
  device_name: ""        # 留空自动使用主机名
  sync_on_start: true
  sync_on_end: true
  conflict_resolution: auto  # auto | local_wins | remote_wins
```

**多设备场景：**

| 设备类型 | 冲突策略 | 说明 |
|---------|---------|------|
| local（本地电脑） | local_wins | 本地优先 |
| cloud（云端） | remote_wins | 远程优先 |
| mobile（移动设备） | auto | 自动判断 |

#### 3. 自动提交

```yaml
auto_commit:
  enabled: true
  prefix: "auto"       # commit 前缀
  include_device: true # 包含设备名
  include_timestamp: true  # 包含时间戳
```

**Commit 信息格式：**

```
auto(macbook-pro-2026-03-23-14-30): Session memory update
```

#### 4. 日志配置

```yaml
logging:
  enabled: true
  level: INFO          # DEBUG | INFO | WARNING | ERROR
  file: logs/git-memory.log
```

---

## 使用示例

### 示例 1：基本使用（零配置）

```bash
# 1. 安装
bash skills/git-memory/quick-install.sh

# 2. 重启 OpenClaw
sh /workspace/projects/scripts/restart.sh

# 3. 开始聊天
# Git Memory 会自动工作！
```

### 示例 2：配置远程同步

```bash
# 1. 运行配置向导
python3 skills/git-memory/config-wizard.py

# 输入：
# - 设备类型：local
# - 设备名称：macbook-pro
# - 仓库地址：git@github.com:javamagong/my-memory.git

# 2. 验证配置
cat config/git-memory.yaml

# 3. 测试推送
python3 -c "
from skills.git-memory.lib.git_memory import GitMemorySkill
skill = GitMemorySkill('.')
print(skill.get_sync_status())
"
```

### 示例 3：手动保存记忆

在 OpenClaw 对话中：

```
二明，记住这个：明天上午 10 点有产品评审会议
```

Git Memory 会自动：
1. 保存到 `memory/2026-03-23.md`
2. 创建 Git 提交
3. 推送到远程（如果配置了）

### 示例 4：查看记忆历史

```bash
# 使用 Git 命令
git log --oneline -- memory/

# 搜索特定内容
git grep "产品评审" -- memory/

# 查看某天的记忆
git show 2026-03-23:memory/2026-03-23.md
```

### 示例 5：恢复到历史版本

```bash
# 查看历史
git log --oneline -10 -- MEMORY.md

# 预览变更
git show abc123 -- MEMORY.md

# 恢复（谨慎操作！）
git checkout abc123 -- MEMORY.md

# 提交恢复
git commit -m "revert: 恢复到 abc123"
```

---

## 故障排查

### 问题 1：Hooks 未生效

**症状：** 会话开始/结束时没有自动同步

**检查：**

```bash
# 1. 检查 Hooks 是否安装
ls -la ~/.openclaw/hooks/ | grep git-memory

# 2. 检查 OpenClaw 日志
tail -f /path/to/openclaw/logs/openclaw.log | grep "git-memory"

# 3. 检查 Hooks 语法
node -c ~/.openclaw/hooks/git-memory-session-start.ts
```

**解决：**

```bash
# 重新安装 Hooks
cd /workspace/projects/workspace/skills/git-memory
cp -r .openclaw/hooks/* ~/.openclaw/hooks/

# 重启 OpenClaw
sh /workspace/projects/scripts/restart.sh
```

---

### 问题 2：推送失败

**症状：** `git push` 报错

**常见原因：**

1. **SSH Key 未配置**

```bash
# 检查 SSH Key
ls -la ~/.ssh/*.pub

# 测试 GitHub 连接
ssh -T git@github.com
```

2. **远程仓库不存在**

```bash
# 检查远程配置
git remote -v

# 重新配置
git remote set-url origin git@github.com:user/repo.git
```

3. **网络问题**

```bash
# 测试网络连接
ping github.com

# 检查代理
echo $HTTP_PROXY
echo $HTTPS_PROXY
```

---

### 问题 3：合并冲突

**症状：** `Auto-merge failed` 错误

**解决步骤：**

```bash
# 1. 查看冲突文件
git status

# 2. 手动解决冲突
# 编辑冲突文件，解决 <<< === >>> 标记

# 3. 标记解决
git add <file>

# 4. 完成合并
git commit -m "fix: Resolve merge conflict"

# 5. 推送
git push
```

**预防冲突：**

- 多设备使用不同的 `device_name`
- 配置合适的 `conflict_resolution` 策略
- 定期同步（避免长时间不同步）

---

### 问题 4：性能问题

**症状：** Git 操作变慢

**优化：**

```bash
# 1. 清理无用分支
git branch --merged | grep -v main | xargs git branch -d

# 2. 垃圾回收
git gc --prune=now

# 3. 检查大文件
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | awk '/^blob/ {print $3, $4}' | sort -n | tail -10
```

---

## 高级配置

### 自定义合并策略

创建子系统特定的合并配置：

```bash
# 创建配置文件
cat > subsystems/trading/.mergerc.yaml << 'EOF'
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
    key_field: 'symbol'

_default:
  merge_strategy: local
EOF
```

### 自定义 Hook 行为

编辑 Hook 配置文件：

```typescript
// .openclaw/hooks/git-memory-session-end.ts
export async function onSessionEnd(context: HookContext) {
  // 添加自定义逻辑
  if (context.memory_changes?.includes('trading')) {
    console.log('📈 Trading memory changed, sending notification...');
    // 发送通知等
  }
  
  // 默认行为
  // ...
}
```

### 集成其他工具

```yaml
# config/git-memory.yaml

# 集成通知工具
notifications:
  enabled: true
  on_push: true
  on_conflict: true
  channel: "feishu"  # feishu | discord | slack

# 集成备份工具
backup:
  enabled: true
  schedule: "0 2 * * *"  # 每天凌晨 2 点
  destination: "/backup/memory"
```

---

## 最佳实践

### 1. 定期备份

```bash
# 添加 cron 任务
crontab -e

# 每天凌晨 2 点备份
0 2 * * * cd /workspace && git backup --all /backup/memory
```

### 2. 清理旧记忆

```bash
# 归档 30 天前的记忆
find memory/ -name "*.md" -mtime +30 -exec mv {} archive/ \;

# 提交归档
git add archive/
git commit -m "archive: Move old memory files"
```

### 3. 监控状态

```bash
# 创建监控脚本
cat > scripts/check-memory-status.sh << 'EOF'
#!/bin/bash
cd /workspace
python3 -c "
from skills.git-memory.lib.git_memory import GitMemorySkill
import json
skill = GitMemorySkill('.')
status = skill.get_sync_status()
print(json.dumps(status, indent=2))
"
EOF

chmod +x scripts/check-memory-status.sh
```

---

## 常见问题 (FAQ)

### Q: 需要懂 Git 吗？

**A:** 不需要！所有 Git 操作自动完成。但懂 Git 有助于故障排查。

### Q: 会丢数据吗？

**A:** 不会！Git 版本控制，所有历史都可恢复。建议配置远程备份。

### Q: 会影响 OpenClaw 性能吗？

**A:** 几乎无影响！Git 操作在后台异步执行，延迟 < 100ms。

### Q: 多个会话会冲突吗？

**A:** 有冲突检测机制，会自动合并或提示用户解决。

### Q: 可以离线使用吗？

**A:** 可以！本地版本控制完全正常，联网后自动同步。

---

## 参考资源

- [Git Memory GitHub](https://github.com/javamagong/claw-git-memory-skill)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [Git 官方文档](https://git-scm.com/docs)
- [故障排查指南](docs/conflict-resolution.md)

---

*Built by JavaMaGong & A 小二 via vibe coding 🫡*
