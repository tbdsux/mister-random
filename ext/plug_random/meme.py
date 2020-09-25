import requests
import os
import random
from bs4 import BeautifulSoup

class Meme:
    api_url = "https://meme-api.herokuapp.com/gimme"

    @staticmethod
    def get_meme():
        return requests.get(Meme.api_url).json()['url']

class Giphy:
    api_url = "https://api.giphy.com/v1/gifs/random?api_key="+ os.getenv("GIPHY_KEY") +"&tag=meme&rating=g"

    @staticmethod
    def get_gif():
        return requests.get(Giphy.api_url).json()['data']['image_url']

class GifVif:
    website = "https://www.gif-vif.com/random/"

    @staticmethod
    def get_gif():
        soup = BeautifulSoup(requests.get(GifVif.website).text, 'html.parser')
        memes = soup.find_all("div", class_="left_new_gl_mob")

        m = random.choice(memes)
        try:
            meme = m.find("img")
        except Exception:
            meme = m.find("video")

        return meme['src']