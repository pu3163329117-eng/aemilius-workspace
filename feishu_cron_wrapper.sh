#!/bin/bash
# 飞书定时提醒包装脚本

# 设置日志文件
LOG_FILE="/tmp/feishu_reminder_cron.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "=== 飞书定时提醒执行开始: $TIMESTAMP ===" >> "$LOG_FILE"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未找到，无法执行提醒脚本" >> "$LOG_FILE"
    echo "❌ Python3未找到" >> "$LOG_FILE"
    exit 1
fi

# 检查脚本文件
SCRIPT_PATH="/root/.openclaw/workspace/send_feishu_api.py"
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ 脚本文件不存在: $SCRIPT_PATH" >> "$LOG_FILE"
    exit 1
fi

echo "📋 执行飞书提醒脚本..." >> "$LOG_FILE"

# 执行Python脚本
cd /root/.openclaw/workspace
python3 "$SCRIPT_PATH" >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ 飞书提醒发送成功" >> "$LOG_FILE"
    echo "🎉 定时提醒已发送到飞书群聊！"
else
    echo "❌ 飞书提醒发送失败，退出码: $EXIT_CODE" >> "$LOG_FILE"
    echo "⚠️ 提醒发送失败，请检查日志: $LOG_FILE"
fi

echo "=== 飞书定时提醒执行结束: $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

exit $EXIT_CODE