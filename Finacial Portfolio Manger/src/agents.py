from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field, field_serializer
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import ToolMessage

from src.model import get_llm
from src.tools import get_tool_mappping, get_tool_list
from src.configuration import MAX_TOOL_CALLS
from src.output_schema import IndexReport

# Define the graph state
class AgentState(TypedDict):
    user_input: str
    chat_history: Annotated[list, operator.add]
    target_volatility: float
    selected_index: str
    iterations: int


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

     IMPORTANT: 
     - You must select an index that reflect the risk and return perference of the user. 
     """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_input}")
    ])

    llm = get_llm()
    tool_list = get_tool_list()
    llm_with_tools = llm.bind_tools(tool_list)
    chain = prompt | llm_with_tools

    response = chain.invoke(state)
    return {"chat_history": [response]}

def tool_call_node(state: AgentState):
    # this node will handle the tool call and update the state accordingly
    last_state = state["chat_history"][-1]
    # increment the iteration count
    iterations = state["iterations"] + 1

    print("tool_call")

    tool_messages = []
    for tool_call in last_state.tool_calls:

        name = tool_call.get("name")
        args = tool_call.get("args")
        
        tool_mapping = get_tool_mappping()
        if name in tool_mapping:
            tool_response = tool_mapping[name].invoke(args) #invoke expect dictionary as input
            tool_messages.append(
                ToolMessage(
                    content = str(tool_response),
                    tool_call_id = tool_call.get("id")
                )
            )

    return {
        "chat_history": tool_messages, #the tool_messages is a list
        "iterations": iterations
    }

def strategy_router(state: AgentState):

    # check the max_iterations
    if state["iterations"] >= MAX_TOOL_CALLS:
        return "formatter"
    
    # check the tool calls
    last_state = state["chat_history"][-1]
    if last_state.tool_calls:
         return "tool_call"    
    
    return "formatter"

def formatter_node(state: AgentState):
    # this node will format the final response
    last_state = state["chat_history"][-1]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system",
     """You are an expert financial reporter. You have multiple years of experience in financial analysis and reporting. Your task is to take 
     the output from the previous tool calls, which includes the best matching index and its volatility, and format it into a clear and concise 
     report for the client. The report should include the recommended index, its actual volatility, how it compares to the client's target volatility, 
     and any relevant insights or recommendations based on this information.
     """),
        MessagesPlaceholder(variable_name="chat_history")
    ])

    
    llm = get_llm()
    llm_with_structured_output = llm.with_structured_output(IndexReport)
    chain = prompt | llm_with_structured_output
    response = chain.invoke(state)

    return {"chat_history": [response]}
