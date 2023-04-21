from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape


def _is_error(report) -> bool:
    """
    Determines if an error has occurred in the report.
    """
    return report.when in ["setup", "teardown"] and report.outcome == "failed"


def _process_outcome(report) -> str:
    """
    Processes the outcome for the test report.
    """
    if _is_error(report):
        return "Error"
    if hasattr(report, "wasxfail"):
        if report.outcome in ["passed", "failed"]:
            return "XPassed"
        if report.outcome == "skipped":
            return "XFailed"

    return report.outcome.capitalize()


def _read_template(search_paths, template_name="index.jinja2"):
    """
    Reads the specified jinja2 template file.
    """
    env = Environment(
        loader=FileSystemLoader(search_paths),
        autoescape=select_autoescape(
            enabled_extensions=("jinja2",),
        ),
    )
    return env.get_template(template_name)


def _process_logs(report) -> str:
    """
    Process the logs for a pytest report.
    """
    log = []
    if report.longreprtext:
        log.append(report.longreprtext.replace("<", "&lt;").replace(">", "&gt;") + "\n")
    for section in report.sections:
        header, content = section
        log.append(f"{' ' + header + ' ':-^80}")
        log.append(content)

        # weird formatting related to logs
        if "log" in header:
            log.append("")
            if "call" in header:
                log.append("")
    if not log:
        log.append("No log output captured.")
    return "\n".join(log)
