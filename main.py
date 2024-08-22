import discord
import pokebase as pb
import os
import re
import pandas as pd
from keep import keep_alive

TOKEN = os.getenv("token")

# Botが動作する特定のチャンネルID
TARGET_CHANNEL_ID = 1274647244577968160

# Intentsの設定
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)

en_jp_df = pd.read_csv("pokemon_en_jp_dict.csv", index_col=0)
en_type_type_df = pd.read_csv("en_type.csv", index_col=0)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id != TARGET_CHANNEL_ID:
        return

    query = message.content.strip().lower()
    if query.isdigit():
        pokemon_en_name = list(en_jp_df[en_jp_df["number"] == int(query)]["en_name"])[0]
    elif bool(re.match(r"^[a-zA-Z0-9-]+$", query)):
        pokemon_en_name = query
    elif query == "メガリザードンX":
        pokemon_en_name = "charizard-mega-x"
    elif query == "メガリザードンY":
        pokemon_en_name = "charizard-mega-y"
    elif query == "メガミュウツーX":
        pokemon_en_name = "mewtwo-mega-x"
    elif query == "メガミュウツーY":
        pokemon_en_name = "mewtwo-mega-y"
    else:
        pokemon_en_name = list(en_jp_df[en_jp_df["jp_name"] == query]["en_name"])[0]

    try:
        emoji = "🫶"
        await message.add_reaction(emoji)
        pokemon = pb.pokemon(pokemon_en_name)

        if pokemon:
            name = list(en_jp_df[en_jp_df["en_name"] == pokemon_en_name]["jp_name"])[0]

            # 各タイプを取得
            types = [t.type.name for t in pokemon.types]

            # 各タイプを日本語に変換
            jp_types = []
            for t in types:
                jp_type = en_type_type_df.loc[
                    en_type_type_df["en_type"] == t, "jp_type"
                ]
                if not jp_type.empty:
                    jp_types.append(jp_type.values[0])
                else:
                    jp_types.append(None)  # 対応する日本語がない場合の処理

            # 各タイプを別の変数に格納
            type1 = jp_types[0] if len(jp_types) > 0 else None
            type2 = jp_types[1] if len(jp_types) > 1 else None

            stats = {stat.stat.name: stat.base_stat for stat in pokemon.stats}

            result = (
                f"**{name}**\n"
                f"**タイプ1**: {type1}\n"
                f"**タイプ2**: {type2}\n"
                f"HP: \t\t\t\t{stats['hp']}\n"
                f"こうげき:\t {stats['attack']}\n"
                f"ぼうぎょ:\t {stats['defense']}\n"
                f"とくこう:\t {stats['special-attack']}\n"
                f"とくぼう:\t {stats['special-defense']}\n"
                f"すばやさ:\t {stats['speed']}"
            )

            await message.channel.send(result)

    except Exception as e:
        await message.channel.send(f"エラーが発生しました: {str(e)}")
        emoji = "⚠"
        await message.add_reaction(emoji)


keep_alive()
try:
    client.run(TOKEN)
except:
    os.system("kill 1")
