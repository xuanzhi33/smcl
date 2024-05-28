import webview
from subprocess import run as sp_run, PIPE, Popen
import sys
from os import path, remove, getcwd
import json
from webview import Window
import requests
from datetime import datetime
from locale import getdefaultlocale
PATH = path.dirname(path.abspath(__file__))
CWD = getcwd()

SRC_DIR = path.join(PATH, "src")
GUI_MAIN = path.join(SRC_DIR, "main.html")
CMCL_CONFIG = path.join(SRC_DIR, "cmcl.json")
CMCL = path.join(SRC_DIR, "cmcl.exe")

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
        self.window = None
        self.settings = Settings()
    def _set_window(self, window: Window):
        self.window = window
    def _run(self, args):
        result = sp_run(args, capture_output=True, text=True)
        return result.stdout
    def run_js(self, js):
        return self.window.evaluate_js(js)
    def set_progress(self, progress):
        self.run_js(f"window.setProgress({progress})")
    def show_progress_info(self, info):
        self.run_js(f"window.showProgressInfo(`{info}`)")
    def cmcl_waiting(self, cmd):
        self.log(f"CMCL: {cmd}")
        args = [CMCL]
        if cmd is not None:
            args += cmd.split(" ")
        
        p = Popen(args, stdout=PIPE, stderr=PIPE, text=True)
        prog = 0
        for line in p.stdout:
            print(line)
            self.set_progress(prog)
            self.show_progress_info(line)
            prog += 1

    def set_title(self, title):
        self.log(f"New title: {title}")
        self.window.title = title
    def log(self, message):
        if not DEBUG:
            return
        time_str = datetime.now().strftime("%H:%M:%S")
        print(f"[SMCL] [{time_str}] {message}")
    def alert(self, message, title="SMCL"):
        return self.window.create_confirmation_dialog(title, message)
    def cmcl(self, cmd):
        self.log(f"CMCL: {cmd}")
        args = cmd.split(" ")
        return self._run([CMCL] + args)
    def config(self, key, value = None):
        if value == None:
            return self.settings.get(key)
        else:
            return self.settings.set({key: value})
    def close(self):
        self.window.destroy()
    def minimize(self):
        self.window.minimize()
    def get_setting(self, key):
        return self.settings.get(key)
    def set_setting(self, key, value):
        self.settings.set(key, value)
    def isDebug(self):
        return DEBUG
    def get(self, url):
        self.log(f"GET: {url}")
        return requests.get(url).text
    def cmcl_config_exists(self):
        return path.exists(CMCL_CONFIG)
    
    def default_settings(self):
        self.log("Initializing cmcl.json")
        self.cmcl("config --clear")
        lang = "en"
        if getdefaultlocale()[0] == "zh_CN":
            lang = "zh"
        self.settings.set({
            "downloadSource": 0,
            "exitWithMinecraft": False,
            "printStartupInfo": True,
            "checkAccountBeforeStart": True,
            "gameDir": path.join(CWD, ".minecraft"),
            "language": lang
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
        window = webview.create_window('SMCL', GUI_MAIN,
                                       width=SIZE[0], height=SIZE[1],
                                       js_api=self.api)
        self.api._set_window(window)
        webview.start(debug=self.isDebug())
    def isDebug(self):
        return not hasattr(sys, "frozen") and DEBUG

if __name__ == "__main__":
    UI().start()
