import requests
from bs4 import BeautifulSoup
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

def netflix(url):
    r = requests.get(url)
    souped =  BeautifulSoup(r.text, 'html.parser')
    logger.info(souped)
    a = souped.find_all('h3', class_='episode-title')
    latest_episode = len(a)

    return latest_episode

# debugger
if __name__ == '__main__':
    print(netflix("https://www.netflix.com/th/title/81499847"))