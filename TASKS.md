# Dashboard Tasks

This file tracks all work for the dashboard, based on [the PRD](prd/ecommerce-analytics.md).

## Definition of Done

Before any milestone moves to Done:

- Its deliverables are complete and meet the applicable Phase 1 PRD requirements.
- Relevant checks pass, calculations match the CSV where applicable, and the dashboard runs without errors or warnings.
- Any affected charts and metrics have clear labels, correct formatting, and a professional appearance.
- Code is simple, readable, and modular, with helpful comments and updated setup or usage instructions where needed.
- Verification results are recorded and any issues blocking the milestone are resolved.

## To Do

### TASK-3: Implement KPI cards (M3)

Display Total Sales as the sum of `total_amount` and Total Orders as the transaction count. Show both prominently with currency formatting and thousands separators as appropriate.

### TASK-4: Build the sales trend chart (M4)

Create an interactive line chart of daily or monthly sales, ordered by time, with labeled time and sales axes and tooltips showing exact values.

### TASK-5: Build category and region breakdowns (M5)

Create interactive bar charts showing sales for every category and region in the dataset. Sort each chart from highest to lowest sales and include clear labels and exact-value tooltips.

### TASK-6: Test and refine the dashboard (M6)

Verify all PRD acceptance criteria and calculations against the CSV, using the expected sample results as a sanity check: approximately $116,500 in sales, 482 orders, Electronics as the top category, and all four regions. Refine the presentation, confirm there are no errors or warnings, and check compatibility with Chrome, Firefox, Safari, and Edge. Verify dashboard loading within 5 seconds and chart rendering within 2 seconds of data load.

### TASK-7: Deploy to Streamlit Community Cloud (M7)

Prepare deployment configuration and instructions, deploy the dashboard, and verify that its KPIs and charts work at a publicly accessible URL. Record the shareable URL for stakeholder review.

## In Progress

None.

## Done

### TASK-2: Load the data and build the dashboard structure (M2)

Load `data/sales-data.csv`, validate the required columns, and parse date, numeric, and categorical values correctly. Create the basic Streamlit layout and prepare aggregations for the metrics and charts.

Acceptance criteria:

- [x] Complete CSV loads with required-column, value, date, numeric, and unique-ID validation.
- [x] Monetary precision is preserved as integer cents; invalid input gives actionable errors without partial results.
- [x] KPI, monthly, category, and region summaries are implemented and tested, including missing months and deterministic sorting.
- [x] Basic page structure, reporting-period caption, light theme, and blue accent are implemented.
- [x] Data loads once per run from an application-relative path; expected errors stop the page before KPI/chart areas.
- [x] All 66 automated tests pass; usage instructions and verification evidence are recorded.
- [x] Milestone closed at the user's explicit request, with the unperformed browser visual check disclosed below.

Commit: `b61519cf4fb36e97e62cbd9b2ebce251e98620aa` (TASK-2: Load sales data and build dashboard structure)

Notes: Codex left TASK-2 implementation uncommitted in prior turns; this is corrected by the code commit above. Codex initially assumed incorrect reporting-period dates in a test and corrected them to Jan 03 through Dec 31, 2024 after the test failed. No user code changes were reported. Moved to Done at the user's explicit request; browser visual verification was unavailable and is not claimed as passed. Carry that visual check into TASK-6.

Step 2 complete: CSV loading and validation (2026-09-16).

- Wrote `tests/test_sales_data.py` first and confirmed the initial run failed because `sales_data` did not yet exist. Implemented the loader, then reran the tests successfully.
- Added `load_sales_data(path)` and `SalesDataError` in `sales_data.py`, with no Streamlit imports. Invalid input raises an actionable explanation without returning partial data.
- Validates the eight required columns, nonblank values, ISO dates, finite numbers, integer quantities, and unique text order IDs. Rejects missing, unreadable, malformed, empty, or invalid files; messages include columns and CSV row numbers where applicable.
- Parses money with Decimal and stores Python integer cents, preserving precision even for amounts beyond fixed-width integer limits. Fractions of a cent are rejected without rounding.
- `venv\Scripts\python.exe -m pytest tests/test_sales_data.py -q`: **59 passed** on Python 3.14.7 / Windows. Tests use temporary fixtures for validation failures and leave the supplied CSV unchanged.
- An independent `csv.DictReader` / Decimal calculation in the tests confirmed all **482 transactions**, preserved order IDs, and **$116,500.21** matching the loader's **11,650,021 cents**.
- Updated README test instructions and documented the loader's returned data format. The starter app is unchanged.
- Step 3 implementation and automated checks are complete (2026-09-18); visual verification remains outstanding as described below.

