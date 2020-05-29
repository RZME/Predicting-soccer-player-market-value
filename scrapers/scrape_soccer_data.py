import re
import urllib
from bs4 import BeautifulSoup
from scrapers.player_data.scrape_player_data import scrape_player_data
from scrapers.player_ratings.scrape_fifa_rating import scrape_fifa_rating
from scrapers.transfer_details.scrape_transfer_details import get_transfer_details
from scrapers.utils.utils import get_data, headers, replace_all, nationalities


def scrape_soccer_data(league_name: str, league_id: str, season: int):
    """
    Scrapes and combines soccer data from:
      - www.transfermarkt.co.uk
      - www.sofifa.com

    given
    :param league_name: the name of the league e.g. 1-bundesliga
    :param league_id: the id of the league e.g. L1
    :param season: the season e.g. 2019

    output: .csv
    
    """

    url = "https://www.transfermarkt.co.uk/" + league_name\
          + "/transfers/wettbewerb/" + league_id\
          + "/plus/?saison_id=" + str(season)\
          + "&s_w=&leihe=0&intern=0"

    req = urllib.request.Request(url, get_data(), headers=headers)
    html_code = str(urllib.request.urlopen(req).read())
    bs = BeautifulSoup(html_code, 'html.parser')

    f = open("soccer_data" + "\\" + league_name + '-' + str(season) + '.csv', 'w')
    f.write('club,'
            + 'club_league,'
            + 'club_league_tier,'
            + 'club_country,'
            + 'transfer_movement,'
            + 'player_name,'
            + 'player_age,'
            + 'player_nationality,'
            + 'player_club,'
            + 'player_club_country,'
            + 'player_position,'
            + 'player_position_category,'
            + 'player_rating,'
            + 'player_potential,'
            + 'club_involved,'
            + 'club_involved_league,'
            + 'club_involved_league_tier,'
            + 'club_involved_country,'
            + 'transfer_fee,'
            + 'market_value,'
            + 'remaining_contract_duration,'
            + 'total_apps,'
            + 'total_apps_ratio,'
            + 'total_minutes_per_point,'
            + 'total_goals,'
            + 'total_assists,'
            + 'total_minutes_played,'
            + 'ucl_apps,'
            + 'ucl_apps_ratio,'
            + 'ucl_minutes_per_point,'
            + 'ucl_goals,'
            + 'ucl_assists,'
            + 'ucl_minutes_played,'
            + 'el_apps,'
            + 'el_apps_ratio,'
            + 'el_minutes_per_point,'
            + 'el_goals,'
            + 'el_assists,'
            + 'el_minutes_played,'
            + 'season' + '\n')

    competition_profile_header = bs.find(attrs={'class': 'profilheader'})
    country_club_origin = str(competition_profile_header.img).lower()
    country_club_origin = country_club_origin[country_club_origin.index('title="') + len('title="'):]
    country_club_origin = country_club_origin[:country_club_origin.index('"')]

    boxes = bs.find_all(attrs={'class': 'box'})

    season = (int(season) - 1)
    # we want to check transfers of the given year but we want to check player data
    # from 1 season ago

    print(season)
    counter = 0

    for box in boxes:

        bs = BeautifulSoup(str(box), 'html.parser')

        club_origin = str(bs.find(attrs={'vereinprofil_tooltip'}))

        if club_origin.__contains__('href'):
            club_origin = club_origin[club_origin.index('href="/') + len('href="/'):]
            club_origin = club_origin[:club_origin.index('/')]
            club_origin = replace_all(club_origin, ' ', '-')

        tables = box.findAll(attrs={'class': 'responsive-table'})

        for table in tables:
            transfer_direction = str(table.find(attrs={'spieler-transfer-cell'}))

            if transfer_direction.__contains__('cell">'):
                transfer_direction = transfer_direction[transfer_direction.index('cell">') + 6:]
                transfer_direction = transfer_direction[:transfer_direction.index('<')].lower()

            rows = table.findAll(lambda tag: tag.name == 'tr')

            for row in rows:
                row = str(row)

                bs = BeautifulSoup(row, 'html.parser')
                player_profile = bs.find(attrs={'class': 'spielprofil_tooltip'})
                age = bs.find(attrs={'class': 'zentriert alter-transfer-cell'})
                nationality = bs.find(attrs={'class': 'flaggenrahmen'})
                position = bs.find(attrs={'class': 'kurzpos-transfer-cell zentriert'})
                club_involved = bs.find(attrs={'class': 'vereinprofil_tooltip'})
                market_value = bs.find(attrs={'class': 'rechts mw-transfer-cell'})
                country_club_involved = bs.find(attrs={'class': 'no-border-links verein-flagge-transfer-cell'})
                fee = False

                a_tags = bs.findAll(lambda tag: tag.name == 'a')

                for tag in a_tags:
                    tag_to_string = str(tag)
                    if tag_to_string.__contains__('jumplist'):
                        fee = tag
                        break

                if player_profile and age and nationality and position and club_involved and fee:
                    market_value = str(market_value.text)
                    fee = fee.text

                    if fee.__contains__("xa3"):
                        fee = fee[fee.index("xa3") + 3:]

                    if market_value.__contains__("xa3"):
                        market_value = market_value[market_value.index("xa3") + 3:]

                    market_value_cleaned = replace_all(market_value, '', 'm')
                    fee_cleaned = replace_all(fee, '', 'm')

                    if fee.__contains__('transfer') or fee.__contains__('?'):
                        fee_cleaned = 0

                    if market_value.__contains__('transfer') or market_value.__contains__('?'):
                        fee_cleaned = 0

                    if fee.__contains__('k'):
                        fee_cleaned = replace_all(fee, '', 'k')
                        fee_cleaned = float(fee_cleaned) / 1000
                    elif fee.__contains__('Th.'):
                        fee_cleaned = replace_all(fee, '', 'Th.')
                        fee_cleaned = float(fee_cleaned) / 1000

                    if market_value_cleaned.__contains__('Th.'):
                        print(market_value)
                        market_value_cleaned = replace_all(market_value, '', 'Th.')
                        market_value_cleaned = float(market_value_cleaned) / 1000
                    elif market_value_cleaned.__contains__('k'):
                        print(market_value)
                        market_value_cleaned = replace_all(market_value, '', 'k')
                        market_value_cleaned = float(market_value_cleaned) / 1000

                    try:
                        fee_cleaned = float(fee_cleaned)
                    except ValueError:
                        pass
                    except Exception:
                        pass

                    try:
                        market_value_cleaned = float(market_value_cleaned)
                    except ValueError:
                        pass
                    except Exception:
                        pass

                    if fee_cleaned == 0:
                        continue

                    counter += 1
                    fee_cleaned = str(fee_cleaned)
                    market_value_cleaned = str(market_value_cleaned)

                    transfer_link = row[row.index('/jumplist'):]
                    transfer_link = transfer_link[:transfer_link.index('"')].strip()

                    club_involved = str(club_involved.get('href'))

                    club_involved = club_involved[club_involved.index('/') + len('/'):]
                    club_involved = club_involved[:club_involved.index('/')]
                    club_involved = replace_all(club_involved, ' ', '-')

                    country_club_involved = str(country_club_involved.img)
                    country_club_involved = country_club_involved[
                                            country_club_involved.index('title="') + len('title="'):]
                    country_club_involved = country_club_involved[:country_club_involved.index('"')].lower()

                    if country_club_involved.__contains__('korea'):
                        country_club_involved = 'south korea'

                    name = player_profile.get('href')
                    pid = int("".join(re.findall('\\d', name)))

                    name = name[name.index('/') + len('/'):]
                    name = name[:name.index('/')]
                    name = replace_all(name, ' ', '-')

                    age = age.text
                    position = position.text

                    nationality = str(nationality.get('title')).lower()

                    if nationality.__contains__('korea'):
                        nationality = 'south korea'

                    data_values = scrape_player_data(name, pid, season)

                    squad_appearances = 0
                    player_appearances = 1
                    points_per_game = 2
                    goals = 3
                    assists = 4
                    minutes_played = 5

                    rem_contract, competitions, tiers = get_transfer_details(transfer_link)

                    player_club = club_involved if transfer_direction == 'in' else club_origin
                    player_club_country = country_club_involved if transfer_direction == 'in' else country_club_origin

                    try:

                        player_fifa_rating, player_fifa_potential_rating =\
                            scrape_fifa_rating(name, season + 1, age, nationalities[nationality], player_club)
                    except KeyError:
                        player_fifa_rating, player_fifa_potential_rating = 'NA', 'NA'

                    player_position_category = 'NA'

                    position = str(position)

                    if position.__contains__('B'):
                        player_position_category = 'defender'
                    elif position.__contains__('M'):
                        player_position_category = 'midfielder'
                    elif position.__contains__('F') or position.__contains__('W') or position.__contains__('S'):
                        player_position_category = 'attacker'
                    elif position.__contains__('K'):
                        player_position_category = 'keeper'

                    print(club_origin, '-',
                          competitions[1 if transfer_direction == 'in' else 0], '-',
                          'tier: ', tiers[0 if transfer_direction == 'in' else 1], '-',
                          country_club_origin, '-',
                          transfer_direction, '-',
                          name, '-',
                          age, '-',
                          nationality, '-',
                          player_club, '-',
                          player_club_country, '-',
                          position, '-',
                          player_position_category, '-',
                          'R: ' + str(player_fifa_rating), '-',
                          'P: ' + str(player_fifa_potential_rating), '-',
                          club_involved, '-',
                          competitions[0 if transfer_direction == 'in' else 1], '-',
                          'Tier: ', tiers[1 if transfer_direction == 'in' else 0], '-',
                          country_club_involved, '-',
                          fee_cleaned + 'm', '-',
                          market_value_cleaned + 'm', '-',
                          rem_contract, 'days', '-',
                          'all:', data_values['TOTAL'], '-',
                          'cl:', data_values['CL'], '-',
                          'el:', data_values['EL'])

                    print('--------')

                    total_player_app = data_values['TOTAL'][player_appearances]
                    cl_player_app = data_values['CL'][player_appearances]
                    el_player_app = data_values['EL'][player_appearances]

                    f.write(str(club_origin) + ','
                            + str(competitions[1 if transfer_direction == 'in' else 0]) + ','
                            + str(tiers[0 if transfer_direction == 'in' else 1]) + ','
                            + str(country_club_origin) + ','
                            + str(transfer_direction) + ','
                            + str(name) + ','
                            + str(age) + ','
                            + str(nationality) + ','
                            + str(player_club) + ','
                            + str(player_club_country) + ','
                            + str(position) + ','
                            + str(player_position_category) + ','
                            + str(player_fifa_rating) + ','
                            + str(player_fifa_potential_rating) + ','
                            + str(club_involved) + ','
                            + str(competitions[0 if transfer_direction == 'in' else 1]) + ','
                            + str(tiers[1 if transfer_direction == 'in' else 0]) + ','
                            + str(country_club_involved) + ','
                            + str(fee_cleaned) + ','
                            + str(market_value_cleaned) + ','
                            + str(rem_contract) + ','
                            + str(data_values['TOTAL'][player_appearances]) + ','
                            + str(0 if total_player_app == 0
                                  else round(total_player_app / data_values['TOTAL'][squad_appearances], 2)) + ','
                            + str(data_values['TOTAL'][points_per_game]) + ','
                            + str(data_values['TOTAL'][goals]) + ','
                            + str(data_values['TOTAL'][assists]) + ','
                            + str(data_values['TOTAL'][minutes_played]) + ','
                            + str(data_values['CL'][player_appearances]) + ','
                            + str(0 if cl_player_app == 0
                                  else round(cl_player_app / data_values['CL'][squad_appearances], 2)) + ','
                            + str(data_values['CL'][points_per_game]) + ','
                            + str(data_values['CL'][goals]) + ','
                            + str(data_values['CL'][assists]) + ','
                            + str(data_values['CL'][minutes_played]) + ','
                            + str(data_values['EL'][player_appearances]) + ','
                            + str(0 if el_player_app == 0
                                  else round(el_player_app / data_values['EL'][squad_appearances], 2)) + ','
                            + str(data_values['EL'][points_per_game]) + ','
                            + str(data_values['EL'][goals]) + ','
                            + str(data_values['EL'][assists]) + ','
                            + str(data_values['EL'][minutes_played]) + ','
                            + str(int(season) + 1) + '/' + str(int(season) + 2)
                            + '\n')

    f.close()
