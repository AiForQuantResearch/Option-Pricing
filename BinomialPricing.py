import numpy as np
from math import exp, sqrt
import pandas as pd


def up_down(sigma, N, T, r):
    dt = T / N
    u = exp(sigma * sqrt(dt))
    d = 1 / u
    q = (exp(r * dt) - d) / (u - d)
    return u, d, q

def eu_option_pricing(K, T, S0, r, N, u, d, q, option_type):
    
    #Parameters
    dt = T / N
    disc_factor = exp(-r * dt)

    # Asset Price
    S = S0 * np.array([d ** (N - i) * u ** i for i in range(N + 1)])
    
    #Option Payoff
    if option_type == 'call':
        C = np.maximum(S - K, np.zeros(N + 1))
    elif option_type == 'put':
        C = np.maximum(K - S, np.zeros(N + 1))
    
    #Option Price
    for i in np.arange(N, 0, -1):
        C = disc_factor * (q * C[1:i + 1] + (1 - q) * C[0:i])

    return C[0]


def am_option_pricing(K, T, S0, r, N, u, d, q, option_type):
    
    dt = T / N
    disc_factor = exp(-r * dt)

    # Asset Price
    S = S0 * np.array([d ** (N - i) * u ** i for i in range(N + 1)])
    
    # Option Payoff
    if option_type == 'call':
        C = np.maximum(S - K, np.zeros(N + 1))
    elif option_type == 'put':
        C = np.maximum(K - S, np.zeros(N + 1))
    
    # Option Price
    for i in np.arange(N, 0, -1):
        C = disc_factor * (q * C[1:i + 1] + (1 - q) * C[0:i])
        # American option exercise
        S = S[:-1]  # Current asset price
        if option_type == 'call':
            exercise = np.maximum(S - K, np.zeros(i))
        elif option_type == 'put':
            exercise = np.maximum(K - S, np.zeros(i))
        C = np.maximum(C, exercise)

    return C[0]


