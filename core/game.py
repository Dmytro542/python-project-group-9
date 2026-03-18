"""Міні-гра в стилі Chrome Dino для термінала."""

import os
import sys
import time
import random


# ASCII-арт динозавра — компактний, два кадри анімації
DINO_FRAME_1 = [
    " ▓▓▓",
    " ▓░▓",
    "▓▓▓ ",
    " ▓ ▓",
]

DINO_FRAME_2 = [
    " ▓▓▓",
    " ▓░▓",
    "▓▓▓ ",
    "▓  ▓",
]

DINO_WIDTH = 4
DINO_HEIGHT = 4

# Варіанти кактусів — компактні
CACTUS_SMALL = [
    "▌▌",
    "▌▌",
]

CACTUS_TALL = [
    " ▌",
    "▌▌",
    "▌▌",
]

CACTUS_DOUBLE = [
    "▌ ▌",
    "▌▌▌",
]


def _kbhit():
    """Перевіряє чи натиснуто клавішу (неблокуюче)."""
    if os.name == "nt":
        import msvcrt
        return msvcrt.kbhit()
    else:
        import select
        return select.select([sys.stdin], [], [], 0)[0] != []


def _read_key():
    """Зчитує натискання клавіші та повертає код."""
    if os.name == "nt":
        import msvcrt
        key = msvcrt.getch()
        if key in (b'\x00', b'\xe0'):
            key = msvcrt.getch()
            if key == b'H':
                return "UP"
            return None
        elif key == b' ':
            return "SPACE"
        elif key == b'\r':
            return "ENTER"
        elif key == b'\x1b':
            return "ESC"
        # R/r латиниця + К/к кирилиця (та сама фізична клавіша)
        elif key in (b'r', b'R', b'\xea', b'\xca'):
            return "R"
        # Q/q латиниця + Й/й кирилиця
        elif key in (b'q', b'Q', b'\xe9', b'\xc9'):
            return "Q"
        return None
    else:
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            # Чекаємо трохи на решту escape-послідовності (стрілки)
            import select
            ready, _, _ = select.select([sys.stdin], [], [], 0.05)
            if ready:
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ready2, _, _ = select.select([sys.stdin], [], [], 0.05)
                    if ready2:
                        ch3 = sys.stdin.read(1)
                        if ch3 == 'A':
                            return "UP"
            return "ESC"
        elif ch == ' ':
            return "SPACE"
        elif ch == '\r' or ch == '\n':
            return "ENTER"
        elif ch in ('r', 'R', 'к', 'К'):
            return "R"
        elif ch in ('q', 'Q', 'й', 'Й'):
            return "Q"
        return None


def _flush_input():
    """Очищує буфер вводу."""
    if os.name == "nt":
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        while _kbhit():
            _read_key()


def _wait_key():
    """Блокуюче очікування натискання клавіші."""
    if os.name == "nt":
        import msvcrt
        key = msvcrt.getch()
        if key in (b'\x00', b'\xe0'):
            msvcrt.getch()
            return None
        # R/r латиниця + К/к кирилиця (та сама фізична клавіша)
        if key in (b'r', b'R', b'\xea', b'\xca'):
            return "R"
        return "OTHER"
    else:
        ch = sys.stdin.read(1)
        if ch in ('r', 'R', 'к', 'К'):
            return "R"
        return "OTHER"


