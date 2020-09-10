import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = os.getenv("GOOGLE_CHROME_PATH")
browser = webdriver.Chrome(execution_path=os.getenv("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


class Gagger:
    gag_website = "https://bit.ly/ShuffleNav"

    @staticmethod
    def get_gag():
        browser.get(Gagger.gag_website)
        source = browser.page_source
        browser.close()
        soup = BeautifulSoup(source, "html.parser")
        container = soup.find("div", class_="post-container")

        meme = ""
        try:
            meme = container.find("source")["src"]
        except Exception:
            meme = container.find("source")["srcset"]

        return meme


class Meme:
    api_url = "https://meme-api.herokuapp.com/gimme"

    @staticmethod
    def get_meme():
        return requests.get(Meme.api_url).json()['url']
