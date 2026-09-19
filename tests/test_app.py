"""Check the page and stop-on-invalid-data behavior without changing the CSV."""

from pathlib import Path
import csv
import json
from decimal import Decimal
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


def test_monthly_chart_matches_csv():
    totals = {}
    with (APP_PATH.parent / 'data' / 'sales-data.csv').open(newline='') as source:
        for row in csv.DictReader(source):
            month = row['date'][:7]
            totals[month] = totals.get(month, Decimal('0')) + Decimal(row['total_amount'])
    app = AppTest.from_file(str(APP_PATH)).run()
    assert not app.exception
    assert not app.error
    assert not app.warning
    charts = app.get('plotly_chart')
    assert len(charts) == 1
    figure = json.loads(charts[0].proto.spec)
    trace = figure['data'][0]
    assert trace['x'] == [
        'Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024', 'May 2024', 'Jun 2024',
        'Jul 2024', 'Aug 2024', 'Sep 2024', 'Oct 2024', 'Nov 2024', 'Dec 2024',
    ]
    amounts = [totals[month] for month in sorted(totals)]
    assert trace['y'] == [float(amount) for amount in amounts]
    assert trace['customdata'] == [f'${amount:,.2f}' for amount in amounts]
    assert trace['mode'] == 'lines+markers'
    assert '%{customdata}' in trace['hovertemplate']
    assert figure['layout']['xaxis']['title']['text'] == 'Month'
    assert figure['layout']['yaxis']['title']['text'] == 'Sales (USD)'


def test_monthly_chart_spans_years_and_fills_only_internal_gaps(tmp_path):
    fixture = tmp_path / 'sales.csv'
    fixture.write_text(
        'date,order_id,product,category,region,quantity,unit_price,total_amount\n'
        '2025-02-20,003,Item,Category,North,1,20.02,20.02\n'
        '2024-12-05,001,Item,Category,North,1,10.01,10.01\n'
        '2024-12-10,002,Item,Category,North,1,5.05,5.05\n',
        encoding='utf-8',
    )
    with patch('sales_data.load_sales_data', return_value=load_sales_data(fixture)):
        app = AppTest.from_file(str(APP_PATH)).run()
    assert not app.exception
    assert not app.error
    assert not app.warning
    figure = json.loads(app.get('plotly_chart')[0].proto.spec)
    trace = figure['data'][0]
    assert trace['x'] == ['Dec 2024', 'Jan 2025', 'Feb 2025']
    assert trace['y'] == [15.06, 0.0, 20.02]
    assert trace['customdata'] == ['$15.06', '$0.00', '$20.02']
    assert figure['layout']['xaxis']['categoryarray'] == trace['x']
