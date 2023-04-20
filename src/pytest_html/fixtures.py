import warnings

import pytest


@pytest.fixture
def extra(pytestconfig):
    """Add details to the HTML reports.

    .. code-block:: python

        import pytest_html


        def test_foo(extra):
            extra.append(pytest_html.extras.url("https://www.example.com/"))
    """
    warnings.warn(
        "The 'extra' fixture is deprecated and will be removed in a future release"
        ", use 'extras' instead.",
        DeprecationWarning,
    )
    pytestconfig.extras = []
    yield pytestconfig.extras
    del pytestconfig.extras[:]


@pytest.fixture
def extras(pytestconfig):
    """Add details to the HTML reports.

    .. code-block:: python

        import pytest_html


        def test_foo(extras):
            extras.append(pytest_html.extras.url("https://www.example.com/"))
    """
    pytestconfig.extras = []
    yield pytestconfig.extras
    del pytestconfig.extras[:]
