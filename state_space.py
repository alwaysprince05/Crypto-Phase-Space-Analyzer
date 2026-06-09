import numpy as np

def compute_log_returns(prices):
    return np.log(prices[1:] / prices[:-1])

def compute_velocity(prices):
    return np.gradient(prices)

def compute_acceleration(prices):
    return np.gradient(np.gradient(prices))

def compute_phase_space(prices):
    log_returns = compute_log_returns(prices)
    velocity = compute_velocity(prices)[1:]  # align with log_returns
    acceleration = compute_acceleration(prices)[1:]  # align with log_returns
    return log_returns, velocity, acceleration
