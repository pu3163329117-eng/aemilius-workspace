# GitHub 仓库设置指南

## 仓库信息

- **仓库名称**: aemilius-workspace
- **GitHub URL**: https://github.com/pu3163329117-eng/aemilius-workspace
- **描述**: Aemilius AI assistant workspace with tools, scripts, and skills
- **权限**: 公开仓库

## 已推送的内容

仓库包含以下内容：

### 核心文件
- `IDENTITY.md` - 文歆的身份定义
- `USER.md` - 用户信息（Rain）
- `SOUL.md` - 文歆的核心价值观
- `AGENTS.md` - 工作空间指南
- `TOOLS.md` - 本地工具配置
- `README.md` - 项目说明

### AI 助手工具
- `ai_assistant_builder.py` - AI 助手构建器
- `schedule_assistant.py` - 日程管理助手
- `smart_reminder_system.py` - 智能提醒系统
- `income_tracker.py` - 收入跟踪器
- `project_dashboard.py` - 项目仪表板

### 自动化脚本
- `auto_push.sh` - 自动推送脚本
- 各种 Shell 和 Python 脚本

### 技能库
- `skills/` - 包含各种 AI 技能

### 项目文档
- 各种项目分析和计划文档

## 自动推送设置

### 方法1：使用 auto_push.sh 脚本

```bash
# 授予执行权限（如果尚未设置）
chmod +x auto_push.sh

# 运行自动推送
./auto_push.sh

# 或使用自定义提交信息
./auto_push.sh "修复了某个bug"
```

### 方法2：手动推送

```bash
# 添加所有更改
git add .

# 提交更改
git commit -m "描述你的更改"

# 推送到 GitHub
git push
```

### 方法3：设置 Git 钩子（自动推送）

1. 创建 post-commit 钩子：
   ```bash
   echo '#!/bin/bash
   echo "🚀 自动推送到 GitHub..."
   git push' > .git/hooks/post-commit
   chmod +x .git/hooks/post-commit
   ```

2. 或者使用更智能的钩子：
   ```bash
   cp auto_push.sh .git/hooks/post-commit
   chmod +x .git/hooks/post-commit
   ```

## 日常使用流程

1. **完成代码修改后**：
   ```bash
   ./auto_push.sh
   ```

2. **或使用快捷命令**（添加到 ~/.bashrc）：
   ```bash
   alias aemilius-push='./auto_push.sh'
   ```

3. **查看仓库状态**：
   ```bash
   git status
   ```

## 仓库维护

### 更新本地仓库
```bash
git pull origin master
```

### 查看提交历史
```bash
git log --oneline -10
```

### 检查远程仓库
```bash
git remote -v
```

## 注意事项

1. **敏感信息**：确保不推送包含密码、API密钥等敏感信息的文件
2. **大文件**：GitHub 有文件大小限制，避免推送大文件
3. **定期推送**：建议每次完成重要更改后立即推送
4. **提交信息**：使用清晰的提交信息，便于追踪更改历史

## 故障排除

### 推送失败
1. 检查网络连接
2. 验证 GitHub 令牌是否有效
3. 检查是否有冲突需要解决

### 权限问题
1. 确保有推送权限
2. 检查 Git 配置：
   ```bash
   git config --list
   ```

---

**文歆 (Aemilius)** - 自动化的 GitHub 工作流已设置完成！ 🤝