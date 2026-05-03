import numpy as np
import pandas as pd
import yfinance as yf
from typing import List, Dict

from langchain_core.tools import tool

@tool
def get_best_index_for_volatility(target_volatility: float, test_tikcers: List[str]=None) -> Dict:
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
        #1. Download 1 year of historical daily close prices
        data = yf.download(test_tickers, period="1y")["Close"]
    
        # 2. Calculate daily returns
        daily_returns = data.pct_change().dropna()
    
        # 3. Annualize the standard deviation of daily returns
        # 252 is the number of trading days in a year
        annualized_volatilities = daily_returns.std() * np.sqrt(252)
    
        # 4. Find the ticker that is closest to the target volatility
        best_ticker = None
        closest_diff = float('inf')
        best_actual_vol = 0.0
        
        for ticker, vol in annualized_volatilities.items():
            diff = abs(vol - target_volatility)
            if diff < closest_diff:
                closest_diff = diff
                best_ticker = ticker
                best_actual_vol = vol
    
        return {
            "best_matching_index": best_ticker,
            "target_volatility": target_volatility,
            "actual_volatility": round(best_actual_vol, 4),
            "difference": round(closest_diff, 4)
        }
    except Exception as e:
        return f"error caluclating volatility: {str(e)}"


def get_tool_mappping():
    return {
        "get_best_index_for_volatility": get_best_index_for_volatility
    }

def get_tool_list():
    tool_mapping = get_tool_mappping()
    tool_list = list(tool_mapping.keys())
    return tool_list