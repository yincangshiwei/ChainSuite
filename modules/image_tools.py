#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图像工具模块
图像处理和编辑功能
创建时间: 2025-06-19
"""

import gradio as gr
import io
import time
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
from typing import Optional, Tuple

class ImageToolProcessor:
    """图像工具处理器"""
    
    def __init__(self):
        self.name = "图像工具"
        self.description = "图像处理和编辑功能"
        
    def compress_image(self, image: Image.Image, quality: int = 85) -> Tuple[Image.Image, str]:
        """压缩图像"""
        if image is None:
            return None, "❌ 请上传图片"
        
        try:
            # 获取原始文件大小（估算）
            original_size = len(image.tobytes())
            
            # 转换为RGB模式（如果需要）
            if image.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            # 使用BytesIO进行压缩
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=quality, optimize=True)
            compressed_size = output.tell()
            output.seek(0)
            compressed_image = Image.open(output)
            
            # 计算压缩率
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            status = f"""✅ 图片压缩完成！
            
**压缩信息：**
• 质量设置：{quality}%
• 压缩率：{compression_ratio:.1f}%
• 原始大小：{original_size/1024:.1f} KB
• 压缩后：{compressed_size/1024:.1f} KB
• 节省空间：{(original_size-compressed_size)/1024:.1f} KB"""
            
            return compressed_image, status
            
        except Exception as e:
            return None, f"❌ 压缩失败: {str(e)}"
    
    def convert_format(self, image: Image.Image, format_type: str) -> Tuple[Image.Image, str]:
        """转换图像格式"""
        if image is None:
            return None, "❌ 请上传图片"
        
        try:
            output = io.BytesIO()
            
            if format_type.upper() == 'JPEG':
                if image.mode in ('RGBA', 'LA', 'P'):
                    # 为JPEG格式创建白色背景
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    if image.mode == 'P':
                        image = image.convert('RGBA')
                    background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                    image = background
                image.save(output, format='JPEG', quality=95)
                
            elif format_type.upper() == 'PNG':
                image.save(output, format='PNG')
                
            elif format_type.upper() == 'WEBP':
                image.save(output, format='WEBP', quality=95)
            
            output.seek(0)
            converted_image = Image.open(output)
            
            status = f"""✅ 格式转换完成！
            
**转换信息：**
• 目标格式：{format_type.upper()}
• 图片尺寸：{image.size[0]} x {image.size[1]}
• 色彩模式：{converted_image.mode}
• 转换成功"""
            
            return converted_image, status
            
        except Exception as e:
            return None, f"❌ 转换失败: {str(e)}"
    
    def enhance_image(self, image: Image.Image, brightness: float = 1.0, 
                     contrast: float = 1.0, saturation: float = 1.0, 
                     sharpness: float = 1.0) -> Tuple[Image.Image, str]:
        """图像增强"""
        if image is None:
            return None, "❌ 请上传图片"
        
        try:
            enhanced_image = image.copy()
            
            # 亮度调整
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(enhanced_image)
                enhanced_image = enhancer.enhance(brightness)
            
            # 对比度调整
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(enhanced_image)
                enhanced_image = enhancer.enhance(contrast)
            
            # 饱和度调整
            if saturation != 1.0:
                enhancer = ImageEnhance.Color(enhanced_image)
                enhanced_image = enhancer.enhance(saturation)
            
            # 锐度调整
            if sharpness != 1.0:
                enhancer = ImageEnhance.Sharpness(enhanced_image)
                enhanced_image = enhancer.enhance(sharpness)
            
            status = f"""✅ 图像增强完成！
            
**调整参数：**
• 亮度：{brightness:.1f}
• 对比度：{contrast:.1f}
• 饱和度：{saturation:.1f}
• 锐度：{sharpness:.1f}"""
            
            return enhanced_image, status
            
        except Exception as e:
            return None, f"❌ 增强失败: {str(e)}"
    
    def apply_filter(self, image: Image.Image, filter_type: str) -> Tuple[Image.Image, str]:
        """应用滤镜"""
        if image is None:
            return None, "❌ 请上传图片"
        
        try:
            filtered_image = image.copy()
            
            if filter_type == "模糊":
                filtered_image = filtered_image.filter(ImageFilter.BLUR)
            elif filter_type == "锐化":
                filtered_image = filtered_image.filter(ImageFilter.SHARPEN)
            elif filter_type == "边缘检测":
                filtered_image = filtered_image.filter(ImageFilter.FIND_EDGES)
            elif filter_type == "浮雕":
                filtered_image = filtered_image.filter(ImageFilter.EMBOSS)
            elif filter_type == "轮廓":
                filtered_image = filtered_image.filter(ImageFilter.CONTOUR)
            elif filter_type == "细节增强":
                filtered_image = filtered_image.filter(ImageFilter.DETAIL)
            elif filter_type == "平滑":
                filtered_image = filtered_image.filter(ImageFilter.SMOOTH)
            elif filter_type == "黑白":
                filtered_image = ImageOps.grayscale(filtered_image)
                if filtered_image.mode != 'RGB':
                    filtered_image = filtered_image.convert('RGB')
            elif filter_type == "反色":
                filtered_image = ImageOps.invert(filtered_image)
            elif filter_type == "镜像翻转":
                filtered_image = ImageOps.mirror(filtered_image)
            elif filter_type == "上下翻转":
                filtered_image = ImageOps.flip(filtered_image)
            
            status = f"""✅ 滤镜应用完成！
            
