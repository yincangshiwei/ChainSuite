#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gradio多功能工具平台 - 配置文件
模块化配置管理，类似ComfyUI的分离式架构
创建时间: 2025-06-19
"""

# 应用基本信息
APP_CONFIG = {
    "title": "🚀 AI多功能工具平台",
    "description": """
    <div style="text-align: center; margin: 20px 0;">
        <h2 style="color: #2563eb; margin-bottom: 10px;">欢迎使用 AI 多功能工具平台</h2>
        <p style="color: #64748b; font-size: 16px;">集成AI图像处理、视频编辑、智能对话等多种实用工具</p>
    </div>
    """,
    "theme": "soft",
    "css_file": None
}

# 模块分类配置
MODULE_CATEGORIES = {
    "photo_restoration": {
        "name": "🖼️ 老照片修复",
        "description": "修复老旧照片",
        "icon": "🖼️",
        "color": "#10b981"
    },
    "photo_colorization": {
        "name": "🎨 图片上色",
        "description": "为黑白照片上色",
        "icon": "🎨",
        "color": "#3b82f6"
    },
    "image_enhancement": {
        "name": "✨ 高清放大",
        "description": "提升图片分辨率",
        "icon": "✨",
        "color": "#f59e0b"
    },
    "video_processing": {
        "name": "🎬 视频处理",
        "description": "视频处理和编辑功能",
        "icon": "🎬",
        "color": "#f59e0b"
    },
    "document_processing": {
        "name": "📄 文档处理",
        "description": "文档处理和转换功能",
        "icon": "📄",
        "color": "#3b82f6"
    },
    "navigation": {
        "name": "🧭 平台导航",
        "description": "常用平台和工具导航",
        "icon": "🧭", 
        "color": "#8b5cf6"
    }
}

# 老照片修复配置
PHOTO_RESTORATION_CONFIG = {
    "name": "老照片修复",
    "description": "使用AI技术修复老旧照片",
    "functions": {
        "老照片修复": {
            "description": "上传老旧照片进行修复",
            "inputs": ["image"],
            "outputs": ["image"]
        }
    }
}

# 图片上色配置
PHOTO_COLORIZATION_CONFIG = {
    "name": "图片上色",
    "description": "为黑白照片添加自然色彩",
    "functions": {
        "图片上色": {
            "description": "上传黑白照片进行上色",
            "inputs": ["image"],
            "outputs": ["image"]
        }
    }
}

# 高清放大配置
IMAGE_ENHANCEMENT_CONFIG = {
    "name": "高清放大",
    "description": "使用AI算法提升图片分辨率",
    "functions": {
        "高清放大": {
            "description": "上传图片进行高清放大",
            "inputs": ["image"],
            "outputs": ["image"]
        }
    }
}

# 视频处理配置
VIDEO_PROCESSING_CONFIG = {}

# 文档处理配置
DOCUMENT_PROCESSING_CONFIG = {}

# 图像工具配置
IMAGE_TOOLS_CONFIG = {
    "basic_processing": {
        "name": "基础处理",
        "functions": {
            "图片压缩": {
                "description": "减小图片文件大小",
                "inputs": ["image", "quality"],
                "outputs": ["image"]
            },
            "格式转换": {
                "description": "转换图片格式（JPEG/PNG/WEBP）",
                "inputs": ["image", "format"],
                "outputs": ["image"]
            }
        }
    },
    "enhancement": {
        "name": "图像增强",
        "functions": {
            "亮度调整": {
                "description": "调整图像亮度、对比度、饱和度",
                "inputs": ["image", "brightness", "contrast", "saturation"],
                "outputs": ["image"]
            },
            "滤镜效果": {
                "description": "应用各种图像滤镜",
                "inputs": ["image", "filter_type"],
                "outputs": ["image"]
            }
        }
    }
}

# 视频工具配置
VIDEO_TOOLS_CONFIG = {
    "basic_processing": {
        "name": "基础处理",
        "functions": {
            "格式转换": {
                "description": "转换视频格式",
                "inputs": ["video", "format"],
                "outputs": ["video"]
            },
            "视频压缩": {
                "description": "减小视频文件大小",
                "inputs": ["video", "quality"],
                "outputs": ["video"]
            }
        }
    },
    "editing": {
        "name": "视频编辑",
        "functions": {
            "视频剪辑": {
                "description": "裁剪视频片段",
                "inputs": ["video", "start_time", "end_time"],
                "outputs": ["video"]
            },
            "添加水印": {
                "description": "为视频添加水印",
                "inputs": ["video", "watermark"],
                "outputs": ["video"]
            }
        }
    }
}

# 平台导航配置
NAVIGATION_CONFIG = {
    "categories": {
        "开发工具": {
            "icon": "🛠️",
            "color": "#3b82f6",
            "links": [
                {"name": "GitHub", "url": "https://github.com", "description": "代码托管平台"},
                {"name": "Stack Overflow", "url": "https://stackoverflow.com", "description": "编程问答社区"},
                {"name": "MDN Web Docs", "url": "https://developer.mozilla.org", "description": "Web开发文档"},
                {"name": "VS Code", "url": "https://code.visualstudio.com", "description": "代码编辑器"}
            ]
        },
        "设计工具": {
            "icon": "🎨", 
            "color": "#10b981",
            "links": [
                {"name": "Figma", "url": "https://figma.com", "description": "界面设计工具"},
                {"name": "Canva", "url": "https://canva.com", "description": "图形设计平台"},
                {"name": "Adobe Creative", "url": "https://adobe.com", "description": "创意软件套件"},
                {"name": "Unsplash", "url": "https://unsplash.com", "description": "免费高质量图片"}
            ]
        },
        "AI工具": {
            "icon": "🤖",
            "color": "#8b5cf6", 
            "links": [
                {"name": "ChatGPT", "url": "https://chat.openai.com", "description": "AI对话助手"},
                {"name": "Midjourney", "url": "https://midjourney.com", "description": "AI图像生成"},
                {"name": "Stable Diffusion", "url": "https://stability.ai", "description": "开源AI图像生成"},
                {"name": "Claude", "url": "https://claude.ai", "description": "AI助手"}
            ]
        },
        "学习资源": {
            "icon": "📚",
            "color": "#f59e0b",
            "links": [
                {"name": "Coursera", "url": "https://coursera.org", "description": "在线课程平台"},
                {"name": "edX", "url": "https://edx.org", "description": "高质量在线教育"},
                {"name": "Khan Academy", "url": "https://khanacademy.org", "description": "免费在线学习"},
                {"name": "YouTube", "url": "https://youtube.com", "description": "视频学习资源"}
            ]
        }
    },
    "custom_links": [
        # 用户可以在这里添加自定义链接
        # {"name": "自定义网站", "url": "https://example.com", "description": "描述", "category": "其他"}
    ]
}

# 样式配置
CUSTOM_CSS = """
/* 全局样式 */
.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
}

