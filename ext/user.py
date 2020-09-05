import discord
from discord.ext import commands
import random
from datetime import datetime, timedelta
import pymongo
from bson.objectid import ObjectId
import os

client = pymongo.MongoClient(os.getenv("MONGO_DB").replace('"', "").replace('"', ""))
db = client["MrRandomUsers"]

bals = db["user_bals"]


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.waiting = [
            "Surely, a response will come, you just have to wait patiently...",
            "Why do they call it rush hour when nothing moves?",
            "Keep waiting my friend...",
            "Admit it. You're waiting for something you know won't happen.",
            "The best things in life are worth waiting for.",
            "Waiting, waiting, waiting, wait...",
            "Longest minutes in life: waiting for something that won't happen.",
            "Even if you are bored, learn how to wait!",
        ]

    @commands.command()
    @commands.guild_only()
    async def daily(self, ctx):
        nano = random.randint(10, 100)  # generate a random nano

        if bals.count_documents({"_id": ctx.author.id}) == 0:
            # set the daily
            daily = {
                "_id": ctx.author.id,
                "nano": nano,
                "wallet": 0,
                "datetime": datetime.utcnow(),
                "next_daily": datetime.utcnow() + timedelta(hours=23, minutes=59),
            }
            # insert to database
            bal = bals.insert_one(daily)

            # set the embed
            embed = discord.Embed(
                title=f"Here are your nanos {ctx.author.name}",
                description=f"{nano} nanos has been placed in your bank!",
                colour=discord.Colour.purple(),
            )
            embed.set_footer(text="© Mr. Random")
            await ctx.send(embed=embed)
        else:
            current = bals.find_one({"_id": ctx.author.id})
            if current["next_daily"] <= datetime.utcnow():
                # insert to database
                bal = bals.update_one(
                    {"_id": ctx.author.id},
                    {
                        "$set": {
                            "nano": current["nano"] + nano,
                            "datetime": datetime.utcnow(),
                            "next_daily": datetime.utcnow() + timedelta(hours=23, minutes=59),
                        }
                    },
                )

                # set the embed
                embed = discord.Embed(
                    title=f"Here are your nanos {ctx.author.name}",
                    description=f"**{nano} nanos** has been placed in your bank!",
                    colour=discord.Colour.purple(),
                )
                embed.set_footer(text="© Mr. Random")
                await ctx.send(embed=embed)
            else:
                hours, minutes, seconds = str(current["next_daily"] - datetime.utcnow()).split(":")
                embed = discord.Embed(
                    title=random.choice(self.waiting),
                    description=f"Please wait for **{hours}h {minutes}m {seconds[:-7]}s** and try again. \n\nWhile waiting, you can try other commands with `ran help`",
                    colour=discord.Colour.orange(),
                )
                embed.set_footer(text="© Mr. Random")
                await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def bal(self, ctx):
        user = bals.find_one({"_id": ctx.author.id})  # query the user

        if user is not None:
            bank = user["nano"]
            wallet = user["wallet"]
            total = user["nano"] + user["wallet"]
            # generate the embed
            embed = discord.Embed(
                title=f"Here is your balance {ctx.author.name}",
                description=f"**Bank:** {bank} \n**Wallet:** {wallet} \n**Total:** {total} nanos",
                colour=discord.Colour.light_gray(),
            )
            embed.set_footer(text="© Mr. Random")

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title=f"Sorry, you have 0 nanos in your balance...", description="Try to run `ran daily` to add some nanos to your balance."
            )
            embed.set_footer(text="© Mr. Random")

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(User(bot))
