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
import os
import sys
import webbrowser
from itertools import groupby
from pathlib import Path

from loguru import logger

from src.template import Template
from src.utils import slugify, remove_dash_values
from src.xls_file import XLSFile


ROOT_DIR = Path(os.path.dirname(sys.argv[0]))
LOGGER_PATH = ROOT_DIR / "conceptz.log"
HTML_DIR = ROOT_DIR / "html"


logger.add(LOGGER_PATH, format="{time} | {level} | {message}", level="INFO")
os.makedirs(HTML_DIR, exist_ok=True)


class App:

    def __init__(self, xls_path: Path) -> None:
        self._xls = XLSFile(xls_path)

    def create_html_for_concept(self, template: str, concept: str) -> Path:

        concept_row = self._xls.search("Concepts", key="Name", value=concept, only_first=True)[0]
        concept_id = concept_row["ID"]
        info_rows = self._xls.search("Info", key="Concept ID", value=concept_id)
        remove_dash_values([concept_row] + info_rows)

        info_groups = [
            {
                "section": key,
                "info": list(group)
            }
            for key, group in groupby(info_rows, key=lambda x: x["Section"])
        ]

        template_path = ROOT_DIR / template
        rendered_html = Template(template_path).render(concept=concept_row, info_groups=info_groups)
        html_path = HTML_DIR / f"{slugify(concept)}.html"
        with open(html_path, "w", encoding="utf-8") as file:
            file.write(rendered_html)

        return html_path

    def create_html_for_section(self, template: str, section: str) -> Path:

        info_rows = self._xls.search("Info", key="Section", value=section)
        remove_dash_values(info_rows)

        template_path = ROOT_DIR / template
        rendered_html = Template(template_path).render(section=section, info=info_rows)
        html_path = HTML_DIR / f"{slugify(section)}.html"
        with open(html_path, "w", encoding="utf-8") as file:
            file.write(rendered_html)

        return html_path


@logger.catch
def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument("xls_path", type=str)
    parser.add_argument("-t", "--template", type=str)
    parser.add_argument("-c", "--concept",  type=str)
    parser.add_argument("-s", "--section", type=str)
    args = parser.parse_args()

    app = App(Path(args.xls_path))
    if args.concept:
        html_path = app.create_html_for_concept(args.template, args.concept)
        webbrowser.open(str(html_path), new=2)
    if args.section:
        html_path = app.create_html_for_section(args.template, args.section)
        webbrowser.open(str(html_path), new=2)


if __name__ == '__main__':
    main()


# debug
# C:\Users\Denis\PythonProjects\conceptz\venv\Scripts\python C:\Users\Denis\PythonProjects\conceptz\src\main.py C:\Users\Denis\Desktop\CONCEPTZ\conceptz.xlsm --template "concept.html" --concept "Orchestration"
# C:\Users\Denis\PythonProjects\conceptz\venv\Scripts\python C:\Users\Denis\PythonProjects\conceptz\src\main.py C:\Users\Denis\Desktop\CONCEPTZ\conceptz.xlsm --template "section.html" --section "69 Producer Hacks in 420 Seconds , Ep 02"
# C:\Users\Denis\Desktop\CONCEPTZ\conceptz.exe C:\Users\Denis\Desktop\CONCEPTZ\conceptz.xlsm --template "concept.html" --concept "Orchestration"
# C:\Users\Denis\Desktop\CONCEPTZ\conceptz.exe C:\Users\Denis\Desktop\CONCEPTZ\conceptz.xlsm --template "section.html" --section "69 Producer Hacks in 420 Seconds , Ep 02"

