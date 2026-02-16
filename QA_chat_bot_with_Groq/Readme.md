## Chat bot with Groq model
    - Llama
    - Upload a pdf doc and answer the question based on the doc
    - Gradio interaface

### Result
- local run resulted in 32 second for a single query
- improvement 
    - the document once parsed need not be parsed again
    - need to eleminate loading, splitting, vectorizing for subsequent queres
- Solution
    - gr.Stage