/* 标题样式 */
.main-title {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
    margin: 20px 0;
}

/* 选项卡样式 */
.tab-nav {
    background: #f8fafc;
    border-radius: 12px;
    padding: 4px;
    margin: 10px 0;
}

/* 卡片样式 */
.tool-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    margin: 10px 0;
    border-left: 4px solid #3b82f6;
}

/* 按钮样式 */
.primary-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.primary-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* 成功消息 */
.success-message {
    background: #d1fae5;
    color: #065f46;
    padding: 8px 16px;
    border-radius: 6px;
    border-left: 4px solid #10b981;
}

/* 错误消息 */
.error-message {
    background: #fee2e2;
    color: #991b1b;
    padding: 8px 16px;
    border-radius: 6px;
    border-left: 4px solid #ef4444;
}

/* 导航链接 */
.nav-link {
    display: block;
    padding: 12px 16px;
    background: #f1f5f9;
    border-radius: 8px;
    text-decoration: none;
    color: #334155;
    margin: 5px 0;
    transition: all 0.3s ease;
}

.nav-link:hover {
    background: #e2e8f0;
    transform: translateX(5px);
}

/* 模块标题 */
.module-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 16px;
    color: #1f2937;
}

/* 功能描述 */
.function-desc {
    color: #6b7280;
    font-size: 0.9rem;
    margin-bottom: 12px;
    line-height: 1.5;
}
"""

# 模块导入配置
MODULE_IMPORTS = {
    "ai_image": "modules.ai_image",
    "ai_chat": "modules.ai_chat", 
    "ai_video": "modules.ai_video",
    "image_tools": "modules.image_tools",
    "video_tools": "modules.video_tools",
    "navigation": "modules.navigation"
}

# 默认设置
DEFAULT_SETTINGS = {
    "image_quality": 85,
    "video_quality": "medium",
    "max_file_size": 50,  # MB
    "supported_image_formats": ["JPEG", "PNG", "WEBP"],
    "supported_video_formats": ["MP4", "AVI", "MOV", "WEBM"]
}
