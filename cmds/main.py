import discord
from discord.ext import commands
from core.core import Cog_Extension
import json
with open('grpSetting.json', mode='r', encoding='utf8') as jfile:
    grpData = json.load(jfile)
class Main(Cog_Extension):
    
    # bot新增自己身份組
    @commands.command()
    async def tf(self,ctx):
        # async def testevent(self,ctx):
        tempCnt = 1
        for messageID in grpData["messageList"]:
            test = await self.bot.get_channel(949336536762155009).fetch_message(messageID)
            for grp in grpData[f'emojiPairs{tempCnt}']:
                await test.add_reaction(grp[0])

    # # bot移除自己身份組
    # @commands.command()
    # async def rf(self,ctx):
    #     # async def testevent(self,ctx):
    #     tempCnt = 1
    #     for messageID in grpData["messageList"]:
    #         test = await self.bot.get_channel(949336536762155009).fetch_message(messageID)
    #         for grp in grpData[f'emojiPairs{tempCnt}']:
    #             await test.remove_reaction(grp[0],self.bot)

def setup(bot):
    bot.add_cog(Main(bot))