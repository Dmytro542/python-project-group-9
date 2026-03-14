from colorama import init, Fore, Style

import sys
import os

# Ensure UTF-8 output on Windows
if os.name == "nt":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

init(autoreset=True)

# Color constants
HEADER = Fore.MAGENTA + Style.BRIGHT
SUCCESS = Fore.GREEN + Style.BRIGHT
ERROR = Fore.RED + Style.BRIGHT
WARNING = Fore.YELLOW + Style.BRIGHT
INFO = Fore.CYAN
PROMPT = Fore.YELLOW + Style.BRIGHT
MUTED = Fore.WHITE + Style.DIM
RESET = Style.RESET_ALL

MENU_TITLE = Fore.GREEN + Style.BRIGHT
MENU_OPTION = Fore.CYAN
MENU_KEY = Fore.YELLOW + Style.BRIGHT

TABLE_HEADER = Fore.CYAN + Style.BRIGHT
TABLE_BORDER = Fore.CYAN
TABLE_SEP = Fore.WHITE + Style.DIM

MATRIX_GREEN = Fore.GREEN
MATRIX_BRIGHT = Fore.GREEN + Style.BRIGHT
MATRIX_DIM = Fore.GREEN + Style.DIM


def success(msg: str) -> str:
    return f"{SUCCESS}[OK] {msg}{RESET}"


def error(msg: str) -> str:
    return f"{ERROR}[X] {msg}{RESET}"


def info(msg: str) -> str:
    return f"{INFO}[i] {msg}{RESET}"


def warning(msg: str) -> str:
    return f"{WARNING}[!] {msg}{RESET}"


def header(msg: str) -> str:
    return f"{HEADER}{msg}{RESET}"


def clear_screen():
    import os
    os.system("cls" if os.name == "nt" else "clear")


def render_menu(title: str, options: list[tuple[str, str]]) -> str:
    """Малює красиве меню з рамкою."""
    width = 40
    border = TABLE_BORDER
    lines = [
        f"{border}╔{'═' * width}╗{RESET}",
        f"{border}║{MENU_TITLE}{title:^{width}}{RESET}{border}║{RESET}",
        f"{border}╠{'═' * width}╣{RESET}",
        f"{border}║{' ' * width}║{RESET}",
    ]
    for key, label in options:
        inner = f"   {MENU_KEY}[{key}]{RESET}  {MENU_OPTION}{label}{RESET}"
        # padding: key + label visible length
        pad = width - 5 - len(key) - 2 - len(label)
        lines.append(f"{border}║{RESET}{inner}{' ' * pad}{border}║{RESET}")
    lines.append(f"{border}║{' ' * width}║{RESET}")
    lines.append(f"{border}╚{'═' * width}╝{RESET}")
    return "\n".join(lines)


def mode_header(title: str) -> str:
    """Заголовок при вході в режим."""
    line = f"{TABLE_BORDER}{'─' * 40}{RESET}"
    return f"\n{line}\n  {HEADER}{title}{RESET}\n  {MUTED}help — команди  |  back — меню{RESET}\n{line}"
