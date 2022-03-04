import discord
from discord.ext import commands
from core.core import Cog_Extension

class React(Cog_Extension):
    @commands.command()
    async def test():
        print(1)


def setup(bot):
    bot.add_cog(React(bot))