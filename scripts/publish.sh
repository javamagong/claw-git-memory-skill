#!/bin/bash
# Git Memory Skill - 打包发布脚本

set -e

echo "🚀 打包 Git Memory Skill..."
echo ""

SKILL_DIR="/workspace/projects/workspace/skills/git-memory"
DIST_DIR="/workspace/projects/workspace/skills/git-memory/dist"
VERSION="1.0.0"

# 清理旧包
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

cd "$SKILL_DIR"

# 复制必要文件
echo "📦 复制文件..."
cp -r SKILL.md \
      README.md \
      scripts/ \
      lib/ \
      examples/ \
      docs/ \
      tests/ \
      requirements.txt \
      "$DIST_DIR/"

# 创建安装包
echo "📦 创建安装包..."
cd "$DIST_DIR"
tar -czf "../git-memory-skill-${VERSION}.tar.gz" .

echo ""
echo "✅ 打包完成！"
echo ""
echo "📦 安装包：$SKILL_DIR/git-memory-skill-${VERSION}.tar.gz"
echo ""
echo "📚 发布到 ClawHub:"
echo "   npx clawdhub publish \\"
echo "     --name 'Git Memory' \\"
echo "     --version '$VERSION' \\"
echo "     --file 'git-memory-skill-${VERSION}.tar.gz' \\"
echo "     --description 'AI 记忆自动版本管理系统'"
echo ""
