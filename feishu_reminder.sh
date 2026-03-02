#!/bin/bash
# 飞书定时提醒脚本 - 每隔15分钟发送提醒

# 获取当前时间
CURRENT_TIME=$(date '+%Y-%m-%d %H:%M:%S')

# 创建提醒消息
MESSAGE="⏰ **定时工作提醒** - $CURRENT_TIME

该检查一下工作进度了！保持高效工作节奏很重要。

📋 **建议检查事项：**
1. 当前任务进度如何？是否需要调整计划？
2. 有没有需要优先处理的紧急事项？
3. 工作状态如何？是否需要短暂休息？
4. 有没有遗漏的重要事项或待办任务？

💡 **工作效率提示：**
- 使用番茄工作法（25分钟专注 + 5分钟休息）
- 及时记录工作进展和遇到的问题
- 合理安排任务优先级
- 保持工作环境整洁有序

🔄 下次提醒：15分钟后

🌟 **今日目标进度提醒：**
记得回顾今天的计划，确保朝着目标前进！"

# 记录到日志文件
echo "=== 飞书定时提醒 $CURRENT_TIME ===" >> /tmp/feishu_reminder.log
echo "准备发送消息到飞书群聊..." >> /tmp/feishu_reminder.log

# 使用OpenClaw发送消息到飞书
# 注意：这里需要确保OpenClaw环境可用
if command -v openclaw &> /dev/null; then
    echo "发送消息到飞书..." >> /tmp/feishu_reminder.log
    
    # 尝试发送消息
    /root/.nvm/versions/node/v22.22.0/bin/node /root/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw/dist/index.js message send \
        --channel feishu \
        --to "oc_7604f3568c243772ad758903e150def5" \
        --message "$MESSAGE" \
        >> /tmp/feishu_send.log 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✅ 消息发送成功：$CURRENT_TIME" >> /tmp/feishu_reminder.log
        echo "✅ 飞书提醒已发送：$CURRENT_TIME"
    else
        echo "❌ 消息发送失败：$CURRENT_TIME" >> /tmp/feishu_reminder.log
        echo "❌ 飞书提醒发送失败，已记录到日志" >> /tmp/feishu_reminder.log
        echo "⚠️ 提醒已记录但发送失败，请检查OpenClaw配置"
    fi
else
    echo "❌ OpenClaw不可用，无法发送飞书消息" >> /tmp/feishu_reminder.log
    echo "⚠️ OpenClaw不可用，提醒仅记录到日志"
fi

echo "" >> /tmp/feishu_reminder.log