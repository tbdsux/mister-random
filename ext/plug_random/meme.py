import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver

# class Gagger:
#     gag_website = "https://bit.ly/ShuffleNav"
#
#     @staticmethod
#     def get_gag():
#         chrome_options = webdriver.ChromeOptions()
#         chrome_options.add_argument('--disable-gpu')
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.binary_location = os.getenv("GOOGLE_CHROME_PATH")
#
#         browser = webdriver.Chrome(executable_path=os.getenv("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
#
#         browser.get(Gagger.gag_website)
#         source = browser.page_source
#         browser.close()
#
#         soup = BeautifulSoup(source, "html.parser")
#         try:
#             container = soup.find("div", class_="post-container")
#
#             meme = ""
#             try:
#                 meme = container.find("source")["src"]
#             except Exception:
#                 meme = container.find("source")["srcset"]
#
#             return meme
#         except Exception:
#             Gagger.get_gag()


class Meme:
    api_url = "https://meme-api.herokuapp.com/gimme"

    @staticmethod
    def get_meme():
        return requests.get(Meme.api_url).json()['url']
