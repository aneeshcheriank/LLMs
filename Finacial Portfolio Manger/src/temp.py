import numpy as np
import pandas as pd
from scipy.optimize import minimize
from langchain_core.tools import tool

@tool
def optimize_portfolio_weights(returns_data: dict, sector_map: dict, target_vol: float):
    """
    Solves for weights that match a target volatility while enforcing:
    1. 5% max weight per individual stock.
    2. 20% max weight per sector.
    3. Weights must sum to 100%.
    """
    # Convert dict back to DataFrame for math
    returns_df = pd.DataFrame(returns_data)
    tickers = returns_df.columns
    n = len(tickers)
    
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
        indices = [tickers.get_loc(t) for t in sector_tickers if t in tickers]
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
    return final_weights