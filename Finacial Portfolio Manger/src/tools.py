import numpy as np
import pandas as pd
import yfinance as yf
from typing import List, Dict

from langchain_core.tools import tool

@tool
def get_best_index_for_volatility(target_volatility: float, test_tickers: List[str]=None) -> Dict:
    """
    Fetches historical data from Yahoo Finance for a list of tickers, 
    calculates their 1-year realized volatility, and returns the best match.
    
    :param target_volatility: Target volatility as a decimal (e.g., 0.12 for 12%)
    :param test_tickers: A list of candidate tickers to evaluate.
    :return: Dict containing the best matching ticker, its actual volatility, and the error.
    """
    # Fallback to a highly diversified list across different risk profiles
    if not test_tickers:
        test_tickers = [
            "AGG", "SHY", "BNDX",  # Low Vol (~3-8%)
            "AOM", "AOR",          # Moderate Vol (~8-13%)
            "SPY", "VEA", "IWM",   # High Vol (~13-18%)
            "QQQ", "VWO", "INDA"   # Highest Vol (18%+)
        ]

    try:
        data = yf.download(test_tickers, period="1y")

        if data.empty:
            raise ValueError("No data returned")

        close = data["Close"]
        daily_returns = close.pct_change().dropna(how="all", axis=1).dropna()
        annualized_vol = daily_returns.std() * np.sqrt(252)

        if isinstance(annualized_vol, float):
            annualized_vol = {test_tickers[0]: annualized_vol}

        best_ticker = min(
            annualized_vol,
            key=lambda t: abs(annualized_vol[t] - target_volatility)
        )

        return {
            "best_matching_index": best_ticker,
            "target_volatility": target_volatility,
            "actual_volatility": round(float(annualized_vol[best_ticker]), 4),
            "difference": round(abs(annualized_vol[best_ticker] - target_volatility), 4)
        }

    except Exception as e:
        return {
            "error": True,
            "message": str(e)
        }


def index_matcher_tool_mappping():
    return {
        "get_best_index_for_volatility": get_best_index_for_volatility
    }

def index_matcher_tool_list():
    tool_mapping = index_matcher_tool_mappping()
    tool_list = list(tool_mapping.values())
    return tool_list