Step 3 implementation and verification (2026-09-18):

- Added `summarize_kpis`, `monthly_sales`, `sales_by_category`, and `sales_by_region`. Revenue remains exact integer cents, orders count transaction rows, missing months within the observed range get zero, and breakdowns sort by sales descending with alphabetical ties.
- Added hand-calculated fixture tests for cents, row counts, multi-year grouping, missing months, all breakdown labels, stable ties, and amounts beyond fixed-width integer limits. Confirmed the new tests failed before implementing the functions.
- Connected `app.py` to the loader once per run using an application-relative CSV path. Added the reporting period, two KPI areas, a full-width monthly area, two side-by-side breakdown areas, and a light theme with blue accent. KPI values and charts remain scoped to TASK-3 through TASK-5.
- Added `tests/test_app.py`: normal data renders the expected title and Jan 03, 2024 to Dec 31, 2024 reporting period even from another working directory. A temporary invalid CSV produces an actionable error and stops before KPI/chart areas; the supplied CSV is unchanged.
- `venv\Scripts\python.exe -m pytest -q`: **66 passed**. AppTest reported no page exceptions, errors, or warnings for valid data. Its bare-mode ScriptRunContext warning is identified by Streamlit as ignorable.
- Local Streamlit server on port 8503 started successfully; `/` returned HTTP 200 and `/_stcore/health` returned `ok`. `git diff --check` passed (Git printed only LF-to-CRLF conversion notices).
- Updated README with the current page behavior, summary function contracts, test commands, and visual-check instructions.
- **Verification limitation:** browser automation reported no available browser. Visual inspection of the light theme and layout remains unperformed and is carried into TASK-6 when closing TASK-2 at the user's request.
- Pre-commit verification (2026-09-18): reran the complete suite, **66 passed**; `git diff --check` passed. Code, configuration, tests, and README are included in the milestone code commit above.

### TASK-1: Set up the environment and project (M1)

Initialize the Python 3.11+ project, declare Streamlit, Pandas, and Plotly dependencies, and document how to install dependencies and run the dashboard locally.

Acceptance criteria:

- [x] Python 3.11+ verified and the existing virtual environment reused.
- [x] Streamlit, Pandas, Plotly, and pytest pinned in requirements.txt and installed successfully.
- [x] Virtual environment, Python bytecode, and pytest cache excluded by .gitignore.
- [x] Minimal Streamlit starter page and README setup, launch, and test instructions complete.
- [x] Dependency check, starter-page test, server health check, and user visual verification passed.
- [x] Verification evidence recorded below.

Commit: `0c09624` (TASK-1: Set up Python environment and Streamlit starter app)

Notes: Codex initially left the completed TASK-1 work uncommitted; this was corrected in 0c09624. The existing venv was reused at the user's request, and the user performed visual verification because browser automation was unavailable.

Implementation and verification (2026-09-16):

- Reused the existing `venv/` and confirmed Python 3.14.7.
- Pinned Streamlit 1.64.0, Pandas 2.3.3, Plotly 6.9.0, and pytest 9.1.1 in `requirements.txt`. Installation from that file succeeded; all requirements were already installed.
- Added the minimal `app.py` with the dashboard title and setup message, plus README setup, launch, dependency-check, and test instructions.
- Existing `.gitignore` rules cover `venv/`, Python bytecode, and pytest cache. `git check-ignore` confirmed the environment is ignored; no ignore changes were needed.
- `venv\Scripts\python.exe -m pip check` passed: **No broken requirements found.**
- The README's Streamlit AppTest command passed: the expected title rendered with no page exceptions, errors, or warnings. The test harness emitted only the `missing ScriptRunContext` warning that Streamlit identifies as ignorable in bare mode.
- Launched `venv\Scripts\python.exe -m streamlit run app.py --server.headless true --server.address 127.0.0.1 --server.port 8502 --browser.gatherUsageStats false`. The server started without warnings; `/` returned HTTP 200 and `/_stcore/health` returned `ok`.
- `git diff --check` passed. No pytest tests exist at this milestone; data tests belong to TASK-2.
- User visually verified the starter dashboard at `http://127.0.0.1:8502`: the ShopSmart Sales Dashboard title, description, and setup-complete message appeared correctly, with no visible errors.
- All Step 1 deliverables and applicable Definition of Done checks are complete. TASK-1 is Done; TASK-2 remains To Do.
