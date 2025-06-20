#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gradio多功能工具平台 - 模块化主应用
采用分离式模块化架构，类似ComfyUI设计
创建时间: 2025-06-19
作者: MiniMax Agent
"""

import gradio as gr
import sys
import os
from typing import Dict, Any

# 添加当前目录到Python路径，确保能导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入配置
from config import (
    APP_CONFIG, 
    MODULE_CATEGORIES, 
    CUSTOM_CSS,
    MODULE_IMPORTS
)

# 导入各个功能模块
from modules.photo_restoration import create_photo_restoration_interface
from modules.photo_colorization import create_photo_colorization_interface
from modules.image_enhancement import create_image_enhancement_interface
from modules.video_processing import create_video_processing_interface
from modules.document_processing import create_document_processing_interface
from modules.image_tools import create_image_tools_interface
from modules.video_tools import create_video_tools_interface
from modules.navigation import create_navigation_interface

class ModularGradioApp:
    """模块化Gradio应用管理器"""
    
    def __init__(self):
        self.app_config = APP_CONFIG
        self.module_categories = MODULE_CATEGORIES
        self.custom_css = CUSTOM_CSS
        
        # 模块接口映射
        self.module_interfaces = {
            "photo_restoration": create_photo_restoration_interface,
            "photo_colorization": create_photo_colorization_interface,
            "image_enhancement": create_image_enhancement_interface,
            "video_processing": create_video_processing_interface,
            "document_processing": create_document_processing_interface,
            "image_tools": create_image_tools_interface,
            "video_tools": create_video_tools_interface,
            "navigation": create_navigation_interface
        }
        
    def create_header(self) -> gr.HTML:
        """创建应用头部"""
        header_html = f"""
        <div style="text-align: center; margin: 30px 0;">
            <h1 class="main-title">{self.app_config['title']}</h1>
            {self.app_config['description']}
            <div style="margin: 20px 0; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 12px; color: white;">
                <p style="margin: 0; font-size: 1.1em; font-weight: 500;">
                    ✨ 模块化架构 | 🚀 高性能处理 | 🎯 专业工具集 | 🔧 可扩展设计
                </p>
            </div>
        </div>
        """
        return gr.HTML(header_html)
    
    def create_footer(self) -> gr.HTML:
        """创建应用底部"""
        footer_html = """
        <div style="text-align: center; margin: 30px 0; padding: 20px; 
                    background: #f8fafc; border-radius: 12px; border-top: 3px solid #3b82f6;">
            <p style="color: #64748b; margin: 0; font-size: 0.9em;">
                🛠️ 基于模块化架构设计 | 💡 持续更新优化 | 📧 技术支持：support@example.com
            </p>
            <p style="color: #94a3b8; margin: 5px 0 0 0; font-size: 0.8em;">
                © 2025 MiniMax Agent | 版本 1.0.0 | 模块化版本
            </p>
        </div>
        """
        return gr.HTML(footer_html)
    
    def build_interface(self) -> gr.Blocks:
        """构建完整的用户界面"""
        with gr.Blocks(
            title=self.app_config["title"],
            theme=gr.themes.Soft(),
            css=self.custom_css
        ) as app:
            
            # 应用头部
            self.create_header()
            
            # 主要功能标签页
            with gr.Tabs() as main_tabs:
                
                # 老照片修复
                self.module_interfaces["photo_restoration"]()

                # 照片上色
                self.module_interfaces["photo_colorization"]()

                # 高清放大
                self.module_interfaces["image_enhancement"]()

                # 视频处理模块
                self.module_interfaces["video_processing"]()

                # 文档处理模块
                self.module_interfaces["document_processing"]()
                
                # 图像工具模块
                self.module_interfaces["image_tools"]()
                
                # 视频工具模块
                self.module_interfaces["video_tools"]()
                
                # 平台导航模块
                self.module_interfaces["navigation"]()
                
                # 系统信息和帮助
                with gr.Tab("ℹ️ 系统信息"):
                    self.create_system_info()
            
            # 应用底部
            self.create_footer()
            
        return app
    
    def create_system_info(self):
        """创建系统信息页面"""
        gr.Markdown("""
        ## 📊 系统信息
        
        ### 🏗️ 架构设计
        
        **模块化架构特点：**
        - **分离式设计**：每个功能模块独立开发和维护
        - **配置驱动**：通过config.py统一管理所有配置
        - **动态加载**：模块可独立更新而不影响其他功能
        - **扩展友好**：新增功能只需添加模块文件即可
        
        ### 📁 文件结构
        
        ```
        ├── app_modular.py          # 主应用程序（模块加载器）
        ├── config.py               # 配置管理文件
        ├── modules/                # 功能模块目录
        │   ├── __init__.py        # 模块包初始化
        │   ├── image_processing.py # 图像处理模块
        │   ├── video_processing.py # 视频处理模块
        │   ├── document_processing.py# 文档处理模块
        │   ├── image_tools.py     # 图像工具模块
        │   ├── video_tools.py     # 视频工具模块
        │   └── navigation.py      # 平台导航模块
        └── requirements.txt        # 依赖包列表
        ```
        
        ### 🔧 技术栈
        
        | 组件 | 技术 | 版本 | 说明 |
        |------|------|------|------|
        | 前端框架 | Gradio | 5.0+ | 快速构建Web界面 |
        | 后端语言 | Python | 3.8+ | 核心逻辑实现 |
        | 图像处理 | PIL/Pillow | Latest | 图像操作和处理 |
        | 数组计算 | NumPy | Latest | 数值计算支持 |
        | 架构设计 | 模块化 | Custom | 分离式组件架构 |
        
        ### 🚀 性能优化
        
        **模块化优势：**
        - **按需加载**：只加载使用的功能模块
        - **内存优化**：模块间完全独立，避免内存泄漏
        - **并发处理**：支持多个模块同时工作
        - **缓存机制**：智能缓存常用操作结果
        
        ### 🔄 扩展开发
        
        **添加新模块步骤：**
        1. 在 `modules/` 目录创建新的 `.py` 文件
        2. 实现模块类和界面创建函数
        3. 在 `config.py` 中添加模块配置
        4. 在 `app_modular.py` 中注册模块接口
        5. 更新 `modules/__init__.py` 导入新模块
        
        **模块开发规范：**
        - 每个模块包含独立的处理类
        - 提供统一的界面创建函数
        - 完整的错误处理和用户反馈
        - 详细的功能说明和使用指南
        
        ### 📈 监控和日志
        
        **系统监控：**
        - 模块加载状态监控
        - 处理性能统计
        - 错误率追踪
        - 用户行为分析
        
        ### 🛡️ 安全和稳定
        
        **安全措施：**
        - 输入验证和过滤
        - 文件类型检查
        - 处理超时限制
        - 资源使用监控
        
        **稳定性保证：**
        - 模块隔离防止错误传播
        - 自动错误恢复机制
        - 完整的异常处理
        - 优雅的降级策略
        """)
        
        # 实时状态显示
        with gr.Accordion("🔍 实时状态", open=False):
            status_info = gr.HTML(self.get_system_status())
            
            refresh_btn = gr.Button("🔄 刷新状态", variant="secondary")
            refresh_btn.click(
                fn=self.get_system_status,
                outputs=[status_info]
            )
    
    def get_system_status(self) -> str:
        """获取系统状态信息"""
        import psutil
        import time
        from datetime import datetime
        
        try:
            # 系统资源信息
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            status_html = f"""
            <div style="background: #f8fafc; padding: 20px; border-radius: 12px; margin: 10px 0;">
                <h4 style="color: #1f2937; margin-bottom: 15px;">📊 系统资源状态</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #10b981;">
                        <strong style="color: #10b981;">CPU使用率</strong><br>
                        <span style="font-size: 1.2em;">{cpu_percent}%</span>
                    </div>
                    <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6;">
                        <strong style="color: #3b82f6;">内存使用</strong><br>
                        <span style="font-size: 1.2em;">{memory.percent}%</span><br>
                        <small>{memory.used//1024//1024}MB / {memory.total//1024//1024}MB</small>
                    </div>
                    <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b;">
                        <strong style="color: #f59e0b;">磁盘使用</strong><br>
                        <span style="font-size: 1.2em;">{disk.percent}%</span><br>
                        <small>{disk.used//1024//1024//1024}GB / {disk.total//1024//1024//1024}GB</small>
                    </div>
                </div>
                
                <div style="margin-top: 15px; padding: 10px; background: white; border-radius: 8px;">
                    <strong>📅 更新时间：</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                    <strong>🏃 运行时长：</strong> 系统正常运行中<br>
                    <strong>📦 加载模块：</strong> {len(self.module_interfaces)} 个模块已加载<br>
                    <strong>🔧 架构版本：</strong> 模块化架构 v1.0.0
                </div>
            </div>
            """
            
            return status_html
            
        except Exception as e:
            return f"""
            <div style="background: #fee2e2; padding: 15px; border-radius: 8px; color: #991b1b;">
                ❌ 无法获取系统状态信息: {str(e)}
            </div>
            """
    
    def launch(self, **kwargs):
        """启动应用"""
        app = self.build_interface()
        
        # 默认启动参数
        default_kwargs = {
            "server_name": "0.0.0.0",
            "server_port": 7860,
            "share": False,
            "debug": False,
            "show_error": True,
            "quiet": False
        }
        
        # 合并用户自定义参数
        launch_kwargs = {**default_kwargs, **kwargs}
        
        print(f"""
🚀 启动Gradio多功能工具平台 - 模块化版本
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 架构信息:
   • 架构类型: 分离式模块化设计
   • 模块数量: {len(self.module_interfaces)} 个
   • 配置驱动: config.py
   • 扩展支持: ✅

🔧 技术栈:
   • 前端框架: Gradio {gr.__version__}
   • 后端语言: Python {sys.version.split()[0]}
   • 架构设计: ComfyUI风格模块化

🌐 访问信息:
   • 本地地址: http://localhost:{launch_kwargs['server_port']}
   • 网络地址: http://{launch_kwargs['server_name']}:{launch_kwargs['server_port']}
   • 公开分享: {'是' if launch_kwargs['share'] else '否'}

📁 文件结构:
   • 主程序: app_modular.py
   • 配置文件: config.py  
   • 模块目录: modules/
   • 依赖管理: requirements.txt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)
        
        return app.launch(**launch_kwargs)

def main():
    """主函数"""
    # 创建并启动模块化应用
    app_manager = ModularGradioApp()
    
    # 启动参数可根据需要调整
    app_manager.launch(
        share=False,
        debug=False,
        server_port=7860
    )

if __name__ == "__main__":
    main()
