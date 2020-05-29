import re
import urllib
from bs4 import BeautifulSoup
from scrapers.utils.utils import get_data, headers, replace_all


def scrape_player_data(player_name: str, pid: int, season: int) -> dict:
    """
    Scrapes total season, Champions League and Europa League player performance statistics

    given
    :param player_name: the name of the player e.g. Frenkie de Jong
    :param pid: the transfermarkt's player id of the player e.g. 1784234
    :param season: season: the season e.g. 2019
    :return:
    """
    season = str(season)

    total_stats_url = "https://www.transfermarkt.co.uk/" \
                      + replace_all(player_name, '-', ' ') \
                      + "/leistungsdatendetails/spieler/" + str(pid) \
                      + "/plus/1?saison=" + season\
                      + "&verein=&liga=&wettbewerb=&pos=&trainer_id="

    cl_stats_url = "https://www.transfermarkt.co.uk/" \
                   + replace_all(player_name, '-', ' ') \
                   + "/leistungsdatendetails/spieler/" + str(pid)\
                   + "/plus/1?saison=" + season\
                   + "&verein=&liga=&wettbewerb=CL&pos=&trainer_id="

    el_stats_url = "https://www.transfermarkt.co.uk/"\
                   + replace_all(player_name, '-', ' ')\
                   + "/leistungsdatendetails/spieler/" + str(pid)\
                   + "/plus/1?saison=" + season\
                   + "&verein=&liga=&wettbewerb=EL&pos=&trainer_id="

    urls = {'TOTAL': total_stats_url, 'CL': cl_stats_url, 'EL': el_stats_url}
    data_values = {}

    for url in urls.keys():
        req = urllib.request.Request(urls[url], get_data(), headers=headers)
        html_code = str(urllib.request.urlopen(req).read())
        values = []

        if html_code.__contains__('</tfoot>'):
            table_foot = html_code[html_code.index('<tfoot>'):html_code.index('</tfoot>')]
            bs = BeautifulSoup(table_foot, 'html.parser')

            query_all = bs.find_all(attrs={"class": "zentriert"})
            query_time = bs.find_all(attrs={"class": "rechts"})

            for x in query_all:
                if not x.text.__contains__("/"):
                    if "".join(re.findall("\\d", x.text)) != "":
                        if x.text.__contains__(","):
                            st = x.text.replace(",", ".")
                            values.append(float(st))
                        else:
                            values.append(float(x.text))
                    elif x.text.__contains__("-"):
                        values.append(0)
                if values.__len__() >= 5:
                    break

            if query_time:
                query_time_to_string = str(query_time[2 if query_time.__len__() >= 3 else 1].text)
                if re.match('\\d', query_time_to_string):
                    query_time_to_string = int("".join(re.findall('\\d', query_time_to_string)))
                else:
                    query_time_to_string = 0
                values.append(query_time_to_string)
            else:
                values.append(0)

        if values.__len__() == 0:
            for zero in range(0, 6):
                values.append(0)

        data_values[url] = values

    return data_values
