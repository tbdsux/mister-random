import discord
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, extension: str):
        self.bot.load_extension("ext." + extension)

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, extension: str):
        self.bot.unload_extension("ext." + extension)

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, extension: str):
        self.bot.unload_extension("ext." + extension)
        self.bot.load_extension("ext." + extension)


def setup(bot):
    bot.add_cog(Owner(bot))
