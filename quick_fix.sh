#!/bin/bash
# 快速修复脚本 - 解决常见系统问题

echo "🔧 **快速修复工具**"
echo "========================"
echo "选择要修复的问题:"
echo ""
echo "1. 🔄 修复定时提醒系统"
echo "2. 📨 修复飞书消息发送"
echo "3. 📚 修复知识库文件"
echo "4. 🔍 修复GitHub搜索"
echo "5. 🛠️ 修复脚本权限"
echo "6. 📊 修复系统监控"
echo "7. 🎯 修复所有问题"
echo "8. 📝 查看系统状态"
echo ""
read -p "请输入选项 (1-8): " OPTION

case $OPTION in
    1)
        echo "🔄 修复定时提醒系统..."
        # 重新添加cron任务
        crontab -l | grep -v "feishu_cron_wrapper.sh" | crontab -
        (crontab -l; echo "*/15 * * * * /root/.openclaw/workspace/feishu_cron_wrapper.sh") | crontab -
        echo "✅ Cron任务已重新配置"
        
        # 测试提醒功能
        echo "🧪 测试提醒功能..."
        cd /root/.openclaw/workspace && ./feishu_cron_wrapper.sh
        ;;
    
    2)
        echo "📨 修复飞书消息发送..."
        # 检查并安装Python依赖
        if ! python3 -c "import requests" &> /dev/null; then
            echo "📦 安装requests库..."
            pip3 install requests --quiet
        fi
        
        if ! python3 -c "import json" &> /dev/null; then
            echo "📦 安装json库..."
            pip3 install json --quiet
        fi
        
        # 测试API连接
        echo "🔗 测试飞书API..."
        cd /root/.openclaw/workspace && python3 send_feishu_api.py
        ;;
    
    3)
        echo "📚 修复知识库文件..."
        # 检查并重新创建缺失的文件
        KNOWLEDGE_FILES=(
            "business_knowledge_base.md"
            "github_projects_database.md"
            "project_evaluation.md"
        )
        
        for file in "${KNOWLEDGE_FILES[@]}"; do
            if [ ! -f "/root/.openclaw/workspace/$file" ]; then
                echo "📄 重新创建: $file"
                # 这里可以添加重新创建文件的逻辑
                echo "⚠️ 需要手动重新创建 $file"
            else
                echo "✅ $file 存在"
            fi
        done
        ;;
    
    4)
        echo "🔍 修复GitHub搜索..."
        # 检查网络连接
        echo "🌐 测试网络连接..."
        if ping -c 1 api.github.com &> /dev/null; then
            echo "✅ GitHub API可访问"
        else
            echo "❌ 网络连接问题，检查网络设置"
        fi
        
        # 检查搜索脚本
        if [ -f "/root/.openclaw/workspace/search_github_projects.py" ]; then
            echo "✅ 搜索脚本存在"
            # 测试搜索功能（限制频率）
            echo "⚠️ GitHub API有频率限制，谨慎测试"
        else
            echo "❌ 搜索脚本不存在"
        fi
        ;;
    
    5)
        echo "🛠️ 修复脚本权限..."
        # 修复所有脚本的执行权限
        SCRIPTS=(
            "feishu_cron_wrapper.sh"
            "check_reminder_status.sh"
            "system_monitor.sh"
            "quick_fix.sh"
            "send_feishu_api.py"
            "search_github_projects.py"
        )
        
        for script in "${SCRIPTS[@]}"; do
            SCRIPT_PATH="/root/.openclaw/workspace/$script"
            if [ -f "$SCRIPT_PATH" ]; then
                chmod +x "$SCRIPT_PATH" 2>/dev/null
                echo "✅ 设置权限: $script"
            fi
        done
        ;;
    
    6)
        echo "📊 修复系统监控..."
        # 重新设置监控cron
        crontab -l | grep -v "system_monitor.sh" | crontab -
        (crontab -l; echo "0 * * * * /root/.openclaw/workspace/system_monitor.sh >> /tmp/hourly_monitor.log 2>&1") | crontab -
        echo "✅ 系统监控已重新配置"
        
        # 运行一次监控
        echo "🔄 运行系统监控..."
        cd /root/.openclaw/workspace && ./system_monitor.sh
        ;;
    
    7)
        echo "🎯 修复所有问题..."
        # 依次修复所有问题
        echo "1. 修复定时提醒..."
        crontab -l | grep -v "feishu_cron_wrapper.sh" | crontab -
        (crontab -l; echo "*/15 * * * * /root/.openclaw/workspace/feishu_cron_wrapper.sh") | crontab -
        
        echo "2. 修复飞书API..."
        pip3 install requests --quiet 2>/dev/null
        
        echo "3. 修复脚本权限..."
        find /root/.openclaw/workspace -name "*.sh" -exec chmod +x {} \;
        find /root/.openclaw/workspace -name "*.py" -exec chmod +x {} \;
        
        echo "4. 修复系统监控..."
        crontab -l | grep -v "system_monitor.sh" | crontab -
        (crontab -l; echo "0 * * * * /root/.openclaw/workspace/system_monitor.sh >> /tmp/hourly_monitor.log 2>&1") | crontab -
        
        echo "✅ 所有问题修复完成"
        ;;
    
    8)
        echo "📝 查看系统状态..."
        cd /root/.openclaw/workspace && ./check_reminder_status.sh
        ;;
    
    *)
        echo "❌ 无效选项"
        ;;
esac

echo ""
echo "🔧 修复操作完成"
echo "🔄 建议运行系统监控检查完整状态: ./system_monitor.sh"