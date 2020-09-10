import discord
from discord.ext import commands

from .plug_random.youtube import Youtube
from .plug_random.quote import Quotes
from .plug_random.news import News
from .plug_random.meme import Meme

import pymongo, os

client = pymongo.MongoClient(os.getenv("MONGO_DB").replace('"', "").replace('"', ""))

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = client["RandomCommands"]
        self.collection = ""

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    # Get a RANDOM Video from 'query'
    @commands.command(name="video")
    @commands.guild_only()
    async def random_video(self, ctx, *, query):
        video = Youtube.get_random_vid(query)
        # Send a Random Youtube Video basing from the query
        await ctx.send(video)

    # Get a RANDOM Quote
    @commands.command(name="quote")
    @commands.guild_only()
    async def random_quote(self, ctx):
        quote, author = Quotes.get_random_quote()

        embed = discord.Embed(title=author, description='"' + quote + '"')
        embed.set_thumbnail(url="http://www.quotationspage.com/tag3.gif")
        embed.set_footer(text="www.quotationspage.com")

        await ctx.send(embed=embed)

    # Get a RANDOM News
    @commands.command(name="news")
    @commands.guild_only()
    async def random_news(self, ctx):
        news_title, news_url = News.get_random_news()
        await ctx.send(news_title)
        await ctx.send(news_url)

    # Get a RANDOM Meme from Reddit
    @commands.command(name="meme")
    @commands.guild_only()
    async def random_meme(self, ctx):
        self.collection = self.db[str(ctx.guild.id)]

        meme = self.memer(ctx.guild.id)
        await ctx.send(meme)

    # recursive function for the meme not to repeat itself...
    def memer(self, server_id):
        meme = Meme.get_meme() # get the meme

        # store the meme, so that it will not be the same again
        if self.collection.count_documents({"meme_link": meme, "server_id": server_id}) == 0:
            self.collection.insert_one({"meme_link": meme, "server_id": server_id})
            return meme
        else:
            self.memer(server_id)

    @commands.command()
    @commands.guild_only()
    async def hi(self, ctx):
        await ctx.send(ctx.author.name)


def setup(bot):
    bot.add_cog(Random(bot))
