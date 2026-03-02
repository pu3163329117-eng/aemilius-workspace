#!/bin/bash
# 检查工作进度并发送提醒

# 获取当前时间
CURRENT_TIME=$(date '+%Y-%m-%d %H:%M:%S')

# 创建提醒消息
MESSAGE="⏰ **定时提醒** - $CURRENT_TIME

该检查一下工作进度了！

📋 **建议检查事项：**
1. 当前任务进度如何？
2. 有没有需要优先处理的事情？
3. 是否需要休息一下？
4. 有没有遗漏的重要事项？

💡 **工作提示：**
- 保持专注，高效工作
- 合理安排休息时间
- 及时记录工作进展

🔄 下次提醒：15分钟后"

# 输出到日志文件
echo "=== 定时提醒 $CURRENT_TIME ===" >> /tmp/self_reminder.log
echo "$MESSAGE" >> /tmp/self_reminder.log
echo "" >> /tmp/self_reminder.log

# 同时在控制台输出
echo "✅ 已记录定时提醒：$CURRENT_TIME"

# 这里可以添加发送到飞书的逻辑
# 如果需要实际发送到飞书，需要配置飞书机器人webhook