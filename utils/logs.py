import colorama
import sys


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