**滤镜信息：**
• 应用滤镜：{filter_type}
• 处理完成时间：{time.strftime('%H:%M:%S')}
• 图片尺寸：{filtered_image.size[0]} x {filtered_image.size[1]}"""
            
            return filtered_image, status
            
        except Exception as e:
            return None, f"❌ 滤镜应用失败: {str(e)}"
    
    def resize_image(self, image: Image.Image, width: int, height: int, 
                    keep_ratio: bool = True) -> Tuple[Image.Image, str]:
        """调整图片尺寸"""
        if image is None:
            return None, "❌ 请上传图片"
        
        if width <= 0 or height <= 0:
            return None, "❌ 宽度和高度必须大于0"
        
        try:
            original_size = image.size
            
            if keep_ratio:
                # 保持宽高比
                image.thumbnail((width, height), Image.Resampling.LANCZOS)
                resized_image = image
                new_size = image.size
            else:
                # 强制调整到指定尺寸
                resized_image = image.resize((width, height), Image.Resampling.LANCZOS)
                new_size = (width, height)
            
            status = f"""✅ 尺寸调整完成！
            
**调整信息：**
• 原始尺寸：{original_size[0]} x {original_size[1]}
• 目标尺寸：{width} x {height}
• 实际尺寸：{new_size[0]} x {new_size[1]}
• 保持比例：{'是' if keep_ratio else '否'}"""
            
            return resized_image, status
            
        except Exception as e:
            return None, f"❌ 尺寸调整失败: {str(e)}"

def create_image_tools_interface():
    """创建图像工具界面"""
    processor = ImageToolProcessor()
    
    with gr.Tab("🖼️ 图像工具"):
        gr.Markdown("""
        ### 图像处理工具集
        提供各种实用的图像处理功能，包括压缩、格式转换、增强和滤镜等。
        """)
        
        with gr.Tabs():
            # 基础处理
            with gr.Tab("🔧 基础处理"):
                with gr.Tabs():
                    # 图片压缩
                    with gr.Tab("📦 图片压缩"):
                        gr.Markdown("减小图片文件大小，适合网络传输和存储。")
                        
                        with gr.Row():
                            with gr.Column():
                                compress_input = gr.Image(
                                    label="上传需要压缩的图片",
                                    type="pil",
                                    sources=["upload", "clipboard"]
                                )
                                quality_slider = gr.Slider(
                                    minimum=10,
                                    maximum=100,
                                    step=5,
                                    value=85,
                                    label="压缩质量 (%)"
                                )
                                compress_btn = gr.Button("📦 开始压缩", variant="primary")
                            
                            with gr.Column():
                                compress_output = gr.Image(label="压缩后的图片")
                                compress_status = gr.Textbox(
                                    label="压缩状态",
                                    interactive=False,
                                    lines=6
                                )
                        
                        compress_btn.click(
                            fn=processor.compress_image,
                            inputs=[compress_input, quality_slider],
                            outputs=[compress_output, compress_status]
                        )
                    
                    # 格式转换
                    with gr.Tab("🔄 格式转换"):
                        gr.Markdown("转换图片格式，支持JPEG、PNG、WEBP格式。")
                        
                        with gr.Row():
                            with gr.Column():
                                convert_input = gr.Image(
                                    label="上传需要转换的图片",
                                    type="pil",
                                    sources=["upload", "clipboard"]
                                )
                                format_choice = gr.Radio(
                                    choices=["JPEG", "PNG", "WEBP"],
                                    value="JPEG",
                                    label="目标格式"
                                )
                                convert_btn = gr.Button("🔄 开始转换", variant="primary")
                            
                            with gr.Column():
                                convert_output = gr.Image(label="转换后的图片")
                                convert_status = gr.Textbox(
                                    label="转换状态",
                                    interactive=False,
                                    lines=6
                                )
                        
                        convert_btn.click(
                            fn=processor.convert_format,
                            inputs=[convert_input, format_choice],
                            outputs=[convert_output, convert_status]
                        )
            
            # 图像增强
            with gr.Tab("✨ 图像增强"):
                with gr.Tabs():
                    # 参数调整
                    with gr.Tab("🎛️ 参数调整"):
                        gr.Markdown("调整图像的亮度、对比度、饱和度和锐度。")
                        
                        with gr.Row():
                            with gr.Column():
                                enhance_input = gr.Image(
                                    label="上传需要增强的图片",
                                    type="pil",
                                    sources=["upload", "clipboard"]
                                )
                                
                                brightness_slider = gr.Slider(
                                    minimum=0.1,
                                    maximum=2.0,
                                    step=0.1,
                                    value=1.0,
                                    label="亮度"
                                )
                                
                                contrast_slider = gr.Slider(
                                    minimum=0.1,
                                    maximum=2.0,
                                    step=0.1,
                                    value=1.0,
                                    label="对比度"
                                )
                                
                                saturation_slider = gr.Slider(
                                    minimum=0.0,
                                    maximum=2.0,
                                    step=0.1,
                                    value=1.0,
                                    label="饱和度"
                                )
                                
                                sharpness_slider = gr.Slider(
                                    minimum=0.0,
                                    maximum=2.0,
                                    step=0.1,
                                    value=1.0,
                                    label="锐度"
                                )
                                
                                enhance_btn = gr.Button("✨ 应用增强", variant="primary")
                                
                            with gr.Column():
                                enhance_output = gr.Image(label="增强后的图片")
                                enhance_status = gr.Textbox(
                                    label="增强状态",
                                    interactive=False,
                                    lines=6
                                )
                        
                        enhance_btn.click(
                            fn=processor.enhance_image,
                            inputs=[enhance_input, brightness_slider, contrast_slider, 
                                   saturation_slider, sharpness_slider],
                            outputs=[enhance_output, enhance_status]
                        )
                    
                    # 滤镜效果
                    with gr.Tab("🎨 滤镜效果"):
                        gr.Markdown("应用各种图像滤镜效果。")
                        
                        with gr.Row():
                            with gr.Column():
                                filter_input = gr.Image(
                                    label="上传需要添加滤镜的图片",
                                    type="pil",
                                    sources=["upload", "clipboard"]
                                )
                                
                                filter_choice = gr.Radio(
                                    choices=[
                                        "模糊", "锐化", "边缘检测", "浮雕", "轮廓",
                                        "细节增强", "平滑", "黑白", "反色", 
                                        "镜像翻转", "上下翻转"
                                    ],
                                    value="模糊",
                                    label="选择滤镜"
                                )
                                
                                filter_btn = gr.Button("🎨 应用滤镜", variant="primary")
                                
                            with gr.Column():
                                filter_output = gr.Image(label="添加滤镜后的图片")
                                filter_status = gr.Textbox(
                                    label="滤镜状态",
                                    interactive=False,
                                    lines=6
                                )
                        
                        filter_btn.click(
                            fn=processor.apply_filter,
                            inputs=[filter_input, filter_choice],
                            outputs=[filter_output, filter_status]
                        )
            
            # 尺寸调整
            with gr.Tab("📏 尺寸调整"):
                gr.Markdown("调整图片的尺寸大小。")
                
                with gr.Row():
                    with gr.Column():
                        resize_input = gr.Image(
                            label="上传需要调整尺寸的图片",
                            type="pil",
                            sources=["upload", "clipboard"]
                        )
                        
                        with gr.Row():
                            width_input = gr.Number(
                                label="宽度 (像素)",
                                value=800,
                                minimum=1
                            )
                            height_input = gr.Number(
                                label="高度 (像素)",
                                value=600,
                                minimum=1
                            )
                        
                        keep_ratio = gr.Checkbox(
                            label="保持宽高比",
                            value=True
                        )
                        
                        resize_btn = gr.Button("📏 调整尺寸", variant="primary")
                        
                    with gr.Column():
                        resize_output = gr.Image(label="调整尺寸后的图片")
                        resize_status = gr.Textbox(
                            label="调整状态",
                            interactive=False,
                            lines=6
                        )
                
                resize_btn.click(
                    fn=processor.resize_image,
                    inputs=[resize_input, width_input, height_input, keep_ratio],
                    outputs=[resize_output, resize_status]
                )
        
        # 使用说明
        with gr.Accordion("使用说明", open=False):
            gr.Markdown("""
            ### 📋 功能说明
            
            **基础处理：**
            - **图片压缩**：减小文件大小，质量可调
            - **格式转换**：支持JPEG/PNG/WEBP格式互转
            
            **图像增强：**
            - **参数调整**：精细调节亮度、对比度、饱和度、锐度
            - **滤镜效果**：多种艺术和功能性滤镜
            
            **尺寸调整：**
            - **智能缩放**：支持保持比例或强制尺寸
            - **高质量算法**：使用LANCZOS重采样保证质量
            
            ### 💡 使用技巧
            
            - 压缩质量85%通常是质量和大小的最佳平衡
            - JPEG适合照片，PNG适合图标和透明图片
            - 应用多个效果时建议按顺序：调整尺寸→增强→滤镜
            - 保存前可以预览效果，满意后再下载
            """)

# 导出接口
__all__ = ["ImageToolProcessor", "create_image_tools_interface"]
