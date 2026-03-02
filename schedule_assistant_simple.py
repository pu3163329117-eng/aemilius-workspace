#!/usr/bin/env python3
"""
Rain日程助手 - 简化演示版本
"""

import json
import datetime
import re
from typing import Dict, List, Optional, Any

class SimpleScheduleAssistant:
    def __init__(self):
        self.schedules = []
        print("📅 日程助手已启动")
    
    def parse_natural_language(self, text: str) -> Dict[str, Any]:
        """解析自然语言输入"""
        print(f"📝 解析: {text}")
        
        # 简单的时间解析
        now = datetime.datetime.now()
        
        # 检查"明天"
        if "明天" in text:
            match = re.search(r'明天(上午|下午)?(\d+)点', text)
            if match:
                hour = int(match.group(2))
                if match.group(1) == "下午" and hour < 12:
                    hour += 12
                
                event_time = (now + datetime.timedelta(days=1)).replace(
                    hour=hour, minute=0, second=0, microsecond=0
                )
            else:
                event_time = (now + datetime.timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
        
        # 检查"今天"
        elif "今天" in text:
            match = re.search(r'今天(上午|下午)?(\d+)点', text)
            if match:
                hour = int(match.group(2))
                if match.group(1) == "下午" and hour < 12:
                    hour += 12
                
                event_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            else:
                event_time = now.replace(hour=14, minute=0, second=0, microsecond=0)
        
        else:
            event_time = now.replace(hour=10, minute=0, second=0, microsecond=0)
        
        # 提取事件类型
        if "开会" in text or "会议" in text:
            title = "会议"
        elif "完成" in text:
            title = "任务"
        elif "提醒" in text:
            title = "提醒"
        else:
            title = "日程"
        
        # 提取优先级
        priority = 1
        if "重要" in text or "紧急" in text:
            priority = 3
        elif "尽快" in text:
            priority = 2
        
        return {
            'title': title,
            'description': text,
            'time': event_time,
            'priority': priority
        }
    
    def add_schedule(self, text: str) -> Dict[str, Any]:
        """添加日程"""
        parsed = self.parse_natural_language(text)
        
        schedule = {
            'id': f"schedule_{len(self.schedules)}",
            'title': parsed['title'],
            'description': parsed['description'],
            'time': parsed['time'],
            'priority': parsed['priority'],
            'added_at': datetime.datetime.now()
        }
        
        self.schedules.append(schedule)
        
        # 安排提醒
        self.schedule_reminders(schedule)
        
        result = {
            'success': True,
            'schedule': schedule,
            'message': f"✅ {parsed['title']} 已安排在 {parsed['time'].strftime('%m月%d日 %H:%M')}"
        }
        
        print(result['message'])
        return result
    
    def schedule_reminders(self, schedule: Dict[str, Any]):
        """安排提醒"""
        event_time = schedule['time']
        priority = schedule['priority']
        
        reminders = []
        
        if priority >= 3:  # 高优先级
            reminders.extend([
                ("提前2小时", event_time - datetime.timedelta(hours=2)),
                ("提前30分钟", event_time - datetime.timedelta(minutes=30)),
                ("提前10分钟", event_time - datetime.timedelta(minutes=10))
            ])
        elif priority >= 2:  # 中优先级
            reminders.extend([
                ("提前1小时", event_time - datetime.timedelta(hours=1)),
                ("提前15分钟", event_time - datetime.timedelta(minutes=15))
            ])
        else:  # 低优先级
            reminders.append(("提前30分钟", event_time - datetime.timedelta(minutes=30)))
        
        schedule['reminders'] = reminders
        print(f"⏰ 安排了 {len(reminders)} 个提醒")
    
    def check_reminders(self):
        """检查需要发送的提醒"""
        now = datetime.datetime.now()
        reminders_to_send = []
        
        for schedule in self.schedules:
            if 'reminders' in schedule:
                for reminder_name, reminder_time in schedule['reminders']:
                    # 检查是否到了提醒时间（简单版本）
                    if now >= reminder_time and reminder_time > schedule['added_at']:
                        reminders_to_send.append({
                            'schedule': schedule,
                            'reminder_name': reminder_name,
                            'reminder_time': reminder_time
                        })
        
        if reminders_to_send:
            print(f"🔔 有 {len(reminders_to_send)} 个提醒需要发送")
            for reminder in reminders_to_send:
                self.send_reminder(reminder)
        else:
            print("⏳ 暂无需要发送的提醒")
        
        return len(reminders_to_send)
    
    def send_reminder(self, reminder: Dict[str, Any]):
        """发送提醒"""
        schedule = reminder['schedule']
        event_time = schedule['time'].strftime('%H:%M')
        
        message = f"⏰ **{reminder['reminder_name']}提醒**\n\n"
        message += f"**{schedule['title']}**\n"
        message += f"时间: {event_time}\n"
        message += f"备注: {schedule['description']}\n\n"
        message += "请做好准备！"
        
        print(f"📨 发送提醒: {schedule['title']} ({event_time})")
        
        # 这里可以集成飞书发送
        # 暂时先打印
        print("=" * 40)
        print(message)
        print("=" * 40)
    
    def get_today_schedule(self) -> List[Dict[str, Any]]:
        """获取今日日程"""
        today = datetime.datetime.now().date()
        
        today_schedules = []
        for schedule in self.schedules:
            if schedule['time'].date() == today:
                today_schedules.append(schedule)
        
        return today_schedules
    
    def show_today_schedule(self):
        """显示今日日程"""
        schedules = self.get_today_schedule()
        
        if not schedules:
            print("🎉 今日暂无安排")
            return
        
        print("📅 今日日程:")
        print("-" * 40)
        
        for i, schedule in enumerate(schedules, 1):
            time_str = schedule['time'].strftime('%H:%M')
            priority_text = ['低', '中', '高'][min(schedule['priority'], 3)-1]
            
            print(f"{i}. {time_str} - {schedule['title']} ({priority_text}优先级)")
            print(f"   备注: {schedule['description']}")
            
            if 'reminders' in schedule:
                reminder_times = [rt[1].strftime('%H:%M') for rt in schedule['reminders']]
                print(f"   提醒时间: {', '.join(reminder_times)}")
            
            print()
    
    def generate_briefing(self) -> str:
        """生成简报"""
        schedules = self.get_today_schedule()
        
        if not schedules:
            return "🎉 今日暂无安排，可以自由安排工作！"
        
        briefing = ["📅 **今日日程简报**", ""]
        
        for i, schedule in enumerate(schedules, 1):
            time_str = schedule['time'].strftime('%H:%M')
            priority_text = ['低', '中', '高'][min(schedule['priority'], 3)-1]
            
            briefing.append(f"{i}. **{schedule['title']}**")
            briefing.append(f"   时间: {time_str}")
            briefing.append(f"   优先级: {priority_text}")
            briefing.append(f"   备注: {schedule['description']}")
            briefing.append("")
        
        # 统计
        total = len(schedules)
        high_priority = sum(1 for s in schedules if s['priority'] >= 3)
        
        briefing.append(f"📊 **今日统计**")
        briefing.append(f"   总安排: {total} 个")
        briefing.append(f"   高优先级: {high_priority} 个")
        briefing.append("")
        briefing.append("💪 祝今日工作顺利！")
        
        return "\n".join(briefing)

def main():
    """主函数"""
    import sys
    
    assistant = SimpleScheduleAssistant()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "add" and len(sys.argv) > 2:
            user_input = " ".join(sys.argv[2:])
            result = assistant.add_schedule(user_input)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif command == "check":
            count = assistant.check_reminders()
            print(f"检查完成，处理了 {count} 个提醒")
        
        elif command == "today":
            assistant.show_today_schedule()
        
        elif command == "briefing":
            briefing = assistant.generate_briefing()
            print(briefing)
        
        else:
            print("用法:")
            print("  python schedule_assistant_simple.py add \"明天下午3点开会\"")
            print("  python schedule_assistant_simple.py check")
            print("  python schedule_assistant_simple.py today")
            print("  python schedule_assistant_simple.py briefing")
    else:
        # 演示模式
        print("=" * 50)
        print("📅 Rain日程助手 - 演示版")
        print("=" * 50)
        
        # 添加示例日程
        print("\n1. 添加示例日程:")
        assistant.add_schedule("明天上午10点产品评审会")
        assistant.add_schedule("今天下午3点和技术团队开会")
        assistant.add_schedule("明天前完成项目计划书")
        
        print("\n2. 查看今日日程:")
        assistant.show_today_schedule()
        
        print("\n3. 生成简报:")
        briefing = assistant.generate_briefing()
        print(briefing)
        
        print("\n4. 检查提醒:")
        assistant.check_reminders()
        
        print("\n" + "=" * 50)
        print("✅ 演示完成！")
        print("你可以使用命令行来管理日程:")
        print("  python schedule_assistant_simple.py add \"你的日程描述\"")
        print("  python schedule_assistant_simple.py today")

if __name__ == "__main__":
    main()