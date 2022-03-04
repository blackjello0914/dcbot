import discord
import googletrans
import os
import json
import requests
import re
import random
import io
import aiohttp

from pprint import pprint
# 輸入自己Bot的TOKEN碼
TOKEN = os.environ['TOKEN']
SRCLanguage=os.environ['SRC']
DSTLanguage=os.environ['DST']

DATA_PATH = os.path.join("data")
SETTINGS_JSON = os.path.join(DATA_PATH, "settings.json")

client = discord.Client()

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text);
    quote = json_data[0]["q"] + " -" +json_data[0]["a"]
    return quote


class MyClient(client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.role_message_id = 949168167048060939 # ID of the message that can be reacted to to add/remove a role.
        self.emoji_to_role = {
            discord.PartialEmoji(name='🔴'): 0, # ID of the role associated with unicode emoji '🔴'.
            discord.PartialEmoji(name='🟡'): 949151654970802187, # ID of the role associated with unicode emoji '🟡'.
            discord.PartialEmoji(name='green', id=949177753461219328): 949151583051087923, # ID of the role associated with a partial emoji's ID.
        }

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally, add the role.
            await payload.member.add_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass
    # 起動時呼叫
    @client.event
    async def on_ready():
        print('成功登入')

    # 收到訊息時呼叫
    @client.event
    async def on_message(message):
        msg = message.content
        names = ["茯茯","ㄈㄈ","四一","41","大師","米可","ㄇㄎ","杯杯","老七","米腸","樹人","肉乾","阿元","球球","L宇"]
        nameGroup = {
            "Welkin": "茯茯",
            "茯茯": "茯茯",
            "ㄈㄈ": "茯茯",
            "四一": "四一",
            "41": "四一",
            "米可": "米可",
            "ㄇㄎ": "米可",
            "球": "球球",
            "ball": "球球",
            "流羽": "L宇",
            "Black13":"L宇",
            "玩什麼都神就是沒裝":"大師",
            "酒杯":"杯杯",
            "z99725238":"米腸",
            "樂悠魔":"樹人",
            "Blackjello":"阿元"
        }
        nameStr = ("|").join(names)
        # 送信者為Bot時無視
        if message.author.bot:
            return
        # msg = str(message.mentions[0].name)+msg
        if "甲賽" in msg or "吃屎" in msg or "好帥" in msg :
            regex = r"(?=({})({})*(甲賽|也甲賽|好帥))".format(nameStr, nameStr)
            matches = re.finditer(regex, msg)
            eatShitList = [match.group(1) for match in matches]

            if eatShitList:
                targetList = {}
                for name in eatShitList:
                    if name in nameGroup:
                        targetName = nameGroup[name]
                        if not targetName in targetList:
                            targetList[targetName] = name
                    else:
                        targetList[name] = name

                eatShitStr = ""
                for key in targetList:
                    if eatShitStr == "":
                        eatShitStr += targetList[key] + "甲賽賽 <:guraseeyou:873967596582625321>"
                    else:
                        eatShitStr += " " + targetList[key] + "也甲賽賽 <:guraseeyou:873967596582625321>"

                await message.reply("好，" + eatShitStr)
                return
            else:
                await message.reply("娃沒看到說誰，那就還是茯茯甲賽賽吧 <:guraseeyou:873967596582625321>")
                return

        if "在戳" in msg or "死戳仔" in msg :
            regex = r"(?=({})({})*(在戳|死戳仔))".format(nameStr, nameStr)
            matches = re.finditer(regex, msg)
            eatShitList = [match.group(1) for match in matches]

            if eatShitList:
                targetList = {}
                for name in eatShitList:
                    if name in nameGroup:
                        targetName = nameGroup[name]
                        if not targetName in targetList:
                            targetList[targetName] = name
                    else:
                        targetList[name] = name

                eatShitStr = ""
                for key in targetList:
                    if eatShitStr == "":
                        eatShitStr += targetList[key] + "死戳仔 轉守為攻<a:takesiAngry:875747116247560253>"
                    else:
                        eatShitStr += "，啊" + targetList[key] + "也在戳 <a:takesiAngry:875747116247560253>"

                await message.reply("哭啊，" + eatShitStr)
                return
            else:
                await message.reply("哪個北七在戳，484杯杯 <:guraseeyou:873967596582625321>")
                return
        # if "拆丼" in msg or "拆井" in msg :
        #     async with aiohttp.ClientSession() as session:
        #         async with session.get("https://media.discordapp.net/attachments/873135014676664354/889125450633343006/unknown.png") as resp:
        #             if resp.status != 200:
        #                 return await message.channel.send('Could not download file...')
        #             data = io.BytesIO(await resp.read())
        #             await message.channel.send("再拆丫<a:takesiAngry:875747116247560253>", file=discord.File(data, 'unknown.png'))
        #     # await message.reply("哭啊")
        #     return
        # if "四一" in msg or "4187" in msg :
        #     await message.reply("4187 <:guraseeyou:873967596582625321>")
        #     return
        # if "A一下" in msg :
        #     await message.reply("哭啊阿元帳號還沒回來 <a:takesiAngry:875747116247560253>")
        #     return
        if "沒屁用" in msg :
            await message.reply("你4說老七沒屁用嗎？ <:guraseeyou:873967596582625321>")
            return
        if "無恥" in msg :
            await message.reply("你4說老七無恥嗎？ <:guraseeyou:873967596582625321>")
            return
        if msg.startswith("!古戰") or msg.startswith("！古戰") :
            async with aiohttp.ClientSession() as session:
                async with session.get("https://media.discordapp.net/attachments/873135014676664354/889139922647269376/321.png") as resp:
                    if resp.status != 200:
                        return await message.channel.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await message.channel.send("<:guraseeyou:873967596582625321>,哭啊不想更新", file=discord.File(data, '321.png'))
            return
        if msg.startswith("!隨便講點啥") :
            await message.reply(get_quote() + "<:guraseeyou:873967596582625321>")
            return
        if msg.startswith("!dice"):
            try:
                await message.reply("隨機1到" + msg[5:] + "，結果：" + str(random.randint(1,int(msg[5:]))))
            except:
                await message.reply("你妹在那邊亂填")
            return

        if client.user in message.mentions: # @判定
            translator = googletrans.Translator()
            robotName = client.user.name
            first, space, content = message.clean_content.partition('@'+robotName+' ')
            
            if content == '':
                content = first
            if translator.detect(content).lang == DSTLanguage:
                return
            if translator.detect(content).lang == SRCLanguage or SRCLanguage == '':
                remessage = translator.translate(content, dest=DSTLanguage).text
                await message.reply(remessage) 
        
        if(message.mentions):
            if "好爛" in msg :
                await message.reply("他就爛 <:shibahehe:881814045848666144>")
            return
        
        if msg.startswith("!testbot") :
            await message.reply(str(message))
            return

intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)

# Bot起動
client.run(TOKEN)
