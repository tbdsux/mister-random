import discord
from discord.ext import commands
import random
from datetime import datetime, timedelta
import pymongo
from bson.objectid import ObjectId
import os

client = pymongo.MongoClient(os.getenv("MONGO_DB").replace('"', "").replace('"', ""))

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
        self.db = client["MrRandomUsers"]
        self.collection = ""
        self.levels = {
            "1": 300,
            "2": 350,
            "3": 400,
            "4": 450,
            "5": 500,
            "6": 550,
            "7": 600,
            "8": 650,
            "9": 700,
            "10": 800,
        }

    # @commands.command()
    # @commands.is_owner()
    # async def configure(self, ctx):
    #     self.db = client["MrRandomUsers"]
    #     self.collection = self.db[str(ctx.guild.id)]
    #     await ctx.send(embed=discord.Embed(title="Server Configured", description="Your server has been successfully configured. \nYou can now run `ran help` to get the available commands."))

    @commands.command()
    @commands.guild_only()
    async def daily(self, ctx):
        # set the collection
        self.collection = self.db[str(ctx.guild.id)]

        # generate a random lootbox, how many
        loots = [{"nanos": random.randint(10, 100), "xp": random.randint(5, 10)} for _ in range(random.randint(1, 5))]

        if self.collection.count_documents({"_id": ctx.author.id}) == 0:
            # set the daily
            daily = {
                "_id": ctx.author.id,
                "server_id": ctx.guild.id,
                "nano": 0,
                "lootbox": loots,
                "wallet": 0,
                "level": 0,
                "xp": 0,
                "datetime": datetime.utcnow(),
                "next_daily": datetime.utcnow() + timedelta(hours=11, minutes=59), # change the time when developing
            }
            # insert to database
            bal = self.collection.insert_one(daily)

            # set the embed
            embed = discord.Embed(
                title=f"Here are your daily rewards {ctx.author.name}",
                description=f"You have received **{len(loots)}** lootbox!",
                colour=discord.Colour.purple(),
            )
            embed.set_footer(text="© Mr. Random")
            await ctx.send(embed=embed)
        else:
            current = self.collection.find_one({"_id": ctx.author.id, "server_id": ctx.guild.id})
            if current["next_daily"] <= datetime.utcnow():
                # insert to database
                bal = self.collection.update_one(
                    {"_id": ctx.author.id, "server_id": ctx.guild.id},
                    {
                        "$set": {
                            "lootbox": current["lootbox"] + loots,
                            "datetime": datetime.utcnow(),
                            "next_daily": datetime.utcnow() + timedelta(hours=11, minutes=59), # change the time when developing
                        }
                    },
                )

                # set the embed
                embed = discord.Embed(
                    title=f"Here are your daily rewards {ctx.author.name}",
                    description=f"You have received **{len(loots)}** lootbox!",
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
        # set the collection
        self.collection = self.db[str(ctx.guild.id)]

        user = self.collection.find_one({"_id": ctx.author.id, "server_id": ctx.guild.id})  # query the user

        if user is not None:
            bank = user["nano"]
            wallet = user["wallet"]
            lootbox = user["lootbox"]
            total = user["nano"] + user["wallet"]
            # generate the embed
            embed = discord.Embed(
                title=f"Here is your Balance {ctx.author.name}",
                colour=discord.Colour.light_gray(),
            )
            embed.add_field(name="Bank", value=str(bank), inline=True)
            embed.add_field(name="Wallet", value=str(wallet), inline=True)
            embed.add_field(name="LootBox", value=str(len(lootbox)), inline=True)
            embed.set_footer(text="© Mr. Random")

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title=f"Sorry, you have **0** nanos in your balance...", description="Try to run `ran daily` to add some nanos to your balance."
            )
            embed.set_footer(text="© Mr. Random")

            await ctx.send(embed=embed)

    @commands.command(name="lbox")
    @commands.guild_only()
    async def open_lootbox(self, ctx, *, lt_count: int):
        # set the collectionint
        self.collection = self.db[str(ctx.guild.id)]

        user = self.collection.find_one({"_id": ctx.author.id, "server_id": ctx.guild.id})  # query the user

        if user is not None:
            loots = user["lootbox"]
            to_open = [loots[i] for i in range(lt_count)]

            # remove the gathered to be open loot boxes
            for i in to_open: loots.remove(i)

            nanos = 0
            xps = 0
            for i in to_open:
                nanos += i["nanos"]
                xps += i["xp"]

            level = user["level"]
            total_xp = xps + user["xp"]

            for l, i in enumerate(self.levels):
                if level == l:
                    if total_xp >= self.levels[str(l+1)]:
                        total_xp -= self.levels[str(l+1)]
                        level += 1

            update = self.collection.update_one(
                {"_id": ctx.author.id, "server_id": ctx.guild.id},
                {
                    "$set": {
                        "wallet": nanos,
                        "lootbox": loots,
                        "xp": total_xp,
                        "level": level,
                        "datetime": datetime.utcnow(),
                        "next_daily": datetime.utcnow() + timedelta(seconds=30), # change the time when developing
                    }
                },
            )

            embed = discord.Embed(title=f"Unboxed {len(to_open)} lootbox!", description=f"You have received **{nanos} nanos** and **{xps} xp**! Loots are automatically added to your balance.\n\nRun `ran bal` to check tou balance.", colour=discord.Colour.blue())
            embed.set_footer(text="© Mr. Random")

            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def profile(self, ctx):
        # set the collection
        self.collection = self.db[str(ctx.guild.id)]

        user = self.collection.find_one({"_id": ctx.author.id, "server_id": ctx.guild.id})  # query the user

        embed=discord.Embed(title=f"{ctx.author.name}'s Profile", colour=discord.Colour.teal())
        embed.add_field(name="Current Level", value=str(user["level"]), inline=False)
        embed.add_field(name="Total Nanos", value=str(user["nano"] + user["wallet"]), inline=False)
        embed.add_field(name="XP", value=str(user["xp"]), inline=False)
        embed.set_footer(text="© Mr. Random")

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def level(self, ctx):
        # set the collection
        self.collection = self.db[str(ctx.guild.id)]

        user = self.collection.find_one({"_id": ctx.author.id, "server_id": ctx.guild.id})  # query the user

        __xp__ = 0

        for l, i in enumerate(self.levels):
            if user["level"] == l:
                __xp__ = self.levels[str(l+1)]

        embed = discord.Embed(title=f"{ctx.author.name}'s Level")
        embed.add_field(name="Current Level", value=str(user["level"]), inline=True)
        embed.add_field(name="XP", value=str(user["xp"]) + "/" + str(__xp__), inline=True)
        embed.set_footer(text="© Mr. Random")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(User(bot))
