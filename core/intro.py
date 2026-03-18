import os
import sys
import time
import random


def _kbhit():
    """Перевіряє чи натиснуто клавішу (неблокуюче)."""
    if os.name == "nt":
        import msvcrt
        return msvcrt.kbhit()
    else:
        import select
        return select.select([sys.stdin], [], [], 0)[0] != []


def _read_key():
    """Зчитує одне натискання клавіші."""
    if os.name == "nt":
        import msvcrt
        return msvcrt.getch()
    else:
        return sys.stdin.read(1)


def _maximize_terminal():
    """Розгортає вікно терміналу кількома методами."""
    if os.name == "nt":
        try:
            # Метод 1: Win32 API розгортання
            import ctypes
            kernel32 = ctypes.windll.kernel32
            user32 = ctypes.windll.user32
            hwnd = kernel32.GetConsoleWindow()
            if hwnd:
                user32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE
                time.sleep(0.15)
        except Exception:
            pass
        try:
            # Метод 2: mode con для макс. буфера
            size = os.get_terminal_size()
            os.system(f"mode con: cols={size.columns} lines={size.lines} >nul 2>&1")
        except Exception:
            pass
    else:
        # xterm повноекранний escape
        sys.stdout.write("\033[9;1t")
        sys.stdout.flush()
        time.sleep(0.15)


def play_intro():
    """Анімація Matrix rain з водоспадом NEOVERSITY."""
    try:
        _maximize_terminal()
        time.sleep(0.1)

        size = os.get_terminal_size()
        cols, rows = size.columns, size.lines
    except OSError:
        return

    if cols < 20 or rows < 10:
        return

    try:
        from core.theme import MATRIX_GREEN, MATRIX_BRIGHT, MATRIX_DIM, RESET, clear_screen

        clear_screen()

        title = "TEAM-9"
        subtitle = "Бот-помічник"
        title_row = rows // 2 - 1
        title_col = (cols - len(title)) // 2
        sub_row = title_row + 1
        sub_col = (cols - len(subtitle)) // 2
        hint = "Натисніть будь-яку клавішу..."
        hint_row = sub_row + 3
        hint_col = (cols - len(hint)) // 2

        # Захищена зона навколо тексту заголовка
        protected_top = title_row - 1
        protected_bottom = hint_row + 1
        protected_left = min(title_col, sub_col, hint_col) - 2
        protected_right = max(
            title_col + len(title),
            sub_col + len(subtitle),
            hint_col + len(hint),
        ) + 2

        neo_word = "YTISREVOEN"  # NEOVERSITY задом наперед — читається знизу вгору

        # Побудова колонок — 25% випадкові символи, 75% краплі NEOVERSITY
        chars = "01" + "アイウエオカキクケコサシスセソ" + "╋╊╉╈┿┽"
        all_cols = list(range(cols))
        random.shuffle(all_cols)
        neo_col_set = set(all_cols[: cols * 3 // 4])

        columns = []
        for c in range(cols):
            is_neo = c in neo_col_set
            columns.append({
                "row": random.randint(-rows, 0),
                "speed": 1 if is_neo else random.randint(1, 3),
                "trail": random.randint(6, 14) if is_neo else random.randint(3, 8),
                "active": random.random() < 0.5,
                "neo": is_neo,
                "neo_offset": random.randint(0, len(neo_word) - 1) if is_neo else 0,
            })

        # Приховати курсор
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

        def in_protected(r, c):
            return (protected_top <= r <= protected_bottom
                    and protected_left <= c <= protected_right)

        while True:
            output = []

            for c_idx, col in enumerate(columns):
                if not col["active"]:
                    if random.random() < 0.06:
                        col["active"] = True
                        col["row"] = random.randint(-5, 0)
                    continue

                head = col["row"]
                tail_start = head - col["trail"]
                is_neo = col["neo"]

                # Головний символ (найяскравіший)
                if 0 <= head < rows and not in_protected(head, c_idx):
                    if is_neo:
                        ch = neo_word[(head + col["neo_offset"]) % len(neo_word)]
                    else:
                        ch = random.choice(chars)
                    output.append(f"\033[{head + 1};{c_idx + 1}H{MATRIX_BRIGHT}{ch}")

                # Тіло (звичайний зелений)
                if 0 <= head - 1 < rows and not in_protected(head - 1, c_idx):
                    if is_neo:
                        ch = neo_word[(head - 1 + col["neo_offset"]) % len(neo_word)]
                    else:
                        ch = random.choice(chars)
                    output.append(f"\033[{head};{c_idx + 1}H{MATRIX_GREEN}{ch}")

                # Хвіст (тьмяний)
                if 0 <= tail_start < rows and not in_protected(tail_start, c_idx):
                    if is_neo:
                        ch = neo_word[(tail_start + col["neo_offset"]) % len(neo_word)]
                    else:
                        ch = random.choice(chars)
                    output.append(f"\033[{tail_start + 1};{c_idx + 1}H{MATRIX_DIM}{ch}")

                # Стерти за хвостом
                if 0 <= tail_start - 1 < rows and not in_protected(tail_start - 1, c_idx):
                    output.append(f"\033[{tail_start};{c_idx + 1}H {RESET}")

                col["row"] += col["speed"]

                # Скинути колонку коли за межами екрану
                if tail_start > rows:
                    col["active"] = random.random() < 0.4
                    col["row"] = random.randint(-8, 0)
                    col["speed"] = 1 if is_neo else random.randint(1, 3)
                    col["trail"] = random.randint(6, 14) if is_neo else random.randint(3, 8)
                    if is_neo:
                        col["neo_offset"] = random.randint(0, len(neo_word) - 1)

            # Заголовок з ефектом світіння
            glow = "\033[1;97m" if int(time.time() * 4) % 2 == 0 else MATRIX_BRIGHT
            output.append(f"\033[{title_row + 1};{title_col + 1}H{glow}{title}{RESET}")

            # Підзаголовок
            output.append(f"\033[{sub_row + 1};{sub_col + 1}H{MATRIX_GREEN}{subtitle}{RESET}")

            # Блимаюча підказка
            if int(time.time() * 2) % 2 == 0:
                output.append(f"\033[{hint_row + 1};{hint_col + 1}H{MATRIX_DIM}{hint}{RESET}")
            else:
                output.append(f"\033[{hint_row + 1};{hint_col + 1}H{' ' * len(hint)}")

            sys.stdout.write("".join(output))
            sys.stdout.flush()
            time.sleep(0.045)

            if _kbhit():
                _read_key()
                break

        # Показати курсор та очистити
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        clear_screen()

    except Exception:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        try:
            from core.theme import clear_screen
            clear_screen()
        except Exception:
            pass
