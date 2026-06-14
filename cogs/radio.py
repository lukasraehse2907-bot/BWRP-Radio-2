import discord
from discord.ext import commands
from discord import app_commands

STREAM_URL = "https://s3.eu-central-3.ionoscloud.com/media-files-2026/SpotiDown.App%20-%20BIERBRUNNEN%20-%20TIEFBASSKOMMANDO.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=EEAAAAEFUDiECSVDZolniioKpyoZH3dFQaSIXPS7_4uB-lxzygCo2BYCTjhjAAAAAAJOOGNFFSZ8FcopUrkMF7QDqDYy%2F20260614%2Feu-central-3%2Fs3%2Faws4_request&X-Amz-Date=20260614T000725Z&X-Amz-Expires=1800&X-Amz-Signature=059b4f94034a38963327f082a1306004165fc93c3eccdd7b06ef15847ec12310&X-Amz-SignedHeaders=host&x-id=GetObject"

class Radio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="play",
        description="Startet das Radio"
    )
    async def play(self, interaction: discord.Interaction):

        try:
            # Discord sofort antworten lassen
            await interaction.response.defer()

            if interaction.user.voice is None:
                await interaction.followup.send(
                    "❌ Du musst in einem Voice-Channel sein."
                )
                return

            channel = interaction.user.voice.channel

            if interaction.guild.voice_client is None:
                vc = await channel.connect()
            else:
                vc = interaction.guild.voice_client

            print("FFmpeg wird gestartet")

            source = discord.FFmpegPCMAudio(
                STREAM_URL,
                before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                options="-vn"
            )

            print("FFmpeg Objekt erstellt")

            vc.stop()
            vc.play(source)

            print("Audio wird abgespielt")

            await interaction.followup.send(
                "▶️ Radio gestartet!"
            )

        except Exception as e:
            print("FEHLER:", e)

            if interaction.response.is_done():
                await interaction.followup.send(f"❌ Fehler: {e}")
            else:
                await interaction.response.send_message(f"❌ Fehler: {e}")

async def setup(bot):
    await bot.add_cog(Radio(bot))