import requests

class Meme:
    api_url = "https://meme-api.herokuapp.com/gimme"

    @staticmethod
    def get_meme():
        return requests.get(Meme.api_url).json()['url']
