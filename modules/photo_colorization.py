import gradio as gr
from config import PHOTO_COLORIZATION_CONFIG

def create_photo_colorization_interface():
    with gr.Tab("🎨 图片上色"):
        gr.Markdown(f"## {PHOTO_COLORIZATION_CONFIG['name']}")
        gr.Markdown(PHOTO_COLORIZATION_CONFIG['description'])
        
        config = PHOTO_COLORIZATION_CONFIG['functions']['图片上色']
        
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
            title=PHOTO_COLORIZATION_CONFIG['name'],
            description=config['description']
        )