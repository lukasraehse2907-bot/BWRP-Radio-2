import discord
from discord.ext import commands
from discord import app_commands

STREAM_URL = "https://copyrights-recorder-cement-totals.trycloudflare.com/bwrp"

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
