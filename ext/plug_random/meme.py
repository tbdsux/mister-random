import requests
import os
import random

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