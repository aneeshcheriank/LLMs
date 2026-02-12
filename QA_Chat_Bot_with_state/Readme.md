## gr.Blocks

```python
with gr.Blocks() as demo:
    # Multiple states are allowed here!
    qa_chain_state = gr.State(None)
    file_name_state = gr.State(None)

    with gr.Row():
        file_input = gr.File(label="Upload PDF")
        
    query_input = gr.Textbox(label="Question")
    submit_btn = gr.Button("Submit")
    output_text = gr.Textbox(label="Answer")

    # Use the logic from your original function
    submit_btn.click(
        fn=qa_bot, 
        inputs=[file_input, query_input, qa_chain_state, file_name_state],
        outputs=[output_text, qa_chain_state, file_name_state]
    )

demo.launch(server_port=7080)
```

- early attempt

```python
## QA bot
def qa_bot(file, query, history_state):
    # 1. Initialize state if it's the first time
    if history_state is None:
        history_state = {"qa_chain": None, "last_file_name": None}
    
    # 2. Extract values from state so they are available
    qa_chain = history_state.get("qa_chain")
    last_file_name = history_state.get("last_file_name")

    # 3. Check if we need to parse (New file or first run)
    if qa_chain is None or (file and file.name != last_file_name):
        print("Status: Parsing new document...")
        llm_model = llm()
        retriever_obj = retriever(file)
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm_model,
            chain_type="stuff",
            retriever=retriever_obj,
            return_source_documents=False
        )
        
        # Update our dictionary values
        history_state["qa_chain"] = qa_chain
        history_state["last_file_name"] = file.name if file else None

    # 4. Run the query
    if qa_chain:
        response = qa_chain.invoke(query)
        result = response['result']
    else:
        result = "Please upload a file first."

    # 5. Return both the answer AND the updated dictionary
    return result, history_state

## Gradio interface
rag_application = gr.Interface(
    fn=qa_bot,
    inputs=[
        gr.File(label="Upload PDF file"),
        gr.Textbox(lines=2, placeholder="Enter your question here"),
        gr.State(value=None)  # Added 'value=None' to ensure it sends an initial value
    ],
    outputs=[
        gr.Textbox(label="Answer"),
        gr.State() 
    ],
    title="PDF QA bot using LLM"
)
```