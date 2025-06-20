#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
平台导航模块
常用平台和工具导航功能
创建时间: 2025-06-19
"""

import gradio as gr
import json
from typing import Dict, List, Any
from config import NAVIGATION_CONFIG

class NavigationManager:
    """导航管理器"""
    
    def __init__(self):
        self.name = "平台导航"
        self.description = "常用平台和工具导航"
        self.config = NAVIGATION_CONFIG
        self.custom_links = []
        
    def get_category_links(self, category: str) -> List[Dict[str, str]]:
        """获取指定分类的链接"""
        return self.config["categories"].get(category, {}).get("links", [])
    
    def add_custom_link(self, name: str, url: str, description: str, category: str) -> str:
        """添加自定义链接"""
        if not name.strip() or not url.strip():
            return "❌ 名称和URL不能为空"
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        custom_link = {
            "name": name,
            "url": url,
            "description": description,
            "category": category
        }
        
        self.custom_links.append(custom_link)
        return f"✅ 成功添加自定义链接：{name}"
    
    def get_custom_links(self) -> List[Dict[str, str]]:
        """获取自定义链接列表"""
        return self.custom_links
    
    def clear_custom_links(self) -> str:
        """清空自定义链接"""
        self.custom_links.clear()
        return "✅ 已清空所有自定义链接"
    
    def generate_category_html(self, category_name: str, category_data: Dict[str, Any]) -> str:
        """生成分类HTML"""
        icon = category_data.get("icon", "🔗")
        color = category_data.get("color", "#3b82f6")
        links = category_data.get("links", [])
        
        html = f"""
        <div style="margin-bottom: 25px;">
            <h3 style="color: {color}; display: flex; align-items: center; gap: 8px; margin-bottom: 15px;">
                <span style="font-size: 1.5em;">{icon}</span>
                {category_name}
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px;">
        """
        
        for link in links:
            html += f"""
                <a href="{link['url']}" target="_blank" class="nav-link" 
                   style="display: block; padding: 15px; background: #f8fafc; border-radius: 12px; 
                          text-decoration: none; color: #1f2937; border-left: 4px solid {color};
                          transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-weight: 600; font-size: 1.1em; margin-bottom: 5px;">
                        {link['name']}
                    </div>
                    <div style="color: #6b7280; font-size: 0.9em; line-height: 1.4;">
                        {link['description']}
                    </div>
                </a>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html
    
    def generate_custom_links_html(self) -> str:
        """生成自定义链接HTML"""
        if not self.custom_links:
            return """
            <div style="text-align: center; padding: 40px; color: #6b7280;">
                <p style="font-size: 1.1em;">暂无自定义链接</p>
                <p style="font-size: 0.9em;">使用右侧面板添加您常用的网站链接</p>
            </div>
            """
        
        # 按分类组织自定义链接
        categories = {}
        for link in self.custom_links:
            category = link.get("category", "其他")
            if category not in categories:
                categories[category] = []
            categories[category].append(link)
        
        html = ""
        for category, links in categories.items():
            html += f"""
            <div style="margin-bottom: 25px;">
                <h3 style="color: #8b5cf6; display: flex; align-items: center; gap: 8px; margin-bottom: 15px;">
                    <span style="font-size: 1.5em;">📌</span>
                    {category}
                </h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px;">
            """
            
            for link in links:
                html += f"""
                    <a href="{link['url']}" target="_blank" class="nav-link"
                       style="display: block; padding: 15px; background: #f8fafc; border-radius: 12px;
                              text-decoration: none; color: #1f2937; border-left: 4px solid #8b5cf6;
                              transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="font-weight: 600; font-size: 1.1em; margin-bottom: 5px;">
                            {link['name']}
                        </div>
                        <div style="color: #6b7280; font-size: 0.9em; line-height: 1.4;">
                            {link['description']}
                        </div>
                    </a>
                """
            
            html += """
                </div>
            </div>
            """
        
        return html

