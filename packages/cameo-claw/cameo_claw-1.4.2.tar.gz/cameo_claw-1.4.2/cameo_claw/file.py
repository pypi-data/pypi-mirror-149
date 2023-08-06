from pathlib import Path


def mkdir(target_directory):
    Path(target_directory).mkdir(parents=True, exist_ok=True)
