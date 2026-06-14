import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from radio import RADIOS, play_radio, stop_radio

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Online als {bot.user}")


@bot.tree.command(name="techno", description="Sunshine Live Techno")
async def techno(interaction: discord.Interaction):
    await play_radio(interaction, "techno")


@bot.tree.command(name="house", description="HouseTime FM")
async def house(interaction: discord.Interaction):
    await play_radio(interaction, "house")


@bot.tree.command(name="charts", description="N-JOY Charts")
async def charts(interaction: discord.Interaction):
    await play_radio(interaction, "charts")


@bot.tree.command(name="rock", description="Radio BOB")
async def rock(interaction: discord.Interaction):
    await play_radio(interaction, "rock")


@bot.tree.command(name="stop", description="Stoppt das Radio")
async def stop(interaction: discord.Interaction):
    await stop_radio(interaction)


bot.run(TOKEN)