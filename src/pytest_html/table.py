import re
import warnings
from dataclasses import dataclass
from dataclasses import field
from typing import Dict


@dataclass
class Table:
    """
    Class representing an HTML table
    """

    _html: field = field(default_factory=dict)

    @property
    def html(self) -> Dict:
        return self._html


@dataclass
class Html(Table):
    """
    Class representing an HTML document
    """

    _replace_log: bool = False

    def __post_init__(self) -> None:
        """
        Initializes the "html" key of _html with an empty list if it doesn't already exist
        """
        self.html.setdefault("html", [])

    def __delitem__(self, key: str):
        """
        This means the log should be removed
        """
        self._replace_log = True

    @property
    def replace_log(self) -> bool:
        return self._replace_log

    def append(self, html: str) -> None:
        """
        Appends the html parameter to the "html" key of _html
        """

        self.html["html"].append(html)


@dataclass
class Cell(Table):
    """
    Class representing a cell in an HTML table
    """

    _append_counter: int = 0
    _pop_counter: int = 0
    _sortables: field = field(default_factory=dict)

    def __setitem__(self, key: str, value: str) -> None:
        warnings.warn(
            "list-type assignment is deprecated and support "
            "will be removed in a future release. "
            "Please use 'insert()' instead.",
            DeprecationWarning,
        )
        self.insert(key, value)

    @property
    def sortables(self) -> dict:
        return self._sortables

    def append(self, html: str) -> None:
        """
        Appends the html parameter to the "html" key of _html
        """
        key = "Z" + str(self._append_counter)
        self.insert(key, html)
        self._append_counter += 1

    def insert(self, index: str, html: str) -> None:
        """
        Extracts any sortable data from the html parameter and stores it in the _sortables field
        before storing the html parameter in _html.
        """
        if not isinstance(html, str):
            html = self.check_html(html=html)

        self._extract_sortable(html)
        self._html[index] = html

    @staticmethod
    def check_html(html) -> str:
        """
        Replace any instances of "col=" with "data-column-type="
        """
        if html.__module__.startswith("py."):
            warnings.warn(
                "The 'py' module is deprecated and support "
                "will be removed in a future release.",
                DeprecationWarning,
            )
        html = str(html)
        html = html.replace("col=", "data-column-type=")
        return html

    def pop(self, *args) -> None:
        """
        Pops the item with the specified key from _html and increments _pop_counter
        """

        self._pop_counter += 1

    def get_pops(self) -> int:
        return self._pop_counter

    def _extract_sortable(self, html) -> None:
        """
        Extracts any sortable data from the html parameter and stores it  in the _sortables field.
        """

        match = re.search(r'<td class="col-(\w+)">(.*?)</', html)
        if match:
            sortable = match.group(1)
            value = match.group(2)
            self._sortables[sortable] = value


class Header(Cell):
    pass


class Row(Cell):
    def __delitem__(self, key: str) -> None:
        """
        This means the item should be removed
        """
        self._html = None

    def pop(self, *args):
        """
        Calling pop on header is sufficient
        """
        pass
