import discord
from discord.ext import commands
from discord import app_commands


RADIO_URL = "https://streams.ilovemusic.de/iloveradio1.mp3"


class Radio(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="join")
async def join(self, interaction: discord.Interaction):

    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("❌ Geh erst in einen Voice Channel", ephemeral=True)
        return

    channel = interaction.user.voice.channel
    voice = interaction.guild.voice_client

    if voice:
        await voice.move_to(channel)
    else:
        await channel.connect()

    await interaction.response.send_message("✅ Ich bin jetzt im Voice Channel", ephemeral=True)

    @app_commands.command(name="play", description="Start radio stream")
    async def play(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message("❌ You must be in a voice channel")
            return

        voice = interaction.guild.voice_client

        if not voice:
            channel = interaction.user.voice.channel
            voice = await channel.connect()

        if voice.is_playing():
            voice.stop()

        source = discord.FFmpegPCMAudio(RADIO_URL)
        voice.play(source)

        await interaction.response.send_message("📻 Radio started!")

    @app_commands.command(name="stop", description="Stop radio")
    async def stop(self, interaction: discord.Interaction):
        voice = interaction.guild.voice_client

        if voice and voice.is_playing():
            voice.stop()
            await interaction.response.send_message("⏹️ Stopped radio")
        else:
            await interaction.response.send_message("❌ Nothing is playing")

    @app_commands.command(name="leave", description="Bot leaves voice channel")
    async def leave(self, interaction: discord.Interaction):
        voice = interaction.guild.voice_client

        if voice:
            await voice.disconnect()
            await interaction.response.send_message("👋 Left voice channel")
        else:
            await interaction.response.send_message("❌ I'm not in a voice channel")


async def setup(bot: commands.Bot):
    await bot.add_cog(Radio(bot))