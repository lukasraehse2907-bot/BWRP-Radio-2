import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

from radio import play_radio, stop_radio

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} ist online!")

@bot.tree.command(
    name="radio",
    description="Starte einen Radiosender"
)
@app_commands.describe(
    sender="techno, house, charts oder rock"
)
async def radio(interaction: discord.Interaction, sender: str):
    await play_radio(interaction, sender)

@bot.tree.command(
    name="stop",
    description="Stoppt das Radio"
)
async def stop(interaction: discord.Interaction):
    await stop_radio(interaction)

bot.run(TOKEN)