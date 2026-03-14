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


import unicodedata


def _display_width(text: str) -> int:
    """Обчислює візуальну ширину рядка в терміналі (wide chars = 2)."""
    width = 0
    for ch in text:
        cat = unicodedata.category(ch)
        if cat == "Mn":  # combining marks — zero width
            continue
        eaw = unicodedata.east_asian_width(ch)
        if eaw in ("W", "F"):
            width += 2
        elif cat == "So":  # symbols like emoji
            width += 2
        else:
            width += 1
    return width


def _pad(text: str, target_width: int) -> str:
    """Доповнює рядок пробілами до потрібної візуальної ширини."""
    current = _display_width(text)
    return text + " " * max(0, target_width - current)


def render_table(columns: list[str], rows: list[list[str]], title: str = "") -> str:
    """Малює таблицю з рамкою та кольоровими заголовками.

    columns: список назв колонок
    rows: список рядків (кожен — список значень)
    title: опційний заголовок над таблицею
    """
    if not rows:
        return ""

    # Обчислюємо ширину кожної колонки (візуальну)
    col_widths = [_display_width(c) for c in columns]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], _display_width(cell))

    lines = []

    if title:
        lines.append(f"  {HEADER}{title}{RESET}")

    # Верхня рамка
    top = f"{TABLE_BORDER}┌"
    for i, w in enumerate(col_widths):
        top += "─" * (w + 2)
        top += "┬" if i < len(col_widths) - 1 else "┐"
    lines.append(f"{top}{RESET}")

    # Заголовки колонок
    hdr = f"{TABLE_BORDER}│"
    for i, col in enumerate(columns):
        hdr += f" {TABLE_HEADER}{_pad(col, col_widths[i])}{RESET} {TABLE_BORDER}│"
    lines.append(f"{hdr}{RESET}")

    # Розділювач
    sep = f"{TABLE_BORDER}├"
    for i, w in enumerate(col_widths):
        sep += "─" * (w + 2)
        sep += "┼" if i < len(col_widths) - 1 else "┤"
    lines.append(f"{sep}{RESET}")

    # Рядки даних
    for row in rows:
        line = f"{TABLE_BORDER}│{RESET}"
        for i, w in enumerate(col_widths):
            cell = row[i] if i < len(row) else ""
            line += f" {_pad(cell, w)} {TABLE_BORDER}│{RESET}"
        lines.append(line)

    # Нижня рамка
    bot = f"{TABLE_BORDER}└"
    for i, w in enumerate(col_widths):
        bot += "─" * (w + 2)
        bot += "┴" if i < len(col_widths) - 1 else "┘"
    lines.append(f"{bot}{RESET}")

    return "\n".join(lines)
