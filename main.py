import discord
import pokebase as pb
import os
from keep import keep_alive


TOKEN = os.getenv("token")

# Botが動作する特定のチャンネルID
TARGET_CHANNEL_ID = 1274647244577968160  # 取得したチャンネルIDに置き換えてください

# Intentsの設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージの内容を取得するために必要
intents.messages = True  # メッセージイベントを受け取るために必要

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    # Bot自身のメッセージは無視
    if message.author == client.user:
        return

    # メッセージが特定のチャンネルからのものであるかを確認
    if message.channel.id != TARGET_CHANNEL_ID:
        return  # 特定のチャンネル以外からのメッセージは無視

    query = message.content.strip().lower()

    try:
        emoji = "🫶"
        await message.add_reaction(emoji)
        # pokebaseを使ってポケモンのデータを取得
        pokemon = pb.pokemon(query)

        if pokemon:
            name = pokemon.name.capitalize()
            types = ", ".join([t.type.name.capitalize() for t in pokemon.types])
            stats = {stat.stat.name: stat.base_stat for stat in pokemon.stats}

            result = (
                f"**{name}**\n"
                f"**Type**: {types}\n"
                f"**Stats**:\n"
                f"HP: {stats['hp']}\n"
                f"Attack: {stats['attack']}\n"
                f"Defense: {stats['defense']}\n"
                f"Special Attack: {stats['special-attack']}\n"
                f"Special Defense: {stats['special-defense']}\n"
                f"Speed: {stats['speed']}"
            )

            await message.channel.send(result)

    except Exception as e:
        await message.channel.send(
            "現在このbotはベータ版です。検索したいポケモンの英語名をお確かめください！"
        )


keep_alive()
try:
    client.run(TOKEN)
except:
    os.system("kill 1")
