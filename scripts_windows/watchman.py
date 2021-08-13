#!C:\Python39\python.exe
"""
Uses watchman.exe in order to provide an interface like inotifywait.

This is a thin convenience wrapper around watchman because
watchman doesn't have the friendliest defaults around relative
paths and transient watches.
"""
import uuid
import argparse
import subprocess
from pathlib import Path
from typing import List
import os

parser = argparse.ArgumentParser()
parser.add_argument("watch_path")
parser.add_argument("command", nargs="+")

args = parser.parse_args()

import sys
sys.path.append(str((Path(__file__).parent / "..").resolve()))
from weltanschauung.cli import print_header

def clear_existing_watches():
    result = subprocess.run(["watchman.exe", "watch-del-all"], capture_output=True)
    if result.returncode != 0:
        print("Could not clear existing watches... Do you have watchman.exe installed?")
        exit(result.returncode)

    result = subprocess.run(["watchman.exe", "trigger-del-all"], capture_output=True)
    if result.returncode != 0:
        print("Could not clear existing watches... Do you have watchman.exe installed?")
        exit(result.returncode)

    print("Done.")


def setup_watch(path: Path, command: List[str]):
    path = path.absolute()
    trigger_id = str(uuid.uuid4())
    subprocess.run(["watchman.exe", "watch", str(path)])
    subprocess.run(["watchman.exe", "--", "trigger", str(path), trigger_id, "--", *command])


# Setup
watch_path = Path(args.watch_path).absolute()

print_header("Clearing existing watchman watches...")
clear_existing_watches()

print_header("Setting up watch...")
setup_watch(watch_path, args.command)
