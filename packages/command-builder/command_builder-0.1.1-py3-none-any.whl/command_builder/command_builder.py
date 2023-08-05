"""Module containing the command builder."""
import subprocess
from typing import List


class BColors:
    """ANSI escape sequences."""

    SUCCEEDED = "\033[92m"
    WARNING = "\033[93m"
    FAILED = "\033[91m"
    END = "\033[0m"


class CommandBuilder:
    """Command Builder"""

    def __init__(self):
        self.commands = {}

    def add(self, name: str, command: List[str]):
        """Adds a command to the pipeline."""

        self.commands[name] = {"command": command}

    def _print_summary(self):
        """Print returncode commands."""

        print("_" * 30 + "summary" + "_" * 30)

        for name, command in self.commands.items():
            if command["returncode"] != 0:
                print(BColors.FAILED + f"ERROR: {name}: commands failed" + BColors.END)
            else:
                print(BColors.SUCCEEDED + f"{name}: commands succeeded" + BColors.END)

    @staticmethod
    def _run_command(command: List[str]):
        """Run a command."""

        run = subprocess.run(command, check=False, shell=False)
        return run.returncode

    def run(self, summary: bool = True):
        """Run commands and print summary."""

        for command in self.commands.values():
            command["returncode"] = self._run_command(command["command"])

        if summary:
            self._print_summary()
