import pickle
import time

import scipy.optimize as opt
import tensorflow as tf

from forecast import *
from util import *

# Read historical games from CSV
games = Util.read_games("data/nfl_games.csv")


results = {}

def diff_from_config(p):
    hfa, k, revert = p
    # Forecast every game
    Forecast.forecast(games, HFA=hfa, K=k, REVERT=revert)

    # Evaluate our forecasts against Elo
    res = Util.evaluate_forecasts(games)

    results[(hfa, k, revert)] = res

    return -1.0*res


solution = opt.minimize(diff_from_config, [Forecast.HFA_default, Forecast.K_default, Forecast.REVERT_default])

print(solution)
