from langgraph.graph import StateGraph, START, END

from src.agents import AgentState,create_strategy, tool_call_node, strategy_router, formatter_node

def build_graph():
    workflow = StateGraph(AgentState)

    # nodes
    workflow.add_node("create_strategy", create_strategy)
    workflow.add_node("tool_call", tool_call_node)
    workflow.add_node("formatter", formatter_node)


    # edges
    workflow.add_edge(START, "create_strategy")
    workflow.add_edge("tool_call", "create_strategy")
    workflow.add_edge("formatter", END)

    # conditional edge
    workflow.add_conditional_edges(
        "create_strategy", strategy_router, 
        {"tool_call": "tool_call",
         "formatter": "formatter"}
    )

    compiled_workflow = workflow.compile()

    return compiled_workflow