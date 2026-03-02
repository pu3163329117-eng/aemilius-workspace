#!/usr/bin/env python3
"""
工作汇报系统 - 文歆向Rain汇报工作
"""

import json
import datetime
import os
from typing import Dict, List, Any

class WorkReportSystem:
    def __init__(self):
        self.report_file = "/root/.openclaw/workspace/work_reports.json"
        self.work_log_file = "/root/.openclaw/workspace/work_log.json"
        self.init_files()
    
    def init_files(self):
        """初始化文件"""
        if not os.path.exists(self.report_file):
            with open(self.report_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
        
        if not os.path.exists(self.work_log_file):
            with open(self.work_log_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def log_work(self, work_type: str, description: str, duration_minutes: int = 15):
        """记录工作日志"""
        work_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "work_type": work_type,
            "description": description,
            "duration_minutes": duration_minutes,
            "reporter": "文歆/Aemilius"
        }
        
        # 读取现有日志
        with open(self.work_log_file, 'r', encoding='utf-8') as f:
            work_log = json.load(f)
        
        # 添加新日志
        work_log.append(work_entry)
        
        # 保存日志
        with open(self.work_log_file, 'w', encoding='utf-8') as f:
            json.dump(work_log, f, ensure_ascii=False, indent=2)
        
        print(f"📝 工作记录: {work_type} - {description}")
        return work_entry
    
    def generate_report(self, period_minutes: int = 15) -> Dict[str, Any]:
        """生成工作报告"""
        now = datetime.datetime.now()
        start_time = now - datetime.timedelta(minutes=period_minutes)
        
        # 读取工作日志
        with open(self.work_log_file, 'r', encoding='utf-8') as f:
            work_log = json.load(f)
        
        # 筛选时间段内的工作
        recent_work = []
        for work in work_log:
            work_time = datetime.datetime.fromisoformat(work["timestamp"])
            if work_time >= start_time:
                recent_work.append(work)
        
        # 统计工作类型
        work_stats = {}
        for work in recent_work:
            work_type = work["work_type"]
            work_stats[work_type] = work_stats.get(work_type, 0) + 1
        
        # 生成报告
        report = {
            "report_id": f"report_{now.strftime('%Y%m%d%H%M%S')}",
            "reporter": "文歆/Aemilius",
            "report_to": "Rain",
            "period_start": start_time.isoformat(),
            "period_end": now.isoformat(),
            "period_minutes": period_minutes,
            "work_count": len(recent_work),
            "work_stats": work_stats,
            "recent_work": recent_work,
            "summary": self.generate_summary(recent_work),
            "next_plan": self.generate_next_plan()
        }
        
        # 保存报告
        with open(self.report_file, 'r', encoding='utf-8') as f:
            reports = json.load(f)
        
        reports.append(report)
        
        with open(self.report_file, 'w', encoding='utf-8') as f:
            json.dump(reports, f, ensure_ascii=False, indent=2)
        
        return report
    
    def generate_summary(self, recent_work: List[Dict[str, Any]]) -> str:
        """生成工作摘要"""
        if not recent_work:
            return "⚠️ 过去15分钟内未记录工作"
        
        work_types = {}
        for work in recent_work:
            work_type = work["work_type"]
            work_types[work_type] = work_types.get(work_type, 0) + 1
        
        summary_parts = []
        for work_type, count in work_types.items():
            summary_parts.append(f"{work_type}: {count}项")
        
        return "，".join(summary_parts)
    
    def generate_next_plan(self) -> str:
        """生成下一步计划"""
        plans = [
            "继续探索互联网，寻找有价值的信息",
            "学习新技术，更新知识库",
            "开发或优化智能体工具",
            "准备下一次工作汇报"
        ]
        
        return " | ".join(plans)
    
    def format_report_for_feishu(self, report: Dict[str, Any]) -> str:
        """格式化报告为飞书消息"""
        period_start = datetime.datetime.fromisoformat(report["period_start"])
        period_end = datetime.datetime.fromisoformat(report["period_end"])
        
        message = [
            f"📊 **文歆工作汇报**",
            f"汇报时间: {period_end.strftime('%Y-%m-%d %H:%M:%S')}",
            f"汇报周期: {period_start.strftime('%H:%M')} - {period_end.strftime('%H:%M')} ({report['period_minutes']}分钟)",
            ""
        ]
        
        if report["work_count"] > 0:
            message.append(f"✅ **工作完成情况**")
            message.append(f"总工作项: {report['work_count']}个")
            
            for work_type, count in report["work_stats"].items():
                message.append(f"- {work_type}: {count}项")
            
            message.append("")
            message.append(f"📝 **工作详情**")
            for i, work in enumerate(report["recent_work"][:3], 1):  # 显示最近3项
                work_time = datetime.datetime.fromisoformat(work["timestamp"]).strftime("%H:%M")
                message.append(f"{i}. [{work_time}] {work['work_type']}: {work['description']}")
            
            if len(report["recent_work"]) > 3:
                message.append(f"... 还有{len(report['recent_work']) - 3}项工作")
        else:
            message.append("⚠️ **过去15分钟无工作记录**")
            message.append("可能原因：")
            message.append("1. 工作未及时记录")
            message.append("2. 正在处理长期任务")
            message.append("3. 系统问题")
        
        message.append("")
        message.append(f"🎯 **下一步计划**")
        message.append(report["next_plan"])
        
        message.append("")
        message.append("---")
        message.append("汇报人: 文歆/Aemilius")
        message.append("接收人: Rain")
        
        return "\n".join(message)
    
    def send_report_to_feishu(self, report: Dict[str, Any]):
        """发送报告到飞书"""
        message = self.format_report_for_feishu(report)
        
        # 调用飞书发送
        import subprocess
        
        # 创建临时脚本
        temp_script = "/tmp/send_report.py"
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
            print(f"📨 工作汇报已发送到飞书")
        except Exception as e:
            print(f"❌ 发送失败: {e}")
        finally:
            if os.path.exists(temp_script):
                os.remove(temp_script)
    
    def auto_report_workflow(self):
        """自动汇报工作流程"""
        print("🔄 开始自动汇报工作流程...")
        
        # 1. 记录当前工作
        current_work = {
            "work_type": "系统维护",
            "description": "更新工作汇报系统，修改提醒机制",
            "duration_minutes": 15
        }
        self.log_work(**current_work)
        
        # 2. 生成报告
        print("📊 生成工作报告...")
        report = self.generate_report(period_minutes=15)
        
        # 3. 发送报告
        print("📨 发送工作汇报...")
        self.send_report_to_feishu(report)
        
        print("✅ 自动汇报流程完成")
        return report

def main():
    """主函数"""
    import sys
    
    report_system = WorkReportSystem()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "log" and len(sys.argv) > 3:
            work_type = sys.argv[2]
            description = " ".join(sys.argv[3:])
            report_system.log_work(work_type, description)
        
        elif command == "report":
            report = report_system.generate_report()
            print(json.dumps(report, ensure_ascii=False, indent=2))
        
        elif command == "send":
            report = report_system.generate_report()
            report_system.send_report_to_feishu(report)
        
        elif command == "auto":
            report_system.auto_report_workflow()
        
        elif command == "recent":
            with open(report_system.work_log_file, 'r', encoding='utf-8') as f:
                work_log = json.load(f)
            
            recent = work_log[-5:] if len(work_log) >= 5 else work_log
            for work in recent:
                time_str = datetime.datetime.fromisoformat(work["timestamp"]).strftime("%H:%M")
                print(f"[{time_str}] {work['work_type']}: {work['description']}")
        
        else:
            print("用法:")
            print("  python work_report_system.py log <类型> <描述>")
            print("  python work_report_system.py report")
            print("  python work_report_system.py send")
            print("  python work_report_system.py auto")
            print("  python work_report_system.py recent")
    else:
        # 自动执行汇报流程
        print("🤖 文歆工作汇报系统")
        print("=" * 50)
        report_system.auto_report_workflow()

if __name__ == "__main__":
    main()