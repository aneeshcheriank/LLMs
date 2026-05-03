from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field, field_serializer
from typing import TypedDict

from src.model import get_llm
from src.tools import get_tool_mappping, get_tool_list
from langchain_core.messages import ToolMessage

# Define the graph state
class AgentState(TypedDict):
    user_input: str
    chat_history: list
    target_volatility: float
    selected_index: str


def create_strategy(state: AgentState):
    class Schema(BaseModel):
        index: str = Field(description="The ticker symbol of the selected index from the curated list, e.g., SPY, AGG.")
        volatility: str = Field(description="The perceived volatility as a decimal, e.g., 0.12.")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system",
     """You are an expert financial portfolio manager. Your task is to match a client's risk and investment profile to the most appropriate index.
     you are expected to use tools to find the best index for a volatility target. You will be provided with a client's input describing their 
     investment goals and risk tolerance, and you must convert that into a target volatility. Then, using the get_best_index_for_volatility tool, 
     you will identify the best matching index from the curated universe.
     """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_input}")
    ])

    llm = get_llm()
    tool_list = get_tool_list()
    llm_with_tools = llm.bind_tools(tool_list)
    chain = prompt | llm_with_tools

    response = chain.invoke(input)
    return response

def tool_call_node(state: AgentState):
    # this node will handle the tool call and update the state accordingly
    last_state = state["messages"][-1]

    print("tool_call")

    tool_messages = []
    for tool_call in last_state.tool_calls:

        name = tool_call.get("name")
        args = tool_call.get("args")
        
        tool_mapping = get_tool_mappping()
        if name in tool_mapping:
            tool_response = tool_mapping["name"].invoke(**args)
            tool_messages.append(
                ToolMessage(
                    content = str(tool_response),
                    id = tool_call.get("id")
                )
            )

    return {
        "messages": tool_messages #the tool_messages is a list
    }

def strategy_router(state: AgentState):
    
    # check the tool calls
    last_state = state["messages"][-1]
    if last_state.tool_calls:
         return "tool_call"    
    
    return END

def formatter_node(state: AgentState):
    # this node will format the final response
    last_state = state["messages"][-1]
    pass

