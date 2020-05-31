from scrapers.player_ratings.scrape_fifa_rating import scrape_fifa_rating
from scrapers.player_data.scrape_player_data import scrape_player_data
from scrapers.player_id.scrape_player_id import get_pid
from scrapers.utils.utils import beautify_data
from scrapers.scrape_soccer_data import scrape_soccer_data

competitions = {
    '1-bundesliga': "L1"}


# Checking personal soccer player statistics e.g. #
name = "Iniesta"
club = "FC Barcelona"
season = 2010

player_rating, player_potential = scrape_fifa_rating(name, season, club=club)
print("Name:", name, "-", "Player rating:", player_rating, "-", "Player potential:", player_potential)

beautify_data(scrape_player_data(name, get_pid(name), season))


# Scraping soccer data from transfers given year and competition #

# for competition in competitions.keys():
#     for year in range(2007, 2008):
#         scrape_soccer_data(competition, competitions[competition], year)
