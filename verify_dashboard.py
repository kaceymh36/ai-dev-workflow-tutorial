"""Audit the supplied CSV and report backend timings; run from the project folder."""

import csv
from datetime import date
from decimal import Decimal
from pathlib import Path
import platform
from time import perf_counter
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from sales_data import (
    load_sales_data, monthly_sales, sales_by_category, sales_by_region,
    summarize_kpis,
)


ROOT = Path(__file__).resolve().parent


def main():
    # Independent standard-library calculations do not use the production loader.
    with (ROOT / 'data' / 'sales-data.csv').open(encoding='utf-8-sig', newline='') as source:
        rows = list(csv.DictReader(source))
    total = sum((Decimal(row['total_amount']) for row in rows), Decimal('0'))
    expected = {'month': {}, 'category': {}, 'region': {}}
    for row in rows:
        for column, groups in expected.items():
            label = date.fromisoformat(row['date']).replace(day=1) if column == 'month' else row[column].strip()
            groups[label] = groups.get(label, Decimal('0')) + Decimal(row['total_amount'])

    data = load_sales_data(ROOT / 'data' / 'sales-data.csv')
    assert summarize_kpis(data) == {
        'total_sales_cents': int(total * 100), 'total_orders': len(rows),
    }
    assert total == Decimal('116500.21') and len(rows) == 482
    assert max(expected['category'], key=expected['category'].get) == 'Electronics'
    assert set(expected['region']) == {'North', 'South', 'East', 'West'}
    print(f'{platform.system()} {platform.release()}, Python {platform.python_version()}')
    print(f'Total sales: ${total:,.2f}; orders: {len(rows)}')
    for column, summarize in (
        ('month', monthly_sales), ('category', sales_by_category), ('region', sales_by_region),
    ):
        summary = summarize(data)
        actual = dict(zip(summary[column], summary['total_amount_cents']))
        assert actual == {label: int(amount * 100) for label, amount in expected[column].items()}
        assert sum(actual.values()) == int(total * 100)
        print(f'\n{column.title()} totals (all match CSV):')
        for label, cents in actual.items():
            print(f'  {label}: ${Decimal(cents) / 100:,.2f}')

    # AppTest executes Python and serializes charts, but does not paint a browser.
    # Capture the loader boundary without adding timing code to the dashboard.
    print('\nBackend timings in seconds (NOT browser acceptance measurements):')
    for run in range(1, 4):
        timings = {}

        def timed_loader(path):
            started = perf_counter()
            result = load_sales_data(path)
            timings['loaded'] = perf_counter()
            timings['csv'] = timings['loaded'] - started
            return result

        started = perf_counter()
        with patch('sales_data.load_sales_data', side_effect=timed_loader):
            app = AppTest.from_file(str(ROOT / 'app.py')).run(timeout=10)
        finished = perf_counter()
        assert not app.exception and not app.error and not app.warning
        assert len(app.metric) == 2 and len(app.get('plotly_chart')) == 3
        print(f'  Run {run}: CSV {timings["csv"]:.3f}; '
              f'AppTest total {finished - started:.3f}; '
              f'after CSV through AppTest completion {finished - timings["loaded"]:.3f}')
    print('\nPASS: sample totals, every summary, and valid page checks.')
    print('Browser appearance, interaction, and end-to-end timing require separate evidence.')


if __name__ == '__main__':
    main()
