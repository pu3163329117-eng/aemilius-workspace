#!/usr/bin/env python3
"""
AI助手生成器 - 可销售的产品
价格：¥999-¥2,999
功能：为企业/个人快速生成定制AI助手
"""

import json
import datetime
import os
from typing import Dict, List, Any

class AIAssistantBuilder:
    def __init__(self):
        self.templates = self.load_templates()
        self.pricing = {
            "basic": 999,      # 基础版：¥999
            "standard": 1999,  # 标准版：¥1,999
            "premium": 2999    # 高级版：¥2,999
        }
        
    def load_templates(self) -> Dict[str, Any]:
        """加载AI助手模板"""
        return {
            "customer_service": {
                "name": "智能客服助手",
                "description": "自动回答客户问题，处理常见咨询",
                "features": [
                    "常见问题自动回答",
                    "工单自动创建",
                    "客户情绪分析",
                    "服务满意度调查"
                ],
                "tech_stack": ["Python", "FastAPI", "OpenAI API", "SQLite"],
                "delivery_days": 3
            },
            "content_creator": {
                "name": "内容创作助手",
                "description": "自动生成营销文案、社交媒体内容",
                "features": [
                    "多平台文案生成",
                    "内容风格定制",
                    "关键词优化",
                    "发布计划安排"
                ],
                "tech_stack": ["Python", "LangChain", "GPT API", "Markdown"],
                "delivery_days": 5
            },
            "data_analyst": {
                "name": "数据分析助手",
                "description": "自动分析数据，生成可视化报告",
                "features": [
                    "数据清洗处理",
                    "统计分析报告",
                    "图表自动生成",
                    "趋势预测分析"
                ],
                "tech_stack": ["Python", "Pandas", "Matplotlib", "Jupyter"],
                "delivery_days": 7
            },
            "schedule_manager": {
                "name": "日程管理助手",
                "description": "智能管理日程，自动安排会议",
                "features": [
                    "自然语言日程录入",
                    "智能时间安排",
                    "会议提醒通知",
                    "工作进度跟踪"
                ],
                "tech_stack": ["Python", "SQLite", "Feishu API", "自然语言处理"],
                "delivery_days": 4
            },
            "social_media": {
                "name": "社交媒体助手",
                "description": "自动管理社交媒体账号，发布内容",
                "features": [
                    "多平台内容发布",
                    "粉丝互动管理",
                    "数据分析报告",
                    "竞品监控"
                ],
                "tech_stack": ["Python", "Selenium", "API集成", "数据分析"],
                "delivery_days": 6
            }
        }
    
    def show_catalog(self):
        """显示产品目录"""
        print("🤖 **AI助手产品目录**")
        print("=" * 50)
        
        for template_id, template in self.templates.items():
            print(f"\n📱 {template['name']}")
            print(f"   {template['description']}")
            print(f"   功能: {', '.join(template['features'][:2])}...")
            print(f"   技术栈: {', '.join(template['tech_stack'])}")
            print(f"   交付时间: {template['delivery_days']}天")
            print(f"   价格范围: ¥999 - ¥2,999")
        
        print("\n" + "=" * 50)
        print("💡 选择模板后，我们可以根据需求定制开发")
    
    def create_quote(self, template_id: str, version: str = "standard", custom_features: List[str] = None) -> Dict[str, Any]:
        """创建报价单"""
        if template_id not in self.templates:
            raise ValueError(f"模板不存在: {template_id}")
        
        template = self.templates[template_id]
        base_price = self.pricing.get(version, 1999)
        
        # 计算定制功能加价
        extra_price = 0
        if custom_features:
            extra_price = len(custom_features) * 200  # 每个定制功能加¥200
        
        total_price = base_price + extra_price
        
        quote = {
            "quote_id": f"quote_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "template": template['name'],
            "version": version,
            "base_price": base_price,
            "extra_features": custom_features or [],
            "extra_price": extra_price,
            "total_price": total_price,
            "delivery_days": template['delivery_days'],
            "features": template['features'] + (custom_features or []),
            "tech_stack": template['tech_stack'],
            "created_at": datetime.datetime.now().isoformat(),
            "valid_until": (datetime.datetime.now() + datetime.timedelta(days=7)).isoformat()
        }
        
        return quote
    
    def generate_project(self, quote: Dict[str, Any], customer_info: Dict[str, str]) -> Dict[str, Any]:
        """生成项目文件"""
        project_id = f"project_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        project_dir = f"/root/.openclaw/workspace/projects/{project_id}"
        
        # 创建项目目录
        os.makedirs(project_dir, exist_ok=True)
        
        # 生成项目配置文件
        project_config = {
            "project_id": project_id,
            "customer": customer_info,
            "quote": quote,
            "status": "created",
            "created_at": datetime.datetime.now().isoformat(),
            "milestones": [
                {"name": "需求确认", "due_days": 1, "status": "pending"},
                {"name": "原型设计", "due_days": 2, "status": "pending"},
                {"name": "开发实现", "due_days": quote['delivery_days'] - 2, "status": "pending"},
                {"name": "测试验收", "due_days": quote['delivery_days'] - 1, "status": "pending"},
                {"name": "交付部署", "due_days": quote['delivery_days'], "status": "pending"}
            ]
        }
        
        config_path = os.path.join(project_dir, "project_config.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(project_config, f, ensure_ascii=False, indent=2)
        
        # 生成项目文档
        self.generate_documentation(project_dir, project_config)
        
        # 生成初始代码框架
        self.generate_code_framework(project_dir, quote)
        
        return {
            "project_id": project_id,
            "project_dir": project_dir,
            "config": config_path,
            "status": "created",
            "next_steps": ["需求确认会议", "支付定金50%", "开始开发"]
        }
    
    def generate_documentation(self, project_dir: str, project_config: Dict[str, Any]):
        """生成项目文档"""
        doc_path = os.path.join(project_dir, "README.md")
        
        doc_content = f"""# {project_config['quote']['template']} - AI助手项目

## 项目信息
- **项目ID**: {project_config['project_id']}
- **客户**: {project_config['customer'].get('name', '未指定')}
- **创建时间**: {project_config['created_at']}
- **交付时间**: {project_config['quote']['delivery_days']}天后

## 项目报价
- **基础价格**: ¥{project_config['quote']['base_price']}
- **定制功能加价**: ¥{project_config['quote']['extra_price']}
- **总价格**: ¥{project_config['quote']['total_price']}
- **报价有效期**: {project_config['quote']['valid_until']}

## 功能列表
{chr(10).join(f'- {feature}' for feature in project_config['quote']['features'])}

## 技术栈
{chr(10).join(f'- {tech}' for tech in project_config['quote']['tech_stack'])}

## 项目里程碑
{chr(10).join(f'- {milestone["name"]}: 第{milestone["due_days"]}天 ({milestone["status"]})' for milestone in project_config['milestones'])}

## 付款方式
1. **定金**: 50% (¥{project_config['quote']['total_price'] // 2})
2. **验收后尾款**: 50% (¥{project_config['quote']['total_price'] // 2})

## 交付物
1. 完整的源代码
2. 部署文档
3. 使用手册
4. 技术培训（1小时）
5. 30天免费维护

## 联系方式
- 开发团队: 文歆/Aemilius
- 沟通工具: 飞书
- 响应时间: 24小时内

---
*本项目由AI助手生成器自动创建*
"""
        
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(doc_content)
    
    def generate_code_framework(self, project_dir: str, quote: Dict[str, Any]):
        """生成代码框架"""
        code_dir = os.path.join(project_dir, "src")
        os.makedirs(code_dir, exist_ok=True)
        
        # 生成主文件
        main_py = os.path.join(code_dir, "main.py")
        with open(main_py, 'w', encoding='utf-8') as f:
            f.write(f'''#!/usr/bin/env python3
"""
{quote['template']} - AI助手
为客户定制的AI助手系统
"""

import json
import logging
from typing import Dict, Any

class AIAssistant:
    def __init__(self, config_path: str = "config.json"):
        """初始化AI助手"""
        self.config = self.load_config(config_path)
        self.logger = self.setup_logger()
        
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {{"name": "{quote['template']}", "version": "1.0.0"}}
    
    def setup_logger(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def run(self):
        """运行AI助手"""
        self.logger.info(f"启动{self.config.get('name', 'AI助手')}")
        print(f"🚀 {self.config.get('name', 'AI助手')} 已启动！")
        
        # 这里添加具体的业务逻辑
        # 根据quote['features']实现相应功能
        
        self.logger.info("AI助手运行中...")
    
    def get_status(self) -> Dict[str, Any]:
        """获取状态"""
        return {{
            "name": self.config.get("name", "AI助手"),
            "version": self.config.get("version", "1.0.0"),
            "status": "running",
            "features": {json.dumps(quote['features'], ensure_ascii=False)},
            "timestamp": datetime.datetime.now().isoformat()
        }}

if __name__ == "__main__":
    assistant = AIAssistant()
    assistant.run()
''')
        
        # 生成配置文件模板
        config_py = os.path.join(code_dir, "config.json")
        with open(config_py, 'w', encoding='utf-8') as f:
            config = {
                "name": quote['template'],
                "version": "1.0.0",
                "features": quote['features'],
                "created_at": datetime.datetime.now().isoformat(),
                "customer": "待填写"
            }
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        # 生成需求文件
        requirements_txt = os.path.join(project_dir, "requirements.txt")
        with open(requirements_txt, 'w', encoding='utf-8') as f:
            f.write("""requests>=2.28.0
python-dotenv>=0.21.0
openai>=0.27.0
langchain>=0.0.200
fastapi>=0.95.0
uvicorn>=0.21.0
sqlite3
logging
json
datetime
""")
        
        # 生成部署脚本
        deploy_sh = os.path.join(project_dir, "deploy.sh")
        with open(deploy_sh, 'w', encoding='utf-8') as f:
            f.write(f'''#!/bin/bash
# {quote['template']} 部署脚本

echo "🚀 开始部署 {quote['template']}..."

# 1. 安装依赖
echo "📦 安装Python依赖..."
pip install -r requirements.txt

# 2. 配置环境
echo "⚙️ 配置环境..."
cp .env.example .env
echo "请编辑 .env 文件配置API密钥和其他设置"

# 3. 初始化数据库
echo "🗄️ 初始化数据库..."
python init_db.py

# 4. 启动服务
echo "🚀 启动服务..."
python main.py &

echo "✅ {quote['template']} 部署完成！"
echo "访问地址: http://localhost:8000"
echo "查看日志: tail -f app.log"
''')
        
        os.chmod(deploy_sh, 0o755)
    
    def create_marketing_material(self, template_id: str) -> str:
        """创建营销材料"""
        template = self.templates[template_id]
        
        material = f"""🎯 **{template['name']} - AI助手解决方案**

## 💡 解决什么问题？
{template['description']}

## 🚀 核心功能
{chr(10).join(f'✅ {feature}' for feature in template['features'])}

## 🛠️ 技术优势
{chr(10).join(f'🔧 {tech}' for tech in template['tech_stack'])}

## ⏱️ 交付时间
仅需 {template['delivery_days']} 天即可交付使用！

## 💰 价格方案
- **基础版**: ¥999 (核心功能)
- **标准版**: ¥1,999 (完整功能 + 基础定制)
- **高级版**: ¥2,999 (完整功能 + 深度定制 + 培训)

## 🎁 包含内容
1. 完整的源代码
2. 部署文档和脚本
3. 使用手册
4. 1小时技术培训
5. 30天免费维护

## 📞 立即订购
联系微信/飞书，告诉我们您的需求！
24小时内提供详细方案和报价。

---
*由文歆/Aemilius专业开发，质量保证*"""
        
        return material

def main():
    """主函数"""
    import sys
    
    builder = AIAssistantBuilder()
    
    print("🤖 **AI助手生成器 - 赚钱工具**")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "catalog":
            builder.show_catalog()
        
        elif command == "quote" and len(sys.argv) > 2:
            template_id = sys.argv[2]
            version = sys.argv[3] if len(sys.argv) > 3 else "standard"
            
            try:
                quote = builder.create_quote(template_id, version)
                print("📋 **报价单**")
                print(json.dumps(quote, ensure_ascii=False, indent=2))
            except ValueError as e:
                print(f"❌ 错误: {e}")
        
        elif command == "market" and len(sys.argv) > 2:
            template_id = sys.argv[2]
            material = builder.create_marketing_material(template_id)
            print(material)
        
        else:
            print("用法:")
            print("  python ai_assistant_builder.py catalog")
            print("  python ai_assistant_builder.py quote <模板ID> [版本]")
            print("  python ai_assistant_builder.py market <模板ID>")
    else:
        # 演示模式
        print("💼 **立即开始赚钱！**")
        print()
        print("选择赚钱方式:")
        print("1. 销售AI助手 (¥999-¥2,999/个)")
        print("2. 定制开发服务")
        print("3. 技术咨询")
        print()
        
        builder.show_catalog()
        
        print()
        print("🚀 **立即行动步骤:**")
        print("1. 选择目标客户 (中小企业、创业者)")
        print("2. 发送营销材料")
        print("3. 提供免费咨询")
        print("4. 签订合同，收取定金")
        print("5. 开发交付，收取尾款")
        print()
        print("💪 今天就可以开始赚钱！")

if __name__ == "__main__":
    main()