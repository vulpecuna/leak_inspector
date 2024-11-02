import colorama
import json
import os
import time
import sys


def save_log(log_file_path, data, delay):
    ok(f"Fetched {log_file_path}.")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    with open(log_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    time.sleep(1)


def _print(color, symbol, message):
    print(color + symbol + ' ' + colorama.Style.BRIGHT, end="")
    print(message, end="")
    print(colorama.Fore.RESET)


def error(message, should_exit=False):
    _print(colorama.Fore.RED, '[!]', message)
    if should_exit:
        sys.exit(1)


def warning(message):
    _print(colorama.Fore.YELLOW, '[!]', message)


def ok(message):
    _print(colorama.Fore.GREEN, '[+]', message)


def info(message):
    _print(colorama.Fore.BLUE, '[>]', message)
