import discord
from discord.ext import commands
from discord import app_commands


class Base(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="hello", description="Say hello")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Hey {interaction.user.mention}"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Base(bot))
    bot.tree.add_command(app_commands.Command(
        name="hello",
        description="Say hello",
        callback=Base(bot).hello
    ))