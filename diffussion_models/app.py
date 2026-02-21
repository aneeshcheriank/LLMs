import gradio as gr
from src.model import image_generator

app = gr.Interface(
    fn = image_generator,
    inputs = [gr.Image(type="pil", label="upload an image"), 
              gr.Text(
                  lines=2, 
                  placeholder="Input the prompt to modifiy the image"
              )
             ],
    outputs=gr.Image("generated image"),
    title="Image Modifier",
    description="Upload an image and give the modification prompt"
)

if __name__ == "__main__":
    app.launch(
        server_name="127.0.0.1", 
        server_port=7080, 
        debug=True
    )