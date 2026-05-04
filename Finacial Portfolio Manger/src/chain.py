from langgraph.graph import StateGraph, START, END

from src.agents import (AgentState,index_matcher, tool_call_node, tool_router, formatter_node, stock_picker, 
                        tool_call_node_stock_picker, formatter_node_stock_picker, tool_router_stock_picker)

def build_graph():
    workflow = StateGraph(AgentState)

    # nodes
    workflow.add_node("index_matcher", index_matcher)
    workflow.add_node("tool_call", tool_call_node)
    workflow.add_node("formatter", formatter_node)
    # stock picker
    workflow.add_node("stock_picker", stock_picker)
    workflow.add_node("tool_call_node_stock_picker", tool_call_node_stock_picker)
    workflow.add_node("formatter_node_stock_picker", formatter_node_stock_picker)


    # edges
    workflow.add_edge(START, "index_matcher")
    workflow.add_edge("tool_call", "index_matcher")
    workflow.add_edge("formatter", "stock_picker")
    workflow.add_edge("tool_call_node_stock_picker", "stock_picker")
    workflow.add_edge("formatter_node_stock_picker", END)

    # conditional edge
    workflow.add_conditional_edges(
        "index_matcher", tool_router, 
        {"tool_call": "tool_call",
         "formatter": "formatter"}
    )
    # stock picker conditional edge
    workflow.add_conditional_edges(
        "stock_picker", tool_router_stock_picker,
        {"tool_call_node_stock_picker": "tool_call_node_stock_picker",
         "formatter_node_stock_picker": "formatter_node_stock_picker"}
    )

    compiled_workflow = workflow.compile()

    return compiled_workflow