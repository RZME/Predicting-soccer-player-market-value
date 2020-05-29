import re
import urllib
from urllib import request
from difflib import SequenceMatcher

import unicodedata

tiers = {'primera division': 1,
         'segunda division': 2,
         'ligue 1': 1,
         'premier league': 1,
         'serie a': 1,
         'eredivisie': 1,
         '1 bundesliga': 1,
         '2 bundesliga': 2,
         'superliga': 1,
         'campeonato brasileiro serie a': 1,
         'championship': 2,
         'egyptian premier league': 1,
         'allsvenskan': 1,
         'major league soccer': 1,
         'scottish championship': 1,
         'ekstraklasa': 1
         }

seasons = {2007: "070002",
           2008: "080002",
           2009: "090002",
           2010: "100002",
           2011: "110002",
           2012: "120002",
           2013: "130034",
           2014: "140052",
           2015: "150059",
           2016: "160058",
           2017: "170099",
           2018: "180084",
           2019: "190075",
           2020: "200043"}

nationalities = {'albania': 1,
                 'algeria': 97,
                 'andorra': 2,
                 'angola': 98,
                 'argentina': 52,
                 'armenia': 3,
                 'australia': 195,
                 'austria': 4,
                 'azerbaijan': 5,
                 'barbados': 66,
                 'belarus': 6,
                 'belgium': 7,
                 'benin': 99,
                 'bermuda': 68,
                 'bolivia': 53,
                 'brazil': 54,
                 'bulgaria': 9,
                 'burkina faso': 101,
                 'burundi': 102,
                 'cameroon': 103,
                 'canada': 70,
                 'cape verde': 104,
                 'central african rep.': 105,
                 'chad': 106,
                 'chile': 55,
                 'china pr': 155,
                 'colombia': 56,
                 'congo': 107,
                 'costa rica': 72,
                 'croatia': 10,
                 'cuba': 73,
                 'curacao': 85,
                 'cyprus': 11,
                 'czech republic': 12,
                 'dr congo': 110,
                 'denmark': 13,
                 'ecuador': 57,
                 'egypt': 111,
                 'england': 14,
                 'estonia': 208,
                 'ethiopia': 114,
                 'faroe islands': 16,
                 'finland': 17,
                 'france': 18,
                 'gabon': 115,
                 'gambia': 116,
                 'georgia': 20,
                 'germany': 21,
                 'ghana': 117,
                 'greece': 22,
                 'grenada': 77,
                 'guatemala': 78,
                 'guinea': 118,
                 'guinea bissau': 119,
                 'haiti': 80,
                 'honduras': 81,
                 'hungary': 23,
                 'iceland': 24,
                 'iran': 161,
                 'iraq': 162,
                 'israel': 26,
                 'italy': 27,
                 "cote d\'ivoire": 108,
                 'jamaica': 82,
                 'japan': 163,
                 'kazakhstan': 165,
                 'kenya': 120,
                 'korea dpr': 166,
                 'south korea': 167,
                 'latvia': 28,
                 'lebanon': 171,
                 'lesotho': 121,
                 'liberia': 122,
                 'liechtenstein': 29,
                 'lithuania': 30,
                 'luxembourg': 31,
                 'madagascar': 124,
                 'malawi': 125,
                 'mali': 126,
                 'malta': 32,
                 'mauritania': 127,
                 'mauritius': 128,
                 'mexico': 83,
                 'moldova': 33,
                 'montenegro': 15,
                 'morocco': 129,
                 'mozambique': 130,
                 'namibia': 131,
                 'netherlands': 34,
                 'new zealand': 198,
                 'nigeria': 133,
                 'north macedonia': 19,
                 'northern ireland': 35,
                 'norway': 36,
                 'oman': 178,
                 'pakistan': 179,
                 'panama': 87,
                 'paraguay': 58,
                 'peru': 59,
                 'poland': 37,
                 'portugal': 38,
                 'qatar': 182,
                 'ireland': 25,
                 'rest of world': 211,
                 'romania': 39,
                 'russia': 40,
                 'rwanda': 134,
                 'scotland': 42,
                 'senegal': 136,
                 'serbia': 51,
                 'sierra leone': 138,
                 'slovakia': 43,
                 'slovenia': 44,
                 'somalia': 139,
                 'south africa': 140,
                 'spain': 45,
                 'st kitts nevis': 89,
                 'st vincent grenadine': 91,
                 'suriname': 92,
                 'sweden': 46,
                 'switzerland': 47,
                 'syria': 186,
                 'togo': 144,
                 'tunisia': 145,
                 'turkey': 48,
                 'uganda': 146,
                 'ukraine': 49,
                 'united states': 95,
                 'uruguay': 60,
                 'venezuela': 61,
                 'wales': 50,
                 'zambia': 147,
                 'zimbabwe': 148}

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.1916.47 Safari/537.36'
}


def get_data():
    values = {'name': 'Michael Foord',
              'location': 'Northampton',
              'language': 'Python'}

    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')
    return data


def clean_date(date_as_string):
    total_days = 0

    while date_as_string.__contains__('Years') or date_as_string.__contains__('Months'):
        if date_as_string.__contains__('Years'):
            years = "".join(re.findall('\\d.{,3}Years', date_as_string)).strip()
            years = years.replace('Years', '')
            years = int(years)

            total_days += years * 365

            date_as_string = date_as_string[date_as_string.index('Years') + 5:]

        elif date_as_string.__contains__('Months'):
            months = "".join(re.findall('\\d.{,3}Months', date_as_string)).strip()
            months = months.replace('Months', '')
            months = int(months)

            total_days += months * 31

            date_as_string = date_as_string[date_as_string.index('Months') + 6:]

    days = "".join(re.findall('\\d.{,3}Days', date_as_string)).strip()
    days = days.replace('Days', '')
    days = int(days)

    total_days += days

    return total_days


def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError:  # unicode is a default on python 3
        pass

    text = unicodedata.normalize('NFD', text) \
        .encode('ascii', 'ignore') \
        .decode("utf-8")

    return str(text)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def replace_all(string, replacement, replace, lower=False):
    if lower:
        string = string.lower().strip()
    while string.__contains__(replace):
        string = string.replace(replace, replacement)
    return string


class AppURLopener(request.FancyURLopener):
    version = "Mozilla/5.0"


def beautify_data(data):
    squad_appearances = 0
    player_appearances = 1
    points_per_game = 2
    goals = 3
    assists = 4
    minutes_played = 5

    for league in data.keys():
        if data[league][player_appearances] != 0:
            print(league)
            print('----------------')
            print('Squad apps:', data[league][squad_appearances])
            print('Player apps:', data[league][player_appearances])
            print('Ratio apps:',
                  round(data[league][player_appearances] / data[league][0], 1))
            print('PPG:', data[league][points_per_game])
            print('Goals:', data[league][goals])
            print('AVG goals per app:',
                  round(data[league][goals] / data[league][player_appearances], 1))
            if data[league][goals] != 0:
                print('AVG minutes per goal:',
                      round(data[league][minutes_played] / data[league][goals], 1))
            print('Assists:', data[league][assists])
            print('AVG assists per app:',
                  round(data[league][assists] / data[league][player_appearances], 1))
            if data[league][assists] != 0:
                print('AVG minutes per assist:',
                      round(data[league][minutes_played] / data[league][assists], 1))
            print('Minutes played:', data[league][minutes_played])
            print('AVG minutes per game:',
                  round(data[league][minutes_played] / data[league][player_appearances]))
            print('----------------')
