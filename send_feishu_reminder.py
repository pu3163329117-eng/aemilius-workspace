#!/usr/bin/env python3
"""
飞书定时提醒脚本
每隔15分钟发送提醒到飞书群聊
"""

import os
import json
import requests
import datetime

def send_feishu_message():
    """发送消息到飞书群聊"""
    
    # 获取当前时间
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # 构建消息内容
    message = {
        "msg_type": "text",
        "content": {
            "text": f"⏰ 定时提醒 - {current_time}\n\n该检查一下工作进度了！\n\n📋 建议事项：\n1. 当前任务进度如何？\n2. 有没有需要优先处理的事情？\n3. 是否需要休息一下？\n4. 有没有遗漏的重要事项？\n\n💡 保持专注，高效工作！"
        }
    }
    
    # 这里需要飞书机器人的webhook地址
    # 由于没有实际的webhook地址，我们先打印消息
    print(f"【飞书提醒】{current_time}")
    print("消息内容：")
    print(message["content"]["text"])
    print("\n（需要配置飞书机器人webhook才能实际发送）")
    
    # 如果有webhook地址，可以这样发送：
    # webhook_url = "YOUR_FEISHU_WEBHOOK_URL"
    # response = requests.post(webhook_url, json=message)
    # return response.status_code == 200
    
    return True

if __name__ == "__main__":
    send_feishu_message()