import discord
from discord.ext import commands

# other modules required
from .plug_special.covid19 import COVID19
from .plug_special.shrinker import Shrinker

from datetime import date

class Special(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="covid19")
    @commands.guild_only()
    async def get_covid19(self, ctx):
        confirmed, active, recovered, deaths, severe, fatality = COVID19.get_covid19()

        embed = discord.Embed(
            title="Covid 19 | PH Data",
            description="This is the current summary of the COVID-19 Cases in the Philippines\nAs of " + date.today().strftime("%B %d, %Y"),
            colour=discord.Colour.blue(),
        )
        embed.add_field(name="Confirmed Cases", value="{:,}".format(confirmed), inline=True)
        embed.add_field(name="Active Cases", value="{:,}".format(active), inline=True)
        embed.add_field(name="Recovered", value="{:,}".format(recovered), inline=True)
        embed.add_field(name="Death Cases", value="{:,}".format(deaths), inline=True)
        embed.add_field(name="Severe Cases", value="{:,}".format(severe), inline=True)
        embed.add_field(name="Fatality Rate", value=str(fatality) + "%", inline=True)
        embed.set_footer(text="covid19ph-api.herokuapp.com")

        await ctx.send(embed=embed)

    @commands.command(name="sh")
    @commands.guild_only()
    async def shrink_url(self, ctx, *, url_to_shrink: str):
        resp = await Shrinker.SHRINK_URL(url_to_shrink)

        # send the response
        await ctx.send("URL: *" + url_to_shrink + "*\n" + "```" + resp + "```")


def setup(bot):
    bot.add_cog(Special(bot))
