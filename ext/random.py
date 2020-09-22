import discord
from discord.ext import commands, tasks

from .plug_random.youtube import Youtube
from .plug_random.quote import Quotes
from .plug_random.news import News
from .plug_random.meme import Meme, Giphy  # , Gagger

import pymongo, os, random

client = pymongo.MongoClient(os.getenv("MONGO_DB").replace('"', "").replace('"', ""))


class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = client["RandomCommands"]
        self.collection = ""
        self.meme_source = ["reddit", "9gag"]

    @commands.Cog.listener()
    async def on_ready(self):
        self.auto_memer.start()

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

        meme = await self.memer(ctx.guild.id)
        await ctx.send(meme)

    # recursive function for the meme not to repeat itself...
    async def memer(self, server_id):
        meme = Meme.get_meme()
        # random select from reddit or 9GAG [9gag is not yet working]
        # if random.choice(self.meme_source) == "reddit":
        #     meme = Meme.get_meme() # get the meme
        # else:
        #     meme = Gagger.get_gag()

        self.collection = self.db[str(server_id)]

        # store the meme, so that it will not be the same again
        if self.collection.count_documents({"meme_link": meme, "server_id": server_id}) == 0:
            self.collection.insert_one({"meme_link": meme, "server_id": server_id})
            return meme
        else:
            return await self.memer(server_id)

    @tasks.loop(hours=1)  # use lower when developing
    async def auto_memer(self):
        collection = self.db["Auto_Memer"]

        all_servers = collection.find({})

        for i in all_servers:
            print(i)
            if i["auto_memer"]:
                print("Sending a meme to " + str(i["server_id"]))
                meme = await self.memer(i["server_id"])
                if meme:
                    channel = self.bot.get_channel(i["channel_id"])
                    await channel.send(meme)

    # for setting some configuration like auto sender
    @commands.command(name="configure")
    @commands.guild_only()
    async def configure_server(self, ctx, function, channel_name):
        if function == "automemer":
            collection = self.db["Auto_Memer"]
            if collection.count_documents({"server_id": ctx.guild.id, "auto_memer": True}) == 0:
                collection.insert_one(
                    {"server_id": ctx.guild.id, "auto_memer": True, "channel_id": discord.utils.get(ctx.guild.channels, name=channel_name).id}
                )
            else:
                pass
            await ctx.send("Server has been configured.")
        else:
            await ctx.send(embed=discord.Embed(title="Sorry, that is not available for the meantime."))

    @commands.command()
    @commands.guild_only()
    async def hi(self, ctx):
        await ctx.send(ctx.author.name)

    @commands.command(name="gif")
    @commands.guild_only()
    async def random_gif(self, ctx):
        gif = Giphy.get_gif()
        await ctx.send(gif)


def setup(bot):
    bot.add_cog(Random(bot))
