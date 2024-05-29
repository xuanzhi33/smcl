import subprocess
from os import remove, path
CMCL_JSON = "src/cmcl.json"
if path.exists(CMCL_JSON):
    print("检测到cmcl.json文件，正在删除")
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
