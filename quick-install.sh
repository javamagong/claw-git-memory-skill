#!/bin/bash
# Git Memory Skill - 极简一键安装脚本
# 小白友好：全自动，无需配置，可选远程同步

set -e

echo "🫡 Git Memory Skill - 一键安装"
echo "================================"
echo ""

# 自动检测工作目录
WORKSPACE="${WORKSPACE:-$(pwd)}"
cd "$WORKSPACE"

echo "📁 工作目录：$WORKSPACE"
echo ""

# ========== 1. 检查依赖 ==========
echo "📦 检查依赖..."

# 检查 Git
if ! command -v git &> /dev/null; then
    echo "❌ 未检测到 Git，请先安装 Git"
    echo "   macOS: brew install git"
    echo "   Ubuntu: sudo apt install git"
    exit 1
fi
echo "✅ Git: $(git --version)"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未检测到 Python3，请先安装 Python 3.8+"
    exit 1
fi
echo "✅ Python: $(python3 --version)"

# 检查 PyYAML
if ! python3 -c "import yaml" 2>/dev/null; then
    echo "📦 安装 PyYAML..."
    pip3 install pyyaml --quiet
fi
echo "✅ PyYAML: 已安装"

echo ""

# ========== 2. 初始化 Git（如果需要）==========
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init --quiet
    git config user.name "${USER:-A 小二}"
    git config user.email "${USER:-a-xiaoer}@local"
    echo "✅ Git 仓库已初始化"
else
    echo "✅ Git 仓库已存在"
fi
echo ""

# ========== 3. 创建目录结构 ==========
echo "📁 创建目录结构..."
mkdir -p memory subsystems/trading logs config
echo "✅ 目录结构已创建"
echo ""

# ========== 4. 创建默认配置 ==========
echo "📝 创建配置文件..."

cat > config/git-memory.yaml << 'EOF'
# Git Memory 配置（极简版）

# 远程同步（可选，稍后配置）
remote:
  enabled: false
  url: ""
  auto_pull: true
  auto_push: true

# 多设备同步
multi_device:
  enabled: true
  device_type: local
  device_name: ""  # 自动使用主机名
  sync_on_start: true
  sync_on_end: true
  conflict_resolution: auto

# 自动提交
auto_commit:
  enabled: true
  prefix: "auto"
  include_device: true
  include_timestamp: true

# 日志
logging:
  enabled: true
  level: INFO
  file: logs/git-memory.log
EOF

echo "✅ 配置文件已创建：config/git-memory.yaml"

# ========== 5. 注册 OpenClaw Hooks ==========
echo "🔌 注册 OpenClaw Hooks..."

# 检测 OpenClaw 安装位置
OPENCLAW_HOOKS_DIR=""

# 检查常见位置
if [ -d "$HOME/.openclaw" ]; then
    OPENCLAW_HOOKS_DIR="$HOME/.openclaw/hooks"
elif [ -d "/usr/local/share/openclaw" ]; then
    OPENCLAW_HOOKS_DIR="/usr/local/share/openclaw/hooks"
elif [ -d "/opt/openclaw" ]; then
    OPENCLAW_HOOKS_DIR="/opt/openclaw/hooks"
fi

if [ -n "$OPENCLAW_HOOKS_DIR" ] && [ -d ".openclaw/hooks" ]; then
    echo "📁 检测到 OpenClaw 安装：$OPENCLAW_HOOKS_DIR"
    
    # 创建 hooks 目录（如果不存在）
    mkdir -p "$OPENCLAW_HOOKS_DIR"
    
    # 复制 hooks
    cp -r .openclaw/hooks/* "$OPENCLAW_HOOKS_DIR/" 2>/dev/null || true
    
    echo "✅ OpenClaw Hooks 已注册"
    echo "   重启 OpenClaw 后生效：openclaw gateway restart"
else
    echo "ℹ️  未检测到 OpenClaw 安装，跳过 Hooks 注册"
    echo "   手动安装：cp -r .openclaw/hooks/* /path/to/openclaw/.openclaw/hooks/"
fi
echo ""
echo ""

# ========== 5. 配置 OpenClaw Hooks ==========
echo "🔧 配置 OpenClaw Hooks..."

HOOK_DIR="$WORKSPACE/.openclaw/hooks"
mkdir -p "$HOOK_DIR"

# 会话开始 Hook
cat > "$HOOK_DIR/on-session-start.sh" << 'HOOKEOF'
#!/bin/bash
cd /workspace/projects/workspace

# 自动同步（如果配置了远程）
if git remote get-url origin &>/dev/null 2>&1; then
    python3 -c "
import sys
sys.path.insert(0, 'skills/git-memory/lib')
from git_memory import GitMemorySkill
skill = GitMemorySkill('.')
result = skill.sync_start()
if result.get('synced'):
    print(f'📥 已同步：{result.get(\"message\")}')
" 2>/dev/null || true
fi

# 创建会话分支
SESSION_ID="$(date +%Y%m%d_%H%M%S)_$$"
git checkout -b session-$SESSION_ID 2>/dev/null || true
HOOKEOF

# 会话结束 Hook
cat > "$HOOK_DIR/on-session-end.sh" << 'HOOKEOF'
#!/bin/bash
cd /workspace/projects/workspace

# 检查变更
if ! git diff --quiet 2>/dev/null; then
    python3 -c "
import sys
sys.path.insert(0, 'skills/git-memory/lib')
from git_memory import GitMemorySkill
skill = GitMemorySkill('.')
result = skill.sync_end()
if result.get('synced'):
    print(f'📤 已保存：{result.get(\"message\")}')
" 2>/dev/null || true
fi
HOOKEOF

chmod +x "$HOOK_DIR"/*.sh
echo "✅ Hooks 已配置"
echo ""

# ========== 6. 初始提交 ==========
echo "📝 创建初始提交..."

if ! git log --oneline -1 &>/dev/null; then
    git add -A 2>/dev/null || true
    git commit -m "init: Git Memory 系统初始化" --quiet 2>/dev/null || true
    echo "✅ 初始提交已创建"
else
    echo "✅ Git 已有提交，跳过"
fi
echo ""

# ========== 7. 完成 ==========
echo "🎉 安装完成！"
echo "================================"
echo ""
echo "✅ Git Memory 已就绪"
echo ""
echo "📚 下一步（可选）："
echo ""
echo "   1️⃣  配置远程同步（多设备同步）"
echo "      python3 skills/git-memory/config-wizard.py"
echo ""
echo "   2️⃣  重启 OpenClaw"
echo "      sh /workspace/projects/scripts/restart.sh"
echo ""
echo "   3️⃣  正常使用（记忆自动版本化）"
echo ""
echo "💡 提示："
echo "   - 不配置远程也能用（本地版本控制）"
echo "   - 配置远程后可多设备同步"
echo "   - 查看状态：python3 -m skills.git-memory.sync_manager"
echo ""
echo "📖 文档：skills/git-memory/README.md"
echo ""
