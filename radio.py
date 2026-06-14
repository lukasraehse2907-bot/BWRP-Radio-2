import discord

RADIOS = {
    "techno": "https://stream.sunshine-live.de/techno/mp3-192/",
    "house": "https://listen.housetime.fm/tunein-mp3",
    "charts": "https://icecast.ndr.de/ndr/njoy/live/mp3/128/stream.mp3",
    "rock": "https://streams.radiobob.de/bob-national/mp3-192/streams.radiobob.de/"
}

async def play_radio(interaction, sender: str):
    if interaction.user.voice is None:
        await interaction.response.send_message(
            "❌ Du musst in einem Sprachkanal sein!",
            ephemeral=True
        )
        return

    sender = sender.lower()

    if sender not in RADIOS:
        await interaction.response.send_message(
            f"❌ Sender nicht gefunden.\nVerfügbar: {', '.join(RADIOS.keys())}",
            ephemeral=True
        )
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
        RADIOS[sender],
        before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
    )

    vc.play(source)

    await interaction.response.send_message(
        f"📻 Jetzt läuft **{sender.upper()}**"
    )

async def stop_radio(interaction):
    vc = interaction.guild.voice_client

    if vc:
        await vc.disconnect()
        await interaction.response.send_message("⏹️ Radio gestoppt.")
    else:
        await interaction.response.send_message(
            "❌ Ich bin in keinem Sprachkanal.",
            ephemeral=True
        )