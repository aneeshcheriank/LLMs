- CrewAI is designed for multi-agent collaboration, with agents assigned clear roles and tasks to simulate human-like teamwork

- Tools are standard components in AI workflows (for example, APIs and search engines) that can be used by either the Agent or the Task.

- The Crew object combines agents, tasks, the LLM, and tools into a coordinated workflow.

- CrewOutput captures the final result, task outputs, and token usage, giving a full snapshot of what was generated and its cost

- CrewAI lets you build multi-agent workflows by defining agents with specific roles, goals, and tasks, then grouping them in a Crew for sequential execution

- YAML allows you to define agents and tasks outside of Python, simplifying updates without touching code

- The @CrewBase decorator loads YAML-defined components as methods, making them easy to call and integrate into a Python script or notebook

- Custom functions enhance CrewAI by enabling domain-specific tools that improve flexibility and control

- An agent-centric workflow assigns tools directly to the agent, letting them choose the best tool based on the query

- A task-centric workflow attaches tools to individual tasks, guiding the agent step by step through a fixed process