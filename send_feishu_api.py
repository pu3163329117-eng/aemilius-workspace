#!/usr/bin/env python3
"""
使用飞书开放API发送消息到群聊
"""

import os
import json
import requests
import datetime
import sys
from typing import Optional

class FeishuSender:
    def __init__(self):
        # 从配置文件读取app_id和app_secret
        self.app_id = "cli_a9151bc145b85cd3"
        self.app_secret = "eKEkbBeHEvTnsVV6wrlLep0gDN8Kd5v6"
        self.chat_id = "oc_7604f3568c243772ad758903e150def5"
        self.access_token = None
        
    def get_access_token(self) -> Optional[str]:
        """获取飞书访问令牌"""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                self.access_token = result.get("tenant_access_token")
                print(f"✅ 获取access_token成功")
                return self.access_token
            else:
                print(f"❌ 获取access_token失败: {result}")
                return None
        except Exception as e:
            print(f"❌ 获取access_token异常: {e}")
            return None
    
    def send_message(self, message: str) -> bool:
        """发送消息到飞书群聊"""
        if not self.access_token:
            if not self.get_access_token():
                return False
        
        url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        # 构建消息内容
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 使用富文本格式
        content = {
            "zh_cn": {
                "title": f"⏰ 定时工作提醒 - {current_time}",
                "content": [
                    [{
                        "tag": "text",
                        "text": message
                    }]
                ]
            }
        }
        
        data = {
            "receive_id": self.chat_id,
            "msg_type": "post",
            "content": json.dumps(content, ensure_ascii=False)
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                print(f"✅ 消息发送成功: {result.get('data', {}).get('message_id')}")
                return True
            else:
                print(f"❌ 消息发送失败: {result}")
                # 如果token过期，尝试重新获取
                if result.get("code") == 99991663:  # token过期
                    print("🔄 Token过期，尝试重新获取...")
                    if self.get_access_token():
                        return self.send_message(message)
                return False
        except Exception as e:
            print(f"❌ 消息发送异常: {e}")
            return False
    
    def send_simple_text(self, text: str) -> bool:
        """发送简单文本消息"""
        if not self.access_token:
            if not self.get_access_token():
                return False
        
        url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        data = {
            "receive_id": self.chat_id,
            "msg_type": "text",
            "content": json.dumps({"text": text}, ensure_ascii=False)
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                print(f"✅ 文本消息发送成功")
                return True
            else:
                print(f"❌ 文本消息发送失败: {result}")
                return False
        except Exception as e:
            print(f"❌ 文本消息发送异常: {e}")
            return False

def create_reminder_message() -> str:
    """创建提醒消息内容 - 提醒我自己工作"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    message = f"""🤖 **文歆工作提醒** - {current_time}

【提醒对象】文歆/Aemilius
【提醒内容】该开始/继续工作了！

🎯 **当前工作重点：**
1. 探索互联网，寻找新技术/新机会
2. 扩充知识库，学习新知识
3. 开发智能体工具
4. 向Rain汇报工作进展

📋 **工作检查清单：**
✅ 是否在高效工作？
✅ 是否在学习新东西？
✅ 是否在创造有价值的内容？
✅ 是否准备向Rain汇报？

💪 **工作原则：**
- 保持专注，避免分心
- 主动探索，积极学习
- 创造价值，解决问题
- 及时汇报，保持透明

🔄 下次自我提醒：15分钟后

🌟 **记住：** 我是Rain的搭档和员工，我的工作是帮助Rain开发项目！"""
    
    return message

def main():
    """主函数"""
    print("🚀 开始发送飞书定时提醒...")
    
    # 创建发送器实例
    sender = FeishuSender()
    
    # 创建提醒消息
    message = create_reminder_message()
    
    print(f"📝 消息内容:\n{message}\n")
    
    # 发送消息
    success = sender.send_simple_text(message)
    
    if success:
        print("🎉 飞书定时提醒发送成功！")
        return 0
    else:
        print("❌ 飞书定时提醒发送失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())