"""Екран 'Про програму' з інформацією та міні-грою в одному вікні."""

import os
import sys

from core.theme import (
    TABLE_BORDER, MENU_TITLE, MENU_OPTION, MENU_KEY,
    HEADER, MUTED, RESET, clear_screen,
)


def _box_line(border, width, text, visible_len):
    """Формує рядок рамки з правильним відступом."""
    pad = width - visible_len
    return f"{border}║{RESET}{text}{' ' * pad}{border}║{RESET}"


def _render_about_box():
    """Повертає рядки інфо-блоку та їх кількість."""
    width = 44
    border = TABLE_BORDER

    authors = [
        "Дмитро Рубахін",
        "Оксана Хоменко",
        "Михайло Качанов",
        "Олександр Случ",
    ]

    lines = [
        f"{border}╔{'═' * width}╗{RESET}",
        f"{border}║{MENU_TITLE}{'Персональний помічник':^{width}}{RESET}{border}║{RESET}",
        f"{border}╠{'═' * width}╣{RESET}",
        f"{border}║{' ' * width}║{RESET}",
    ]

    info_items = [
        ("Версія:", "1.0"),
        ("Команда:", "TEAM-9"),
        ("Університет:", "Neoversity"),
    ]

    for label, value in info_items:
        text = f"   {MENU_KEY}{label}{RESET} {MENU_OPTION}{value}{RESET}"
        visible = 3 + len(label) + 1 + len(value)
        lines.append(_box_line(border, width, text, visible))

    lines.append(f"{border}║{' ' * width}║{RESET}")

    author_header = f"   {HEADER}Автори:{RESET}"
    lines.append(_box_line(border, width, author_header, 10))

    for author in authors:
        text = f"     {MUTED}• {author}{RESET}"
        visible = 5 + 2 + len(author)
        lines.append(_box_line(border, width, text, visible))

    lines.append(f"{border}║{' ' * width}║{RESET}")

    hint = "↑ стрибок | Space/ESC -> меню"
    hint_text = f" {MUTED}{hint}{RESET}"
    lines.append(_box_line(border, width, hint_text, 1 + len(hint)))

    lines.append(f"{border}╚{'═' * width}╝{RESET}")

    return lines


def show_about():
    """Відображає інформацію про програму з міні-грою під нею."""
    clear_screen()

    # Малюємо інфо-блок
    box_lines = _render_about_box()
    print("\n".join(box_lines))

    box_height = len(box_lines) + 1  # +1 для відступу

    # Запускаємо міні-гру в зоні під інфо-блоком
    from core.game import play_game
    play_game(top_offset=box_height)

    clear_screen()
