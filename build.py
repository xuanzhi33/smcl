import subprocess

cmds = ["pyinstaller"]

cmds.append("--windowed")
cmds.append("--add-data")
cmds.append("src:src")

cmds.append("smcl.py")

result = subprocess.run(cmds)

print(result)
