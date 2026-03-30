## Overview
- Agentic workflows with **LangChain** and **LangGraph**
- LangGraph
    - memory
    - iteration 
    - conditional logic
- How LangGraph builds on LangChain to support adatptive decision-making using nodes, edges, and shared states.

- **Self-improving agents**
    - using architetures like
        - Reflection
        - Reflexion
        - ReAct

- cordinate agents in multi-agent systems
    - Agentic retrieval-augmented generation (RAG) pipelines

### Course outline
- Module 1: Introduction to LangGraph
    - Agentic AI fundamentals
    - LangGraph workflows
    - LangGraph nodes, edges, and state
- Module 2: Build self-improving Agents with LangGraph
    - self-improving agents
    - Reflection and Reflexion patterns
    - ReAct for resoning and action
    - Prompt engineering techniques
- Module 3: Multi-Agent Systems and Agentic RAG with LangGraph
    - Multi-agent systems
    - Agent orchestration
    - Agentic RAG pipelines
    - Query routing and retrieval


## Generative vs Agentic AI
- Generative AI
    - Reactive systems  (will generte only after a user **prompt**)
        - can generate (text, image, code, or audio)
        - However, the system stops after the generation process

- Agentic AI
    - Proactive systems
        - start with user prompt, however, the generation not stops after the first generatnion
        - prompt -> a series of actions
        - the life cycle of actions
            - the system presives the job in hand -> it decides what to do -> it execute one task -> it learns what task it has completed -> repeat the cycle
            - the process is with minimal human intervention

- use cases

|Generative AI| Agentic AI|
|---|---|
|**createive content creation**: a youtuber can outline a topic on his next video using generative ai models, or to generate a background music|an example can be a personal purchase agent </br>(multi step process)</br>- hunt for products in multiple platforms </br>- it process checkout </br> - it cordinates delivery </br> seek input from human only when it needed|

- Agentic AI using the LLMs as the **Resoning agent** for agentic process
- **Chain of Thought Reasoning**