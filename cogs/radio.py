import discord
from discord.ext import commands
from discord import app_commands


RADIO_URL = "https://streams.ilovemusic.de/iloveradio1.mp3"


class Radio(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="join", description="Bot joint deinen Voice Channel")
    async def join(self, interaction: discord.Interaction):

        if not interaction.user.voice:
            await interaction.response.send_message("❌ Du bist in keinem Voice Channel!")
            return

        channel = interaction.user.voice.channel

        # Falls schon verbunden → erst disconnect
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()

        await channel.connect()

        await interaction.response.send_message("✅ Ich bin im Voice Channel!")

    @app_commands.command(name="leave", description="Bot verlässt Voice Channel")
    async def leave(self, interaction: discord.Interaction):

        vc = interaction.guild.voice_client

        if not vc:
            await interaction.response.send_message("❌ Ich bin in keinem Voice Channel!")
            return

        await vc.disconnect()
        await interaction.response.send_message("👋 Ich habe den Channel verlassen!")

    @app_commands.command(name="radio", description="Startet I Love Radio Stream")
    async def radio(self, interaction: discord.Interaction):

        vc = interaction.guild.voice_client

        if not vc:
            await interaction.response.send_message("❌ Ich bin nicht im Voice Channel!")
            return

        if vc.is_playing():
            vc.stop()

        # STREAM START
        source = discord.FFmpegPCMAudio(
            RADIO_URL,
            before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            options="-vn"
        )

        vc.play(source)

        await interaction.response.send_message("🎶 I Love Radio läuft jetzt!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Radio(bot))