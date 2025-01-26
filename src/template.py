from pathlib import Path
from typing import Optional

from jinja2 import Template as JinjaTemplate
from jinja2.filters import FILTERS


def format_mailru_screenshoter_link(value: Optional[str]) -> Optional[str]:
    """ Для Screenshoter Mail.ru - делает прямые ссылки на скриншоты """
    if value is None:
        return value
    if "mail.ru" not in value:
        return value
    xxxx, yyyyyyyyy = value.split('/')[-2:]
    return f"https://thumb.cloud.mail.ru/weblink/thumb/xw1/{xxxx}/{yyyyyyyyy}"


def join_timestamp(args: list[Optional[str]]) -> Optional[str]:
    link, timestamp = args
    if not link:
        return link
    if not timestamp:
        return link
    if "?" not in link:
        return f"{link}?t={timestamp}"
    else:
        return f"{link}&t={timestamp}"


def format_timestamp(timestamp: Optional[str]) -> Optional[str]:

    if not timestamp:
        return timestamp

    h, _, timestamp = timestamp.rpartition("h")
    m, _, timestamp = timestamp.rpartition("m")
    s, _, timestamp = timestamp.partition("s")

    h, m, s = int(h or 0), int(m or 0), int(s or 0)
    S = s + 60 * m + 60 * 60 * h

    s = S % 60
    M = S // 60
    m = M % 60
    h = M // 60

    if h:
        return ":".join([str(h), str(m).zfill(2), str(s).zfill(2)])
    else:
        return ":".join([str(m), str(s).zfill(2)])


FILTERS["mailru"] = format_mailru_screenshoter_link
FILTERS["jointime"] = join_timestamp
FILTERS["timestamp"] = format_timestamp


class Template:

    def __init__(self, html_path: Path) -> None:
        with open(html_path, "r", encoding="utf-8") as file:
            self._template_html = file.read()

    def render(self, **kwargs) -> str:
        return JinjaTemplate(self._template_html).render(**kwargs)
