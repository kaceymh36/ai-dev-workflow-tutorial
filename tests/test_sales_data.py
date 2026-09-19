"""Exercise complete CSV validation using temporary files with known values."""

import csv
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from sales_data import (
    SalesDataError, load_sales_data, summarize_kpis, monthly_sales,
    sales_by_category, sales_by_region,
)


COLUMNS = ['date', 'order_id', 'product', 'category', 'region',
           'quantity', 'unit_price', 'total_amount']
ROW = ['2024-02-29', '001', 'Cable, USB', 'Accessories', 'North', '2', '0.10', '0.20']


def write_csv(tmp_path, rows=None, columns=None):
    path = tmp_path / 'sales.csv'
    with path.open('w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(COLUMNS if columns is None else columns)
        writer.writerows([ROW] if rows is None else rows)
    return path


def test_valid_data_preserves_text_and_exact_cents(tmp_path):
    second = ['2024-03-01', 'NA', ' Other ', 'New category', 'New region', '3.0', '0.10', '0.30']
    data = load_sales_data(write_csv(tmp_path, [ROW, second]))
    assert len(data) == 2
    assert data['order_id'].tolist() == ['001', 'NA']
    assert data['date'].tolist() == [date(2024, 2, 29), date(2024, 3, 1)]
    assert data['quantity'].tolist() == [2, 3]
    assert data['product'].tolist() == ['Cable, USB', 'Other']
    assert data['category'].tolist() == ['Accessories', 'New category']
    assert data['region'].tolist() == ['North', 'New region']
    assert data['unit_price_cents'].tolist() == [10, 10]
    assert sum(data['total_amount_cents']) == 50
    assert 'total_amount' not in data.columns


@pytest.mark.parametrize('column', COLUMNS)
def test_missing_columns(tmp_path, column):
    position = COLUMNS.index(column)
    path = write_csv(tmp_path, [ROW[:position] + ROW[position + 1:]],
                     COLUMNS[:position] + COLUMNS[position + 1:])
    with pytest.raises(SalesDataError, match=column):
        load_sales_data(path)


@pytest.mark.parametrize('column', COLUMNS)
@pytest.mark.parametrize('value', ['', '   '])
def test_blank_required_values(tmp_path, column, value):
    row = ROW.copy()
    row[COLUMNS.index(column)] = value
    with pytest.raises(SalesDataError) as error:
        load_sales_data(write_csv(tmp_path, [row]))
    assert column in str(error.value)
    assert 'row 2' in str(error.value)


@pytest.mark.parametrize('value', ['2023-02-29', '2024-13-01', '2024-2-01', '02/01/2024', 'bad'])
def test_invalid_dates(tmp_path, value):
    row = ROW.copy()
    row[0] = value
    with pytest.raises(SalesDataError, match="date.*row 2"):
        load_sales_data(write_csv(tmp_path, [row]))


@pytest.mark.parametrize('column', ['quantity', 'unit_price', 'total_amount'])
@pytest.mark.parametrize('value', ['NaN', 'Infinity', '-Infinity', 'bad'])
def test_invalid_numbers(tmp_path, column, value):
    row = ROW.copy()
    row[COLUMNS.index(column)] = value
    with pytest.raises(SalesDataError, match=column + '.*row 2'):
        load_sales_data(write_csv(tmp_path, [row]))


@pytest.mark.parametrize('column,value', [('quantity', '1.5'), ('unit_price', '0.001'), ('total_amount', '0.001')])
def test_fractional_quantity_or_cents(tmp_path, column, value):
    row = ROW.copy()
    row[COLUMNS.index(column)] = value
    with pytest.raises(SalesDataError, match=column + '.*row 2'):
        load_sales_data(write_csv(tmp_path, [row]))


def test_duplicate_ids_after_trimming(tmp_path):
    second = ROW.copy()
    second[1] = ' 001 '
    with pytest.raises(SalesDataError, match='order_id.*row 3.*row 2'):
        load_sales_data(write_csv(tmp_path, [ROW, second]))


@pytest.mark.parametrize('content', ['', ','.join(COLUMNS) + '\n', 'date,order_id\n',
    ','.join(COLUMNS) + '\n"unterminated', ','.join(COLUMNS) + '\n1,2\n',
    ','.join(COLUMNS) + '\n\n', ','.join(COLUMNS + ['date']) + '\n'])
def test_empty_or_malformed_files(tmp_path, content):
    path = tmp_path / 'bad.csv'
    path.write_text(content, encoding='utf-8')
    with pytest.raises(SalesDataError) as error:
        load_sales_data(path)
    assert str(path) in str(error.value)


def test_missing_file(tmp_path):
    with pytest.raises(SalesDataError, match='read'):
        load_sales_data(tmp_path / 'missing.csv')


def test_unreadable_file(tmp_path, monkeypatch):
    path = write_csv(tmp_path)
    def denied(*args, **kwargs):
        raise PermissionError('denied')
    monkeypatch.setattr(Path, 'open', denied)
    with pytest.raises(SalesDataError, match='read'):
        load_sales_data(path)


def test_invalid_encoding(tmp_path):
    path = tmp_path / 'bad.csv'
    path.write_bytes(b'\xff\xfe')
    with pytest.raises(SalesDataError, match='UTF-8'):
        load_sales_data(path)


def test_late_invalid_row_rejects_whole_file(tmp_path):
    second = ROW.copy()
    second[0], second[1] = 'invalid', '002'
    with pytest.raises(SalesDataError, match='row 3'):
        load_sales_data(write_csv(tmp_path, [ROW, second]))


def test_large_money_is_exact_and_extra_columns_are_allowed(tmp_path):
    row = ROW.copy()
    row[-1] = '1000000000000000000000000000.01'
    data = load_sales_data(write_csv(tmp_path, [row + ['extra']], COLUMNS + ['note']))
    assert data['total_amount_cents'][0] == 10**29 + 1
    assert 'note' not in data.columns


def test_supplied_csv_matches_independent_decimal_calculation():
    path = Path(__file__).resolve().parents[1] / 'data' / 'sales-data.csv'
    with path.open(encoding='utf-8-sig', newline='') as file:
        rows = list(csv.DictReader(file))
    data = load_sales_data(path)
    assert len(data) == len(rows) == 482
    assert data['order_id'].tolist() == [row['order_id'] for row in rows]
    expected = sum(Decimal(row['total_amount']) for row in rows)
    assert expected == Decimal('116500.21')
    assert sum(data['total_amount_cents']) == int(expected * 100)


@pytest.fixture
def summary_data(tmp_path):
    # Deliberately unordered; quantities and prices do not determine revenue.
    rows = [
        ['2025-01-20', '1', 'Item', 'Zulu', 'West', '9', '99.00', '3.01'],
        ['2024-01-10', '2', 'Item', 'Alpha', 'East', '2', '99.00', '1.10'],
        ['2024-03-15', '3', 'Item', 'Alpha', 'East', '1', '99.00', '1.91'],
        ['2024-03-01', '4', 'Item', 'Top', 'North', '1', '99.00', '5.00'],
    ]
    return load_sales_data(write_csv(tmp_path, rows))


def test_kpis_count_rows_and_sum_supplied_amounts(summary_data):
    assert summarize_kpis(summary_data) == {'total_sales_cents': 1102, 'total_orders': 4}


def test_monthly_sales_separates_years_and_fills_only_observed_range(summary_data):
    result = monthly_sales(summary_data)
    assert result['month'].tolist() == [date(2024, month, 1) for month in range(1, 13)] + [date(2025, 1, 1)]
    assert result['total_amount_cents'].tolist() == [110, 0, 691] + [0] * 9 + [301]
    assert sum(result['total_amount_cents']) == 1102


@pytest.mark.parametrize('summarize,column,labels', [
    (sales_by_category, 'category', ['Top', 'Alpha', 'Zulu']),
    (sales_by_region, 'region', ['North', 'East', 'West']),
])
def test_breakdowns_include_every_label_and_sort_ties(summary_data, summarize, column, labels):
    result = summarize(summary_data)
    assert result[column].tolist() == labels
    assert result['total_amount_cents'].tolist() == [500, 301, 301]
    assert sum(result['total_amount_cents']) == 1102
    assert summarize(summary_data.iloc[::-1]).to_dict('list') == result.to_dict('list')


def test_summaries_preserve_large_integer_cents_and_single_month(tmp_path):
    first, second = ROW.copy(), ROW.copy()
    first[-1] = '1000000000000000000000000000.01'
    second[1] = '002'
    data = load_sales_data(write_csv(tmp_path, [first, second]))
    expected = 10**29 + 21
    assert summarize_kpis(data) == {'total_sales_cents': expected, 'total_orders': 2}
    for summarize in (monthly_sales, sales_by_category, sales_by_region):
        result = summarize(data)
        assert result['total_amount_cents'].tolist() == [expected]
        assert type(result['total_amount_cents'].iloc[0]) is int
    assert monthly_sales(data)['month'].tolist() == [date(2024, 2, 1)]
