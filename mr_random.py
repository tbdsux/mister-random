from dotenv import load_dotenv
import os

load_dotenv()  # load .env file

import discord
from getter import News, Youtube


class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged on as", self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == "random news":
            news_title, news_url = News.get_random_news()
            await message.channel.send(news_title)
            await message.channel.send(news_url)

        if message.content == "random video":
            embed = discord.Embed(
                title="Mr. Random | video",
                description="Use: `random video {query}`",
                colour=discord.Colour.green(),
            )
            await message.channel.send(embed=embed)

        if message.content.startswith("random video "):
            video = Youtube.get_random_vid(message.content.replace("random video ", ""))
            await message.channel.send(video)


client = MyClient()
client.run(os.getenv("MR_RANDOM_TOKEN"))
