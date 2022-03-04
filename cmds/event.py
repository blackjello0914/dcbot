from numbers import Number
import discord
from discord.ext import commands
from core.core import Cog_Extension
import json
with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open('grpSetting.json', mode='r', encoding='utf8') as jfile:
    grpData = json.load(jfile)

class Event(Cog_Extension):

    # 自定義指令
    @commands.Cog.listener()
    async def testevent(self,ctx):
        await ctx.send(f'round{self.bot.latency*1000} (ms)')
    # 按表情選頻道
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction:discord.Reaction):
        # print(str(reaction))
        tempCnt = 1
        for messageID in grpData["messageList"]:
            print(messageID)
            if(str(reaction.message_id) == messageID):
                print(tempCnt)
                for grp in grpData[f'emojiPairs{tempCnt}']:
                    print(grp[0])
                    if(str(reaction.emoji)==grp[0]):
                        # print("發身份")
                        guild = self.bot.get_guild(reaction.guild_id)
                        role = guild.get_role(int(grp[1]))
                        print(reaction.member)
                        await reaction.member.add_roles(role)#member：Only available if event_type is REACTION_ADD and the reaction is inside a guild.
                        await reaction.member.send(f'本機器人把你加進了{role}身份組，請說謝謝')
            tempCnt+=1
    # 按表情刪頻道
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction:discord.Reaction):
        # print(str(reaction))
        tempCnt = 1
        for messageID in grpData["messageList"]:
            print(messageID)
            if(str(reaction.message_id) == messageID):
                print(tempCnt)
                for grp in grpData[f'emojiPairs{tempCnt}']:
                    print(grp[0])
                    if(str(reaction.emoji)==grp[0]):
                        # print("發身份")
                        guild = self.bot.get_guild(reaction.guild_id)
                        user = guild.get_member(reaction.user_id)
                        role = guild.get_role(int(grp[1]))
                        print(reaction.member)
                        await user.remove_roles(role)
                        await user.send(f'本機器人把你移出了{role}身份組，滾粗')
            tempCnt+=1
def setup(bot):
    bot.add_cog(Event(bot))