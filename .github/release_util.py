import re
from os import getenv, name
with open("./src/main.html", "r", encoding="utf-8") as f:
    content = f.read()
    pattern = re.compile(r'const VERSION = "([0-9.]+)";')
    version = pattern.search(content).group(1)
    print(f"Version: {version}")

if name == "nt":
    os_name = "Windows"
elif name == "posix":
    os_name = "Linux"
elif name == "darwin":
    os_name = "macOS"

envs = {
    "smcl_version": version,
    "smcl_filename": f"SMCL-{version}-{os_name}.zip"
}

download_url = f"https://github.com/xuanzhi33/smcl/releases/download/{version}/{envs['smcl_filename']}"
download_mirror = "https://mirror.ghproxy.com/" + download_url

release_notes = f"""
# SMCL {version}

## Download / 下载
- Windows: [{envs['smcl_filename']}]({download_mirror})

## Notes / 说明
- Zip Password / 解压密码: `smcl`
- Please extract and run smcl.exe / 下载后请解压并运行 smcl.exe

"""

with open("release_notes.md", "w", encoding="utf-8") as f:
    f.write(release_notes)

gh_env = getenv("GITHUB_ENV")

if gh_env is not None:
    print(f"Writing: {gh_env}")
    with open(gh_env, "a") as f:
        for key, value in envs.items():
            f.write(f"{key}={value}\n")
