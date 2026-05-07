from typing import List
from pydantic import BaseModel, Field

# output schema for the index matcher agent
class IndexReport(BaseModel):
    base_index: str = Field(description="The ticker symbol of the selected index from the curated list, e.g., SPY, AGG.")
    perceived_volatility: float = Field(description="The perceived volatility as a decimal, e.g., 0.12.")
    actual_volatility: float = Field(description="The actual volatility of the selected index as a decimal, e.g., 0.11.")

# ouput schema for the stock picker agent
class Stock(BaseModel):
    ticker: str = Field(description="The ticker symbol of the selected stock, e.g., AAPL.")
    alpha: float = Field(description="The alpha of the stock, indicating its performance relative to the market.")
    beta: float = Field(description="The beta of the stock, indicating its volatility relative to the market.")
    pe_ratio: float = Field(description="The price-to-earnings ratio of the stock, indicating its valuation.")  

class StockSelectionReport(BaseModel):
    base_index: str = Field(description="The ticker symbol of the base index from which stocks were selected, e.g., SPY.")
    selected_stocks: List[Stock] = Field(description="A list of selected stocks with their respective alpha, beta, and PE ratio.")

# output schema for portfolio optimizer
class stock_weight(BaseModel):
    ticker: str = Field(description="The ticker symbol of the selected stock, e.g., AAPL.")
    sector: str = Field(description="The sector at which the stock belongs (e.g. Technology, Finance)")
    ratio: float = Field(description="Percentage of the investable sum advised to invest in this stock e.g. 0.05")