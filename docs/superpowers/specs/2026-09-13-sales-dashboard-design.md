# ShopSmart Sales Dashboard Design

Status: Draft for review. This document describes the proposed dashboard; the implementation plan follows design approval.

Sources: [Product requirements](../../../prd/ecommerce-analytics.md) and [milestone board](../../../TASKS.md).

## Purpose and scope

Give managers a clear overview of sales performance using the supplied `data/sales-data.csv`. Phase 1 includes two KPI cards, a monthly sales trend, and category and region breakdowns. The dashboard reports the contents of the CSV; it does not promise live data or automated refresh.

Authentication, database integration, exports, alerts, filters, transaction drill-down, and custom mobile layouts remain outside this release.

## Agreed visual design

Use the title **ShopSmart Sales Dashboard** and a clean, light executive-report style: white background, dark readable text, one restrained blue accent, subtle chart gridlines, and generous spacing. Prefer standard Streamlit components and theme settings over custom styling.

The layout is:

```text
ShopSmart Sales Dashboard
Reporting period: earliest date to latest date in the CSV

Total Sales                    Total Orders

Monthly Sales
[Full-width line chart]

Sales by Category              Sales by Region
[Horizontal bar chart]         [Horizontal bar chart]
```

The reporting period makes the coverage of the totals clear. Both KPI cards summarize the entire dataset. No comparison percentages are shown because the PRD does not define a comparison period.

## Metrics and charts

| Element | Calculation | Presentation |
|---------|-------------|--------------|
| Total Sales | Sum of `total_amount` across validated transactions | Dollar sign, thousands separators, rounded to whole dollars for the card |
| Total Orders | Count of transaction rows | Integer with thousands separators |
| Monthly Sales | Sum of `total_amount` grouped by calendar year and month | Chronological line chart; month/year labels; sales axis in dollars; hover values to cents |
| Sales by Category | Sum of `total_amount` grouped by category | Horizontal bars, largest at the top, all categories included; hover values to cents |
| Sales by Region | Sum of `total_amount` grouped by region | Horizontal bars, largest at the top, all regions included; hover values to cents |

Use `total_amount` as the revenue source rather than recomputing it from price and quantity. Preserve cents during calculations and round only for display. Bar-chart ties use alphabetical order for a stable display. Bar axes start at zero.

Proposed default: include every month between the earliest and latest transaction months, using zero for months with no transactions. Group by year as well as month so data spanning multiple years stays separate. Do not invent months outside the dataset's date range.

## Data validation and error behavior

Validate the complete file before showing any KPIs or charts. Stop and display a clear, actionable explanation when the file is missing, unreadable, malformed, empty, or invalid. Never silently discard bad rows or show partial totals.

Validation checks cover:

- All eight PRD columns are present: `date`, `order_id`, `product`, `category`, `region`, `quantity`, `unit_price`, and `total_amount`.
- Required values are not missing or blank, dates are valid, numeric values are finite, and quantities are integers.
- Order identifiers are unique, as specified by the PRD.

Errors should identify the file, affected column, and example CSV row numbers where possible, with a suggested correction. For example: "Cannot load sales data: column 'date' contains an invalid date on CSV row 12. Use YYYY-MM-DD dates and reload the dashboard."

Category and region values come from the data rather than a hardcoded list. The sample counts and approximate sales total in the PRD are verification references, not restrictions on future valid files. Additional business rules, such as how returns are represented, are outside the current specification.

## Simple technical structure

Use Python 3.11+, Streamlit for the page, Pandas for data handling, Plotly for charts, and pytest for calculation and validation tests. Use a plain Python virtual environment at `venv/` and a `requirements.txt` for dependencies; do not use uv or conda. Keep `venv/` out of Git.

| File | Responsibility |
|------|----------------|
| `app.py` | Assemble the page, call data functions, display validation errors, and render KPI cards and charts |
| `sales_data.py` | Load and validate the CSV; calculate totals and monthly, category, and region summaries without Streamlit dependencies |
| `tests/test_sales_data.py` | Test validation and calculations using small, understandable datasets with known answers |
| `requirements.txt` | Declare the application and test dependencies |
| `.streamlit/config.toml` | Set the light theme and restrained accent color |
| `README.md` | Explain environment setup, running the dashboard, running tests, and the deployment handoff |

Use small, clearly named functions rather than classes or a framework of abstractions. Resolve the CSV path relative to the application files so it does not depend on the launch directory. Load and validate once per application run; the small supplied dataset does not initially require a caching layer.

## Verification expectations

Pytest coverage should check exact known totals, transaction counts, year/month grouping, missing months, descending breakdown order, and validation failures. Include missing files, missing columns, empty input, invalid dates and numbers, and duplicate order IDs. Compare currency results at cent precision.

Check the actual sample CSV against independently calculated results. Treat the PRD's approximately $116,500, 482 orders, Electronics lead, and four regions as sanity checks; investigate discrepancies rather than changing calculations to match an approximate figure.

Review the rendered dashboard for readable labels, currency formatting, exact-value tooltips, correct sorting, and the agreed layout. Confirm normal operation without errors or warnings, dashboard loading within 5 seconds, and chart rendering within 2 seconds of data load. Record browser checks for Chrome, Firefox, Safari, and Edge, including any checks that still require access to a browser.

Each milestone must satisfy the Definition of Done in `TASKS.md` before moving to Done.

## Workflow and deployment ownership

Work stays on the existing `feature/sales-dashboard` branch without creating a Git worktree.

After this design is reviewed, the implementation plan must cover every milestone from TASK-1 through TASK-7. Give plan steps their own numbering, such as "Step 1 [TASK-1]", so step numbers stay separate from milestone identifiers. Label every plan task with its milestone.

Deployment is the final plan step and is owned by the user. After the changes are merged into `main`, the user will deploy from `main` to Streamlit Community Cloud, verify the public dashboard, and record the shareable URL. The plan ends with this handoff; the assistant does not execute deployment. TASK-7 remains incomplete until the user's deployment and verification are finished.

## Review focus

The visual style, title, monthly trend, page layout, and stop-on-invalid-data behavior reflect the agreed decisions. Please review the proposed missing-month behavior, metric formatting, validation rules, and module structure before the implementation plan is written.
