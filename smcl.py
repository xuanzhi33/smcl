import webview
from subprocess import run as sp_run
import sys
CMCL = "./src/cmcl.exe"
SRC_DIR = "./src/"
MAIN = "main.html"

class Api:
    def __init__(self, window) -> None:
        self.window = window
    def set_title(self, title):
        self.window.title = title
    def log(self, message):
        print(message)
    def _run(self, args):
        result = sp_run(args, capture_output=True, text=True)
        return result.stdout
    def cmcl(self, cmd):
        args = cmd.split(" ")
        return self._run([CMCL] + args)

window = webview.create_window('SMCL', SRC_DIR + MAIN)
api = Api(window)
window.expose(api.set_title, api.log, api.cmcl)

if getattr(sys, 'frozen', False):
    debug = False
else:
    debug = True

webview.start(debug=debug)
