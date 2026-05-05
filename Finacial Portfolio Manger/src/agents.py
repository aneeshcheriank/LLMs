from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import ToolMessage

from src.model import get_llm
from src.tools import index_matcher_tool_mappping, index_matcher_tool_list, stock_picker_tool_list, stock_picker_tool_mapping
from src.configuration import MAX_TOOL_CALLS
from src.output_schema import IndexReport, StockSelectionReport

# Index picker agent implementation
# Define the graph state
class AgentState(TypedDict):
    user_input: str

    chat_history: Annotated[list, operator.add]
    stock_picker_history: Annotated[list, operator.add]

    perceived_volatility: float
    actual_volatility: float
    base_index: str
    risk_free_rate: float
    filtered_stocks: StockSelectionReport # from python 3.9 onwards, we can use list[str] instead of List[str]
    portfolio_weights: dict[str, float]

    iterations: int
    iterations_stock_picker: int


def index_matcher(state: AgentState):
    
    prompt = ChatPromptTemplate.from_messages([
        ("system",
     """You are an expert financial portfolio manager. Your task is to match a client's risk and investment profile to the most appropriate index.
     you are expected to use tools to find the best index for a volatility target. You will be provided with a client's input describing their 
     investment goals and risk tolerance, and you must convert that into a target volatility. Then, using the get_best_index_for_volatility tool, 
     you will identify the best matching index.

     IMPORTANT: 
     - You must select an index that reflect the risk and return perference of the user. 
     - You can call the tools at most 5-10 times
     - Do not repeatedly call the tool with similar input
     - If a close match is found, stop and provide the answer
     """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_input}")
    ])

    llm = get_llm()
    tool_list = index_matcher_tool_list()

    # need to implement a hard-stop on tool calls
    # when the limit is reached, the llm will be removed the tool calling capability and only return the final answer
    if state["iterations"] >= MAX_TOOL_CALLS:
        llm_with_tools = llm
    else:
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
        
        tool_mapping = index_matcher_tool_mappping()
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

def tool_router(state: AgentState):    
    # check the tool calls
    # if the tool call is not resolved, the agent can product its final response
    last_state = state["chat_history"][-1]
    if last_state.tool_calls:
         return "tool_call"   

    # check the max_iterations
    if state["iterations"] >= MAX_TOOL_CALLS:
        return "formatter" 
    
    return "formatter"

# def formatter_node(state: AgentState):
#     # this node will format the final response
#     last_state = state["chat_history"][-1]
    
#     prompt = ChatPromptTemplate.from_messages([
#         ("system",
#      """You are an expert financial reporter. You have multiple years of experience in financial analysis and reporting. Your task is to take 
#      the output from the previous tool calls, which includes the best matching index and its volatility, and format it into a clear and concise 
#      report for the client. The report should include the recommended index, its actual volatility, how it compares to the client's target volatility, 
#      and any relevant insights or recommendations based on this information.
#      """),
#         MessagesPlaceholder(variable_name="chat_history")
#     ])

    
#     llm = get_llm()
#     llm_with_structured_output = llm.with_structured_output(IndexReport)
#     chain = prompt | llm_with_structured_output
#     response = chain.invoke({
#         "chat_history": [last_state]
#     })

#     return {"chat_history": [response]}

