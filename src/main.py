"""
Show the Developer tab
https://support.microsoft.com/en-us/office/show-the-developer-tab-e1192344-5e56-4d45-931b-e5fd9bea2d45

Excel VBA - Double Click
https://www.youtube.com/watch?v=vFd2vZw4yJ0

Execute Shell Commands from Excel Cell
https://superuser.com/questions/1220696/execute-shell-commands-from-excel-cell

Python : Reading Large Excel Worksheets using Openpyxl
https://stackoverflow.com/questions/31189727/python-reading-large-excel-worksheets-using-openpyxl
"""

import argparse
import itertools
import os
import sys
import webbrowser
from pathlib import Path
from typing import Optional

from loguru import logger

from src.template import Template
from src.utils.misc import slugify
from src.utils.xls_file import XLSFile


ROOT_DIR = Path(os.path.dirname(sys.argv[0]))  # .exe filepath
APP_DIR = Path.home() / "AppData" / "Local" / "conceptz"
TEMP_DIR = Path.home() / "AppData" / "Local" / "Temp" / "conceptz"
os.makedirs(APP_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

LOGGER_PATH = APP_DIR / "conceptz.log"
logger.add(LOGGER_PATH, format="{time} | {level} | {message}", level="INFO")


def collect_info(xls_path: Path, key: str, value: str, groupby: Optional[str] = None) -> list:
    xls = XLSFile(xls_path)
    data = xls.search("Info", key=key, value=value)
    if not groupby:
        return data
    data.sort(key=lambda x: x[groupby] or "")
    return [
        {
            groupby: group_key,
            "Info": list(group)
        }
        for group_key, group in itertools.groupby(data, key=lambda x: x[groupby])
    ]


def create_html(template_path: Path, value: str, data: list) -> Path:
    rendered_html = Template(template_path).render(value=value, data=data)
    html_path = TEMP_DIR / f"{slugify(value)}.html"
    with open(html_path, "w", encoding="utf-8") as file:
        file.write(rendered_html)
    return html_path


@logger.catch
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("xls_path", type=str)
    parser.add_argument("-t", "--template", type=str)
    parser.add_argument("-k", "--key",  type=str)
    parser.add_argument("-v", "--value", type=str)
    parser.add_argument("-g", "--groupby", type=str)
    args = parser.parse_args()

    data = collect_info(
        xls_path=Path(args.xls_path),
        key=args.key,
        value=args.value,
        groupby=args.groupby
    )
    html_path = create_html(
        template_path=(ROOT_DIR / args.template),
        value=args.value,
        data=data
    )
    webbrowser.open(str(html_path), new=2)


if __name__ == '__main__':
    main()
