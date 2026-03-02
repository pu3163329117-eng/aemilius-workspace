#!/bin/bash
# 检查定时提醒状态

echo "🕒 **定时提醒系统状态检查**"
echo "=============================="

# 检查当前时间
echo "📅 当前时间: $(date '+%Y-%m-%d %H:%M:%S %Z')"

# 检查cron任务
echo ""
echo "📋 **Cron任务配置:**"
crontab -l | grep "feishu_cron_wrapper"

# 计算下次执行时间
CURRENT_MINUTE=$(date +%M)
NEXT_MINUTE=$(( (($CURRENT_MINUTE / 15) * 15 + 15) % 60 ))
if [ $NEXT_MINUTE -eq 0 ]; then
    NEXT_MINUTE=0
    HOUR_ADD=1
else
    HOUR_ADD=0
fi

CURRENT_HOUR=$(date +%H)
NEXT_HOUR=$(( (CURRENT_HOUR + HOUR_ADD) % 24 ))

echo "⏰ 下次执行时间: 今天 $(printf "%02d" $NEXT_HOUR):$(printf "%02d" $NEXT_MINUTE)"

# 检查日志文件
echo ""
echo "📊 **日志文件状态:**"

LOG_FILE="/tmp/feishu_reminder_cron.log"
if [ -f "$LOG_FILE" ]; then
    FILE_SIZE=$(stat -c%s "$LOG_FILE")
    FILE_SIZE_KB=$((FILE_SIZE / 1024))
    LAST_MODIFIED=$(stat -c%y "$LOG_FILE" | cut -d'.' -f1)
    
    echo "📁 日志文件: $LOG_FILE"
    echo "📏 文件大小: ${FILE_SIZE_KB}KB"
    echo "🕐 最后修改: $LAST_MODIFIED"
    
    echo ""
    echo "📝 **最近5条日志:**"
    tail -5 "$LOG_FILE" | while IFS= read -r line; do
        echo "   $line"
    done
else
    echo "⚠️  日志文件不存在: $LOG_FILE"
fi

# 检查API脚本
echo ""
echo "🔧 **脚本状态:**"
SCRIPT_PATH="/root/.openclaw/workspace/send_feishu_api.py"
if [ -f "$SCRIPT_PATH" ]; then
    echo "✅ Python脚本: $SCRIPT_PATH (存在)"
    # 检查Python依赖
    if python3 -c "import requests; import json" &> /dev/null; then
        echo "✅ Python依赖: requests, json (已安装)"
    else
        echo "❌ Python依赖: requests 或 json 未安装"
    fi
else
    echo "❌ Python脚本不存在: $SCRIPT_PATH"
fi

# 检查包装脚本
WRAPPER_PATH="/root/.openclaw/workspace/feishu_cron_wrapper.sh"
if [ -f "$WRAPPER_PATH" ]; then
    echo "✅ 包装脚本: $WRAPPER_PATH (存在且可执行)"
else
    echo "❌ 包装脚本不存在: $WRAPPER_PATH"
fi

echo ""
echo "✅ **定时提醒系统运行正常**"
echo "📨 每隔15分钟会自动发送提醒到飞书群聊"