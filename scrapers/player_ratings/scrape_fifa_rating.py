from typing import Tuple, Union
from bs4 import BeautifulSoup
from scrapers.utils.utils import strip_accents, similar, replace_all, AppURLopener, seasons


def scrape_fifa_rating(player_name: str, season: int, age: int = None,
                       nationality: int = None, club: str = None,
                       user_input: bool = False,
                       min_name_sim: float = 0.75, min_club_sim: float = 0.25) -> \
        Tuple[Union[str, int], Union[str, int]]:
    """
    Scrapes fifa overall and potential rating from www.sofifa.com

    given
    :param player_name: the name of the player e.g. Frenkie de Jong
    :param season: the season e.g. 2019
    :param age: the age of the player e.g. 22
    :param nationality: the nationality dict value of the player e.g. 34 (Netherlands)
    :param club: the name of the player's club e.g. Ajax
    :param user_input: whether or not the user should decide the rating assignment via prompt
    :param min_name_sim: the minimum name similarity threshold
    :param min_club_sim: the minimum club similarity threshold
    :return: the player's fifa overall rating, the player's fifa potential rating
    """

    season = str(season)
    opener = AppURLopener()
    names = player_name.split(" ")

    if age and nationality and club:
        club = club.lower()
        url = "https://sofifa.com/players?keyword=" \
              + replace_all(names[len(names) - 1], '+', ' ') \
              + "&r={}&set=true".format(seasons[int(season)]) \
              + "&na%5B%5D={}".format(nationality) \
              + "&ael={}&aeh={}".format(int(age) - 1, int(age) + 1)
    else:
        url = "https://sofifa.com/players?keyword=" \
              + replace_all(names[len(names) - 1], '+', ' ') \
              + "&r={}&set=true".format(seasons[int(season)])

    html_code = str(opener.open(url).read())
    soup = BeautifulSoup(html_code, 'html.parser')

    print(url)

    query = soup.find_all(lambda tag: tag.name == "tr"
                                      and not tag.attrs)

    best_name_similarity = min_name_sim
    best_club_similarity = min_club_sim
    final_overall_rating = 'NA'
    final_potential_rating = 'NA'

    for result in query:
        name_similarity = 0
        club_similarity = 0
        overall_rating = 'NA'
        potential_rating = 'NA'

        soup = BeautifulSoup(str(result), 'html.parser')
        rows = soup.find_all(lambda tag: tag.name == "td")
        values = soup.find_all(lambda tag: tag.name == "a")

        for value in values:
            try:
                name = value['data-tooltip']
                name = strip_accents(str.encode(name).decode('unicode_escape'))
                player_name_to_check = str(name).lower().strip()
                name_similarity = similar(player_name_to_check, player_name.strip())

                soup = BeautifulSoup(str(value), 'html.parser')
                second_name = soup.find('div', attrs={'class': 'bp3-text-overflow-ellipsis'})
                second_name = strip_accents(str.encode(second_name.text).decode('unicode_escape'))
                second_player_name_to_check = str(second_name).lower().strip()
                second_name_similarity = similar(second_player_name_to_check, player_name.strip())

                if second_name_similarity > name_similarity:
                    name_similarity = second_name_similarity

                print(player_name + ":", name, '-', "String similarity:",
                      name_similarity)
                break
            except KeyError:
                pass

        if club is not None:
            for value in values[1:]:
                try:
                    value.attrs['rel']
                except KeyError or TypeError:
                    team = str(value.text).lower()
                    team_to_compare = strip_accents(str.encode(team).decode('unicode_escape'))
                    club_similarity = similar(team_to_compare, club)
                    print(team_to_compare + ":", team, '-', "String similarity:",
                          club_similarity)
                    break

        for row in rows:
            try:
                data_title = row['data-col']
                if data_title == "oa":
                    rating_query = BeautifulSoup(str(row), 'html.parser')
                    rating = rating_query.find(lambda tag: tag.name == "span")
                    overall_rating = int(rating.text)
                    print('OVR:', overall_rating)
                elif data_title == "pt":
                    rating_query = BeautifulSoup(str(row), 'html.parser')
                    rating = rating_query.find(lambda tag: tag.name == "span")
                    potential_rating = int(rating.text)
                    print('POT:', potential_rating)
            except KeyError:
                pass

        if user_input \
                and input('Do you override the old rating with this rating?') \
                .lower().__contains__('yes'):
            best_name_similarity = name_similarity
            best_club_similarity = club_similarity
            final_overall_rating = overall_rating
            final_potential_rating = potential_rating
        elif not user_input and name_similarity == best_name_similarity:
            if club_similarity > best_club_similarity:
                best_club_similarity = club_similarity
                final_overall_rating = overall_rating
                final_potential_rating = potential_rating
        elif not user_input and name_similarity > best_name_similarity:
            best_name_similarity = name_similarity
            best_club_similarity = club_similarity
            final_overall_rating = overall_rating
            final_potential_rating = potential_rating
        elif not user_input \
                and (best_name_similarity == 0.75 or name_similarity > 0.65) \
                and club_similarity > 0.63:
            best_club_similarity = club_similarity
            final_overall_rating = overall_rating
            final_potential_rating = potential_rating
        print('\n')

    if user_input and final_overall_rating != 'NA' and not input(
            'Do you want to finalize results_market_value?').lower().__contains__('yes'):
        final_overall_rating = 'NA'
        final_potential_rating = 'NA'
    print('Final OVR:', final_overall_rating, 'Final POT:', final_potential_rating)
    print('------------------------------------------------------')
    return final_overall_rating, final_potential_rating
