from cmath import nan
import logging
import logging.handlers
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
from scraper.MAL import mal
# from dotenv import load_dotenv
# load_dotenv()

try:
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
except KeyError:
    ACEESS_TOKEN = "Token not available!"

try:
    ROOM_ID = os.environ["ROOM_ID"]
except KeyError:
    ROOM_ID = "Room ID not available!"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

animelist = pd.read_csv('animelist.csv')
animelist = animelist


def notify(name, episode):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {'content-type': 'application/json',
               'Authorization': f'Bearer {ACCESS_TOKEN}'}
    msg = f'『{name}』の第{episode}話が放送されました!🎉'
    data = {
        "to": ROOM_ID,
        "messages": [
            {
                "type": "text",
                "text": msg
            }
        ]
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(r.text)
    logger.info(f'{name} {episode} ;{r.text}')


# get watching anime
def get_watching_anime():
    url = "https://myanimelist.net/animelist/markmarker?status=1"
    r = requests.get(url, headers={
                     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    souped = BeautifulSoup(r.text, 'html.parser')
    table = souped.find_all('table', class_="list-table")
    data = json.loads(table[0]['data-items'])
    watching_list = []
    for i in data:
        scheme = i['anime_url']
        anime_url = f'https://myanimelist.net{scheme}/episode'
        episode, name = mal(anime_url)
        watching_list.append((scheme, episode, name))

    return watching_list


watching_list = get_watching_anime()
# watching_list = [('/anime/47917/Bocchi_the_Rock', 10, '\nぼっち・ざ・ろっく！\n  '), ('/anime/44511/Chainsaw_Man', 10, '\nチェンソーマン\n  '), ('/anime/37520/Dororo', 24, '\nどろろ\n  '), ('/anime/49220/Isekai_Ojisan', 6, '\n異世界おじさん\n  '), ('/anime/50602/Spy_x_Family_Part_2', 11, '\nSPY×FAMILY\n  ')]
print(watching_list)

for scheme, latest_episode, name in watching_list:
    a = animelist.loc[animelist['scheme'] == scheme]
    found_in_local = len(a)
    if found_in_local:
        if (latest_episode > int(a['episode'])):
            animelist.loc[animelist['scheme'] ==
                          scheme, 'episode'] = latest_episode
            notify(name, latest_episode)
    else:
        animelist.loc[len(animelist.index)] = [scheme, latest_episode]
        notify(name, latest_episode)

animelist.to_csv('./animelist.csv', index=False)
