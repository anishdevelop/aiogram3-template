import html
from typing import Any


def escape(txt: Any) -> str:
    return html.escape(str(txt))
