import numpy as np
import pandas as pd
from scipy.optimize import minimize
from langchain_core.tools import tool
import yfinance as yf

def get_stock_info(tickers):
    ticker_map = {}
    prices = pd.DataFrame()
    for ticker in tickers:
        yf_ticker = yf.Ticker(ticker)
        ticker_map[ticker] = yf_ticker.info["sector"]
    
        price = yf.download(ticker, period="1y")
        if "Adj Close" in price.columns:
            data = price["Adj Close"]
        elif "Close" in price.columns:
            data = price["Close"]
        else:
            next
    
        if len(prices.columns) == 0:
            prices = data
        else:
            prices = prices.join(
                data,
                how = "outer"
            )
    
    prices = prices.dropna()
    daily_returns = prices.pct_change()

    return {
        "sector_mapping": ticker_map,
        "daily_returns": daily_returns.dropna()
    }

@tool
def optimize_portfolio_weights(tickers: list[str], target_vol: float)->dict:
    """
    Solves for weights that match a target volatility.
    
    Args:
        tickers: A list of stock ticker symbols.
        target_vol: The target portfolio volatility (standard deviation) as a decimal.
        
    Returns:
        A dictionary containing the 'final_weights' for each ticker.
    """
    # Convert dict back to DataFrame for math
    n = len(tickers)
    data = get_stock_info(tickers)
    returns_df = data["daily_returns"]
    sector_map = data["sector_mapping"]
    
    # Calculate Covariance Matrix (Annualized)
    cov_matrix = returns_df.cov() * 252
    
    # 1. Objective Function: Minimize the difference from target volatility
    def objective(weights):
        portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return (portfolio_vol - target_vol)**2

    # 2. Constraints
    constraints = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0}  # Weights must sum to 1
    ]
    
    # Sector Constraints: Sum of weights in each sector <= 0.20
    for sector, sector_tickers in sector_map.items():
        indices = [tickers.index(t) for t in sector_tickers if t in tickers]
        if indices:
            constraints.append({
                'type': 'ineq', 
                'fun': lambda x, idx=indices: 0.20 - np.sum(x[idx]) 
            })

    # 3. Individual Bounds: 0% to 5% per stock
    bounds = tuple((0.0, 0.05) for _ in range(n))
    

    # 4. Initial Guess: Equal weighting
    init_guess = np.array([1.0/n] * n)

    # 5. Run Solver
    result = minimize(objective, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)

    if not result.success:
        return f"Optimization failed: {result.message}"

    # Return clean dictionary of {Ticker: Weight}
    final_weights = {tickers[i]: round(result.x[i], 4) for i in range(n)}
    return {
        "final_weights": final_weights
        }

portfolio_optimizer_tool_mapping = {
    "optimize_portfolio_weights": optimize_portfolio_weights
}

portfolio_optimizer_tool_list = list(portfolio_optimizer_tool_mapping.values())