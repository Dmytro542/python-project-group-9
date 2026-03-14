def parse_input(user_input: str) -> tuple[str | None, list[str]]:
    parts = user_input.strip().split()
    if not parts:
        return None, []
    return parts[0].lower(), parts[1:]
