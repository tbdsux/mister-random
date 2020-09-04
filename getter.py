from dotenv import load_dotenv
import os
import random

load_dotenv()  # load .env file

import requests
from bs4 import BeautifulSoup
import googleapiclient.discovery


class News:
    website = "http://newsapi.org/v2/top-headlines?country=ph&apiKey=" + os.getenv("NEWS_API")

    @staticmethod
    def get_random_news():
        news = random.choice(requests.get(News.website).json()["articles"])
        return news["title"], news["url"]


class Youtube:
    youtube_base = "https://www.youtube.com/watch?v="

    @staticmethod
    def get_random_vid(query):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = os.getenv("GOOGLE_DEVELOPER_KEY")

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY
        )

        request = youtube.search().list(maxResults=30, q=query, part="snippet")
        response = request.execute()

        video = random.choice(response["items"])["id"]

        return Youtube.youtube_base + video["videoId"]


class COVID19:
    api_url = "http://covid19ph-api.herokuapp.com/api/cases/all"

    @staticmethod
    def get_covid19():
        resp = requests.get(COVID19.api_url).json()["cases"]
        return resp["confirmed"], resp["active"], resp["recovered"], resp["deaths"], resp["severe"], resp["fatality_rate"]


class Quotes:
    quotes_website = "http://www.quotationspage.com/random.php"

    @staticmethod
    def get_random_quote():
        resp = BeautifulSoup(requests.get(Quotes.quotes_website).text, "html.parser")

        quotes = [i.find("a").text for i in resp.find_all("dt", class_="quote")]
        authors = [[j.text for j in i.find_all("a") if j["href"].startswith("/quotes/")] for i in resp.find_all("dd", class_="author")]
        ran = random.randint(0, len(quotes)-1)

        return quotes[ran], str(authors[ran]).replace("['", "").replace("']", "")


