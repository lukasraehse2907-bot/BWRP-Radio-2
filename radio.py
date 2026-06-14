import discord

RADIOS = {
    "techno": "https://stream.sunshine-live.de/techno/mp3-192/",
    "house": "https://listen.housetime.fm/tunein-mp3",
    "charts": "https://icecast.ndr.de/ndr/njoy/live/mp3/128/stream.mp3",
    "rock": "https://streams.radiobob.de/bob-national/mp3-192/streams.radiobob.de/"
}


async def play_radio(interaction, name):

    await interaction.response.defer()

    if interaction.user.voice is None:
        return await interaction.followup.send(
            "❌ Du musst in einem Sprachkanal sein!"
        )

    channel = interaction.user.voice.channel
    vc = interaction.guild.voice_client

    try:
        if vc is None:
            vc = await channel.connect()
        else:
            await vc.move_to(channel)

        if vc.is_playing():
            vc.stop()

        source = discord.FFmpegPCMAudio(
            RADIOS[name],
            before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            options="-vn"
        )

        vc.play(source)

        await interaction.followup.send(
            f"📻 Jetzt läuft **{name.upper()}**"
        )

    except Exception as e:
        await interaction.followup.send(
            f"❌ Fehler: {e}"
        )


async def stop_radio(interaction):

    vc = interaction.guild.voice_client

    if vc:
        await vc.disconnect()
        await interaction.response.send_message(
            "⏹️ Radio gestoppt"
        )
    else:
        await interaction.response.send_message(
            "❌ Ich bin in keinem Sprachkanal."
        )