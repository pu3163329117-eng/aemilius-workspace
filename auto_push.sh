#!/bin/bash

# Aemilius 自动推送脚本
# 用于在完成代码修改后自动推送到 GitHub

echo "🚀 Aemilius 自动推送脚本启动..."
echo "================================"

# 检查当前目录是否为 Git 仓库
if [ ! -d ".git" ]; then
    echo "❌ 错误：当前目录不是 Git 仓库"
    exit 1
fi

# 获取当前分支
current_branch=$(git branch --show-current)
echo "📁 当前分支: $current_branch"

# 检查是否有未提交的更改
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ 没有未提交的更改"
    exit 0
fi

echo "📝 检测到未提交的更改："

# 显示状态
git status -s

# 添加所有更改
echo "📦 添加所有更改..."
git add .

# 提交更改
commit_message="更新: $(date '+%Y-%m-%d %H:%M:%S') - Aemilius 工作空间"
if [ $# -eq 1 ]; then
    commit_message="$1"
fi

echo "💾 提交更改: $commit_message"
git commit -m "$commit_message"

# 推送到远程仓库
echo "🚀 推送到 GitHub..."
if git push origin "$current_branch"; then
    echo "✅ 推送成功！"
    echo "🔗 仓库地址: https://github.com/pu3163329117-eng/aemilius-workspace"
else
    echo "❌ 推送失败，请检查网络连接或权限"
    exit 1
fi

echo "================================"
echo "🎉 Aemilius 工作空间已同步到 GitHub"