def create_navigation_interface():
    """创建导航界面"""
    manager = NavigationManager()
    
    with gr.Tab("🧭 平台导航"):
        gr.Markdown("""
        ### 平台导航中心
        快速访问常用的开发工具、设计平台、AI工具和学习资源，支持添加自定义链接。
        """)
        
        with gr.Tabs():
            # 预设分类导航
            for category_name, category_data in manager.config["categories"].items():
                with gr.Tab(f"{category_data['icon']} {category_name}"):
                    category_html = manager.generate_category_html(category_name, category_data)
                    gr.HTML(category_html)
            
            # 自定义链接
            with gr.Tab("📌 自定义链接"):
                with gr.Row():
                    with gr.Column(scale=2):
                        # 显示自定义链接
                        custom_links_display = gr.HTML(
                            value=manager.generate_custom_links_html(),
                            label="我的自定义链接"
                        )
                    
                    with gr.Column(scale=1):
                        # 添加自定义链接的表单
                        gr.Markdown("### 🔗 添加自定义链接")
                        
                        with gr.Group():
                            link_name = gr.Textbox(
                                label="网站名称",
                                placeholder="例如：GitHub"
                            )
                            
                            link_url = gr.Textbox(
                                label="网站URL",
                                placeholder="例如：https://github.com"
                            )
                            
                            link_description = gr.Textbox(
                                label="网站描述",
                                placeholder="例如：代码托管平台",
                                lines=2
                            )
                            
                            link_category = gr.Dropdown(
                                choices=["开发工具", "设计工具", "AI工具", "学习资源", "其他"],
                                value="其他",
                                label="分类"
                            )
                            
                            add_btn = gr.Button("➕ 添加链接", variant="primary")
                            add_status = gr.Textbox(label="状态", interactive=False)
                        
                        gr.Markdown("### 🗑️ 管理链接")
                        clear_btn = gr.Button("清空所有自定义链接", variant="secondary")
                        clear_status = gr.Textbox(label="操作状态", interactive=False)
                        
                        gr.Markdown("""
                        **使用说明：**
                        - 添加您常用的网站链接
                        - 支持分类管理
                        - 链接会在新标签页打开
                        - 可随时清空重新添加
                        """)
                
                # 事件绑定
                def add_link_and_refresh(name, url, desc, category):
                    status = manager.add_custom_link(name, url, desc, category)
                    new_html = manager.generate_custom_links_html()
                    return new_html, status, "", "", "", "其他"
                
                add_btn.click(
                    fn=add_link_and_refresh,
                    inputs=[link_name, link_url, link_description, link_category],
                    outputs=[custom_links_display, add_status, link_name, link_url, link_description, link_category]
                )
                
                def clear_links_and_refresh():
                    status = manager.clear_custom_links()
                    new_html = manager.generate_custom_links_html()
                    return new_html, status
                
                clear_btn.click(
                    fn=clear_links_and_refresh,
                    outputs=[custom_links_display, clear_status]
                )
            
            # 网站嵌入（iframe）
            with gr.Tab("🌐 网站嵌入"):
                gr.Markdown("""
                ### 网站嵌入功能
                在当前页面中嵌入外部网站，方便快速访问和操作。
                """)
                
                with gr.Row():
                    with gr.Column():
                        iframe_url = gr.Textbox(
                            label="网站URL",
                            placeholder="请输入要嵌入的网站地址，例如：https://www.google.com",
                            value="https://www.google.com"
                        )
                        
                        iframe_height = gr.Slider(
                            minimum=300,
                            maximum=800,
                            step=50,
                            value=600,
                            label="嵌入高度（像素）"
                        )
                        
                        embed_btn = gr.Button("🌐 嵌入网站", variant="primary")
                        
                        # 快速链接按钮
                        gr.Markdown("**快速嵌入：**")
                        
                        quick_sites = [
                            ("Google搜索", "https://www.google.com"),
                            ("百度搜索", "https://www.baidu.com"),
                            ("GitHub", "https://github.com"),
                            ("ChatGPT", "https://chat.openai.com"),
                        ]
                        
                        for site_name, site_url in quick_sites:
                            quick_btn = gr.Button(site_name, size="sm")
                            quick_btn.click(
                                lambda url=site_url: url,
                                outputs=[iframe_url]
                            )
                
                # iframe显示区域
                iframe_display = gr.HTML(
                    value="""
                    <div style="text-align: center; padding: 40px; background: #f8fafc; border-radius: 12px; border: 2px dashed #d1d5db;">
                        <p style="color: #6b7280; font-size: 1.1em;">输入网站URL并点击"嵌入网站"按钮</p>
                        <p style="color: #9ca3af; font-size: 0.9em;">支持大部分允许嵌入的网站</p>
                    </div>
                    """,
                    label="嵌入网站显示区域"
                )
                
                def embed_website(url, height):
                    if not url.strip():
                        return """
                        <div style="text-align: center; padding: 40px; color: #ef4444;">
                            <p>❌ 请输入有效的网站URL</p>
                        </div>
                        """
                    
                    if not url.startswith(('http://', 'https://')):
                        url = 'https://' + url
                    
                    iframe_html = f"""
                    <div style="border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                        <iframe src="{url}" 
                                width="100%" 
                                height="{height}px" 
                                frameborder="0"
                                style="border-radius: 12px;">
                            <p>您的浏览器不支持iframe，请直接访问：<a href="{url}" target="_blank">{url}</a></p>
                        </iframe>
                    </div>
                    <div style="margin-top: 10px; text-align: center;">
                        <a href="{url}" target="_blank" style="color: #3b82f6; text-decoration: none;">
                            🔗 在新标签页中打开
                        </a>
                    </div>
                    """
                    
                    return iframe_html
                
                embed_btn.click(
                    fn=embed_website,
                    inputs=[iframe_url, iframe_height],
                    outputs=[iframe_display]
                )
                
                gr.Markdown("""
                **注意事项：**
                - 某些网站可能不允许嵌入显示
                - 如遇到显示问题，请尝试在新标签页打开
                - 嵌入的网站功能完全正常，支持登录和操作
                - 建议使用HTTPS协议的网站以获得最佳体验
                """)
        
        # 使用说明和功能介绍
        with gr.Accordion("功能说明", open=False):
            gr.Markdown("""
            ### 🎯 功能特色
            
            **预设分类导航：**
            - **开发工具**：GitHub、Stack Overflow、MDN等开发必备
            - **设计工具**：Figma、Canva、Adobe等设计平台
            - **AI工具**：ChatGPT、Midjourney、Claude等AI服务
            - **学习资源**：Coursera、edX、Khan Academy等学习平台
            
            **自定义链接管理：**
            - 添加个人常用网站
            - 支持分类整理
            - 快速访问和管理
            - 响应式卡片布局
            
            **网站嵌入功能：**
            - 在当前页面直接访问外部网站
            - 可调节嵌入窗口高度
            - 支持快速切换常用网站
            - 提供新标签页打开选项
            
            ### 🚀 使用技巧
            
            1. **快速访问**：将最常用的网站添加到自定义链接
            2. **分类管理**：使用分类功能整理不同类型的网站
            3. **嵌入浏览**：对于需要频繁访问的网站，使用嵌入功能
            4. **新标签页**：复杂操作建议在新标签页中进行
            
            ### ⚠️ 嵌入限制
            
            - 部分网站因安全策略不允许嵌入
            - 银行、支付等敏感网站建议在新标签页打开
            - 嵌入网站的功能和原网站完全一致
            - 如遇显示问题，请检查网站的iframe支持情况
            """)

# 导出接口
__all__ = ["NavigationManager", "create_navigation_interface"]
