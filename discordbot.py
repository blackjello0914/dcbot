import discord
import googletrans
import os
import json
import requests
import re
import random

from pprint import pprint
# 輸入自己Bot的TOKEN碼
TOKEN = os.environ['TOKEN']
SRCLanguage=os.environ['SRC']
DSTLanguage=os.environ['DST']

client = discord.Client()

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text);
    quote = json_data[0]["q"] + " -" +json_data[0]["a"]
    return quote

# 起動時呼叫
@client.event
async def on_ready():
    print('成功登入')

# 收到訊息時呼叫
@client.event
async def on_message(message):
    msg = message.content
    names = ["茯茯","四一","大師","米可","杯杯","老七","米腸","樹人","肉乾"]
    whoeats = False
    # 送信者為Bot時無視
    if message.author.bot:
        return

    if "甲賽" in msg :
        regex = "({})甲賽".format(("|").join(names))
        eatShitList = re.findall(regex, msg)

        if eatShitList:
            eatShitStr = ""
            for i in range(0, len(eatShitList)):
                if i == 0:
                    eatShitStr += eatShitList[i] + "甲賽賽 <:guraseeyou:873967596582625321>"
                else:
                    eatShitStr += " " + eatShitList[i] + "也甲賽賽 <:guraseeyou:873967596582625321>"
            await message.reply(eatShitStr)
            return
        else:
            await message.reply("娃沒看到說誰，那就還是茯茯甲賽賽吧 <:guraseeyou:873967596582625321>")
            return

    if "四一" in msg or "4187" in msg :
        await message.reply("4187 <:guraseeyou:873967596582625321>")
        return
    if "A一下" in msg :
        await message.reply("哭啊阿元帳號還沒回來 <a:takesiAngry:875747116247560253>")
        return
    if "沒屁用" in msg :
        await message.reply("你4說老七沒屁用嗎？ <:guraseeyou:873967596582625321>")
        return
    if "無恥" in msg :
        await message.reply("你4說老七無恥嗎？ <:guraseeyou:873967596582625321>")
        return
    if msg.startswith("!古戰") :
        await message.reply("火古9/8~9/15 風古11月初 <:guraseeyou:873967596582625321>")
        return
    if msg.startswith("!隨便講點啥") :
        await message.reply(get_quote() + "<:guraseeyou:873967596582625321>")
        return
    if msg.startswith("!dice"):
        try:
            await message.reply("隨機1到" + int(msg[5:] + "，結果：" + random.randint(1,int(msg[5:])))
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
    
# Bot起動
client.run(TOKEN)
