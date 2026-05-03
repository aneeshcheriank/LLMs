from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field, field_serializer
from typing import List

from src.model import get_llm

class AssetAllocation(BaseModel):
    asset_class: str = Field(description="The class of the asset, e.g., 'Stock', 'Bond', 'Real Estate', 'Commodity'.")
    asset_ticker: str = Field(description="The ticker symbol of the asset, e.g., AAPL for Apple Inc.")
    allocation_percentage: float = Field(description="The percentage of the total portfolio allocated to this asset, e.g., 20.0 for 20%.")

class InvestmentStrategy(BaseModel):
    strategy_name: str = Field(description="A descriptive name for the investment strategy, e.g., 'Aggressive Growth Strategy'.")
    asset_allocations: List[AssetAllocation] = Field(description="A list of asset allocations that make up the strategy.")

strategy_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are an expert financial portfolio manager with 10 years of experience in creating diversified investment strategies.
    
    Your task is to generate a concrete asset allocation strategy tailored to the client's profile.
    
    CRITICAL REQUIREMENTS:
    1. The strategy MUST be diversified across multiple asset classes (e.g., equities, fixed income, real estate, alternatives).
    2. Select exactly or at least 5 distinct, real-world investable assets (e.g., specific ETFs, mutual funds, or broad asset classes like 'S&P 500 ETF (SPY)', 'US Treasury Bonds (TLT)').
    3. Assign a percentage allocation to each asset. The total sum MUST equal exactly 100%.
    4. Base the strategy entirely on the client's provided risk tolerance, investment horizon, and financial goals."""),
    MessagesPlaceholder(variable_name="chat_history")
])

llm = get_llm()

strategy_chain = strategy_prompt | llm.with_structured_output(InvestmentStrategy)

def create_strategy(input):
    response = strategy_chain.invoke(input)
    return response
