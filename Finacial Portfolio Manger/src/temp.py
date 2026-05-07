import numpy as np
import pandas as pd
from scipy.optimize import minimize
from langchain_core.tools import tool
import yfinance as yf

def get_stock_info(tickers):
    # 1. Fetch info for sectors
    ticker_map = {}
    for t in tickers:
        try:
            ticker_map[t] = yf.Ticker(t).info.get("sector", "Unknown")
        except:
            ticker_map[t] = "Unknown"
    
    # 2. Download all price data at once (Faster & Aligned)
    data = yf.download(tickers, period="1y", progress=False)
    
    # Handle both MultiIndex and Single Ticker cases
    if "Adj Close" in data.columns:
        prices = data["Adj Close"]
    else:
        prices = data["Close"]
        
    prices = prices.dropna()
    daily_returns = prices.pct_change().dropna()

    return {
        "sector_mapping": ticker_map,
        "daily_returns": daily_returns
    }

@tool
def optimize_portfolio_weights(tickers: list[str], target_vol: float) -> dict:
    """
    Solves for weights that match target volatility and maximize returns.
    """
    try:
        n = len(tickers)
        if n == 0: return {"error": "No tickers provided"}

        data = get_stock_info(tickers)
        returns_df = data["daily_returns"]
        expected_returns = data["expected_returns"]
        cov_matrix = returns_df.cov() * 252
        
        def objective(weights):
            portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            portfolio_return = np.dot(weights, expected_returns)
            
            # NORMALIZED OBJECTIVE:
            # We use a higher scale (100) for vol diff to ensure risk target is met,
            # but we heavily weight the return to force the solver to shift positions.
            return 100 * (portfolio_vol - target_vol)**2 - (portfolio_return * 2)

        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0}]
        
        # Widen bounds: Min 1%, Max 35%
        bounds = tuple((0.01, 0.35) for _ in range(n))
        
        # FIX: RANDOMIZED INITIAL GUESS
        # Starting away from 1/N forces the solver to recalculate paths.
        np.random.seed(42) # For consistency in testing
        random_guess = np.random.dirichlet(np.ones(n), size=1)[0]

        result = minimize(objective, random_guess, method='SLSQP', bounds=bounds, constraints=constraints)

        if not result.success:
            return {"error": f"Optimization failed: {result.message}"}

        # Format output
        final_weights = {tickers[i]: round(float(result.x[i]), 4) for i in range(n)}
        
        opt_weights = np.array(list(final_weights.values()))
        final_vol = np.sqrt(np.dot(opt_weights.T, np.dot(cov_matrix, opt_weights)))
        final_ret = np.dot(opt_weights, expected_returns)

        return {
            "final_weights": final_weights,
            "expected_annual_return": round(float(final_ret), 4),
            "expected_annual_volatility": round(float(final_vol), 4)
        }

    except Exception as e:
        return {"error": f"Tool failed: {str(e)}"}
    
portfolio_optimizer_tool_mapping = {
    "optimize_portfolio_weights": optimize_portfolio_weights
}

portfolio_optimizer_tool_list = list(portfolio_optimizer_tool_mapping.values())