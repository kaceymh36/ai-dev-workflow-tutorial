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

### TASK-6: Test and refine the dashboard (M6)

Verify all PRD acceptance criteria and calculations against the CSV, using the expected sample results as a sanity check: approximately $116,500 in sales, 482 orders, Electronics as the top category, and all four regions. Refine the presentation, confirm there are no errors or warnings, and check compatibility with Chrome, Firefox, Safari, and Edge. Verify dashboard loading within 5 seconds and chart rendering within 2 seconds of data load.

### TASK-7: Deploy to Streamlit Community Cloud (M7)

Prepare deployment configuration and instructions, deploy the dashboard, and verify that its KPIs and charts work at a publicly accessible URL. Record the shareable URL for stakeholder review.

## In Progress

None.

## Done

### TASK-5: Build category and region breakdowns (M5)

Create interactive bar charts showing sales for every category and region in the dataset. Sort each chart from highest to lowest sales and include clear labels and exact-value tooltips.

Scope: implementation plan Step 6. Started 2026-09-18.

Acceptance criteria:

- [x] Side-by-side horizontal charts include every category and region.
- [x] Chart configuration places highest sales at the top, with alphabetical ordering for ties.
- [x] Numeric axes include zero, axes are labeled, and hover values preserve cents.
- [x] Both breakdowns match the CSV and sum to Total Sales.
- [x] All 70 automated tests pass; README instructions and verification evidence are updated.
- [x] Milestone closed at the user's explicit request, with the unrecorded browser visual check disclosed below and carried into TASK-6.

Commit: `70698753e3b55a316e28e650d15644cdf2ed12b2` (TASK-5: Implement category and region sales charts)

Notes: Codex initially left the TASK-5 implementation uncommitted; this is corrected by the code commit above. No user code changes were reported or found in the reviewed diff. The app was launched for user testing and its health check returned `ok`, but no visual-test result was explicitly recorded. Moved to Done at the user's explicit request; visual verification is not claimed as passed and is carried into TASK-6.

Step 6 implementation and automated verification (2026-09-18):

- Replaced both placeholders with horizontal Plotly bar charts using the existing category and region summaries, placed side by side below the trend.
- Added a small shared chart function in `app.py`. Explicit category order and a reversed vertical axis put descending totals at the top; the summaries retain alphabetical ties. Automatic label margins and height based on group count support readability.
- Used the existing blue accent and light chart theme, labeled axes, zero-inclusive sales axes, and exact two-decimal currency hover text. Calculations remain integer cents; floats are only chart coordinates.
- Added page tests comparing every category and region bar and hover value independently against the CSV. Both breakdowns total **$116,500.21**. A temporary fixture verifies new labels, alphabetical ties, and zero-sales groups.
- `venv\Scripts\python.exe -m pytest -q`: **70 passed**. Execution required access outside the sandbox to the existing Python interpreter. Valid AppTest pages had no exceptions, errors, or warnings.
- Updated README with chart behavior and visual-check instructions.
- Pre-commit verification (2026-09-18): all **70 tests passed** again and `git diff --check` passed, with only Git's LF-to-CRLF conversion notices. Code, tests, and README are included in the milestone code commit above, pushed to `origin/feature/sales-dashboard`.
- **Verification limitation:** browser automation returned no available browsers or apps. Actual rendered order, label readability, and hover interaction remain unverified. This check is carried into TASK-6 when closing TASK-5 at the user's request.

### TASK-4: Build the sales trend chart (M4)

Create an interactive line chart of daily or monthly sales, ordered by time, with labeled time and sales axes and tooltips showing exact values.

Scope: implementation plan Step 5. Started 2026-09-18.

Acceptance criteria:

- [x] Full-width interactive Plotly line chart uses the tested monthly sales summary.
- [x] Month/year labels follow chronological order, including zero-valued missing months only within the observed range.
- [x] Month and Sales (USD) axes are labeled, sales ticks use dollar formatting, and tooltip text preserves cents.
- [x] Restrained blue styling and a light chart theme are implemented.
- [x] All plotted sample months and hover totals match independent CSV calculations; a cross-year missing-month fixture passes.
- [x] All 68 automated tests pass; README instructions and verification evidence are updated.
- [x] Milestone closed at the user's explicit request, with the unrecorded browser visual check disclosed below and carried into TASK-6.

Commit: `f3066e204aba48b55db49c2464c52d8d9e2a9632` (TASK-4: Implement monthly sales trend chart)