def play_game(top_offset=0):
    """Запускає міні-гру Dino Run в зоні від top_offset до низу екрану."""
    try:
        from core.theme import (
            MATRIX_GREEN, MATRIX_BRIGHT,
            SUCCESS, ERROR, HEADER, MUTED, MENU_KEY,
            TABLE_BORDER, RESET,
        )
    except ImportError:
        return

    try:
        size = os.get_terminal_size()
        cols, rows = size.columns, size.lines
    except OSError:
        cols, rows = 80, 24

    # Ігрова зона: від top_offset до rows
    game_rows = rows - top_offset
    if cols < 40 or game_rows < 10:
        print("\n  Збільшіть вікно терміналу для запуску гри.")
        try:
            input("  Натисніть Enter...")
        except (KeyboardInterrupt, EOFError):
            pass
        return

    # Налаштування гри відносно ігрової зони
    ground_row = top_offset + game_rows - 3
    dino_col = 5
    dino_base_row = ground_row - DINO_HEIGHT

    # Рядок для рахунку
    score_row = top_offset + 1

    # Стан гри
    score = 0
    speed = 1.0
    jump_velocity = 0.0
    jump_height = 0.0
    is_jumping = False
    game_over = False
    frame_count = 0

    # Перешкоди
    obstacles = []
    cactus_types = [CACTUS_SMALL, CACTUS_TALL, CACTUS_DOUBLE]
    next_obstacle_timer = 30

    # Встановлюємо raw-режим для Unix
    old_settings = None
    if os.name != "nt":
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)

    # Приховати курсор
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    # Очистити буфер вводу (залишки від набору команди)
    time.sleep(0.15)
    _flush_input()

    try:
        while not game_over:
            frame_count += 1

            # Обробка вводу
            while _kbhit():
                key = _read_key()
                if key in ("UP", "SPACE") and not is_jumping:
                    is_jumping = True
                    jump_velocity = -2.5
                elif key in ("ESC", "Q"):
                    _restore_terminal(old_settings)
                    return

            # Фізика стрибка
            if is_jumping:
                jump_height += jump_velocity
                jump_velocity += 0.35  # гравітація
                if jump_height >= 0:
                    jump_height = 0
                    is_jumping = False
                    jump_velocity = 0

            # Рух перешкод
            step = 1 + int(speed * 0.5)
            obstacles = [
                (c - step, cactus) for c, cactus in obstacles if c - step > -6
            ]

            # Генерація нових перешкод
            next_obstacle_timer -= 1
            if next_obstacle_timer <= 0:
                cactus = random.choice(cactus_types)
                obstacles.append((cols - 1, cactus))
                gap_min = max(15, 35 - int(speed * 3))
                gap_max = max(25, 50 - int(speed * 3))
                next_obstacle_timer = random.randint(gap_min, gap_max)

            # Позиція динозавра
            dino_row = dino_base_row + int(jump_height)
            dino_bottom = dino_row + DINO_HEIGHT - 1

            # Перевірка колізій
            for obs_col, cactus in obstacles:
                cactus_height = len(cactus)
                cactus_width = max(len(line) for line in cactus)
                cactus_top = ground_row - cactus_height

                if (dino_col + DINO_WIDTH - 1 >= obs_col and
                    dino_col <= obs_col + cactus_width - 1 and
                    dino_bottom >= cactus_top):
                    game_over = True
                    break

            # Рахунок та складність
            score += 1
            if frame_count % 100 == 0:
                speed += 0.3

            # Рендеринг
            output = []

            # Рахунок (перший рядок ігрової зони)
            score_text = f" Рахунок: {score}"
            output.append(f"\033[{score_row};1H{HEADER}{score_text}{RESET}\033[K")

            # Очищення ігрової зони (крім рядка рахунку)
            for r in range(score_row + 1, ground_row + 2):
                output.append(f"\033[{r};1H\033[2K")

            # Малюємо динозавра
            dino_frame = DINO_FRAME_1 if (frame_count // 5) % 2 == 0 else DINO_FRAME_2
            if is_jumping:
                dino_frame = DINO_FRAME_1

            for i, line in enumerate(dino_frame):
                r = dino_row + i
                if score_row < r < ground_row:
                    output.append(
                        f"\033[{r + 1};{dino_col + 1}H{MATRIX_BRIGHT}{line}{RESET}"
                    )

            # Малюємо перешкоди
            for obs_col, cactus in obstacles:
                cactus_height = len(cactus)
                for i, line in enumerate(cactus):
                    r = ground_row - cactus_height + i
                    if score_row < r < ground_row and 0 < obs_col < cols - 3:
                        output.append(
                            f"\033[{r + 1};{obs_col + 1}H{MATRIX_GREEN}{line}{RESET}"
                        )

            # Малюємо землю
            ground = "▔" * cols
            output.append(f"\033[{ground_row + 1};1H{MUTED}{ground}{RESET}")

            sys.stdout.write("".join(output))
            sys.stdout.flush()
            time.sleep(0.05)

        # Кінець гри — очищуємо буфер та показуємо Game Over
        time.sleep(0.2)
        _flush_input()

        _show_game_over(score, cols, top_offset, game_rows)

        # Блокуюче очікування: R — перегра, інше — вихід
        choice = _wait_key()
        if choice == "R":
            # Перезапуск без виходу з raw-режиму
            play_game(top_offset=top_offset)
            return

    finally:
        _restore_terminal(old_settings)


def _show_game_over(score, cols, top_offset, game_rows):
    """Відображає Game Over по центру ігрової зони."""
    try:
        from core.theme import (
            ERROR, SUCCESS, HEADER, MUTED, MENU_KEY,
            TABLE_BORDER, RESET,
        )
    except ImportError:
        return

    w = 30
    b = TABLE_BORDER

    def pad_line(text, visible_len):
        """Рядок рамки з правильним відступом."""
        return f"{b}║{RESET}{text}{' ' * (w - visible_len)}{b}║{RESET}"

    score_str = str(score)

    lines = [
        f"{b}╔{'═' * w}╗{RESET}",
        f"{b}║{ERROR}{'GAME OVER':^{w}}{RESET}{b}║{RESET}",
        f"{b}╠{'═' * w}╣{RESET}",
        pad_line(f"  {HEADER}Рахунок: {SUCCESS}{score_str}{RESET}", 2 + 9 + len(score_str)),
        f"{b}║{' ' * w}{b}║{RESET}",
        pad_line(f"  {MENU_KEY}[R]{RESET} {MUTED}Грати знову{RESET}", 2 + 3 + 1 + 11),
        pad_line(f"  {MUTED}Інша клавіша — вихід{RESET}", 2 + 20),
        f"{b}╚{'═' * w}╝{RESET}",
    ]

    mid_row = top_offset + game_rows // 2 - len(lines) // 2
    mid_col = (cols - w - 2) // 2

    for i, line in enumerate(lines):
        sys.stdout.write(f"\033[{mid_row + i + 1};{mid_col + 1}H{line}")
    sys.stdout.flush()


def _restore_terminal(old_settings):
    """Відновлює налаштування терміналу."""
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

    if old_settings is not None:
        import termios
        fd = sys.stdin.fileno()
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
