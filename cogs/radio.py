import discord
from discord.ext import commands
from discord import app_commands

RADIO_URL = "https://streams.ilovemusic.de/iloveradio1.mp3"

class Radio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="join",
        description="Joint deinem Voice Channel"
    )
    async def join(self, interaction: discord.Interaction):

        if interaction.user.voice is None:
            await interaction.response.send_message(
                "❌ Du bist in keinem Voice Channel!"
            )
            return

        channel = interaction.user.voice.channel

        if interaction.guild.voice_client:
            await interaction.response.send_message(
                "✅ Bereits verbunden!"
            )
            return

        await channel.connect()

        await interaction.response.send_message(
            f"✅ Verbunden mit {channel.name}"
        )

    @app_commands.command(
        name="play",
        description="Startet das Radio"
    )
    async def play(self, interaction: discord.Interaction):

        vc = interaction.guild.voice_client

        if vc is None:
            await interaction.response.send_message(
                "❌ Nutze zuerst /join"
            )
            return

        source = discord.FFmpegPCMAudio(RADIO_URL)

        vc.play(source)

        await interaction.response.send_message(
            "📻 Radio gestartet"
        )

    @app_commands.command(
        name="leave",
        description="Verlässt den Voice Channel"
    )
    async def leave(self, interaction: discord.Interaction):

        vc = interaction.guild.voice_client

        if vc is None:
            await interaction.response.send_message(
                "❌ Nicht verbunden"
            )
            return

        await vc.disconnect()

        await interaction.response.send_message(
            "👋 Getrennt"
        )

async def setup(bot):
    await bot.add_cog(Radio(bot))