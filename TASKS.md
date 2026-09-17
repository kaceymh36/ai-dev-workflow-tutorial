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

### TASK-2: Load the data and build the dashboard structure (M2)

Load `data/sales-data.csv`, validate the required columns, and parse date, numeric, and categorical values correctly. Create the basic Streamlit layout and prepare aggregations for the metrics and charts.

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

## Done

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
