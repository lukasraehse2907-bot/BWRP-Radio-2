import discord

RADIOS = {
    "techno": "https://stream.sunshine-live.de/techno/mp3-192/",
    "house": "https://listen.housetime.fm/tunein-mp3",
    "charts": "https://icecast.ndr.de/ndr/njoy/live/mp3/128/stream.mp3",
    "rock": "https://streams.radiobob.de/bob-national/mp3-192/streams.radiobob.de/"
}


async def play_radio(interaction, name: str):

    if not interaction.user.voice:
        await interaction.response.send_message("❌ Du bist in keinem Voice Channel!", ephemeral=True)
        return

    url = RADIOS.get(name)

    if not url:
        await interaction.response.send_message("❌ Sender nicht gefunden!", ephemeral=True)
        return

    channel = interaction.user.voice.channel
    vc = interaction.guild.voice_client

    if vc is None:
        vc = await channel.connect()
    else:
        await vc.move_to(channel)

    if vc.is_playing():
        vc.stop()

    source = discord.FFmpegPCMAudio(
        url,
        before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        options="-vn"
    )

    vc.play(source)

    await interaction.response.send_message(f"📻 Jetzt läuft **{name.upper()}**")


async def stop_radio(interaction):
    vc = interaction.guild.voice_client

    if vc:
        await vc.disconnect()
        await interaction.response.send_message("⏹️ Radio gestoppt")
    else:
        await interaction.response.send_message("❌ Nicht im Voice Channel", ephemeral=True)