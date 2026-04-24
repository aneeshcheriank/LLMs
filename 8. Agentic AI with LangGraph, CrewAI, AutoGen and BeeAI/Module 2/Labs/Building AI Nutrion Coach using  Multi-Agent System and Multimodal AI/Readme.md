## AI Nutrition Coach using Multi-Agent System and Multimodal AI

- Build and deploy a multi-agent system that powers intelligent decision-making.
- Integrate multimodal AI to handle both visual and textual data.
- Create a user-friendly interface using Gradio, so your app is accessible to anyone.

- model: Llama 3.2 90B Vision Instruct

- message structure from llama-vision models
```python
{
  "id": "chatcmpl-123",          # Unique request ID
  "object": "chat.completion",   # Type of object
  "created": 1677652288,         # Unix timestamp
  "model": "llama-3.3-70b",      # The model name used
  "choices": [                   # A list (usually contains 1 item)
    {
      "index": 0,
      "message": {               # <--- The most important key
        "role": "assistant",
        "content": "Hello! How can I help you today?",
        "tool_calls": []         # (Optional) If the model called a function
      },
      "logprobs": null,          # Probability data (if requested)
      "finish_reason": "stop"    # Why it finished (stop, length, tool_calls)
    }
  ],
  "usage": {                     # Token counting data
    "prompt_tokens": 15,
    "completion_tokens": 10,
    "total_tokens": 25
  }
}
```