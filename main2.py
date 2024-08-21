import discord
import pokebase as pb
import os
import re
import pandas as pd
from keep import keep_alive

TOKEN = os.getenv("token")

# Botが動作する特定のチャンネルID
TARGET_CHANNEL_ID = 1275796834085765204

# Intentsの設定
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)

en_jp_df = pd.read_csv("pokemon_en_jp_dict.csv", index_col=0)
# en_type_type_df = pd.read_csv("en_type.csv", index_col=0)

iv = 31
ev = 252
level = 50
nature_mod_fast = 1.1  # 最速（性格補正+10%）
nature_mod_neutral = 1.0  # 準速（性格補正なし）
nature_mod_slow = 0.9  # 最遅（性格補正-10%）


def calculate_stat(base_stat, iv, ev, level, nature_mod, scarf=False):
    # 実数値計算
    stat = (((2 * base_stat + iv + ev // 4) * level) // 100 + 5) * nature_mod
    stat = int(stat)
    if scarf:
        stat = int(stat * 1.5)
    return stat


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
    elif bool(re.match(r"^[a-zA-Z0-9\s'-]+$", query)):
        pokemon_en_name = query
    else:
        pokemon_en_name = list(en_jp_df[en_jp_df["jp_name"] == query]["en_name"])[0]

    try:
        emoji = "🫶"
        await message.add_reaction(emoji)
        pokemon = pb.pokemon(pokemon_en_name)

        if pokemon:
            name = list(en_jp_df[en_jp_df["en_name"] == pokemon_en_name]["jp_name"])[0]

            speed_base_stat = next(
                stat.base_stat for stat in pokemon.stats if stat.stat.name == "speed"
            )
            # 各種ステータスの計算
            fastest = calculate_stat(speed_base_stat, iv, ev, level, nature_mod_fast)
            fast_with_scarf = calculate_stat(
                speed_base_stat, iv, ev, level, nature_mod_fast, scarf=True
            )
            semi_fastest = calculate_stat(
                speed_base_stat, iv, ev, level, nature_mod_neutral
            )
            semi_fast_with_scarf = calculate_stat(
                speed_base_stat, iv, ev, level, nature_mod_neutral, scarf=True
            )
            normal_s = calculate_stat(speed_base_stat, iv, 0, level, nature_mod_neutral)
            normal_s_down = calculate_stat(
                speed_base_stat, iv, 0, level, nature_mod_slow
            )
            slowest = calculate_stat(speed_base_stat, 0, 0, level, nature_mod_slow)

            result = (
                f"**{name}**(Lv.50)\n"
                f"{'すばやさ種族値：':　<8} {speed_base_stat: >3}\n"
                f"{'最速：':　<8} {fastest: >3}\n"
                f"{'最速スカーフ：':　<8} {fast_with_scarf: >3}\n"
                f"{'準速：':　<8} {semi_fastest: >3}\n"
                f"{'準速スカーフ：':　<8} {semi_fast_with_scarf: >3}\n"
                f"{'無振り：':　<8} {normal_s: >3}\n"
                f"{'無振り下降：':　<8} {normal_s_down: >3}\n"
                f"{'最遅：':　<8} {slowest: >3}"
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
