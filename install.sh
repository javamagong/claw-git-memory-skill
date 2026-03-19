#!/bin/bash
# Git Memory Skill - 一键安装（真正的一句话）
# 可以在任何目录执行

set -e

# 自动检测工作目录
WORKSPACE="${WORKSPACE:-/workspace/projects/workspace}"

# 检查 Skill 是否存在
if [ ! -d "$WORKSPACE/skills/git-memory" ]; then
    echo "❌ Git Memory Skill 未找到"
    echo ""
    echo "请先克隆或下载 Skill 到："
    echo "  $WORKSPACE/skills/git-memory"
    echo ""
    exit 1
fi

# 切换到工作目录并执行安装
cd "$WORKSPACE"
bash skills/git-memory/scripts/install.sh
