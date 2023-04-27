import warnings
from collections import defaultdict

from pytest_html.helpful_functions import _process_logs
from pytest_html.util import _handle_ansi


class ReportData:
    """
    A class for storing report data in dictionary format.
    """

    def __init__(self, title, config):
        self._config = config
        self._data = {
            "title": title,
            "collectedItems": 0,
            "runningState": "not_started",
            "environment": {},
            "tests": defaultdict(list),
            "resultsTableHeader": {},
            "additionalSummary": defaultdict(list),
        }

        collapsed = config.getini("render_collapsed")
        if collapsed:
            if collapsed.lower() == "true":
                warnings.warn(
                    "'render_collapsed = True' is deprecated and support "
                    "will be removed in the next major release. "
                    "Please use 'render_collapsed = all' instead.",
                    DeprecationWarning,
                )
            self.set_data(
                "collapsed", [outcome.lower() for outcome in collapsed.split(",")]
            )

    @property
    def title(self) -> str:
        """
        Returns the current title of the report.
        """
        return self._data["title"]

    @title.setter
    def title(self, title: str) -> None:
        """
        Sets the title of the report to a new string.
        """
        self._data["title"] = title

    @property
    def config(self):
        """
        Returns the current pytest configuration object.
        """
        return self._config

    @property
    def data(self) -> dict:
        """
        Returns the current report data dictionary.
        """
        return self._data

    def set_data(self, key, value) -> None:
        self._data[key] = value

    def add_test(self, test_data, report, row, remove_log=False) -> bool:
        """
        Adds the information for a test to the report data dictionary.
        """
        for sortable, value in row.sortables.items():
            test_data[sortable] = value

        # regardless of pass or fail we must add teardown logging to "call"
        if report.when == "teardown" and not remove_log:
            self.update_test_log(report)

        # passed "setup" and "teardown" are not added to the html
        if report.when == "call" or (
            report.when in ["setup", "teardown"] and report.outcome != "passed"
        ):
            if not remove_log:
                processed_logs = _process_logs(report)
                test_data["log"] = _handle_ansi(processed_logs)
            self._data["tests"][report.nodeid].append(test_data)
            return True

        return False

    def update_test_log(self, report) -> None:
        """
        Adds the log for a test to the report data dictionary.
        """
        log = []
        for test in self._data["tests"][report.nodeid]:
            if test["testId"] == report.nodeid and "log" in test:
                for section in report.sections:
                    header, content = section
                    if "teardown" in header:
                        log.append(f"{' ' + header + ' ':-^80}")
                        log.append(content)
                test["log"] += _handle_ansi("\n".join(log))