def formatter_node(state: AgentState):
    # 1. Convert the message history into a clean string for the reporter
    # This prevents the "Unknown Tool" error and the "List vs Object" error.
    context_string = ""
    for msg in state["chat_history"]:
        if hasattr(msg, 'content') and msg.content:
            # only care about the text, not the tool_call attributes
            context_string += f"{msg.type}: {msg.content}\n"

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert financial reporter. 
         Review the following research context and extract the final details 
         into the required structured format."""),
        ("human", "Research Context:\n\n{context}")
    ])
    
    llm = get_llm()
    # Structured output works best when the input is plain text context
    llm_with_structured_output = llm.with_structured_output(IndexReport)
    
    chain = prompt | llm_with_structured_output
    
    # 2. Invoke with a plain string variable instead of a message list
    response = chain.invoke({
        "context": context_string
    })
    report_data = response.model_dump()
    print(report_data)

    return {
        "chat_history": [response],
        "base_index": report_data["base_index"],
        "perceived_volatility": report_data["perceived_volatility"],
        "actual_volatility": report_data["actual_volatility"]
    }

# Stock picker agent implementation
# - select the stock in the index based of alpha, beta, PE and other related factors
def stock_picker(state: AgentState):
    
    prompt = ChatPromptTemplate.from_messages([
        ("system",
     """You are an expert financial portfolio manager. Your pick best stocks from the {base_index}.

     IMPORTANT: 
     - you are expected to use tools to find the stocks constitues the {base_index} and get the stock analytics. 
     - You can use the "duckduckgo search tool" and "get_index_constituents" to find the underlying stocks of the {base_index}.
     - The selection of the stocks should not change the overall perceived volatility of the portfolio.
     - The stock should have a postive alpha.
     - Beta sould be between match the user's risk preference.
     - The stock should have 0.25 percentile in the group of stocks in the index based on PE ratio.
     - Also use other indicator that you think is relevant.
     - use "get_stock_analytics" to get the stock analysis data. don't guss these values always use the tool to get the data.
     - consider the investable sum when picking the stocks, as some stocks might be too expensive for 
     the user to buy given their investable sum.
     - keep the number of stocks between 10-15 to ensure diversification.
     """),
        ("human", """
         investment objective: {user_input}, base index: {base_index}, target volatility: {perceived_volatility}, risk free rate: {risk_free_rate}.
         stock picking history: {stock_picker_history}.
         """),
    ])

    llm = get_llm()
    llm_with_tools = llm.bind_tools(stock_picker_tool_list) # need to define a new output schema for the stock picker
    chain = prompt | llm_with_tools
    response = chain.invoke({
        "user_input": state["user_input"],
        "base_index": state["base_index"],
        "perceived_volatility": state["perceived_volatility"],
        "risk_free_rate": state["risk_free_rate"],
        "stock_picker_history": state["stock_picker_history"]
    })

    return {
        "stock_picker_history": [response]
        }

def tool_call_node_stock_picker(state: AgentState):
    # this node will handle the tool call and update the state accordingly
    last_state = state["stock_picker_history"][-1]
    # increment the iteration count
    iterations = state["iterations_stock_picker"] + 1

    print(f"tool_call: {iterations}")

    tool_messages = []
    for tool_call in last_state.tool_calls:

        name = tool_call.get("name")
        args = tool_call.get("args")
        print(f"tool_call_name: {name}, args: {args}")
        
        try:
            tool_mapping = stock_picker_tool_mapping
            if name in tool_mapping:
                tool_response = tool_mapping[name].invoke(args) #invoke expect dictionary as input
                tool_messages.append(
                    ToolMessage(
                        content = str(tool_response),
                        tool_call_id = tool_call.get("id")
                    )
                )
        except Exception as e:
            tool_messages.append(
                ToolMessage(
                    content = f"Error calling tool {name} with args {args}: {str(e)}",
                    tool_call_id = tool_call.get("id")
                )
            )

    return {
        "stock_picker_history": tool_messages, #the tool_messages is a list
        "iterations_stock_picker": iterations
    }

def formatter_node_stock_picker(state: AgentState):
    # 1. Convert the message history into a clean string for the reporter
    # This prevents the "Unknown Tool" error and the "List vs Object" error.
    context_string = ""
    for msg in state["stock_picker_history"]:
        if hasattr(msg, 'content') and msg.content:
            context_string += f"{msg.type}: {msg.content}\n"

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         """You are an expert financial reporter. 
         Take the following context (User goals and Tool results) and 
         generate the final IndexReport.
         """),
        ("human", "Here is the investment context:\n\n{context}")
    ])
    
    llm = get_llm()
    # Structured output works best when the input is plain text context
    llm_with_structured_output = llm.with_structured_output(StockSelectionReport)
    
    chain = prompt | llm_with_structured_output
    
    # 2. Invoke with a plain string variable instead of a message list
    response = chain.invoke({
        "context": context_string
    })
    report_data = response.model_dump()

    return {
        "stock_picker_history": [response],
        "filtered_stocks": report_data["selected_stocks"]
    }

def tool_router_stock_picker(state: AgentState):    
    # check the tool calls
    # if the tool call is not resolved, the agent can product its final response
    last_state = state["stock_picker_history"][-1]
    if last_state.tool_calls:
         return "tool_call_node_stock_picker"   

    # # check the max_iterations
    # if state["iterations"] >= MAX_TOOL_CALLS:
    #     return "formatter" 
    
    return "formatter_node_stock_picker"