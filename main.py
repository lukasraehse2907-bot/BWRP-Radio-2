import os
import asyncio
import importlib
import importlib.util

def _load_discord_library():
    for package in ("discord", "nextcord"):
        if importlib.util.find_spec(package) is not None:
            discord = importlib.import_module(package)
            commands = importlib.import_module(f"{package}.ext.commands")
            return discord, commands

    raise ImportError(
        "Keine kompatible Discord-Bibliothek gefunden. Installiere discord.py, py-cord oder nextcord."
    )

discord, commands = _load_discord_library()

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Online als {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} Commands synchronisiert")
    except Exception as e:
        print(e)

async def main():
    async with bot:
        await bot.load_extension("cogs.base")
        await bot.load_extension("cogs.radio")

        token = os.getenv("TOKEN")

        if not token:
            print("TOKEN FEHLT!")
            return

        await bot.start(token)

asyncio.run(main())