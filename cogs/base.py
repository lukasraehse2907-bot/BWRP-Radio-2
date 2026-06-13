import discord  # type: ignore[import]
from discord import app_commands  # type: ignore[import]
from discord.ext import commands  # type: ignore[import]

class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="hello",
        description="Sagt Hallo"
    )
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"👋 Hallo {interaction.user.mention}"
        )

async def setup(bot):
    await bot.add_cog(Base(bot))