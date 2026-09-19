"""Check the page and stop-on-invalid-data behavior without changing the CSV."""

from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from sales_data import load_sales_data


APP_PATH = Path(__file__).resolve().parents[1] / 'app.py'


def test_page_loads_once_from_app_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch('sales_data.load_sales_data', wraps=load_sales_data) as loader:
        app = AppTest.from_file(str(APP_PATH)).run()
    loader.assert_called_once_with(APP_PATH.parent / 'data' / 'sales-data.csv')
    assert not app.exception
    assert not app.error
    assert not app.warning
    assert app.title[0].value == 'ShopSmart Sales Dashboard'
    assert app.caption[0].value == 'Reporting period: Jan 03, 2024 to Dec 31, 2024'
    assert [heading.value for heading in app.subheader] == [
        'Monthly Sales', 'Sales by Category', 'Sales by Region',
    ]
    assert [(metric.label, metric.value) for metric in app.metric] == [
        ('Total Sales', '$116,500'), ('Total Orders', '482'),
    ]
    assert all(metric.delta == '' for metric in app.metric)


def test_invalid_file_shows_actionable_error_and_stops(tmp_path):
    invalid_path = tmp_path / 'invalid.csv'
    invalid_path.write_text('date,order_id\n2024-01-01,001\n', encoding='utf-8')
    with patch('sales_data.load_sales_data', side_effect=lambda path: load_sales_data(invalid_path)):
        app = AppTest.from_file(str(APP_PATH)).run()
    assert not app.exception
    assert len(app.error) == 1
    assert 'missing required columns' in app.error[0].value
    assert 'Restore these header names' in app.error[0].value
    assert not app.caption
    assert not app.subheader
    assert not app.metric
    assert not app.get('plotly_chart')
