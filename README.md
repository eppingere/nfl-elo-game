# Me vs Nate Silver on NFL ELO Rating Game

## My Strategy
* Generalize constants to `Forecast.forcast` to be optional inputs
* Find optimal values for those inputs using `scipy`

## How do I test it
Simply run:

    python eval.py
    
 Will output something like
 
        ...
        From 2000 to 2017, my forecast scored an average of 851.37 vs Nate Silver's 839.36
        ...
    
Fork from [Nate Silver's FiveThirtyEight NFL Predictor](https://github.com/fivethirtyeight/nfl-elo-game)
