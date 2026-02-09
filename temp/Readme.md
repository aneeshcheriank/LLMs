## Model Selection
- Caipabilities
    - meets your requirements
    - need a multimodel, when the model need to process text, image and audio
- Cost
    - Cost of using the model
        - input and output tokens
- Speed
    - does speed important
    - real-time application
- Quality
    - does the model output satisfies your quality standards?
- Other Considerations
    - License restrictions, integration with existing systems

## Another model
- llama-4-maveric-17b-128e-insturct-fp8

## Some Latest Models available in Watson-AI platform
| Provider | Model ID | Use Cases | Context | Price (USD/1M) |
| :--- | :--- | :--- | :--- | :--- |
| **IBM** | `ibm/granite-3-8b-instruct` | Q&A, Summarization, RAG, Coding | 128k | $0.20 |
| **IBM** | `ibm/granite-3-2b-instruct` | Q&A, Summarization, RAG, Coding | 128k | $0.10 |
| **IBM** | `ibm/granite-13b-instruct-v2` | Q&A, Summarization, RAG | 8k | $0.60 |
| **Meta** | `llama-4-maverick-17b-fp8` | Multimodal, STEM, 200+ languages | 1M | In: $0.15 / Out: $0.60 |
| **Meta** | `llama-3-2-90b-vision` | Multilingual Vision Q&A, RAG | 128k | $2.00 |
| **Meta** | `llama-3-2-11b-vision` | OCR, Image captioning, Object ID | 128k | $0.35 |
| **Mistral** | `mistral-small-3-1-24b` | Agentic tasks, Function calling | 128k | In: $0.10 / Out: $0.30 |
| **Google** | `google/flan-t5-xl` | Prompt-tuning, Summarization | 4k | $0.60 |

## Special Tokens & Prompt Formatting
### Llama
| Token Name | Description |
|---|---|
| `<|begin_of_text|>` | Specifies the start of the prompt. |
| `<|end_of_text|>` | Specifies the end of the prompt. |
| `<|start_header_id|>` | These tokens enclose the role for a particular message, always paired with `<|end_header_id|>`. The possible roles are: `system`, `user`, `assistant`, and `ipython`. |
| `<|end_header_id|>` | Pairs with `<|start_header_id|>` to define the role for a particular message. |
| `<|eot_id|>` | End of turn. Represents when the model has determined that it has finished interacting with the user message that initiated its response. This token signals to the executor that the model has finished generating a response. |

- In Llama there are 4 roles (to be enclosed with in `<|start_header_id|>` and `<|end_header_id|>` tags)
    - System: 
        - behaviour, context, or the personality of the assistent
        - set guideliens of instruct that shaoe how th assistent interacts, responds and helps users
        - incluldee the tone, fromality and any background knowledge needed to better assist
    - User:
        - Person interacting with the assitent
        - This role contains the queries, requests, or commands made by the user
        - Assistent:
            - AI generated response
        - Ipython
            - Introduced in Llama 3.1
            - mark messages with the output of a tool call when sent back to model from the executor

## Mistral
| Token Name | Description |
|---|---|
| `<s>` | Marks the start of a sentence or sequence. |
| `</s>` | Marks the end of a sentence or sequence. |
| `[INST]` | Signifies the start of an instructional message or command. Typically used for instructions. |
| `[/INST]` | Marks the end of the instructional message. |


## Granite
| Token Name | Description |
|---|---|
| `<|system|>` | Identifies the instruction, commonly referred to as the system prompt for the foundation model. |
| `<|user|>` | The query text to be answered. |
| `<|assistant|>` | A cue at the end of the prompt that indicates that a generated answer is expected. |
