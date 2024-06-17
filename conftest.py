#conftest.py

import pytest
import pytest_html
from pytest_html import extras

def pytest_configure(config):
    if not config.option.htmlpath:
        config.option.htmlpath = "pytest.html"
        config.option.self_contained_html = True

def pytest_html_results_table_header(cells):
    cells.insert(1, '<th class="sortable time" data-column-type="time">Fail count</th>')

def pytest_html_results_table_row(report, cells):
    fail_count = getattr(report, 'out_of_range_count', 'N/A')
    cells.insert(1, f'<td class="col-time">{fail_count}</td>')

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    report.out_of_range_count = getattr(item, 'out_of_range_count', 'N/A')


    #Embded the plotly.html into the test information
    custom_html = '<div><h3>Plotly Chart</h3><iframe src="plotly.html" width="100%" height="600"></iframe></div>'
    extra = pytest_html.extras.html(custom_html)
    report.extras = getattr(report, 'extra', []) + [extra]