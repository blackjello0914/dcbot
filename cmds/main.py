import discord
from discord.ext import commands
from core.core import Cog_Extension

class Main(Cog_Extension):
    
    # 自定義指令
    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'round{self.bot.latency*1000} (ms)')

def setup(bot):
    bot.add_cog(Main(bot))