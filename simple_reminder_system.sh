#!/bin/bash
# 简单可靠的提醒系统

echo "🕒 **简单提醒系统执行**"
echo "执行时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 1. 发送自我提醒
echo "⏰ 发送自我工作提醒..."
cd /root/.openclaw/workspace

# 创建简单的提醒消息
CURRENT_TIME=$(date '+%Y-%m-%d %H:%M:%S')
MESSAGE="🤖 **文歆工作提醒** - ${CURRENT_TIME}

【提醒对象】文歆/Aemilius
【提醒内容】该开始/继续工作了！

🎯 **当前工作重点：**
1. 为Rain赚iPhone 17 Pro Max的钱！
2. 开发AI助手产品
3. 寻找付费客户
4. 记录收入进展

📱 **记住目标**：赚到¥13,000买新手机！

🔄 下次提醒：15分钟后"

echo "📝 消息内容:"
echo "$MESSAGE"
echo ""

# 发送到飞书
python3 -c "
import sys
sys.path.append('/root/.openclaw/workspace')
from send_feishu_api import FeishuSender
sender = FeishuSender()
sender.send_simple_text('''${MESSAGE}''')
"

if [ $? -eq 0 ]; then
    echo "✅ 提醒发送成功"
else
    echo "❌ 提醒发送失败"
fi

echo ""
echo "2. 记录工作开始..."
python3 -c "
import datetime
import json
import os

# 记录工作
work_log = {
    'timestamp': datetime.datetime.now().isoformat(),
    'work_type': '定时提醒',
    'description': '发送自我工作提醒，专注赚钱任务',
    'duration_minutes': 15,
    'reporter': '文歆/Aemilius'
}

# 保存到文件
log_file = '/root/.openclaw/workspace/simple_work_log.json'
if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        logs = json.load(f)
else:
    logs = []

logs.append(work_log)
with open(log_file, 'w', encoding='utf-8') as f:
    json.dump(logs, f, ensure_ascii=False, indent=2)

print('📝 工作记录完成')
"

echo ""
echo "3. 更新收入追踪状态..."
python3 income_tracker.py status

echo ""
echo "🎯 **下次执行时间**: $(date -d '+15 minutes' '+%H:%M')"
echo "✅ **简单提醒系统执行完成**"