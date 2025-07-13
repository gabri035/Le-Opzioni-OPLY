import numpy as np
from scipy.stats import norm


def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Black-Scholes option pricing formula
    
    Parameters:
    S: Current stock price
    K: Strike price
    T: Time to expiration (in years)
    r: Risk-free rate
    sigma: Volatility
    option_type: 'call' or 'put'
    
    Returns:
    Option price
    """
    if T <= 0:
        return max(0, S - K) if option_type == 'call' else max(0, K - S)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def black_scholes_greeks(S, K, T, r, sigma, option_type='call'):
    """
    Calculate Black-Scholes Greeks
    
    Parameters:
    S: Current stock price
    K: Strike price
    T: Time to expiration (in years)
    r: Risk-free rate
    sigma: Volatility
    option_type: 'call' or 'put'
    
    Returns:
    Dictionary containing delta, gamma, vega, theta, rho
    """
    if T <= 0:
        return {'delta': 0, 'gamma': 0, 'vega': 0, 'theta': 0, 'rho': 0}
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Delta
    delta = norm.cdf(d1) if option_type == 'call' else -norm.cdf(-d1)
    
    # Gamma
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    
    # Vega (expressed per 1% change)
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100
    
    # Theta (per day)
    theta_call = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                  - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    theta_put = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                 + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
    theta = theta_call if option_type == 'call' else theta_put
    
    # Rho (per 1% change in interest rate)
    rho_call = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    rho_put = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100
    rho = rho_call if option_type == 'call' else rho_put

    return {
        'delta': delta,
        'gamma': gamma,
        'vega': vega,
        'theta': theta,
        'rho': rho
    }


def calculate_strategy_payoff(spot_price, options_legs, price_range=None):
    """
    Calculate payoff for a multi-leg options strategy
    
    Parameters:
    spot_price: Current stock price
    options_legs: List of dictionaries with keys: strike, premium, option_type, position
    price_range: Optional numpy array of stock prices to evaluate
    
    Returns:
    Dictionary with price_range, payoff_at_expiry, current_theoretical_value
    """
    if price_range is None:
        buffer = spot_price * 0.75
        S_min = max(0, spot_price - buffer)
        S_max = spot_price + buffer
        price_range = np.linspace(S_min, S_max, 300)
    
    payoff_at_expiry = np.zeros_like(price_range)
    
    for leg in options_legs:
        strike = leg['strike']
        premium = leg['premium']
        option_type = leg['option_type']
        position = leg['position']  # 1 for long, -1 for short
        
        if option_type == 'call':
            intrinsic_value = np.maximum(price_range - strike, 0)
        else:  # put
            intrinsic_value = np.maximum(strike - price_range, 0)
        
        payoff_at_expiry += position * (intrinsic_value - premium)
    
    return {
        'price_range': price_range,
        'payoff_at_expiry': payoff_at_expiry
    }


def calculate_strategy_greeks(spot_price, options_legs, T, r, sigma):
    """
    Calculate aggregate Greeks for a multi-leg options strategy
    
    Parameters:
    spot_price: Current stock price
    options_legs: List of dictionaries with keys: strike, premium, option_type, position
    T: Time to expiration (in years)
    r: Risk-free rate
    sigma: Volatility
    
    Returns:
    Dictionary with aggregate Greeks
    """
    total_greeks = {'delta': 0, 'gamma': 0, 'vega': 0, 'theta': 0, 'rho': 0}
    
    for leg in options_legs:
        strike = leg['strike']
        option_type = leg['option_type']
        position = leg['position']
        
        greeks = black_scholes_greeks(spot_price, strike, T, r, sigma, option_type)
        
        for key in total_greeks:
            total_greeks[key] += position * greeks[key]
    
    return total_greeks 