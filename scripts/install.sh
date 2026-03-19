#!/bin/bash
# Git Memory Skill - 一键安装脚本
# 小白友好：全自动，无需配置

set -e

echo "🚀 安装 Git Memory Skill..."
echo ""

# 检查工作目录
WORKSPACE="${WORKSPACE:-/workspace/projects/workspace}"
cd "$WORKSPACE"
echo "✅ 工作目录：$WORKSPACE"

# 1. 检查 Git
if ! command -v git &> /dev/null; then
    echo "❌ 未检测到 Git，请先安装 Git"
    echo "   macOS: brew install git"
    echo "   Ubuntu: sudo apt install git"
    echo "   Windows: 下载安装 https://git-scm.com"
    exit 1
fi
echo "✅ Git 已安装：$(git --version)"

# 2. 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未检测到 Python3，请先安装 Python 3.8+"
    exit 1
fi
echo "✅ Python 已安装：$(python3 --version)"

# 3. 初始化 Git（如果未初始化）
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init
    git config user.name "A 小二"
    git config user.email "a-xiaoer@local"
else
    echo "✅ Git 仓库已存在"
fi

# 4. 创建目录结构
echo "📁 创建记忆目录结构..."
mkdir -p memory
mkdir -p subsystems/{trading,conversation,skills,tools}
mkdir -p logs

# 5. 创建 .gitignore（如果不存在）
if [ ! -f ".gitignore" ]; then
    echo "📝 创建 .gitignore..."
    cat > .gitignore << 'EOF'
# 敏感信息
*.pem
*.key
*secret*
*password*
*.env
.env.local

# 临时文件
*.tmp
*.log
.cache/
__pycache__/

# 系统文件
.DS_Store
Thumbs.db
*.swp
*.swo
EOF
else
    echo "✅ .gitignore 已存在"
fi

# 6. 创建示例 .mergerc.yaml
echo "📝 创建示例合并配置..."
mkdir -p subsystems/trading
cat > subsystems/trading/.mergerc.yaml << 'EOF'
version: 1
description: "股票交易系统合并配置"

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
EOF

# 7. 迁移现有记忆（如果有）
if [ -f "MEMORY.md" ] || [ -d "memory" ]; then
    echo "🔄 迁移现有记忆到 Git 管理..."
    git add MEMORY.md memory/ 2>/dev/null || true
    git commit -m "init: 迁移现有记忆到 Git 管理" || true
fi

# 8. 初始提交
if ! git log --oneline -1 &>/dev/null; then
    echo "📝 创建初始提交..."
    git add .
    git commit -m "init: Git Memory 系统初始化

- MEMORY.md: 全局长期记忆
- memory/: 每日记忆
- subsystems/: 子系统记忆
  - trading/: 股票交易
  - conversation/: 对话
  - skills/: 技能学习
  - tools/: 工具配置
"
fi

# 9. 配置 OpenClaw Hook
echo "🔧 配置 OpenClaw 自动 Hook..."

HOOK_DIR="$WORKSPACE/.openclaw/hooks"
mkdir -p "$HOOK_DIR"

# 会话开始 Hook
cat > "$HOOK_DIR/on-session-start.sh" << 'EOF'
#!/bin/bash
# 会话开始：拉取最新记忆 + 创建会话分支

cd /workspace/projects/workspace

# 启动恢复（清理残留 worktree）
python3 -c "
from lib.git_memory.worktree import WorktreeRegistry
registry = WorktreeRegistry('.')
registry.startup_recovery()
" 2>/dev/null || true

# 拉取最新记忆（如果有远程）
if git remote get-url origin &>/dev/null; then
    git pull --quiet origin main 2>/dev/null || true
fi

# 创建会话分支
SESSION_ID=$(date +%Y%m%d_%H%M%S)_$$
git checkout -b session-$SESSION_ID 2>/dev/null || true

echo "✅ 会话开始：$SESSION_ID"
EOF

chmod +x "$HOOK_DIR/on-session-start.sh"

# 会话结束 Hook
cat > "$HOOK_DIR/on-session-end.sh" << 'EOF'
#!/bin/bash
# 会话结束：自动提交变更

cd /workspace/projects/workspace

# 检查是否有变更
if ! git diff --quiet || ! git diff --cached --quiet; then
    # 获取当前分支
    SESSION_BRANCH=$(git branch --show-current 2>/dev/null || echo "")
    
    # 自动添加
    git add -A 2>/dev/null || true
    
    # 自动提交
    TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
    git commit -m "auto: 会话结束记忆更新 [$TIMESTAMP]" --quiet || true
    
    # 合并到 main（如果是会话分支）
    if [[ "$SESSION_BRANCH" == session-* ]]; then
        git checkout main --quiet 2>/dev/null || true
        git merge "$SESSION_BRANCH" --no-ff --no-edit --quiet 2>/dev/null || true
        git branch -d "$SESSION_BRANCH" --quiet 2>/dev/null || true
    fi
    
    # 异步推送（不阻塞）
    if git remote get-url origin &>/dev/null; then
        (
            timeout 30 git push --quiet origin main 2>/dev/null || {
                echo "[$(date)] Push failed or timeout" >> logs/git-memory.log
            }
        ) &
    fi
    
    echo "✅ 会话结束：记忆已保存"
else
    echo "ℹ️  无记忆变更"
fi
EOF

chmod +x "$HOOK_DIR/on-session-end.sh"

echo "✅ Hook 已配置"

# 10. 完成
echo ""
echo "🎉 安装完成！"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Git Memory 已就绪"
echo ""
echo "📚 下一步："
echo "   1. 重启 OpenClaw 生效"
echo "   2. 正常使用，记忆自动版本化"
echo "   3. 查询历史：git log --oneline"
echo ""
echo "📖 查看文档："
echo "   - 飞书设计文档：https://feishu.cn/docx/..."
echo "   - 使用示例：skills/git-memory/examples/"
echo ""
echo "💡 提示："
echo "   - 配置远程备份（可选）：git remote add origin <url>"
echo "   - 查看帮助：git-memory --help"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
