import discord
from discord.ext import commands
import os
import logging

# set logger
logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="ran ")

for i in os.listdir("./ext"):
    if i.endswith(".py"):
        bot.load_extension(f"ext.{i[:-3]}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")


bot.run(os.getenv("MR_RANDOM_TOKEN"))
