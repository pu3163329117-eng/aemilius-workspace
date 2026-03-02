#!/usr/bin/env python3
"""
项目托管看板 - Rain开学后的项目状态可视化
"""

import json
import datetime
import os
from typing import Dict, List, Any

class ProjectDashboard:
    def __init__(self):
        self.status_file = "/root/.openclaw/workspace/project_status.json"
        self.work_log_file = "/root/.openclaw/workspace/smart_work_log.json"
        self.income_file = "/root/.openclaw/workspace/income_data.json"
        
    def load_data(self) -> Dict[str, Any]:
        """加载所有数据"""
        data = {}
        
        # 加载项目状态
        if os.path.exists(self.status_file):
            with open(self.status_file, 'r', encoding='utf-8') as f:
                data["status"] = json.load(f)
        else:
            data["status"] = {}
        
        # 加载工作日志
        if os.path.exists(self.work_log_file):
            with open(self.work_log_file, 'r', encoding='utf-8') as f:
                data["work_log"] = json.load(f)
        else:
            data["work_log"] = []
        
        # 加载收入数据
        if os.path.exists(self.income_file):
            with open(self.income_file, 'r', encoding='utf-8') as f:
                data["income"] = json.load(f)
        else:
            data["income"] = {}
        
        return data
    
    def generate_dashboard(self) -> str:
        """生成看板内容"""
        data = self.load_data()
        
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        dashboard = [
            "📱 **Rain的项目托管看板**",
            f"更新时间: {current_time}",
            "=" * 50,
            ""
        ]
        
        # 1. iPhone基金状态
        if "income" in data and data["income"]:
            target = data["income"].get("target_amount", 13000)
            current = data["income"].get("current_balance", 0)
            progress = (current / target * 100) if target > 0 else 0
            
            dashboard.append("🎯 **核心目标**: 赚到iPhone 17 Pro Max")
            dashboard.append(f"目标金额: ¥{target:,}")
            dashboard.append(f"当前余额: ¥{current:,}")
            dashboard.append(f"目标进度: {progress:.1f}%")
            
            # 进度条
            bar_length = 30
            filled = int(bar_length * progress / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            dashboard.append(f"[{bar}] {progress:.1f}%")
            
            # 预计完成时间
            if current > 0 and progress < 100:
                daily_goal = 500  # 每日目标
                days_needed = (target - current) / daily_goal
                if days_needed > 0:
                    completion_date = now + datetime.timedelta(days=days_needed)
                    dashboard.append(f"预计完成: {completion_date.strftime('%Y-%m-%d')}")
            
            dashboard.append("")
        
        # 2. 项目状态
        if "status" in data and "projects" in data["status"]:
            dashboard.append("📋 **进行中项目**:")
            
            active_projects = 0
            for project_id, project in data["status"]["projects"].items():
                if project.get("status") == "active":
                    active_projects += 1
                    progress = project.get("progress", 0)
                    
                    dashboard.append(f"📱 {project['name']}")
                    dashboard.append(f"   进度: {progress}% | 状态: {project['status']}")
                    
                    if 'next_task' in project:
                        dashboard.append(f"   下一任务: {project['next_task']}")
                    elif 'next_milestone' in project:
                        dashboard.append(f"   下一里程碑: {project['next_milestone']}")
                    
                    # 项目进度条
                    proj_bar_length = 20
                    proj_filled = int(proj_bar_length * progress / 100)
                    proj_bar = "█" * proj_filled + "░" * (proj_bar_length - proj_filled)
                    dashboard.append(f"   [{proj_bar}] {progress}%")
                    dashboard.append("")
            
            if active_projects == 0:
                dashboard.append("   暂无进行中项目")
                dashboard.append("")
        
        # 3. 今日完成情况
        if "work_log" in data and data["work_log"]:
            today = now.date()
            today_work = []
            
            for work in data["work_log"][-20:]:  # 检查最近20条
                work_time = datetime.datetime.fromisoformat(work["timestamp"])
                if work_time.date() == today:
                    today_work.append(work)
            
            if today_work:
                dashboard.append("✅ **今日完成**:")
                for work in today_work[-5:]:  # 显示最近5项
                    work_time = datetime.datetime.fromisoformat(work["timestamp"]).strftime("%H:%M")
                    dashboard.append(f"- [{work_time}] {work['work_type']}: {work['description'][:50]}...")
                dashboard.append("")
        
        # 4. 待办事项
        if "status" in data and "daily_tasks" in data["status"]:
            pending_tasks = [t for t in data["status"]["daily_tasks"] if not t.get("completed", False)]
            
            if pending_tasks:
                dashboard.append("📝 **待办事项**:")
                for i, task in enumerate(pending_tasks[:5], 1):
                    priority = task.get("priority", "medium")
                    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
                    dashboard.append(f"{i}. {priority_emoji} {task['task']}")
                dashboard.append("")
        
        # 5. 待决策事项
        if "status" in data and "pending_decisions" in data["status"]:
            pending_decisions = [d for d in data["status"]["pending_decisions"] if not d.get("resolved", False)]
            
            if pending_decisions:
                urgent_decisions = [d for d in pending_decisions if d.get("priority") == "high"]
                if urgent_decisions:
                    dashboard.append("🚨 **待决策事项** (需要关注):")
                    for decision in urgent_decisions[:3]:
                        dashboard.append(f"- {decision['question'][:60]}...")
                    dashboard.append("")
        
        # 6. 系统状态
        dashboard.append("🖥️ **系统状态**:")
        
        # 文件状态
        files_status = []
        for file_path, name in [
            (self.status_file, "项目状态"),
            (self.work_log_file, "工作日志"),
            (self.income_file, "收入数据")
        ]:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                files_status.append(f"{name}: {size:,} bytes")
            else:
                files_status.append(f"{name}: 缺失")
        
        dashboard.append(f"数据文件: {', '.join(files_status)}")
        
        # cron状态
        try:
            import subprocess
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            cron_count = result.stdout.count('\n')
            dashboard.append(f"定时任务: {cron_count} 个配置")
        except:
            dashboard.append("定时任务: 检查失败")
        
        dashboard.append("")
        
        # 7. 下一周期计划
        next_cycle_time = (now + datetime.timedelta(minutes=15)).strftime("%H:%M")
        dashboard.append(f"🔄 **下一工作周期**: {next_cycle_time}")
        
        # 基于当前时间的建议
        current_hour = now.hour
        if 8 <= current_hour < 12:
            dashboard.append("💡 **当前建议**: 客户开发与营销推广")
        elif 12 <= current_hour < 18:
            dashboard.append("💡 **当前建议**: 项目执行与开发工作")
        elif 18 <= current_hour < 22:
            dashboard.append("💡 **当前建议**: 优化改进与学习提升")
        else:
            dashboard.append("💡 **当前建议**: 系统维护与准备工作")
        
        dashboard.append("")
        dashboard.append("📞 **沟通说明**:")
        dashboard.append("重要更新随时通知 | 决策事项集中处理 | 每日固定时间汇报")
        
        return "\n".join(dashboard)
    
    def send_dashboard(self):
        """发送看板到飞书"""
        dashboard = self.generate_dashboard()
        
        import subprocess
        
        temp_script = "/tmp/send_dashboard.py"
        with open(temp_script, 'w', encoding='utf-8') as f:
            f.write(f'''
import sys
sys.path.append('/root/.openclaw/workspace')

from send_feishu_api import FeishuSender

sender = FeishuSender()
sender.send_simple_text("""{dashboard}""")
''')
        
        try:
            subprocess.run(['python3', temp_script], check=True)
            print("✅ 项目看板发送成功")
            return True
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return False
        finally:
            if os.path.exists(temp_script):
                os.remove(temp_script)
    
    def show_dashboard(self):
        """在终端显示看板"""
        dashboard = self.generate_dashboard()
        print(dashboard)

def main():
    """主函数"""
    import sys
    
    dashboard = ProjectDashboard()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "show":
            dashboard.show_dashboard()
        
        elif command == "send":
            success = dashboard.send_dashboard()
            if success:
                print("✅ 看板发送完成")
            else:
                print("❌ 发送失败")
        
        elif command == "update":
            # 更新项目状态
            import json
            status_file = "/root/.openclaw/workspace/project_status.json"
            
            if os.path.exists(status_file):
                with open(status_file, 'r', encoding='utf-8') as f:
                    status = json.load(f)
                
                status["last_updated"] = datetime.datetime.now().isoformat()
                
                with open(status_file, 'w', encoding='utf-8') as f:
                    json.dump(status, f, ensure_ascii=False, indent=2)
                
                print("✅ 看板数据已更新")
            else:
                print("❌ 状态文件不存在")
        
        else:
            print("用法:")
            print("  python project_dashboard.py show")
            print("  python project_dashboard.py send")
            print("  python project_dashboard.py update")
    else:
        # 默认显示看板
        print("📱 **项目托管看板系统**")
        print("=" * 50)
        dashboard.show_dashboard()

if __name__ == "__main__":
    main()