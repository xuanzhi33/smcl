import subprocess
from os import remove, path
import re
CMCL_JSON = "src/cmcl.json"
if path.exists(CMCL_JSON):
    print("Removing cmcl.json...")
    remove(CMCL_JSON)

cmds = ["pyinstaller"]

cmds.append("--windowed")

cmds.append("--icon")
cmds.append("src/image/logo.png")

cmds.append("--add-data")
cmds.append("src:src")

cmds.append("smcl.py")

result = subprocess.run(cmds)

print(result)

with open("src/main.html", "r", encoding="utf-8") as f:
    content = f.read()
    pattern = re.compile(r'const VERSION = "([0-9.]+)";')
    version = pattern.search(content).group(1)
    print(f"::set-output name=version::{version}")
