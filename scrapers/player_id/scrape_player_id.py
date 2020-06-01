import re
import urllib
from bs4 import BeautifulSoup
from scrapers.utils.utils import get_data, headers, replace_all


def get_pid(player_name: str) -> int:
    """

    gets the player id on www.transfermarkt.co.uk

    given
    :param player_name: the name of the player e.g. Frenkie de Jong
    :return:

    """
    url = "https://www.transfermarkt.co.uk/schnellsuche/ergebnis/schnellsuche?query=" \
                 + replace_all(player_name, "+", ' ')
    req = urllib.request.Request(url, get_data(), headers=headers)
    html_code = str(urllib.request.urlopen(req).read())
    soup = BeautifulSoup(html_code, 'html.parser')
    query = soup.find_all(attrs={"class": "inline-table"})

    for result in query:
        soup = BeautifulSoup(str(result), 'html.parser')

        if soup.find(attrs={'spielprofil_tooltip'})\
                and (soup.find(attrs={'vereinprofil_tooltip'})
                     or soup.find(attrs={'title': 'Retired'})):

            name = soup.find(attrs={'spielprofil_tooltip'})
            pid = int("".join(re.findall("\\d", name.get('href'))))

            return pid
