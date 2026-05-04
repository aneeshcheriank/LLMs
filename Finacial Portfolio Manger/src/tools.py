import numpy as np
import pandas as pd
import yfinance as yf
from typing import List, Dict
import re

from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults

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

# tools for the stock picker agent
@tool
def get_index_constituents(index_name: str) -> str:
    """
    Finds the constituent stock tickers for a given market index (e.g., 'S&P 500', 'CAC 40').
    Uses DuckDuckGo to find the correct data source and then extracts the ticker list.
    """
    search = DuckDuckGoSearchRun()
    
    # 1. Search specifically for the Wikipedia list or a direct data source
    search_query = f"{index_name} constituents list wikipedia"
    search_results = search.run(search_query)
    
    # 2. Extract URLs from the search results using regex
    # We look for Wikipedia first as it's the most structured
    urls = re.findall(r'https?://[^\s)\]]+', search_results)
    wiki_urls = [u for u in urls if "wikipedia.org" in u]
    
    # Use the first Wikipedia URL found, or fall back to the first result overall
    target_url = wiki_urls[0] if wiki_urls else (urls[0] if urls else None)
    
    if not target_url:
        return f"Could not find a reliable URL for the constituents of {index_name}."

    try:
        # 3. Use Pandas to scrape all tables from the target URL
        tables = pd.read_html(target_url)
        
        for df in tables:
            # Look for common column names that contain tickers
            # We add 'Symbol', 'Ticker', 'Code', and 'Identifier'
            potential_cols = ['Symbol', 'Ticker', 'Ticker symbol', 'Component', 'Code', 'Company']
            found_col = next((c for c in df.columns if any(p in str(c) for p in potential_cols)), None)
            
            if found_col:
                # Clean the tickers: remove whitespace and handle dual-class formats (e.g., BRK.B -> BRK-B)
                tickers = df[found_col].astype(str).str.replace(r'\s+', '', regex=True).unique().tolist()
                
                # Basic cleaning for yfinance compatibility
                clean_tickers = [t.replace('.', '-') for t in tickers if len(t) < 10] 
                
                # Filter out header names if they were accidentally scraped
                clean_tickers = [t for t in clean_tickers if t.upper() == t and t.isalpha()]
                
                if clean_tickers:
                    return f"Found {len(clean_tickers)} tickers for {index_name} at {target_url}: {', '.join(clean_tickers)}..."
        
        return f"Found the page {target_url}, but couldn't find a clear ticker table. go for a duckduck go search"
        
    except Exception as e:
        return f"Attempted to scrape {target_url} but failed: {str(e)}, go for a duckduckgo search"
    
# search_tool = DuckDuckGoSearchRun()
search_tool = DuckDuckGoSearchResults(max_results=3)

@tool
def get_stock_analytics(ticker: str, benchmark_selected: str = "SPY") -> dict:
    """
    Retrieves P/E Ratio, Beta, and calculates Alpha (relative to S&P 500) for a given ticker.
    Also returns Market Cap and Dividend Yield.
    inputs: - ticker: stock ticker symbol (e.g., AAPL)
            - benchmark_selected: the index to compare against for alpha calculation (default is SPY)
    output: dict with keys 'symbol', 'pe_ratio', 'beta', 'alpha_1y', 'market_cap', 'dividend_yield', 'current_price'
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # 1. Fetch direct metrics from .info
        pe_ratio = info.get("trailingPE", "N/A")
        beta = info.get("beta", "N/A")
        market_cap = info.get("marketCap", "N/A")
        dividend_yield = info.get("dividendYield", 0) * 100
        
        # 2. Calculate Alpha (Excess return over SPY)
        # We compare 1-year returns of the stock vs the benchmark
        history = stock.history(period="1y")['Close']
        benchmark = yf.Ticker(benchmark_selected).history(period="1y")['Close']
        
        if not history.empty and not benchmark.empty and beta != "N/A":
            stock_return = (history.iloc[-1] / history.iloc[0]) - 1
            market_return = (benchmark.iloc[-1] / benchmark.iloc[0]) - 1
            
            # Simple Alpha Formula: R_i - (Beta * R_m)
            alpha = stock_return - (beta * market_return)
        else:
            alpha = "N/A"

        return {
            "symbol": ticker.upper(),
            "pe_ratio": pe_ratio,
            "beta": beta,
            "alpha_1y": f"{alpha:.2%}" if isinstance(alpha, float) else "N/A",
            "market_cap": f"${market_cap:,}" if isinstance(market_cap, int) else "N/A",
            "dividend_yield": f"{dividend_yield:.2f}%",
            "current_price": info.get("currentPrice", "N/A")
        }

    except Exception as e:
        return {"error": f"Failed to fetch data for {ticker}: {str(e)}"}

stock_picker_tool_mapping = {
    "get_index_constituents": get_index_constituents,
    "duckduckgo_search": search_tool,
    "get_stock_analytics": get_stock_analytics
}

stock_picker_tool_list = list(stock_picker_tool_mapping.values())