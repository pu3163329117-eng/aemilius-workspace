#!/usr/bin/env python3
"""
GitHub项目搜索和收集脚本
"""

import json
import requests
import time
from datetime import datetime
from typing import List, Dict, Any

class GitHubProjectSearcher:
    def __init__(self):
        self.base_url = "https://api.github.com/search/repositories"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        # 为了避免API限制，添加延迟
        self.delay = 1  # 秒
        
    def search_projects(self, query: str, per_page: int = 10, page: int = 1) -> Dict[str, Any]:
        """搜索GitHub项目"""
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": per_page,
            "page": page
        }
        
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # 遵守API限制
            time.sleep(self.delay)
            
            return response.json()
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return {"total_count": 0, "items": []}
    
    def extract_project_info(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """提取项目关键信息"""
        return {
            "name": project.get("name"),
            "full_name": project.get("full_name"),
            "description": project.get("description", ""),
            "html_url": project.get("html_url"),
            "stars": project.get("stargazers_count", 0),
            "forks": project.get("forks_count", 0),
            "language": project.get("language"),
            "created_at": project.get("created_at"),
            "updated_at": project.get("updated_at"),
            "topics": project.get("topics", []),
            "license": project.get("license", {}).get("key") if project.get("license") else None,
            "open_issues": project.get("open_issues_count", 0),
            "homepage": project.get("homepage")
        }
    
    def search_multiple_categories(self) -> Dict[str, List[Dict[str, Any]]]:
        """搜索多个类别的项目"""
        categories = {
            "ai_assistant": "AI assistant productivity workflow automation",
            "business_intelligence": "business analytics dashboard open source",
            "project_management": "project management agile team collaboration",
            "developer_tools": "developer productivity tools automation",
            "saas_starter": "SaaS starter template boilerplate"
        }
        
        results = {}
        
        print("🚀 开始搜索GitHub项目...")
        print("=" * 50)
        
        for category, query in categories.items():
            print(f"\n🔍 搜索类别: {category}")
            print(f"📝 查询词: {query}")
            
            data = self.search_projects(query, per_page=5)
            
            if data.get("total_count", 0) > 0:
                projects = []
                for item in data.get("items", [])[:3]:  # 只取前3个
                    project_info = self.extract_project_info(item)
                    projects.append(project_info)
                    
                    # 显示项目信息
                    print(f"  ⭐ {project_info['stars']} - {project_info['full_name']}")
                    print(f"     {project_info['description'][:80]}...")
                    print(f"     📚 语言: {project_info['language']} | 🍴 Fork: {project_info['forks']}")
                
                results[category] = projects
            else:
                print(f"  ⚠️ 未找到相关项目")
                results[category] = []
        
        return results
    
    def save_results(self, results: Dict[str, List[Dict[str, Any]]], filename: str = "github_projects.json"):
        """保存搜索结果到文件"""
        output = {
            "search_date": datetime.now().isoformat(),
            "categories": results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 结果已保存到: {filename}")
        return filename
    
    def generate_markdown_report(self, results: Dict[str, List[Dict[str, Any]]]) -> str:
        """生成Markdown格式的报告"""
        report = ["# 🔍 GitHub项目搜索结果报告", ""]
        report.append(f"**搜索时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        for category, projects in results.items():
            # 转换类别名称为中文
            category_names = {
                "ai_assistant": "AI助手工具",
                "business_intelligence": "商业智能",
                "project_management": "项目管理",
                "developer_tools": "开发者工具",
                "saas_starter": "SaaS启动模板"
            }
            
            category_name = category_names.get(category, category)
            report.append(f"## 📊 {category_name}")
            report.append("")
            
            if projects:
                for i, project in enumerate(projects, 1):
                    report.append(f"### {i}. {project['full_name']}")
                    report.append(f"- **⭐ Stars**: {project['stars']:,}")
                    report.append(f"- **🍴 Forks**: {project['forks']:,}")
                    report.append(f"- **📚 语言**: {project['language'] or '未指定'}")
                    report.append(f"- **📝 描述**: {project['description']}")
                    report.append(f"- **🔗 链接**: {project['html_url']}")
                    
                    if project.get('homepage'):
                        report.append(f"- **🏠 主页**: {project['homepage']}")
                    
                    if project.get('topics'):
                        topics = ', '.join(project['topics'][:5])
                        report.append(f"- **🏷️ 标签**: {topics}")
                    
                    report.append(f"- **🔄 最后更新**: {project['updated_at'][:10]}")
                    report.append("")
            else:
                report.append("⚠️ 未找到相关项目")
                report.append("")
        
        # 添加总结
        report.append("## 📈 总结")
        total_projects = sum(len(projects) for projects in results.values())
        report.append(f"- **总计项目数**: {total_projects}")
        report.append(f"- **搜索类别数**: {len(results)}")
        report.append("")
        report.append("## 💡 建议")
        report.append("1. **AI助手工具**：重点关注Cherry Studio等成熟项目")
        report.append("2. **商业智能**：寻找数据可视化和分析工具")
        report.append("3. **项目管理**：评估团队协作和工作流自动化")
        report.append("4. **技术选型**：考虑TypeScript、Python等主流技术栈")
        
        return "\n".join(report)

def main():
    """主函数"""
    print("🎯 GitHub项目搜索工具")
    print("=" * 50)
    
    # 创建搜索器实例
    searcher = GitHubProjectSearcher()
    
    # 搜索多个类别的项目
    results = searcher.search_multiple_categories()
    
    # 保存结果到JSON文件
    json_file = searcher.save_results(results)
    
    # 生成Markdown报告
    markdown_report = searcher.generate_markdown_report(results)
    
    # 保存Markdown报告
    md_file = "github_projects_report.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(markdown_report)
    
    print(f"\n📄 Markdown报告已保存到: {md_file}")
    
    # 显示简要统计
    print("\n📊 搜索结果统计:")
    print("-" * 30)
    for category, projects in results.items():
        category_names = {
            "ai_assistant": "AI助手工具",
            "business_intelligence": "商业智能",
            "project_management": "项目管理",
            "developer_tools": "开发者工具",
            "saas_starter": "SaaS启动模板"
        }
        category_name = category_names.get(category, category)
        print(f"  {category_name}: {len(projects)} 个项目")
    
    total = sum(len(projects) for projects in results.values())
    print(f"\n✅ 总计: {total} 个项目")
    
    # 显示最有前景的项目
    print("\n🌟 最有前景的项目:")
    print("-" * 30)
    all_projects = []
    for projects in results.values():
        all_projects.extend(projects)
    
    # 按star数排序
    top_projects = sorted(all_projects, key=lambda x: x['stars'], reverse=True)[:3]
    
    for i, project in enumerate(top_projects, 1):
        print(f"{i}. {project['full_name']} (⭐ {project['stars']:,})")
        print(f"   描述: {project['description'][:60]}...")
        print(f"   语言: {project['language']} | 链接: {project['html_url']}")
        print()

if __name__ == "__main__":
    main()