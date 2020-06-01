import pandas as pd
from scrapers.player_ratings.scrape_fifa_rating import scrape_fifa_rating
from scrapers.player_data.scrape_player_data import scrape_player_data
from scrapers.player_id.scrape_player_id import get_pid
from scrapers.utils.utils import beautify_data
from testing_utils.testing_utils import norm
from scrapers.scrape_soccer_data import scrape_soccer_data
import _pickle as cPickle

competitions = {
    '1-bundesliga': "L1"}

# Checking personal soccer player statistics from a season ago e.g. #
name = "Lionel Messi"
season = 2020
GOALS = 3
ASSISTS = 4
MINUTES_PLAYED = 5

player_rating, player_potential = scrape_fifa_rating(name, season)
print("Name:", name, "-", "Player rating:", player_rating, "-", "Player potential:", player_potential)

p_data = scrape_player_data(name, get_pid(name), season - 1)
beautify_data(p_data)

train_stats = pd.read_csv('train_stats.csv')
train_stats.rename(columns={'Unnamed: 0': 'Feature'},
                   inplace=True)
train_stats.set_index('Feature', inplace=True)

with open('final_rf_model', 'rb') as f:
    rf = cPickle.load(f)
with open('final_ann_model', 'rb') as f:
    ann = cPickle.load(f)

df = pd.DataFrame(columns=['player_age', 'player_rating', 'player_potential', 'total_goals',
                           'total_assists', 'total_minutes_played', 'season'])
new = pd.DataFrame([[32, player_rating,
                     player_potential,
                     p_data['TOTAL'][GOALS],
                     p_data['TOTAL'][ASSISTS],
                     p_data['TOTAL'][MINUTES_PLAYED],
                     season - 2008]],
                   columns=['player_age', 'player_rating', 'player_potential', 'total_goals',
                            'total_assists', 'total_minutes_played', 'season'])
df = df.append(new)
player = norm(df, train_stats)
rf_pred = rf.predict(player)
ann_pred = ann.predict(player)

print("RF Prediction {}:".format(name), rf_pred)
print("ANN Prediction {}:".format(name), ann_pred)

# Scraping soccer data from transfers given year and competition #

# for competition in competitions.keys():
#     for year in range(2007, 2008):
#         scrape_soccer_data(competition, competitions[competition], year)
