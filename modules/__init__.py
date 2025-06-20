#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gradio多功能工具平台 - 模块包
模块化架构的核心组件包
创建时间: 2025-06-19
"""

__version__ = "1.0.0"
__author__ = "MiniMax Agent"

# 模块导入
from . import image_tools
from . import video_tools
from . import navigation

__all__ = [
    "image_tools",
    "video_tools",
    "navigation"
]
