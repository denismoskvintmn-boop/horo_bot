import html


def escape_user_input(text: str) -> str:
    """Escape user input for safe HTML rendering in Telegram."""
    return html.escape(text)
