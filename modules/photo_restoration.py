import gradio as gr
from config import PHOTO_RESTORATION_CONFIG

def create_photo_restoration_interface():
    with gr.Tab("🖼️ 老照片修复"):
        gr.Markdown(f"## {PHOTO_RESTORATION_CONFIG['name']}")
        gr.Markdown(PHOTO_RESTORATION_CONFIG['description'])
        
        config = PHOTO_RESTORATION_CONFIG['functions']['老照片修复']
        
        inputs = []
        for input_type in config['inputs']:
            if input_type == 'image':
                inputs.append(gr.Image(type="pil", label="上传图片"))
                
        outputs = []
        for output_type in config['outputs']:
            if output_type == 'image':
                outputs.append(gr.Image(type="pil", label="处理结果"))
                
        gr.Interface(
            fn=lambda x: x,  # Placeholder function
            inputs=inputs,
            outputs=outputs,
            title=PHOTO_RESTORATION_CONFIG['name'],
            description=config['description']
        )