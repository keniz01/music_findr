import subprocess
from pathlib import Path

folders = ["src", "tests"]

for folder in folders:
    if Path(folder).exists():
        subprocess.run(["black", folder])
        subprocess.run(["isort", folder])
