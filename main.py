import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


GUILD_ID = 1510593847972073653 

@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)

    await bot.tree.sync(guild=guild)

    print("Synced to guild")

async def main():
    async with bot:
        await bot.load_extension("cogs.base")
        await bot.start(os.getenv("DISCORD_TOKEN"))


asyncio.run(main())