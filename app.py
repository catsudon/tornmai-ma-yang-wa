from cmath import nan
import logging
import logging.handlers
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
from scraper.MAL import mal
from scraper.bilibili import bilibili
from scraper.illegal import get_latest_episode

if(not os.getenv("GITHUB_ACTIONS")):
    from dotenv import load_dotenv
    load_dotenv()

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
animelist = animelist.fillna("-")


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
    logger.info(f'🔔: {name} {episode} ;{r.text}')



for i in range(animelist.shape[0]):
    anime = animelist.loc[i]
    print("-- "*8,"\n",anime.values,"\n","-- "*8)

    name, latest_episode, bilibili_scheme, pirate = anime.values
    fetched_episode = 0
    if bilibili_scheme not in ['-', '']:
        fetched_episode = bilibili(
            f"https://www.bilibili.tv/th/play{bilibili_scheme}")
    else:
        fetched_episode = get_latest_episode("https://animekimi.com/anime/tokyo-revengers-seiya-kessen-hen/")

    print(name, fetched_episode)
    logger.info(f'🤖: {name} {fetched_episode}')

    if fetched_episode > latest_episode:
        notify(name, fetched_episode)
        animelist.loc[i] = [name, fetched_episode, bilibili_scheme, pirate]

animelist.to_csv('./animelist.csv', index=False)
