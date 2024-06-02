import webview
from subprocess import run as sp_run, PIPE, Popen
import subprocess
import sys
from os import path
import os
import json
from webview import Window
from datetime import datetime
from locale import getdefaultlocale
PATH = path.dirname(path.abspath(__file__))
CWD = os.getcwd()

SRC_DIR = path.join(PATH, "src")
GUI_MAIN = path.join(SRC_DIR, "main.html")
CMCL_CONFIG = path.join(SRC_DIR, "cmcl.json")
CMCL_PATH = path.join(SRC_DIR, "cmcl.jar")
CMCL_CMD = ["java", "-jar", CMCL_PATH]

SIZE = (800, 450)
DEBUG = True

class Settings:
    def get(self, key):
        with open(CMCL_CONFIG, "r", encoding="utf-8") as f:
            data = json.load(f)
            if key in data:
                return data[key]
            else:
                return None
    def set(self, settings):
        with open(CMCL_CONFIG, "r", encoding="utf-8") as f:
            data = json.load(f)
            for key in settings:
                data[key] = settings[key]
        with open(CMCL_CONFIG, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

class Api:
    def __init__(self) -> None:
        self._window = None
        self.settings = Settings()
        if os.name == "nt":
            self.startupinfo = subprocess.STARTUPINFO()
            self.startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        else:
            self.startupinfo = None
        
    def _set_window(self, window: Window):
        self._window = window
    def run_js(self, js):
        return self._window.evaluate_js(js)
    def cmd_result(self, result):
        resultJson = json.dumps(result)
        self.run_js(f"window.cmdResult({resultJson});")
    def cmcl_waiting(self, cmd):
        args = CMCL_CMD
        if cmd is not None:
            self.log(f"CMCL: {cmd}")
            args += cmd
        else:
            self.log(f"CMCL: Launch Game")

        p = Popen(args, stdout=PIPE, stderr=PIPE, text=True, startupinfo=self.startupinfo)
        last_lines = []
        for line in p.stdout:
            self.cmd_result(line)
            last_lines.append(line)
            if len(last_lines) > 10:
                last_lines.pop(0)

        return "".join(last_lines)
    def makedirs(self, path_list):
        dir_path = path.join(*path_list)
        self.log(f"Creating directory: {dir_path}")
        os.makedirs(dir_path, exist_ok=True)

    def open_file(self, path_list):
        file_path = path.join(*path_list)
        self.log(f"Opening file: {file_path}")
        if not path.exists(file_path):
            return False

        if os.name == "nt":
            os.startfile(file_path)
        elif os.name == "darwin":
            sp_run(["open", file_path])
        else:
            sp_run(["xdg-open", file_path])
        
        return True

    def set_title(self, title):
        self.log(f"New title: {title}")
        self._window.title = title
    def log(self, message):
        if not DEBUG:
            return
        time_str = datetime.now().strftime("%H:%M:%S")
        print(f"[SMCL] [{time_str}] {message}")
    def confirm_dialog(self, message, title="SMCL"):
        self.log(f"ALERT: {title} - {message}")
        return self._window.create_confirmation_dialog(title, message)
    def cmcl(self, args):
        self.log(f"CMCL: {args}")
        p = sp_run(CMCL_CMD + args, capture_output=True, text=True, startupinfo=self.startupinfo)
        result = p.stdout
        self.log(result)
        return result
    def config(self, key, value = None):
        if value == None:
            return self.settings.get(key)
        else:
            return self.settings.set({key: value})
    def get_all_settings(self):
        with open(CMCL_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    def close(self):
        self._window.destroy()
    def minimize(self):
        self._window.minimize()
    def isDebug(self):
        return DEBUG
    def cmcl_config_exists(self):
        return path.exists(CMCL_CONFIG)
    
    def default_settings(self):
        self.log("Initializing cmcl.json")
        self.cmcl(["config","--clear"])
        lang = "en"
        sysLocale = getdefaultlocale()[0]
        self.log(f"System locale: {sysLocale}")
        if "zh" in sysLocale or "Chinese" in sysLocale:
            lang = "zh"
        self.settings.set({
            "downloadSource": 0,
            "exitWithMinecraft": False,
            "printStartupInfo": True,
            "checkAccountBeforeStart": True,
            "gameDir": path.join(CWD, ".minecraft"),
            "language": lang,
            "smclActionAfterLaunch": "minimize"
        })

    def init_cmcl(self):
        if not self.cmcl_config_exists():
            self.log("cmcl.json not found, initializing...")
            self.default_settings()
            return True
        else:
            return False

class UI:
    def __init__(self) -> None:
        self.api = Api()
    def start(self):
        self.api.log(f"SMCL is starting, DEBUG: {self.isDebug()}")
        webview.settings['ALLOW_DOWNLOADS'] = True

        window = webview.create_window('SMCL', GUI_MAIN,
                                       width=SIZE[0], height=SIZE[1],
                                       js_api=self.api)
        self.api._set_window(window)
        webview.start(debug=self.isDebug())
    def isDebug(self):
        return not hasattr(sys, "frozen") and DEBUG

if __name__ == "__main__":
    UI().start()
