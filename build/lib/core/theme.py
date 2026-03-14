from colorama import init, Fore, Style

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
