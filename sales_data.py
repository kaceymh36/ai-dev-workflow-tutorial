"""Load and validate complete sales files without any Streamlit dependencies."""

import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re

import pandas as pd


REQUIRED_COLUMNS = (
    'date', 'order_id', 'product', 'category', 'region',
    'quantity', 'unit_price', 'total_amount',
)


class SalesDataError(ValueError):
    """An expected input problem with an explanation suitable for the dashboard."""


def _number(value, path, column, row_number):
    try:
        number = Decimal(value)
    except InvalidOperation:
        number = Decimal('NaN')
    if not number.is_finite():
        raise SalesDataError(
            f"Cannot load {path}: {column} on CSV row {row_number} must be a finite number. "
            'Correct the value and reload.'
        )
    return number


def _cents(value, path, column, row_number):
    number = _number(value, path, column, row_number)
    # Integer arithmetic avoids both float errors and Decimal context rounding.
    numerator, denominator = number.as_integer_ratio()
    cents, remainder = divmod(numerator * 100, denominator)
    if remainder:
        raise SalesDataError(
            f'Cannot load {path}: {column} on CSV row {row_number} has a fraction of a cent. '
            'Use an amount in whole cents and reload.'
        )
    return cents


def load_sales_data(path):
    """Return all validated transactions or raise SalesDataError; never skip rows.

    Text is stripped; IDs remain text and dates become datetime.date values.
    Quantity is a Python integer. The money columns are replaced by
    unit_price_cents and total_amount_cents, also Python integers. Object dtype
    preserves exact sums even beyond fixed-width integer limits. Extra columns
    are allowed but omitted. Display formatting belongs to the UI.
    """
    path = Path(path)
    records = []
    seen_ids = {}
    row_number = 1
    try:
        with path.open(encoding='utf-8-sig', newline='') as file:
            reader = csv.reader(file, strict=True)
            columns = next(reader, None)
            if not columns:
                raise SalesDataError(f'Cannot load {path}: empty file. Add a header and transaction rows.')
            if len(columns) != len(set(columns)):
                duplicates = sorted({name for name in columns if columns.count(name) > 1})
                raise SalesDataError(
                    f"Cannot load {path}: duplicate columns on CSV row 1: {', '.join(duplicates)}. "
                    'Give each column a unique name.'
                )
            missing = [name for name in REQUIRED_COLUMNS if name not in columns]
            if missing:
                raise SalesDataError(
                    f"Cannot load {path}: missing required columns: {', '.join(missing)}. "
                    'Restore these header names and reload.'
                )

            while True:
                # Physical row numbers remain useful when quoted fields span lines.
                row_number = reader.line_num + 1
                values = next(reader, None)
                if values is None:
                    break
                if len(values) != len(columns):
                    raise SalesDataError(
                        f'Cannot load {path}: CSV row {row_number} has {len(values)} fields; '
                        f'expected {len(columns)}. Check commas and quotes, then reload.'
                    )
                record = {name: value.strip() for name, value in zip(columns, values)
                          if name in REQUIRED_COLUMNS}
                for column, value in record.items():
                    if not value:
                        raise SalesDataError(
                            f'Cannot load {path}: {column} is blank on CSV row {row_number}. '
                            'Fill in the required value and reload.'
                        )
                try:
                    if not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', record['date']):
                        raise ValueError('Incorrect date format')
                    record['date'] = date.fromisoformat(record['date'])
                except ValueError as error:
                    raise SalesDataError(
                        f'Cannot load {path}: date is invalid on CSV row {row_number}. '
                        'Use a valid YYYY-MM-DD date and reload.'
                    ) from error

                order_id = record['order_id']
                if order_id in seen_ids:
                    raise SalesDataError(
                        f'Cannot load {path}: order_id on CSV row {row_number} duplicates '
                        f'row {seen_ids[order_id]}. Give each order a unique ID.'
                    )
                seen_ids[order_id] = row_number
                quantity = _number(record['quantity'], path, 'quantity', row_number)
                if quantity != quantity.to_integral_value():
                    raise SalesDataError(
                        f'Cannot load {path}: quantity on CSV row {row_number} must be a whole number. '
                        'Correct the value and reload.'
                    )
                record['quantity'] = int(quantity)
                for column in ('unit_price', 'total_amount'):
                    record[column + '_cents'] = _cents(record.pop(column), path, column, row_number)
                records.append(record)
    except (OSError, UnicodeError) as error:
        raise SalesDataError(
            f'Cannot read {path}. Check that the file exists, permissions allow reading, '
            'and the file is saved as UTF-8 CSV.'
        ) from error
    except csv.Error as error:
        raise SalesDataError(
            f'Cannot load {path}: malformed CSV near row {row_number}. '
            'Check separators and matching quotes, then reload.'
        ) from error

    if not records:
        raise SalesDataError(f'Cannot load {path}: no transaction rows. Add sales data below the header.')
    return pd.DataFrame(records, dtype=object)


def summarize_kpis(data):
    """Summarize validated transactions, keeping revenue in exact cents."""
    return {
        'total_sales_cents': sum(data['total_amount_cents']),
        'total_orders': len(data),
    }


def monthly_sales(data):
    """Return chronological month-start dates and cents, including gap months.

    Expects nonempty, validated data from load_sales_data.
    """
    totals = {}
    for day, cents in zip(data['date'], data['total_amount_cents']):
        month = day.replace(day=1)
        totals[month] = totals.get(month, 0) + cents

    month, last_month = min(totals), max(totals)
    records = []
    while True:
        records.append({'month': month, 'total_amount_cents': totals.get(month, 0)})
        if month == last_month:
            break
        month = date(month.year + 1, 1, 1) if month.month == 12 else date(month.year, month.month + 1, 1)
    return pd.DataFrame(records, dtype=object)


def _sales_breakdown(data, column):
    # Python integers preserve cents even when sums exceed fixed-width limits.
    totals = {}
    for label, cents in zip(data[column], data['total_amount_cents']):
        totals[label] = totals.get(label, 0) + cents
    ordered = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    return pd.DataFrame(ordered, columns=[column, 'total_amount_cents'], dtype=object)


def sales_by_category(data):
    """Return every category by descending sales, then alphabetically for ties."""
    return _sales_breakdown(data, 'category')


def sales_by_region(data):
    """Return every region by descending sales, then alphabetically for ties."""
    return _sales_breakdown(data, 'region')
