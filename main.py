import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from radio import play_radio, stop_radio

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Online als {bot.user}")


@bot.tree.command(name="radio", description="Starte das Radio")
async def radio(interaction: discord.Interaction):
    await play_radio(interaction)


@bot.tree.command(name="stop", description="Stoppt das Radio")
async def stop(interaction: discord.Interaction):
    await stop_radio(interaction)


bot.run(TOKEN)