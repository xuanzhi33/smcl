import re
from os import getenv
with open("./src/main.html", "r", encoding="utf-8") as f:
    content = f.read()
    pattern = re.compile(r'const VERSION = "([0-9.]+)";')
    version = pattern.search(content).group(1)
    print(f"Version: {version}")
    if getenv("GITHUB_ENV") is not None:
        print(f"Writing version to {getenv('GITHUB_ENV')}")
        with open(getenv("GITHUB_ENV"), "a") as f:
            f.write(f"smcl_version={version}\n")
