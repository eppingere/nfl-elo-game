import os
import pickle
import sys
import time

import IPython
import numpy
import scipy.optimize as opt
import tensorflow as tf
from scipy.optimize import fmin

import pylab
from forecast import *
from util import *

# Read historical games from CSV
games = Util.read_games("data/nfl_games.csv")

def diff_from_config(p):

    hfa, k, revert = p

    # Forecast every game
    Forecast.forecast(games, HFA=hfa, K=k, REVERT=revert)

    # Evaluate our forecasts against Elo
    return -1.0*Util.evaluate_forecasts(games)

# Run on default parameters
diff_from_config((Forecast.HFA_default, Forecast.K_default, Forecast.REVERT_default))

# Find optimal inputs
sys.stdout = open(os.devnull, "w")
solution = opt.minimize(diff_from_config, [Forecast.HFA_default, Forecast.K_default, Forecast.REVERT_default])
sys.stdout = sys.__stdout__

print(solution)

IPython.embed()
