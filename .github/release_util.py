import re
import os
with open("./src/main.html", "r", encoding="utf-8") as f:
    content = f.read()
    pattern = re.compile(r'const VERSION = "([0-9.]+)";')
    version = pattern.search(content).group(1)
    print(f"Version: {version}")


platforms = {
    "nt": "Windows",
    "posix": "Linux",
    "darwin": "macOS"
}

def get_filename(os_name):
    name = platforms[os_name]
    return f"SMCL-{version}-{name}.zip"

envs = {
    "smcl_version": version,
    "smcl_filename": get_filename(os.name)
}

DOWNLOAD_URL = "https://github.com/xuanzhi33/smcl/releases/download/"
MIRROR = "https://mirror.ghproxy.com/"

download_md = ""
for i in platforms:
    os_name = platforms[i]
    filename = get_filename(i)
    url = f"{MIRROR}{DOWNLOAD_URL}{version}/{filename}"
    download_md += f"- {os_name}: [{filename}]({url})\n"

release_notes = f"""
# SMCL {version}

## Download / 下载
{download_md}
## Notes / 说明
- Zip Password / 解压密码: `smcl`
- Please extract and run smcl.exe / 下载后请解压并运行 smcl.exe

"""

with open("release_notes.md", "w", encoding="utf-8") as f:
    f.write(release_notes)

gh_env = os.getenv("GITHUB_ENV")

if gh_env is not None:
    print(f"Writing: {gh_env}")
    with open(gh_env, "a") as f:
        for key, value in envs.items():
            f.write(f"{key}={value}\n")
