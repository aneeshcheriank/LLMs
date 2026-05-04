from typing import List
from pydantic import BaseModel, Field


class IndexReport(BaseModel):
    base_index: str = Field(description="The ticker symbol of the selected index from the curated list, e.g., SPY, AGG.")
    perceived_volatility: float = Field(description="The perceived volatility as a decimal, e.g., 0.12.")
    actual_volatility: float = Field(description="The actual volatility of the selected index as a decimal, e.g., 0.11.")