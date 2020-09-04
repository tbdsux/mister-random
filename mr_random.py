from dotenv import load_dotenv
import os

load_dotenv()  # load .env file

import discord
from getter import News, Youtube, COVID19, Quotes
from datetime import date

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
        
        if message.content == ">>covid19":
            confirmed, active, recovered, deaths, severe, fatality = COVID19.get_covid19()

            embed = discord.Embed(
                title = "Covid 19 | PH Data",
                description= "This is the current summary of the COVID-19 Cases in the Philippines\nAs of " + date.today().strftime("%B %d, %Y"),
                colour = discord.Colour.blue()
            )
            embed.add_field(name="Confirmed Cases", value="{:,}".format(confirmed), inline=True)
            embed.add_field(name="Active Cases", value="{:,}".format(active), inline=True)
            embed.add_field(name="Recovered", value="{:,}".format(recovered), inline=True)
            embed.add_field(name="Death Cases", value="{:,}".format(deaths), inline=True)
            embed.add_field(name="Severe Cases", value="{:,}".format(severe), inline=True)
            embed.add_field(name="Fatality Rate", value=str(fatality) + "%", inline=True)
            embed.set_footer(text="covid19ph-api.herokuapp.com")

            await message.channel.send(embed=embed)

        if message.content.startswith("random video "):
            video = Youtube.get_random_vid(message.content.replace("random video ", ""))
            await message.channel.send(video)

        if message.content == "random quote":
            quote, author = Quotes.get_random_quote()
            
            embed = discord.Embed(title='"' + quote + '"', description="- " + author)
            embed.set_thumbnail(url="http://www.quotationspage.com/tag3.gif")
            embed.set_footer(text="www.quotationspage.com")
            
            await message.channel.send(embed=embed)


client = MyClient()
client.run(os.getenv("MR_RANDOM_TOKEN"))
