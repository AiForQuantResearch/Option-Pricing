import numpy as np

#Option Payoff    
def payoff_call(S, strike = K):
    return np.maximum(S - strike, 0)

def payoff_put(S, strike = K):
    return np.maximum(strike - K, 0)

def up_down(sigma, N, T):
    dt = T / N
    u = exp(sigma * sqrt(dt))
    d = 1 / u
    q = (exp(r * dt) - d) / (u - d)
    return u, d, q


def OptionPrice(r, u, d, fonction_prix_t_i_plus_one, delta_flag=0):
    
    """
    On effectue une itération de la date t_{i+1} à la date t_i.
    
    Paramètres
    + r, u, d: les paramètres du modèle binomial 
    + fonction_prix_t_i_plus_one (une fonction Python):
        La fonction de prix v(t_{i+1}, .) à la date t_{i+1}.
        Doit prendre comme argument la valeur S_{t_{i+1}} du sous-jacent à la date t_{i+1}.
    
    Output:
    + Une fonction Python, la fonction de prix v(t_i, .) à la date t_i.
      Doit prendre comme argument la valeur S_{t_i} du sous-jacent.
            
    + Si delta_flag: renvoie une autre fonction Python, le delta delta(t_i, .) du portefeuille à la date t_i.
      Doit prendre comme argument la valeur S_{t_i} du sous-jacent.
    """
    
    q_up = (1 + r - d) / (u - d)
    q_down = 1 - q_up
    
    def fonction_prix_t_i(S):
        valeur = (fonction_prix_t_i_plus_one(S*u)*q_up + fonction_prix_t_i_plus_one(S*d)*q_down) / (1+r)
        return valeur
    
    if delta_flag:
            def delta_t_i(S):
                delta = (fonction_prix_t_i_plus_one(S*u) - fonction_prix_t_i_plus_one(S*d)) / (S*(u - d))
                return delta
   
    if delta_flag == 0:
        return fonction_prix_t_i
    
    else:
        return fonction_prix_t_i, delta_t_i
    
    
def OptionPrice_n(r, u, d, payoff, i, n, delta_flag=0):
    fonction_prix_et_delta = [payoff, 0]
        
    for j in range(n, i, -1):
        fonction_prix_et_delta = OptionPrice(r, u, d, fonction_prix_et_delta[0], delta_flag=1)
        ## la variable fonction_prix_et_delta contient un couple de fonctions
    
    if delta_flag == 0:
        return fonction_prix_et_delta[0]
    
    else:
        return fonction_prix_et_delta


    

def recursion_americaine(r, u, d, payoff, fonction_prix_t_i_plus_one):
    """
    On effectue une itération dans l'équation de programmation dynamique de la date t_{i+1} à la date t_i.
    
    Paramètres
    + r, u, d: les paramètres du modèle binomial 
    
    + payoff (fonction Python): la fonction payoff de l'opt américaine
    
    + fonction_prix_t_i_plus_one (fonction Python): la fonction de prix v_{Am}(t_{i+1}, .) de l'opt américaine à la date t_{i+1}.
      Cette fonction doit prendre comme argument la valeur S_{t_{i+1}} du sous-jacent.
    
    Output: une fonction Python, la fonction de prix v_{Am}(t_i, .) de l'opt américaine à la date t_i.
            Cette fonction prendra comme argument la valeur S_{t_i} du sous-jacent.
    """
    q_up = (1 + r - d) / (u-d)
    q_down = 1 - q_up
    
    def fonction_prix_t_i(S):

        valeur_continuation = (fonction_prix_t_i_plus_one(S*u) * q_up + fonction_prix_t_i_plus_one(S*d) * q_down) / (1 + r)
        
        valeur = np.maximum(payoff(S), valeur_continuation)
        
        return valeur
    
    return fonction_prix_t_i


def prix_americain_t_i(r, u, d, payoff, i, n):
    """
    Prix à la date t_i, i < n, de l'option américaine de maturité t_n et de fct de payoff donnée.
    
    Output: une fonction Python, la fonction de prix v_{Am}(t_i, .) à la date t_i.
            Cette fonction prendra comme argument la valeur S_{t_i} du sous-jacent.
    """
    fonction_prix = payoff    
    for j in range (i, n):
        fonction_prix = recursion_americaine(r, u, d, payoff, fonction_prix)
    return fonction_prix