Notes: Codex initially left the TASK-4 implementation uncommitted; this is corrected by the code commit above. No user code changes were reported or found in the reviewed diff. The app was launched for user testing and its health check returned `ok`, but no visual-test result was explicitly recorded. Moved to Done at the user's explicit request; visual verification is not claimed as passed and is carried into TASK-6.

Step 5 implementation and automated verification (2026-09-18):

- Replaced the monthly placeholder with a full-width Plotly line chart using the tested monthly summary, a restrained blue line, and visible point markers.
- Month/year labels follow chronological summary order. Axes are labeled Month and Sales (USD), with dollar ticks and exact two-decimal currency hover text.
- Calculations remain integer cents; Decimal produces hover text and floats are used only for chart coordinates.
- Added page tests comparing all 12 plotted months and hover totals independently against the CSV, plus an out-of-order cross-year fixture verifying December $15.06, missing January $0.00, and February $20.02 with no extra months.
- `venv\Scripts\python.exe -m pytest -q`: **68 passed**. Execution required access outside the sandbox to the existing Python interpreter. Valid AppTest pages had no exceptions, errors, or warnings.
- Updated README with chart behavior, interaction, and visual-check instructions.
- Pre-commit verification (2026-09-18): all **68 tests passed** again and `git diff --check` passed, with only Git's LF-to-CRLF conversion notices. Code, tests, and README are included in the milestone code commit above, pushed to `origin/feature/sales-dashboard`.
- **Verification limitation:** browser automation returned no available browsers or apps. Actual appearance and hover interaction could not be visually verified. This check is carried into TASK-6 when closing TASK-4 at the user's request.

### TASK-3: Implement KPI cards (M3)

Display Total Sales as the sum of `total_amount` and Total Orders as the transaction count. Show both prominently with currency formatting and thousands separators as appropriate.

Scope: implementation plan Step 4. Started 2026-09-18.

Acceptance criteria:

- [x] Total Sales uses the tested sum of `total_amount`; Total Orders counts transaction rows.
- [x] Two prominent, side-by-side metric cards display labeled totals without undefined comparison percentages.
- [x] Sales display a dollar sign, thousands separators, and whole-dollar rounding; orders display an integer with separators.
- [x] Display rounding preserves exact underlying calculations; CSV totals independently verified as $116,500.21 and 482 orders.
- [x] All 66 automated tests pass; formatting checks and README instructions are updated.
- [x] Milestone closed at the user's explicit request, with the unrecorded browser visual check disclosed below and carried into TASK-6.

Commit: `031c51df3dcb84ed328c4612d99d2008f0eeb65e` (TASK-3: Implement sales and order KPI cards)

Notes: Codex initially left the TASK-3 implementation uncommitted; this is corrected by the code commit above. No user code changes were reported. The app was launched for user testing and its health check returned `ok`, but no visual-test result was explicitly recorded. Moved to Done at the user's explicit request; visual verification is not claimed as passed and is carried into TASK-6.

Step 4 implementation and automated verification (2026-09-18):

- Connected two side-by-side, bordered Streamlit metric cards to `summarize_kpis`.
- Total Sales displays **$116,500**; Total Orders displays **482**. Sales use whole-dollar rounding and thousands separators; orders use integer formatting with separators. No comparison percentages are shown.
- Formatting uses Decimal at the UI boundary; the summary remains **11,650,021 cents**. No calculation changes were needed.
- Updated the existing page test to check KPI labels, displayed values, and absent comparison values; updated README behavior and visual-check instructions.
- `venv\Scripts\python.exe -m pytest -q`: **66 passed**. Tests required execution outside the sandbox because it denied access to the existing Python interpreter.
- Independent `csv.DictReader` / Decimal calculation confirmed **$116,500.21** and **482 transactions**, matching the displayed cards and exact summary.
- Additional AppTest checks passed for rounding $1,234.49 down to $1,234, rounding $1,234.51 up to $1,235, displaying 1,234 orders, and omitting comparison values. Valid pages had no exceptions, errors, or warnings; the test harness emitted only Streamlit's ignorable bare-mode ScriptRunContext warning.
- `git diff --check` passed, with only Git's LF-to-CRLF conversion notices.
- Pre-commit verification (2026-09-18): all **66 tests passed** again and `git diff --check` passed. Code, tests, and README are included in the milestone code commit above.
- **Verification limitation:** browser automation returned no available browsers. Card prominence, spacing, and formatting still require a recorded visual check in TASK-6; the user requested TASK-3 be moved to Done.

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
