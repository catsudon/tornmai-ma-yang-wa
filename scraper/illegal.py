import requests
from bs4 import BeautifulSoup
import logging
import logging.handlers


def animekimi(url): 
    r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    souped =  BeautifulSoup(r.text, 'html.parser')
    a = souped.find_all('div', class_='episodiotitle')
    latest_episode = len(a)

    return latest_episode

def animemasters(url): 
    r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    souped =  BeautifulSoup(r.text, 'html.parser')
    a = souped.find_all('td', class_='text-center')
    latest_episode = len(a)

    return latest_episode

def animeshiro(url):
    r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    souped =  BeautifulSoup(r.text, 'html.parser')
    a = souped.find_all('a', class_='widget-list-item')
    latest_episode = len(a)

    return latest_episode

def get_latest_episode(url):
    r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    souped =  BeautifulSoup(r.text, 'html.parser')
    a = souped.find_all('a', class_='widget-list-item')
    b = souped.find_all('td', class_='text-center')
    c = souped.find_all('div', class_='episodiotitle')
    latest_episode = len(max((a,b,c), key=len))

    return latest_episode

# debugger
if __name__ == '__main__':
    print(get_latest_episode("https://www.anime-masters.com/isekai-ojisan/"))