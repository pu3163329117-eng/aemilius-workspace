#!/usr/bin/env python3
"""
收入追踪系统 - 追踪iPhone基金进度
"""

import json
import datetime
import os
from typing import Dict, List, Any

class IncomeTracker:
    def __init__(self):
        self.data_file = "/root/.openclaw/workspace/income_data.json"
        self.target_amount = 13000  # iPhone 17 Pro Max 目标
        self.init_data()
    
    def init_data(self):
        """初始化数据文件"""
        if not os.path.exists(self.data_file):
            data = {
                "target_amount": self.target_amount,
                "start_date": datetime.datetime.now().isoformat(),
                "current_balance": 0,
                "transactions": [],
                "daily_goals": {},
                "milestones": [
                    {"amount": 1300, "name": "10% - 第一个项目", "achieved": False},
                    {"amount": 3900, "name": "30% - 稳定收入", "achieved": False},
                    {"amount": 6500, "name": "50% - 过半目标", "achieved": False},
                    {"amount": 9100, "name": "70% - 接近完成", "achieved": False},
                    {"amount": 13000, "name": "100% - 购买iPhone!", "achieved": False}
                ]
            }
            self.save_data(data)
    
    def load_data(self) -> Dict[str, Any]:
        """加载数据"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data: Dict[str, Any]):
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_income(self, amount: float, source: str, description: str = ""):
        """添加收入"""
        data = self.load_data()
        
        transaction = {
            "id": f"tx_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "amount": amount,
            "source": source,
            "description": description,
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "income"
        }
        
        data["transactions"].append(transaction)
        data["current_balance"] += amount
        
        # 检查里程碑
        self.check_milestones(data)
        
        self.save_data(data)
        
        print(f"✅ 收入记录: +¥{amount} ({source})")
        print(f"   当前余额: ¥{data['current_balance']}")
        print(f"   目标进度: {self.get_progress(data):.1f}%")
        
        return transaction
    
    def add_expense(self, amount: float, category: str, description: str = ""):
        """添加支出"""
        data = self.load_data()
        
        transaction = {
            "id": f"exp_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "amount": amount,
            "category": category,
            "description": description,
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "expense"
        }
        
        data["transactions"].append(transaction)
        data["current_balance"] -= amount
        
        self.save_data(data)
        
        print(f"📤 支出记录: -¥{amount} ({category})")
        print(f"   当前余额: ¥{data['current_balance']}")
        
        return transaction
    
    def check_milestones(self, data: Dict[str, Any]):
        """检查里程碑"""
        current_balance = data["current_balance"]
        
        for milestone in data["milestones"]:
            if not milestone["achieved"] and current_balance >= milestone["amount"]:
                milestone["achieved"] = True
                print(f"🎉 达成里程碑: {milestone['name']}!")
    
    def get_progress(self, data: Dict[str, Any] = None) -> float:
        """获取进度百分比"""
        if data is None:
            data = self.load_data()
        
        current = data["current_balance"]
        target = data["target_amount"]
        
        if target == 0:
            return 0
        
        return (current / target) * 100
    
    def set_daily_goal(self, date: str, goal_amount: float):
        """设置每日目标"""
        data = self.load_data()
        
        if "daily_goals" not in data:
            data["daily_goals"] = {}
        
        data["daily_goals"][date] = {
            "goal_amount": goal_amount,
            "achieved_amount": 0,
            "achieved": False
        }
        
        self.save_data(data)
        print(f"🎯 设置每日目标: {date} - ¥{goal_amount}")
    
    def update_daily_goal(self, date: str, amount: float):
        """更新每日目标进度"""
        data = self.load_data()
        
        if date in data.get("daily_goals", {}):
            goal = data["daily_goals"][date]
            goal["achieved_amount"] += amount
            
            if goal["achieved_amount"] >= goal["goal_amount"]:
                goal["achieved"] = True
                print(f"✅ 完成每日目标: {date}")
            else:
                remaining = goal["goal_amount"] - goal["achieved_amount"]
                print(f"📊 每日目标进度: ¥{goal['achieved_amount']}/¥{goal['goal_amount']} (剩余: ¥{remaining})")
            
            self.save_data(data)
    
    def generate_report(self) -> str:
        """生成报告"""
        data = self.load_data()
        
        current_balance = data["current_balance"]
        target_amount = data["target_amount"]
        progress = self.get_progress(data)
        
        # 计算统计
        total_income = sum(t["amount"] for t in data["transactions"] if t["type"] == "income")
        total_expense = sum(t["amount"] for t in data["transactions"] if t["type"] == "expense")
        
        # 最近交易
        recent_transactions = data["transactions"][-5:] if len(data["transactions"]) >= 5 else data["transactions"]
        
        # 里程碑状态
        achieved_milestones = [m for m in data["milestones"] if m["achieved"]]
        pending_milestones = [m for m in data["milestones"] if not m["achieved"]]
        
        report = [
            "📱 **iPhone 17 Pro Max 基金追踪报告**",
            "=" * 50,
            f"目标金额: ¥{target_amount}",
            f"当前余额: ¥{current_balance}",
            f"目标进度: {progress:.1f}%",
            "",
            f"📊 **统计信息**",
            f"总收入: ¥{total_income}",
            f"总支出: ¥{total_expense}",
            f"净收入: ¥{total_income - total_expense}",
            "",
            f"🏆 **里程碑进度**",
            f"已完成: {len(achieved_milestones)}/{len(data['milestones'])}"
        ]
        
        for milestone in achieved_milestones:
            report.append(f"✅ {milestone['name']}")
        
        for milestone in pending_milestones[:2]:  # 显示接下来2个
            needed = milestone['amount'] - current_balance
            report.append(f"⏳ {milestone['name']} (还需: ¥{needed})")
        
        report.append("")
        report.append("💳 **最近交易**")
        
        for tx in recent_transactions:
            time_str = datetime.datetime.fromisoformat(tx["timestamp"]).strftime("%m-%d %H:%M")
            if tx["type"] == "income":
                report.append(f"  +¥{tx['amount']} - {tx.get('source', '未知')} ({time_str})")
            else:
                report.append(f"  -¥{tx['amount']} - {tx.get('category', '未知')} ({time_str})")
        
        if len(data["transactions"]) > 5:
            report.append(f"  ... 还有{len(data['transactions']) - 5}条记录")
        
        report.append("")
        report.append("💪 **今日建议**")
        
        if progress < 10:
            report.append("立即开始客户开发，争取第一个项目！")
        elif progress < 30:
            report.append("建立稳定客户流，提高月收入")
        elif progress < 50:
            report.append("过半目标！保持势头，优化服务")
        elif progress < 70:
            report.append("接近完成！考虑扩大服务范围")
        else:
            report.append("即将达成目标！准备购买iPhone")
        
        report.append("")
        report.append(f"📅 报告时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(report)
    
    def send_daily_report(self):
        """发送每日报告到飞书"""
        report = self.generate_report()
        
        # 调用飞书发送
        import subprocess
        
        temp_script = "/tmp/send_income_report.py"
        with open(temp_script, 'w', encoding='utf-8') as f:
            f.write(f'''
import sys
sys.path.append('/root/.openclaw/workspace')

from send_feishu_api import FeishuSender

sender = FeishuSender()
sender.send_simple_text("""{report}""")
''')
        
        try:
            subprocess.run(['python3', temp_script], check=True)
            print("📨 收入报告已发送到飞书")
        except Exception as e:
            print(f"❌ 发送失败: {e}")
        finally:
            if os.path.exists(temp_script):
                os.remove(temp_script)

def main():
    """主函数"""
    import sys
    
    tracker = IncomeTracker()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "add" and len(sys.argv) > 3:
            amount = float(sys.argv[2])
            source = sys.argv[3]
            description = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""
            tracker.add_income(amount, source, description)
        
        elif command == "expense" and len(sys.argv) > 3:
            amount = float(sys.argv[2])
            category = sys.argv[3]
            description = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""
            tracker.add_expense(amount, category, description)
        
        elif command == "report":
            report = tracker.generate_report()
            print(report)
        
        elif command == "send":
            tracker.send_daily_report()
        
        elif command == "goal" and len(sys.argv) > 3:
            date = sys.argv[2]
            amount = float(sys.argv[3])
            tracker.set_daily_goal(date, amount)
        
        elif command == "update" and len(sys.argv) > 3:
            date = sys.argv[2]
            amount = float(sys.argv[3])
            tracker.update_daily_goal(date, amount)
        
        elif command == "status":
            data = tracker.load_data()
            progress = tracker.get_progress(data)
            print(f"📱 iPhone基金状态")
            print(f"目标: ¥{data['target_amount']}")
            print(f"当前: ¥{data['current_balance']}")
            print(f"进度: {progress:.1f}%")
            
            # 显示进度条
            bar_length = 30
            filled = int(bar_length * progress / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"[{bar}] {progress:.1f}%")
        
        else:
            print("用法:")
            print("  python income_tracker.py add <金额> <来源> [描述]")
            print("  python income_tracker.py expense <金额> <类别> [描述]")
            print("  python income_tracker.py report")
            print("  python income_tracker.py send")
            print("  python income_tracker.py goal <日期> <金额>")
            print("  python income_tracker.py update <日期> <金额>")
            print("  python income_tracker.py status")
    else:
        # 显示当前状态
        print("💰 **iPhone 17 Pro Max 收入追踪系统**")
        print("=" * 50)
        
        data = tracker.load_data()
        progress = tracker.get_progress(data)
        
        print(f"目标金额: ¥{data['target_amount']}")
        print(f"当前余额: ¥{data['current_balance']}")
        print(f"目标进度: {progress:.1f}%")
        
        # 进度条
        bar_length = 40
        filled = int(bar_length * progress / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"[{bar}] {progress:.1f}%")
        
        print()
        print("🎯 今日行动:")
        print("1. 设置每日收入目标")
        print("2. 开始客户开发")
        print("3. 记录第一笔收入")
        print("4. 发送进度报告")

if __name__ == "__main__":
    main()