import os
import re

# Attributes code
from edos.settings import conf

ATTRIBUTES = dict(
    list(
        zip(
            [
                "bold",
                "dark",
                "",
                "underline",
                "blink",
            ],
            list(range(1, 6)),
        )
    )
)
del ATTRIBUTES[""]
ATTRIBUTES_RE = "\033\[(?:%s)m" % "|".join(["%d" % v for v in ATTRIBUTES.values()])

# Colors code
COLORS = dict(
    list(
        zip(
            [
                "grey",
                "red",
                "green",
                "yellow",
                "blue",
                "magenta",
                "cyan",
                "white",
            ],
            list(range(30, 38)),
        )
    )
)
COLORS_RE = "\033\[(?:%s)m" % "|".join(["%d" % v for v in COLORS.values()])

# Reset code
RESET = "\033[0m"
RESET_RE = "\033\[0m"


def colored(text, color=None, attrs=None):
    if text:
        text = str(text)
    if color:
        color = str(color).lower().strip()
    if os.getenv("ANSI_COLORS_DISABLED") is None and conf.INTERACTIVE:
        fmt_str = "\033[%dm%s"
        if color is not None:
            text = re.sub(COLORS_RE + "(.*?)" + RESET_RE, r"\1", text)
            text = fmt_str % (COLORS[color], text)
        if attrs is not None:
            text = re.sub(ATTRIBUTES_RE + "(.*?)" + RESET_RE, r"\1", text)
            for attr in attrs:
                text = fmt_str % (ATTRIBUTES[attr], text)
        return text + RESET
    else:
        return text
