from get_version import get_version
from os import getenv
version = get_version()

DOWNLOAD_URL = "https://github.com/xuanzhi33/smcl/releases/download/"
MIRROR = "https://mirror.ghproxy.com/"
os_list = ["Windows", "Linux", "macOS"]

download_md = ""
for os_name in os_list:
    filename = f"SMCL-{version}-{os_name}.zip"
    url = f"{MIRROR}{DOWNLOAD_URL}{version}/{filename}"
    download_md += f"- {os_name}: [{filename}]({url})\n"

release_notes = f"""
## Download / 下载
{download_md}
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
        f.write(f"smcl_version={version}\n")
