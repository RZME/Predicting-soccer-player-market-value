import re
import urllib
from bs4 import BeautifulSoup
from scrapers.utils.utils import headers, get_data, replace_all, clean_date


def get_transfer_details(transfer_link: str):
    """
    gets the transfer details

    given
    :param transfer_link: the transfermarkt's transfer detail link

    :return: remaining contract duration,
             competition list of both clubs involved,
             competition tier list of both clubs involved
    """
    tier_dict = {'First': 1, 'Second': 2, 'Third': 3, 'Fourth': 4, 'Fifth': 5, 'Play-Offs': 6, '': 'NA'}

    url = "https://www.transfermarkt.co.uk" + transfer_link
    req = urllib.request.Request(url, get_data(), headers=headers)

    html_code = str(urllib.request.urlopen(req).read())
    bs = BeautifulSoup(html_code, 'html.parser')
    rows = bs.find_all(lambda tag: tag.name == 'tr', attrs={'class': None})

    competitions = []
    remaining_contract = 0
    tiers = []

    for row in rows:
        row_to_string = str(row)

        if row_to_string.__contains__('Competition'):

            b = BeautifulSoup(row_to_string, 'html.parser')

            for competition in b.find_all(lambda tag: tag.name == 'td'):
                if competition.text != 'Competition':
                    b = BeautifulSoup(str(competition), 'html.parser')
                    if b.find('a'):
                        competition = competition.a

                    if competition.get('href'):
                        competition = str(competition.get('href'))

                        competition = competition[competition.index('/') + len('/'):]
                        competition = competition[:competition.index('/')]
                        competition = replace_all(competition, ' ', '-')
                    else:
                        competition = 'NA'

                    competitions.append(competition)

        elif row_to_string.__contains__('Remaining'):

            remaining_contract = row_to_string[row_to_string.index('Remaining'):]

            remaining_contract = \
                remaining_contract[re.search('\\d.{,3}(Years|Days|Months)', remaining_contract).start():].strip()

            remaining_contract = remaining_contract[:remaining_contract.index("Days") + len('Days')].strip()

            remaining_contract = clean_date(remaining_contract)

        elif row_to_string.__contains__('League type'):

            tier_team_1 = row_to_string[
                          re.search('(First|Second|Third|Fourth|Fifth).?(Tier)|(Play-Offs)',
                                    row_to_string).start():].strip()

            tier_team_2 = tier_team_1[tier_team_1.index('Tier') + len('Tier'):].strip()

            if tier_team_1.__contains__('Play-Offs'):
                t = tier_team_1[:tier_team_1.index('Play-Offs')].strip()
                if not t.__contains__('Tier'):
                    tier_team_1 = tier_dict[tier_team_1[:tier_team_1.index('Play-Offs')].strip()]
                else:
                    tier_team_1 = tier_dict[t[:t.index('Tier')].strip()]
            else:
                tier_team_1 = tier_dict[tier_team_1[:tier_team_1.index('Tier')].strip()]

            if not re.search('(First|Second|Third|Fourth|Fifth).?(Tier)|(Play-Offs)', tier_team_2):
                tier_team_2 = 'NA'
            else:
                tier_team_2 = tier_team_2[
                              re.search('(First|Second|Third|Fourth|Fifth).?(Tier)|(Play-Offs)', tier_team_2).start():]

                if tier_team_2.__contains__('Play-Offs'):
                    tier_team_2 = tier_dict[tier_team_2[:tier_team_2.index('Play-Offs')].strip()]
                else:
                    tier_team_2 = tier_dict[tier_team_2[:tier_team_2.index('Tier')].strip()]

            tiers.append(tier_team_2)
            tiers.append(tier_team_1)

    return remaining_contract, competitions, tiers
