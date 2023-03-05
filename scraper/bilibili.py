import requests
from bs4 import BeautifulSoup

def bilibili(url):
    r = requests.get(url)
    souped =  BeautifulSoup(r.text, 'html.parser')
    a = souped.find_all('a', class_='ep-item__reference')
    latest_episode = len(a)
    for i in a:
        if('PV' in i.text):
            latest_episode-=1

    try:
        a = souped.find_all('li', class_='section-bar__item')
        l = a[-1].text[::-1]
        s = ""
        for i in l:
            if(i.isdigit()):
                s+=i
            else: break
        
        latest_episode = max(latest_episode, int(s[::-1]))
    except Exception: pass

    return latest_episode

# debugger
if __name__ == '__main__':
    print(bilibili("https://www.bilibili.tv/th/play/2069747"))