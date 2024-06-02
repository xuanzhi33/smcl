from get_version import get_version
from platform import system
from os import getenv
version = get_version()
os_name = system()

if os_name == "Darwin":
    os_name = "macOS"

envs = {
    "smcl_version": version,
    "smcl_filename": f"SMCL-{version}-{os_name}.zip"
}

gh_env = getenv("GITHUB_ENV")

if gh_env is not None:
    print(f"Writing: {gh_env}")
    with open(gh_env, "a") as f:
        for key, value in envs.items():
            f.write(f"{key}={value}\n")
