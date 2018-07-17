import csv

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

class Util:

    @staticmethod
    def read_games(file):
        """ Initializes game objects from csv """
        games = [item for item in csv.DictReader(open(file))]

        # Uncommenting these three lines will grab the latest game results for 2017, update team ratings accordingly, and make forecasts for upcoming games
        file_2017 = file.replace(".", "_2017.")
        urlretrieve("https://projects.fivethirtyeight.com/nfl-api/2017/nfl_games_2017.csv", file_2017)
        games += [item for item in csv.DictReader(open(file_2017))]

        for game in games:
            game['season'], game['neutral'], game['playoff'] = int(game['season']), int(game['neutral']), int(game['playoff'])
            game['score1'], game['score2'] = int(game['score1']) if game['score1'] != '' else None, int(game['score2']) if game['score2'] != '' else None
            game['elo_prob1'], game['result1'] = float(game['elo_prob1']) if game['elo_prob1'] != '' else None, float(game['result1']) if game['result1'] != '' else None

        return games

    @staticmethod
    def evaluate_forecasts(games):
        """ Evaluates and scores forecasts in the my_prob1 field against those in the elo_prob1 field for each game """
        my_points_by_season, elo_points_by_season = {}, {}

        forecasted_games = [g for g in games if g['result1'] != None]
        upcoming_games = [g for g in games if g['result1'] == None and 'my_prob1' in g]

        # Evaluate forecasts and group by season
        for game in forecasted_games:

            # Skip unplayed games and ties
            if game['result1'] == None or game['result1'] == 0.5:
                continue

            # Don't count the 2017 NE/KC game because it wasn't included in our game
            # if game['date'] == '2017-09-07':
            #   continue

            if game['season'] not in elo_points_by_season:
                elo_points_by_season[game['season']] = 0.0
                my_points_by_season[game['season']] = 0.0

            # Calculate elo's points for game
            rounded_elo_prob = round(game['elo_prob1'], 2)
            elo_brier = (rounded_elo_prob - game['result1']) * (rounded_elo_prob - game['result1'])
            elo_points = 25 - (100 * elo_brier)
            elo_points = round(elo_points + 0.001 if elo_points < 0 else elo_points, 1) # Round half up
            if game['playoff'] == 1:
                elo_points *= 2
            elo_points_by_season[game['season']] += elo_points

            # Calculate my points for game
            rounded_my_prob = round(game['my_prob1'], 2)
            my_brier = (rounded_my_prob - game['result1']) * (rounded_my_prob - game['result1'])
            my_points = 25 - (100 * my_brier)
            my_points = round(my_points + 0.001 if my_points < 0 else my_points, 1) # Round half up
            if game['playoff'] == 1:
                my_points *= 2
            my_points_by_season[game['season']] += my_points


        start_season = 2000
        num_seasons = 18
        my_avg, elo_avg = 0, 0

        # Print individual seasons
        for season in range(start_season, start_season + num_seasons):
            my_avg += my_points_by_season[season]
            elo_avg += elo_points_by_season[season]
            print("In %s, your forecasts would have gotten %s points. Elo got %s points." % (season, round(my_points_by_season[season], 2), round(elo_points_by_season[season], 2)))

        # Show overall performance
        # my_avg = sum(my_points_by_season.values())/len(my_points_by_season.values())
        # elo_avg = sum(elo_points_by_season.values())/len(elo_points_by_season.values())
        my_avg /= num_seasons
        elo_avg /= num_seasons

        print("\nFrom %s to %s, your forecast scored an average of %s vs Nate Silver's %s\n" % (start_season, start_season + num_seasons - 1, round(my_avg, 2), round(elo_avg, 2)))

        # print("\nCurrent Configuration: %s\nTheir Configuration: %s\n" % (round(my_avg, 2), round(elo_avg, 2)))

        # Print forecasts for upcoming games
        # if len(upcoming_games) > 0:
        #     print("Forecasts for upcoming games:")
        #     for game in upcoming_games:
        #         print("%s\t%s vs. %s\t\t%s%% (Elo)\t\t%s%% (You)" % (game['date'], game['team1'], game['team2'], int(round(100*game['elo_prob1'])), int(round(100*game['my_prob1']))))
        #     print("")

        return my_avg - elo_avg
