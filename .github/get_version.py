import re
def get_version():
    with open("./src/main.html", "r", encoding="utf-8") as f:
        content = f.read()
        pattern = re.compile(r'const VERSION = "([0-9.]+)";')
        version = pattern.search(content).group(1)
        print(f"Version: {version}")
        return version
