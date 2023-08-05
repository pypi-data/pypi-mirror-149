from gocept.bbissues.bbissues import Base
from gocept.bbissues.bbissues import timefmt
import pytest


@pytest.mark.parametrize('test_input,expected', [
    ('2015-10-15T16:38:55.491628+00:00', '2015-10-15 16:38'),  # Bitbucket
    ('2011-04-10T20:09:31Z', '2011-04-10 20:09'),  # Github
])
def test_timefmt(test_input, expected):
    """It returns the same output format for Github and Bitbucket API."""
    assert expected == timefmt(test_input)


@pytest.mark.parametrize('func, args', [
    ('get_error_message', ('data',)),
    ('collect_projects', ('owner',)),
    ('collect_project_issues', ('owner', 'project')),
    ('collect_project_pullrequests', ('owner', 'project')),
])
def test_bbissues__Base__1(func, args):
    """It fails on incomplete Implementations."""
    class Derived(Base):
        """Incomplete Implementation"""

    with pytest.raises(NotImplementedError):
        derived = Derived()
        getattr(derived, func)(*args)


@pytest.mark.parametrize('export_method', [
    ('export_html'),
    ('export_json'),
])
def test_bbissues__Handler__1(dummy_handler, export_method):
    """It runs the export methods."""
    getattr(dummy_handler, export_method)()
