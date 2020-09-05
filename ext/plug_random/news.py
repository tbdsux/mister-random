import random
import requests
import os


class News:
    website = "http://newsapi.org/v2/top-headlines?country=ph&apiKey=" + os.getenv("NEWS_API")

    @staticmethod
    def get_random_news():
        news = random.choice(requests.get(News.website).json()["articles"])
        return news["title"], news["url"]
