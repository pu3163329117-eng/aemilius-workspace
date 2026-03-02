#!/usr/bin/env python3
"""
智能提醒系统 - 为Rain开学后的项目托管设计
"""

import json
import datetime
import os
import time
from typing import Dict, List, Any

class SmartReminderSystem:
    def __init__(self):
        self.work_log_file = "/root/.openclaw/workspace/smart_work_log.json"
        self.project_status_file = "/root/.openclaw/workspace/project_status.json"
        self.init_files()
        
    def init_files(self):
        """初始化文件"""
        # 工作日志文件
        if not os.path.exists(self.work_log_file):
            with open(self.work_log_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
        
        # 项目状态文件
        if not os.path.exists(self.project_status_file):
            initial_status = {
                "last_updated": datetime.datetime.now().isoformat(),
                "projects": {
                    "iphone_fund": {
                        "name": "iPhone赚钱计划",
                        "target": 13000,
                        "current": 999,
                        "progress": 7.7,
                        "status": "active",
                        "next_milestone": "第一个真实客户",
                        "milestone_date": "2026-03-05"
                    },
                    "ai_assistant": {
                        "name": "AI助手产品开发",
                        "target": "完成5个产品模板",
                        "current": "已完成",
                        "progress": 100,
                        "status": "completed",
                        "next_task": "营销推广",
                        "task_date": "2026-03-02"
                    },
                    "system_build": {
                        "name": "托管系统建设",
                        "target": "完全自动化托管",
                        "current": "规划阶段",
                        "progress": 30,
                        "status": "active",
                        "next_task": "实施基础系统",
                        "task_date": "2026-03-01"
                    }
                },
                "daily_tasks": [],
                "completed_tasks": [],
                "pending_decisions": []
            }
            with open(self.project_status_file, 'w', encoding='utf-8') as f:
                json.dump(initial_status, f, ensure_ascii=False, indent=2)
    
    def log_work(self, work_type: str, description: str, duration_minutes: int = 15):
        """记录工作"""
        work_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "work_type": work_type,
            "description": description,
            "duration_minutes": duration_minutes,
            "cycle": self.get_current_cycle()
        }
        
        with open(self.work_log_file, 'r', encoding='utf-8') as f:
            work_log = json.load(f)
        
        work_log.append(work_entry)
        
        with open(self.work_log_file, 'w', encoding='utf-8') as f:
            json.dump(work_log, f, ensure_ascii=False, indent=2)
        
        return work_entry
    
    def get_current_cycle(self) -> str:
        """获取当前工作周期"""
        now = datetime.datetime.now()
        hour = now.hour
        
        if 0 <= hour < 8:
            return "夜间执行"
        elif 8 <= hour < 12:
            return "上午工作"
        elif 12 <= hour < 18:
            return "下午工作"
        elif 18 <= hour < 22:
            return "晚上工作"
        else:
            return "夜间准备"
    
    def get_last_cycle_work(self) -> List[Dict[str, Any]]:
        """获取上一周期工作"""
        now = datetime.datetime.now()
        fifteen_min_ago = now - datetime.timedelta(minutes=15)
        
        with open(self.work_log_file, 'r', encoding='utf-8') as f:
            work_log = json.load(f)
        
        recent_work = []
        for work in work_log[-10:]:  # 检查最近10条记录
            work_time = datetime.datetime.fromisoformat(work["timestamp"])
            if work_time >= fifteen_min_ago:
                recent_work.append(work)
        
        return recent_work
    
    def update_project_status(self, project_id: str, updates: Dict[str, Any]):
        """更新项目状态"""
        with open(self.project_status_file, 'r', encoding='utf-8') as f:
            status = json.load(f)
        
        if project_id in status["projects"]:
            status["projects"][project_id].update(updates)
            status["last_updated"] = datetime.datetime.now().isoformat()
            
            with open(self.project_status_file, 'w', encoding='utf-8') as f:
                json.dump(status, f, ensure_ascii=False, indent=2)
            
            return True
        return False
    
    def add_daily_task(self, task: str, priority: str = "medium"):
        """添加每日任务"""
        with open(self.project_status_file, 'r', encoding='utf-8') as f:
            status = json.load(f)
        
        task_entry = {
            "id": f"task_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "task": task,
            "priority": priority,
            "added_at": datetime.datetime.now().isoformat(),
            "completed": False
        }
        
        status["daily_tasks"].append(task_entry)
        
        with open(self.project_status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
        
        return task_entry
    
    def complete_task(self, task_id: str):
        """完成任务"""
        with open(self.project_status_file, 'r', encoding='utf-8') as f:
            status = json.load(f)
        
        for task in status["daily_tasks"]:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.datetime.now().isoformat()
                status["completed_tasks"].append(task)
                break
        
        # 移除已完成任务
        status["daily_tasks"] = [t for t in status["daily_tasks"] if not t.get("completed", False)]
        
        with open(self.project_status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
    
    def add_decision_request(self, question: str, options: List[str], priority: str = "medium"):
        """添加决策请求"""
        with open(self.project_status_file, 'r', encoding='utf-8') as f:
            status = json.load(f)
        
        decision = {
            "id": f"decision_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "question": question,
            "options": options,
            "priority": priority,
            "added_at": datetime.datetime.now().isoformat(),
            "resolved": False
        }
        
        status["pending_decisions"].append(decision)
        
        with open(self.project_status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
        
        return decision
    
    def generate_reminder_message(self) -> str:
        """生成提醒消息"""
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        next_time = (now + datetime.timedelta(minutes=15)).strftime("%H:%M")
        
        # 获取上一周期工作
        last_work = self.get_last_cycle_work()
        
        # 获取项目状态
        with open(self.project_status_file, 'r', encoding='utf-8') as f:
            status = json.load(f)
        
        # 构建消息
        message = [
            f"🤖 **文歆工作提醒** - {current_time}",
            f"工作周期: {self.get_current_cycle()}",
            ""
        ]
        
        # 上一周期成果
        if last_work:
            message.append("📊 **上一周期成果** (过去15分钟):")
            for work in last_work[:3]:  # 显示最近3项
                work_time = datetime.datetime.fromisoformat(work["timestamp"]).strftime("%H:%M")
                message.append(f"- [{work_time}] {work['work_type']}: {work['description']}")
        else:
            message.append("📊 **上一周期成果**: 无记录")
        
        message.append("")
        
        # 项目状态摘要
        message.append("🎯 **项目状态摘要**:")
        for project_id, project in status["projects"].items():
            if project["status"] == "active":
                message.append(f"- {project['name']}: {project['progress']}% | 下一目标: {project.get('next_task', project.get('next_milestone', 'N/A'))}")
        
        message.append("")
        
        # iPhone基金状态
        iphone_project = status["projects"]["iphone_fund"]
        message.append(f"📱 **iPhone基金状态**:")
        message.append(f"目标: ¥{iphone_project['target']} | 当前: ¥{iphone_project['current']} | 进度: {iphone_project['progress']}%")
        
        # 进度条
        progress = iphone_project['progress']
        bar_length = 20
        filled = int(bar_length * progress / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        message.append(f"[{bar}] {progress}%")
        
        message.append("")
        
        # 待办事项
        if status["daily_tasks"]:
            message.append("📋 **本周期计划**:")
            for i, task in enumerate(status["daily_tasks"][:3], 1):
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task["priority"], "⚪")
                message.append(f"{i}. {priority_emoji} {task['task']}")
        else:
            message.append("📋 **本周期计划**: 自动执行项目任务")
        
        message.append("")
        
        # 待决策事项
        if status["pending_decisions"]:
            urgent_decisions = [d for d in status["pending_decisions"] if d["priority"] == "high"]
            if urgent_decisions:
                message.append("🚨 **待决策事项** (需要你的关注):")
                for decision in urgent_decisions[:2]:
                    message.append(f"- {decision['question']}")
        
        message.append("")
        message.append(f"🔄 **下次汇报**: {next_time}")
        message.append("💪 **专注目标**: 为Rain赚iPhone 17 Pro Max！")
        
        return "\n".join(message)
    
    def send_reminder(self):
        """发送提醒"""
        message = self.generate_reminder_message()
        
        # 记录发送
        self.log_work("系统提醒", "发送智能工作提醒")
        
        # 发送到飞书
        import subprocess
        
        temp_script = "/tmp/send_smart_reminder.py"
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
            print("✅ 智能提醒发送成功")
            return True
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return False
        finally:
            if os.path.exists(temp_script):
                os.remove(temp_script)
    
    def run_daily_plan(self):
        """运行每日计划"""
        now = datetime.datetime.now()
        current_hour = now.hour
        
        if current_hour == 8:  # 早晨计划
            self.send_daily_plan()
        elif current_hour == 12:  # 中午进展
            self.send_morning_progress()
        elif current_hour == 18:  # 傍晚总结
            self.send_daily_summary()
        elif current_hour == 22:  # 晚上准备
            self.send_tomorrow_preparation()
    
    def send_daily_plan(self):
        """发送每日计划"""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # 添加今日任务
        self.add_daily_task("客户开发与营销推广", "high")
        self.add_daily_task("AI助手产品优化", "medium")
        self.add_daily_task("系统维护与改进", "low")
        
        message = f"""📅 **每日工作计划** - {today}

🎯 **今日重点**:
1. 客户开发：争取第一个付费客户
2. 产品优化：完善AI助手功能
3. 系统建设：准备开学托管系统

📱 **iPhone基金目标**:
今日收入目标: ¥500
累计目标: ¥13,000

🔄 **今日工作周期**:
08:00-12:00: 客户开发与营销
12:00-18:00: 项目执行与开发
18:00-22:00: 优化改进与学习
22:00-08:00: 系统维护与准备

💪 **今日成功标准**:
✅ 完成客户开发任务
✅ 推进至少一个项目
✅ 系统改进有进展

📞 **沟通安排**:
重要更新随时通知
决策事项集中处理
每日固定时间汇报

---
准备好开始今天的工作了吗？"""
        
        # 发送消息
        import subprocess
        
        temp_script = "/tmp/send_daily_plan.py"
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
            print("✅ 每日计划发送成功")
        except Exception as e:
            print(f"❌ 发送失败: {e}")
        finally:
            if os.path.exists(temp_script):
                os.remove(temp_script)
    
    def send_morning_progress(self):
        """发送上午进展"""
        # 实现类似 send_daily_plan 的方法
        pass
    
    def send_daily_summary(self):
        """发送每日总结"""
        # 实现类似 send_daily_plan 的方法
        pass
    
    def send_tomorrow_preparation(self):
        """发送明日准备"""
        # 实现类似 send_daily_plan 的方法
        pass

def main():
    """主函数"""
    import sys
    
    system = SmartReminderSystem()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "remind":
            success = system.send_reminder()
            if success:
                print("✅ 智能提醒已发送")
            else:
                print("❌ 发送失败")
        
        elif command == "log" and len(sys.argv) > 3:
            work_type = sys.argv[2]
            description = " ".join(sys.argv[3:])
            system.log_work(work_type, description)
            print("📝 工作记录完成")
        
        elif command == "task" and len(sys.argv) > 2:
            task = " ".join(sys.argv[2:])
            system.add_daily_task(task)
            print("📋 任务添加完成")
        
        elif command == "status":
            with open(system.project_status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            
            print("📊 **项目状态看板**")
            print(f"更新时间: {status['last_updated']}")
            print()
            
            for project_id, project in status["projects"].items():
                print(f"📱 {project['name']}")
                print(f"   进度: {project['progress']}% | 状态: {project['status']}")
                if 'next_task' in project:
                    print(f"   下一任务: {project['next_task']}")
                elif 'next_milestone' in project:
                    print(f"   下一里程碑: {project['next_milestone']}")
                print()
        
        elif command == "plan":
            system.send_daily_plan()
        
        else:
            print("用法:")
            print("  python smart_reminder_system.py remind")
            print("  python smart_reminder_system.py log <类型> <描述>")
            print("  python smart_reminder_system.py task <任务描述>")
            print("  python smart_reminder_system.py status")
            print("  python smart_reminder_system.py plan")
    else:
        # 默认发送提醒
        print("🤖 **智能提醒系统启动**")
        print("=" * 50)
        
        success = system.send_reminder()
        
        if success:
            print("✅ 系统运行正常")
            print("🔄 下次提醒: 15分钟后")
        else:
            print("❌ 系统运行异常，请检查")

if __name__ == "__main__":
    main()