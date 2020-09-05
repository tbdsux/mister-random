import random
import requests
from bs4 import BeautifulSoup


class Quotes:
    quotes_website = "http://www.quotationspage.com/random.php"

    @staticmethod
    def get_random_quote():
        resp = BeautifulSoup(requests.get(Quotes.quotes_website).text, "html.parser")

        quotes = [i.find("a").text for i in resp.find_all("dt", class_="quote")]
        authors = [
            [j.text for j in i.find_all("a") if j["href"].startswith("/quotes/")]
            for i in resp.find_all("dd", class_="author")
        ]
        ran = random.randint(0, len(quotes) - 1)

        return quotes[ran], str(authors[ran]).replace("['", "").replace("']", "")
