import requests
from bs4 import BeautifulSoup

def mal(url):
    r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    souped =  BeautifulSoup(r.text, 'html.parser')
    ep_list = souped.find_all('a', class_="js-episode-vote-button")
    return (len(ep_list), getName(souped))


def getName(souped):
    for elem in souped.find_all('div', class_="spaceit_pad"):
        if "Japanese" in elem.text:
            print(elem.text)
            return elem.text.replace("Japanese: ", "").replace("\n", "").strip()



# debugger
if __name__ == '__main__':
    # print(getName("https://myanimelist.net/anime/47917/Bocchi_the_Rock/episode"))
    print(mal("https://myanimelist.net/anime/47917/Bocchi_the_Rock/episode"))