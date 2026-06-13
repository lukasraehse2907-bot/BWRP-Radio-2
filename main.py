import discord
from discord.ext import commands
import asyncio
import os
import subprocess
import shutil

# FFmpeg testen
print("FFMPEG PATH:", shutil.which("ffmpeg"))

try:
    print(subprocess.check_output(
        ["ffmpeg", "-version"]
    ).decode())
except Exception as e:
    print("FFMPEG FEHLT:", e)

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} Slash Commands synchronisiert")
    except Exception as e:
        print("Sync Fehler:", e)

async def main():
    async with bot:
        await bot.load_extension("cogs.radio")
        await bot.start(os.getenv("TOKEN"))

asyncio.run(main())