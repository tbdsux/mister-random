from dotenv import load_dotenv
import os
import random

load_dotenv()  # load .env file

import requests
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
