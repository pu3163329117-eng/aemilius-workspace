#!/bin/bash
# 自我工作系统 - 提醒自己工作并汇报

echo "🤖 **文歆自我工作系统**"
echo "========================"
echo "执行时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 1. 发送自我提醒
echo "⏰ 步骤1: 发送自我工作提醒..."
cd /root/.openclaw/workspace
python3 send_feishu_api.py

# 2. 记录工作开始
echo ""
echo "📝 步骤2: 记录工作开始..."
python3 work_report_system.py log "系统执行" "执行自我提醒和工作汇报流程"

# 3. 执行工作（模拟15分钟工作）
echo ""
echo "💼 步骤3: 执行工作..."
echo "工作内容:"
echo "  1. 探索互联网，寻找新技术/新机会"
echo "  2. 学习新知识，更新知识库"
echo "  3. 开发或优化智能体工具"
echo "  4. 准备向Rain汇报"

# 这里可以添加实际的工作内容
# 例如: python3 smart_explorer.py

# 4. 记录工作完成
echo ""
echo "✅ 步骤4: 记录工作完成..."
python3 work_report_system.py log "探索学习" "探索互联网，学习新技术"
python3 work_report_system.py log "工具开发" "开发或优化智能体工具"
python3 work_report_system.py log "知识管理" "更新知识库，整理学习内容"

# 5. 生成并发送工作报告
echo ""
echo "📊 步骤5: 生成并发送工作报告..."
python3 work_report_system.py auto

echo ""
echo "🎉 **自我工作流程完成**"
echo "已提醒自己工作，并已向Rain汇报工作成果"
echo ""
echo "🔄 下次自我提醒: 15分钟后"