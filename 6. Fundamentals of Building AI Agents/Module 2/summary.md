## Summary and Highlights: Introduction to Chaining and LCEL Basics

- Large language models (LLMs) specify task parameters and suggest tools.

- Agents automatically invoke tools based on direction from the LLM.

- During manual invocation, developers verify inputs and outputs and adjust actions as needed.

- Manual invocation provides organizations with the opportunity for greater control, which enhances safety, manages costs, and can support enhanced accurate results.

- Mapping a dictionary connects tool names, such as add, to functions, enabling the large language model (LLM) to call the correct function by name and pass inputs as key-value pairs.

- You can manually control and validate tool inputs that the LLM can access by defining each tool using the @tool decorator.

- Before using .invoke(), bind the tools to the LLM so the LLM can identify and apply the correct tool based on the prompt.

- Use .invoke(input_) to pass a dictionary of key-value pairs that match the tool’s parameter names.