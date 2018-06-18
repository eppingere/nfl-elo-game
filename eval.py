import pickle
import time

import tensorflow as tf

from forecast import *
from util import *

# Read historical games from CSV
games = Util.read_games("data/nfl_games.csv")

best_config = (0.0, 0.0, 0.0)
best_res = -10000.0
temp_time = 0.0

results = {}

for hfa_i in range(600, 700):
    hfa = 0.1 * hfa_i
    for k_i in range(100, 300):
        k = 0.1 * k_i
        for revert_i in range(10, 50):
            revert = 0.01 * revert_i

            before = time.time()

            # Forecast every game
            Forecast.forecast(games, HFA=hfa, K=k, REVERT=revert)

            # Evaluate our forecasts against Elo
            res = Util.evaluate_forecasts(games)

            if res > best_res:
                best_res = res
                best_config = (hfa, k, revert)
                results[(hfa, k, revert)] = res

            temp_time = time.time() - before

        print("Current Configuration: ")
        print("HFA: " + str(hfa))
        print("K: " + str(k))
        print("REVERT: " + str(revert))
        print("Best Difference: " + str(best_res))
        print("Time: " + str(temp_time))
        print("")

with open("configurations.pickle", "wb") as handle:
    pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)
