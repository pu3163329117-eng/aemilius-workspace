#!/bin/bash
# 实时监控脚本 - 观察系统运行状态

echo "👀 **实时系统监控**"
echo "========================"
echo "监控开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "监控间隔: 30秒"
echo "按 Ctrl+C 停止监控"
echo ""

# 设置颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 监控循环
while true; do
    clear
    echo -e "${BLUE}🕒 系统实时监控 - $(date '+%H:%M:%S')${NC}"
    echo "========================================"
    
    # 1. 检查定时任务状态
    echo -e "\n${YELLOW}📋 1. 定时任务状态${NC}"
    echo "----------------------------------------"
    
    # 检查cron任务
    CRON_COUNT=$(crontab -l | grep -c "feishu_cron_wrapper.sh")
    if [ "$CRON_COUNT" -eq 1 ]; then
        echo -e "${GREEN}✅ 定时提醒任务: 已配置${NC}"
        CRON_TIME=$(crontab -l | grep "feishu_cron_wrapper.sh")
        echo "   配置: $CRON_TIME"
    else
        echo -e "${RED}❌ 定时提醒任务: 配置异常${NC}"
    fi
    
    # 2. 检查最近执行
    echo -e "\n${YELLOW}📋 2. 最近执行记录${NC}"
    echo "----------------------------------------"
    
    LOG_FILE="/tmp/feishu_reminder_cron.log"
    if [ -f "$LOG_FILE" ]; then
        LAST_EXEC=$(tail -3 "$LOG_FILE" 2>/dev/null | grep -E "执行开始|执行结束" || echo "暂无执行记录")
        echo "📝 最后执行:"
        echo "$LAST_EXEC" | while IFS= read -r line; do
            echo "   $line"
        done
    else
        echo -e "${RED}⚠️ 日志文件不存在${NC}"
    fi
    
    # 3. 检查飞书API状态
    echo -e "\n${YELLOW}📋 3. 飞书API状态${NC}"
    echo "----------------------------------------"
    
    # 检查Python脚本
    if [ -f "/root/.openclaw/workspace/send_feishu_api.py" ]; then
        echo -e "${GREEN}✅ API脚本: 正常${NC}"
    else
        echo -e "${RED}❌ API脚本: 缺失${NC}"
    fi
    
    # 4. 检查系统资源
    echo -e "\n${YELLOW}📋 4. 系统资源${NC}"
    echo "----------------------------------------"
    
    # CPU使用率
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    if [ $(echo "$CPU_USAGE < 80" | bc) -eq 1 ]; then
        echo -e "${GREEN}⚡ CPU使用率: ${CPU_USAGE}%${NC}"
    else
        echo -e "${RED}⚡ CPU使用率: ${CPU_USAGE}%${NC}"
    fi
    
    # 内存使用率
    MEM_TOTAL=$(free -m | awk 'NR==2{print $2}')
    MEM_USED=$(free -m | awk 'NR==2{print $3}')
    MEM_PERCENT=$((MEM_USED * 100 / MEM_TOTAL))
    if [ "$MEM_PERCENT" -lt 80 ]; then
        echo -e "${GREEN}🧠 内存使用: ${MEM_PERCENT}% (${MEM_USED}M/${MEM_TOTAL}M)${NC}"
    else
        echo -e "${RED}🧠 内存使用: ${MEM_PERCENT}% (${MEM_USED}M/${MEM_TOTAL}M)${NC}"
    fi
    
    # 5. 检查下次执行时间
    echo -e "\n${YELLOW}📋 5. 下次执行时间${NC}"
    echo "----------------------------------------"
    
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
    
    MINUTES_LEFT=$(( (NEXT_MINUTE - CURRENT_MINUTE + 60) % 60 ))
    if [ "$MINUTES_LEFT" -eq 0 ]; then
        MINUTES_LEFT=15  # 整点时刻
    fi
    
    if [ "$MINUTES_LEFT" -le 5 ]; then
        echo -e "${YELLOW}⏰ 下次提醒: $(printf "%02d" $NEXT_HOUR):$(printf "%02d" $NEXT_MINUTE) (${MINUTES_LEFT}分钟后)${NC}"
    else
        echo -e "${GREEN}⏰ 下次提醒: $(printf "%02d" $NEXT_HOUR):$(printf "%02d" $NEXT_MINUTE) (${MINUTES_LEFT}分钟后)${NC}"
    fi
    
    # 6. 检查监控任务
    echo -e "\n${YELLOW}📋 6. 系统监控${NC}"
    echo "----------------------------------------"
    
    MONITOR_COUNT=$(crontab -l | grep -c "system_monitor.sh")
    if [ "$MONITOR_COUNT" -eq 1 ]; then
        echo -e "${GREEN}✅ 系统监控: 已启用${NC}"
    else
        echo -e "${RED}❌ 系统监控: 未启用${NC}"
    fi
    
    # 7. 显示实时日志
    echo -e "\n${YELLOW}📋 7. 实时日志 (最后5行)${NC}"
    echo "----------------------------------------"
    
    if [ -f "$LOG_FILE" ]; then
        tail -5 "$LOG_FILE" 2>/dev/null | while IFS= read -r line; do
            if echo "$line" | grep -q "成功\|正常\|✅"; then
                echo -e "${GREEN}   $line${NC}"
            elif echo "$line" | grep -q "失败\|错误\|❌"; then
                echo -e "${RED}   $line${NC}"
            elif echo "$line" | grep -q "警告\|注意\|⚠️"; then
                echo -e "${YELLOW}   $line${NC}"
            else
                echo "   $line"
            fi
        done
    else
        echo "   暂无日志"
    fi
    
    echo -e "\n${BLUE}========================================${NC}"
    echo "监控更新: $(date '+%H:%M:%S')"
    echo "按 Ctrl+C 停止监控"
    
    # 等待30秒
    sleep 30
done