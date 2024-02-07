import webview
from subprocess import run as sp_run
import sys
from os import path
import json
from webview import Window
import requests

CMCL = "./src/cmcl.exe"
PATH = path.dirname(path.abspath(__file__))

SRC_DIR = path.join(PATH, "src")
GUI_MAIN = path.join(SRC_DIR, "main.html")
SETTINGS = path.join(PATH, "smcl.json")
SIZE = (800, 600)
DEBUG = True

class Settings:
    def __init__(self, file) -> None:
        self.file = file
        self.settings = {"test": "测试"}
        self.load()
    def init_file(self):
        with open(self.file, "w") as f:
            json.dump(self.settings, f)

    def load(self):
        if not path.exists(self.file):
            self.init_file()
               
        with open(self.file, "r") as f:
            self.settings = json.load(f)

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.settings, f)
    
    def get(self, key):
        return self.settings[key]
    
    def set(self, key, value):
        self.settings[key] = value
        self.save()

class Api:
    def __init__(self) -> None:
        self.window = None
        self.settings = Settings(SETTINGS)
    def _set_window(self, window: Window):
        self.window = window
    def _run(self, args):
        result = sp_run(args, capture_output=True, text=True)
        return result.stdout
    def set_title(self, title):
        self.window.title = title
    def log(self, message):
        print(message)
    def alert(self, message, title="SMCL"):
        return self.window.create_confirmation_dialog(title, message)
    def cmcl(self, cmd):
        args = cmd.split(" ")
        return self._run([CMCL] + args)
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
        return requests.get(url).text

class UI:
    def __init__(self) -> None:
        self.api = Api()
    def start(self):
        window = webview.create_window('SMCL', GUI_MAIN,
                                       width=SIZE[0], height=SIZE[1],
                                       js_api=self.api)
        self.api._set_window(window)
        webview.start(debug=self.isDebug())
    def isDebug(self):
        return not hasattr(sys, "frozen") and DEBUG

if __name__ == "__main__":
    UI().start()
