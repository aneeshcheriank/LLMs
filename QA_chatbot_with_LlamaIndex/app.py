import gradio as gr
from module.main import rag_app

with gr.Blocks() as app:
    gr.Markdown("# PDF Question Answering with LlamaIndex")
    
    with gr.Row():
        with gr.Column():
            file_input = gr.File(label="Upload your PDF file")
            query_input = gr.Textbox(lines=2, placeholder="Enter your question")
            state_input = gr.State({
                "query_engine": None,
                "old_file": None
            })
            submit_btn = gr.Button("Ask Question")
        
        with gr.Column():
            output_text = gr.Textbox(label="Answer from Bot")

    submit_btn.click(
        fn=rag_app,
        inputs=[file_input, query_input, state_input],
        outputs=[output_text, state_input]
    )
    
if __name__ == "__main__":
    app.launch(
        server_name="127.0.0.1", server_port=7070
    )