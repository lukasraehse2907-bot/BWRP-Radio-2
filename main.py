import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from radio import RADIOS, play_radio, stop_radio

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Online als {bot.user}")


# 📻 automatisch Commands aus RADIOS erstellen
def create_command(name):

    @bot.tree.command(name=name, description=f"Starte {name} Radio")
    async def cmd(interaction: discord.Interaction):
        await play_radio(interaction, name)


for radio_name in RADIOS.keys():
    create_command(radio_name)


# ⏹ Stop Command
@bot.tree.command(name="stop", description="Stoppt das Radio")
async def stop(interaction: discord.Interaction):
    await stop_radio(interaction)


bot.run(TOKEN)