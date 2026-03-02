#!/usr/bin/env python3
"""
Rain日程助手 - 基础版本
"""

import json
import datetime
import re
from typing import Dict, List, Optional, Any
import sqlite3
import os

class ScheduleAssistant:
    def __init__(self):
        self.db_path = "/root/.openclaw/workspace/schedule.db"
        self.init_database()
        
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建日程表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            title TEXT,
            description TEXT,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            priority INTEGER DEFAULT 1,
            reminder_settings TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 创建提醒记录表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id TEXT PRIMARY KEY,
            schedule_id TEXT,
            reminder_time TIMESTAMP,
            sent BOOLEAN DEFAULT FALSE,
            sent_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ 数据库初始化完成")
    
    def parse_natural_language(self, text: str) -> Dict[str, Any]:
        """解析自然语言输入"""
        print(f"📝 解析输入: {text}")
        
        # 简单的时间解析（实际应该用更复杂的NLP）
        time_patterns = [
            (r'明天(上午|下午)?(\d+)点', 1),  # 明天下午3点
            (r'今天(上午|下午)?(\d+)点', 0),  # 今天下午2点
            (r'(\d+)月(\d+)日(上午|下午)?(\d+)点', None),  # 3月5日下午3点
            (r'每周[一二三四五六日]', 7),  # 每周一
        ]
        
        # 提取时间信息
        event_time = None
        for pattern, day_offset in time_patterns:
            match = re.search(pattern, text)
            if match:
                now = datetime.datetime.now()
                if day_offset == 0:  # 今天
                    event_time = now.replace(hour=int(match.group(2)), minute=0, second=0)
                elif day_offset == 1:  # 明天
                    event_time = now.replace(hour=int(match.group(2)), minute=0, second=0) + datetime.timedelta(days=1)
                break
        
        # 提取事件类型
        event_types = {
            '会议': ['开会', '会议', 'meeting'],
            '任务': ['完成', '做', '写', '开发'],
            '提醒': ['提醒', '记得', '别忘了']
        }
        
        event_type = '其他'
        for etype, keywords in event_types.items():
            if any(keyword in text for keyword in keywords):
                event_type = etype
                break
        
        # 提取优先级关键词
        priority = 1  # 默认普通
        if any(word in text for word in ['重要', '紧急', '必须']):
            priority = 3
        elif any(word in text for word in ['尽快', '尽快完成']):
            priority = 2
        
        result = {
            'title': self.extract_title(text),
            'description': text,
            'event_type': event_type,
            'priority': priority,
            'parsed_time': event_time.isoformat() if event_time else None
        }
        
        print(f"✅ 解析结果: {result}")
        return result
    
    def extract_title(self, text: str) -> str:
        """从文本中提取标题"""
        # 简单提取，实际应该更智能
        if '开会' in text or '会议' in text:
            return '会议'
        elif '完成' in text:
            return '任务'
        elif '提醒' in text:
            return '提醒'
        else:
            return text[:20] + '...'
    
    def add_schedule(self, user_input: str, user_id: str = "rain") -> Dict[str, Any]:
        """添加日程"""
        parsed = self.parse_natural_language(user_input)
        
        if not parsed['parsed_time']:
            return {'success': False, 'error': '无法识别时间'}
        
        schedule_id = f"schedule_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        start_time = datetime.datetime.fromisoformat(parsed['parsed_time'])
        
        # 默认持续1小时
        end_time = start_time + datetime.timedelta(hours=1)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO schedules (id, user_id, title, description, start_time, end_time, priority)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            schedule_id,
            user_id,
            parsed['title'],
            parsed['description'],
            start_time.isoformat(),
            end_time.isoformat(),
            parsed['priority']
        ))
        
        # 创建提醒
        self.create_reminders(schedule_id, start_time, parsed['priority'])
        
        conn.commit()
        conn.close()
        
        result = {
            'success': True,
            'schedule_id': schedule_id,
            'title': parsed['title'],
            'time': start_time.strftime('%Y-%m-%d %H:%M'),
            'priority': parsed['priority']
        }
        
        print(f"✅ 日程添加成功: {result}")
        return result
    
    def create_reminders(self, schedule_id: str, event_time: datetime.datetime, priority: int):
        """创建提醒"""
        # 使用新的数据库连接
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 基于优先级设置提醒时间
            reminder_times = []
            
            if priority >= 3:  # 高优先级
                reminder_times.extend([
                    event_time - datetime.timedelta(hours=2),
                    event_time - datetime.timedelta(minutes=30),
                    event_time - datetime.timedelta(minutes=10)
                ])
            elif priority >= 2:  # 中优先级
                reminder_times.extend([
                    event_time - datetime.timedelta(hours=1),
                    event_time - datetime.timedelta(minutes=15)
                ])
            else:  # 低优先级
                reminder_times.append(event_time - datetime.timedelta(minutes=30))
            
            for i, reminder_time in enumerate(reminder_times):
                reminder_id = f"reminder_{schedule_id}_{i}"
                cursor.execute('''
                INSERT INTO reminders (id, schedule_id, reminder_time)
                VALUES (?, ?, ?)
                ''', (reminder_id, schedule_id, reminder_time.isoformat()))
            
            conn.commit()
            print(f"✅ 创建了 {len(reminder_times)} 个提醒")
        finally:
            conn.close()
    
    def check_reminders(self):
        """检查需要发送的提醒"""
        now = datetime.datetime.now()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 查找需要发送的提醒
        cursor.execute('''
        SELECT r.id, r.schedule_id, s.title, s.description, s.start_time
        FROM reminders r
        JOIN schedules s ON r.schedule_id = s.id
        WHERE r.sent = FALSE 
        AND r.reminder_time <= ?
        AND s.status = 'active'
        ''', (now.isoformat(),))
        
        reminders = cursor.fetchall()
        
        for reminder in reminders:
            reminder_id, schedule_id, title, description, start_time = reminder
            
            # 发送提醒
            self.send_reminder(reminder_id, title, description, start_time)
            
            # 标记为已发送
            cursor.execute('''
            UPDATE reminders SET sent = TRUE, sent_at = ? WHERE id = ?
            ''', (now.isoformat(), reminder_id))
        
        conn.commit()
        conn.close()
        
        if reminders:
            print(f"✅ 发送了 {len(reminders)} 个提醒")
        else:
            print("⏳ 暂无需要发送的提醒")
        
        return len(reminders)
    
    def send_reminder(self, reminder_id: str, title: str, description: str, event_time: str):
        """发送提醒到飞书"""
        # 使用现有的飞书发送功能
        event_time_dt = datetime.datetime.fromisoformat(event_time)
        time_str = event_time_dt.strftime('%H:%M')
        
        message = f"⏰ **日程提醒**\n\n**{title}**\n时间: {time_str}\n备注: {description}\n\n请做好准备！"
        
        # 调用飞书发送脚本
        import subprocess
        script_path = "/root/.openclaw/workspace/send_feishu_api.py"
        
        # 临时修改发送内容
        original_script = None
        with open(script_path, 'r', encoding='utf-8') as f:
            original_script = f.read()
        
        # 创建临时脚本发送提醒
        temp_script = script_path.replace('.py', '_temp.py')
        with open(temp_script, 'w', encoding='utf-8') as f:
            f.write(f'''
import sys
sys.path.append('/root/.openclaw/workspace')

from send_feishu_api import FeishuSender

sender = FeishuSender()
sender.send_simple_text("""{message}""")
''')
        
        try:
            subprocess.run(['python3', temp_script], check=True)
            print(f"📨 提醒已发送: {title} ({time_str})")
        except Exception as e:
            print(f"❌ 发送失败: {e}")
        finally:
            # 清理临时文件
            if os.path.exists(temp_script):
                os.remove(temp_script)
    
    def get_today_schedule(self, user_id: str = "rain") -> List[Dict[str, Any]]:
        """获取今日日程"""
        today = datetime.datetime.now().date()
        tomorrow = today + datetime.timedelta(days=1)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, title, description, start_time, end_time, priority
        FROM schedules
        WHERE user_id = ?
        AND DATE(start_time) = ?
        AND status = 'active'
        ORDER BY start_time
        ''', (user_id, today.isoformat()))
        
        schedules = []
        for row in cursor.fetchall():
            schedule_id, title, description, start_time, end_time, priority = row
            
            start_dt = datetime.datetime.fromisoformat(start_time)
            end_dt = datetime.datetime.fromisoformat(end_time)
            
            schedules.append({
                'id': schedule_id,
                'title': title,
                'description': description,
                'start_time': start_dt.strftime('%H:%M'),
                'end_time': end_dt.strftime('%H:%M'),
                'priority': priority,
                'priority_text': ['低', '中', '高'][min(priority, 3)-1]
            })
        
        conn.close()
        return schedules
    
    def generate_daily_briefing(self, user_id: str = "rain") -> str:
        """生成每日简报"""
        schedules = self.get_today_schedule(user_id)
        
        if not schedules:
            return "🎉 今日暂无安排，可以自由安排工作！"
        
        briefing = ["📅 **今日日程简报**", ""]
        
        for i, schedule in enumerate(schedules, 1):
            briefing.append(f"{i}. **{schedule['title']}**")
            briefing.append(f"   时间: {schedule['start_time']}-{schedule['end_time']}")
            briefing.append(f"   优先级: {schedule['priority_text']}")
            if schedule['description']:
                briefing.append(f"   备注: {schedule['description']}")
            briefing.append("")
        
        # 添加统计
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
    
    assistant = ScheduleAssistant()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "add" and len(sys.argv) > 2:
            # 添加日程: python schedule_assistant.py add "明天下午3点开会"
            user_input = " ".join(sys.argv[2:])
            result = assistant.add_schedule(user_input)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif command == "check":
            # 检查提醒: python schedule_assistant.py check
            count = assistant.check_reminders()
            print(f"检查完成，处理了 {count} 个提醒")
        
        elif command == "today":
            # 查看今日日程: python schedule_assistant.py today
            schedules = assistant.get_today_schedule()
            if schedules:
                print("📅 今日日程:")
                for schedule in schedules:
                    print(f"  {schedule['start_time']} - {schedule['title']} ({schedule['priority_text']})")
            else:
                print("🎉 今日暂无安排")
        
        elif command == "briefing":
            # 生成简报: python schedule_assistant.py briefing
            briefing = assistant.generate_daily_briefing()
            print(briefing)
        
        else:
            print("用法:")
            print("  python schedule_assistant.py add \"明天下午3点开会\"")
            print("  python schedule_assistant.py check")
            print("  python schedule_assistant.py today")
            print("  python schedule_assistant.py briefing")
    else:
        # 交互模式
        print("📅 Rain日程助手")
        print("=" * 30)
        
        while True:
            print("\n请选择操作:")
            print("1. 添加日程")
            print("2. 查看今日日程")
            print("3. 生成简报")
            print("4. 退出")
            
            choice = input("请输入选项 (1-4): ").strip()
            
            if choice == "1":
                user_input = input("请输入日程描述 (例如: 明天下午3点开会): ").strip()
                if user_input:
                    result = assistant.add_schedule(user_input)
                    print(f"✅ {result['title']} 已安排在 {result['time']}")
            
            elif choice == "2":
                schedules = assistant.get_today_schedule()
                if schedules:
                    print("\n📅 今日日程:")
                    for schedule in schedules:
                        print(f"  {schedule['start_time']} - {schedule['title']} ({schedule['priority_text']})")
                else:
                    print("🎉 今日暂无安排")
            
            elif choice == "3":
                briefing = assistant.generate_daily_briefing()
                print("\n" + briefing)
            
            elif choice == "4":
                print("👋 再见！")
                break
            
            else:
                print("❌ 无效选项")

if __name__ == "__main__":
    main()