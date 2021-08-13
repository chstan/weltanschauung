#!C:\Python39\python.exe
"""
Uses watchgod in order to provide an interface like inotifywait.

This is a thin convenience wrapper around watchgod so that I can use
it for running CLI commands.
"""
import argparse
from dataclasses import dataclass
import subprocess
from pathlib import Path
from typing import List

parser = argparse.ArgumentParser()
parser.add_argument("watch_path")
parser.add_argument("command", nargs=argparse.REMAINDER)

args = parser.parse_args()

import sys

sys.path.append(str((Path(__file__).parent / "..").resolve()))
from weltanschauung.cli import print_header
import watchgod


@dataclass
class CLICommand:
    command: List[str]

    def __call__(self):
        print(self.command)
        subprocess.run(self.command)


watch_path = Path(args.watch_path).absolute()
print_header(f"Starting on {watch_path}...")

command = CLICommand(command=args.command)

watch_iter = watchgod.watch(str(watch_path))
for _ in watch_iter:
    command()
