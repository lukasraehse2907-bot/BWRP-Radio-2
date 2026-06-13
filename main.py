import os
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Online als {bot.user}")
    await bot.tree.sync()


async def main():
    async with bot:
        await bot.load_extension("cogs.base")
        await bot.load_extension("cogs.radio")

        token = os.getenv("TOKEN")  # WICHTIG

        if not token:
            print("TOKEN FEHLT!")
            return

        await bot.start(token)


asyncio.run(main())