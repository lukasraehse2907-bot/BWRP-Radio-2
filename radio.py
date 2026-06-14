import discord

RADIO_URL = "https://stream.sunshine-live.de/techno/mp3-192/"


async def play_radio(interaction):

    await interaction.response.defer()

    if not interaction.user.voice:
        return await interaction.followup.send("❌ Du bist in keinem Voice Channel!")

    channel = interaction.user.voice.channel

    try:
        vc = interaction.guild.voice_client

        print("➡️ JOINING VOICE...")

        if vc is None:
            vc = await channel.connect(timeout=30.0, reconnect=True)
        else:
            await vc.move_to(channel)

        print("✅ VOICE CONNECTED")

        if vc.is_playing():
            vc.stop()

        source = discord.FFmpegPCMAudio(
            RADIO_URL,
            before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            options="-vn"
        )

        vc.play(source)

        await interaction.followup.send("📻 Radio läuft!")

    except Exception as e:
        await interaction.followup.send(f"❌ Voice Fehler: {e}")


async def stop_radio(interaction):

    vc = interaction.guild.voice_client

    if vc:
        await vc.disconnect()
        await interaction.response.send_message("⏹️ Gestoppt")
    else:
        await interaction.response.send_message("❌ Nicht im Voice Channel")