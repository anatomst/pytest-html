from unittest.mock import Mock

import pytest

from pytest_html.report_data import _process_logs
from pytest_html.report_data import ReportData
from pytest_html.table import Row
from pytest_html.util import _handle_ansi


class TestReportData:
    @pytest.fixture(autouse=True)
    def _setup_method(self) -> None:
        self.config = Mock()
        self.title = "test_title"
        self.config.getini.return_value = "Html"

    @pytest.fixture
    def report_data(self):
        return ReportData(self.title, self.config)

    @pytest.fixture
    def test_data(self):
        return {
            "testId": "test_id",
            "name": "test_example",
            "status": "passed",
            "time": 0.001,
            "log": "",
            "extra": {},
        }

    def test_set_data(self):
        report = ReportData(self.title, self.config)
        report.set_data("test_key", 1)

        assert report.data["test_key"] == 1

    def test_report_data_init(self, report_data):
        assert report_data._config

    def test_report_data_title(self, report_data):
        assert report_data.title == "test_title"
        report_data.title = "Updated title"
        assert report_data._data["title"] == "Updated title"

    @pytest.mark.parametrize(
        "values, expect",
        [
            ["Html", "html"],
            ["false", "false"],
        ],
    )
    def test__handle_render_collapsed__success(self, values, expect):
        self.config.getini.return_value = values
        report = ReportData(self.title, self.config)

        assert report.title == self.title
        assert expect in report.data["collapsed"]

    def test_report_data_set_data(self, report_data):
        report_data.set_data("some_key", "some_value")
        assert report_data._data["some_key"] == "some_value"

    def test_report_data_update_test_log(self, report_data, test_data):
        report = Mock()
        report.when = "teardown"
        report.longreprtext = "Some long error message."
        report.sections = [("section_1", "Some log."), ("teardown", "Some teardown.")]
        test_data["log"] = _handle_ansi("Some log.\n")
        report_data._data["tests"][test_data["testId"]] = [test_data]
        report_data.update_test_log(report)
        assert report_data._data["tests"][test_data["testId"]][0][
            "log"
        ] == _handle_ansi("Some log.\n")

    def test__process_logs(self):
        report = Mock()
        report.longreprtext = "Some long error message."
        report.sections = [("section_1", "Some log."), ("teardown", "Some teardown.")]
        assert (
            _process_logs(report) == "Some long error message.\n"
            "\n"
            "---------------------------------- section_1 "
            "-----------------------------------\n"
            "Some log.\n"
            "----------------------------------- teardown "
            "-----------------------------------\n"
            "Some teardown."
        )

    @pytest.mark.parametrize(
        "when, longreprtext, outcome, expect",
        [
            ["call", "test", "", True],
            ["call", "<test>", "", True],
            ["teardown", "error", "", True],
            ["teardown", "tt", "passed", False],
            ["setup", "", "", True],
        ],
    )
    def test_add_test(self, when, longreprtext, outcome, expect):
        test_data = {"result": "Passed"}
        row = Row()
        report = Mock(spec=["when", "longreprtext", "sections", "nodeid"])
        report.when = when
        report.longreprtext = longreprtext
        report.outcome = outcome
        report.sections = [("header", "test")]

        report_data = ReportData(self.title, self.config)
        res = report_data.add_test(test_data, report, row)

        assert res is expect
