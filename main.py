import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Online als {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


async def main():
    async with bot:
        await bot.load_extension("cogs.base")
        await bot.start("DEIN_TOKEN")


asyncio.run(main())