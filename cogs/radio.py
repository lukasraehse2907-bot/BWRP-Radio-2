import discord
from discord.ext import commands
from discord import app_commands

STREAM_URL = "https://streams.ilovemusic.de/iloveradio1.mp3"

class Radio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="play",
        description="Startet den Radiostream"
    )
    async def play(self, interaction: discord.Interaction):

        if interaction.user.voice is None:
            await interaction.response.send_message(
                "❌ Du musst in einem Voice-Channel sein.",
                ephemeral=True
            )
            return

        await interaction.response.defer()

        channel = interaction.user.voice.channel

        if interaction.guild.voice_client is None:
            vc = await channel.connect()
        else:
            vc = interaction.guild.voice_client

        source = discord.FFmpegPCMAudio(
            STREAM_URL,
            before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            options="-vn"
        )

        vc.stop()
        vc.play(source)

        await interaction.followup.send("▶️ Radio gestartet!")

    @app_commands.command(
        name="stop",
        description="Stoppt das Radio"
    )
    async def stop(self, interaction: discord.Interaction):

        vc = interaction.guild.voice_client

        if vc:
            vc.stop()
            await vc.disconnect()
            await interaction.response.send_message("⏹️ Radio gestoppt.")
        else:
            await interaction.response.send_message(
                "❌ Ich bin in keinem Voice-Channel."
            )

async def setup(bot):
    await bot.add_cog(Radio(bot))