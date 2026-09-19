# ShopSmart Sales Dashboard Implementation Plan

Based on the [approved design](../specs/2026-09-13-sales-dashboard-design.md), [PRD](../../../prd/ecommerce-analytics.md), and [milestone board](../../../TASKS.md).

This is an implementation plan, not a record of completed work. Step numbers describe execution order; labels such as `[TASK-2]` refer to milestones in `TASKS.md`. Multiple steps can belong to the same milestone.

## Working agreements

Work on the existing `feature/sales-dashboard` branch without a Git worktree. Explain each change before making it and summarize it afterward in plain language. Use simple functions and helpful comments, a plain Python environment in `venv/`, and `requirements.txt`; do not use uv or conda.

Move a milestone to In Progress when its implementation starts. Move it to Done only after all its steps and the board's Definition of Done are satisfied. Record verification evidence with the milestone. Writing this plan does not complete any milestone.

## Step 1 [TASK-1]: Set up the Python project

**Files:** `requirements.txt`, `.gitignore`, `README.md`, initial `app.py`.

- Check the available Python version is 3.11 or newer and inspect existing files before editing them.
- Create the environment with `python -m venv venv`.
- Declare compatible Streamlit, Pandas, Plotly, and pytest dependencies in `requirements.txt`, recording the versions verified during implementation.
- Install using `venv\Scripts\python.exe -m pip install -r requirements.txt`.
- Ignore `venv/`, Python bytecode, and pytest cache without replacing existing ignore rules.
- Add a minimal Streamlit entry point and document setup, launch, and test commands in the README.

**Verify:** Run `venv\Scripts\python.exe -m pip check` and launch with `venv\Scripts\python.exe -m streamlit run app.py`. Confirm the initial page opens without errors.

## Step 2 [TASK-2]: Load and validate the complete CSV

**Files:** `sales_data.py`, `tests/test_sales_data.py`.

- Inspect the supplied CSV and implement a small `load_sales_data(path)` function with no Streamlit imports.
- Validate the eight required columns, nonblank required values, valid dates, finite numeric values, integer quantities, and unique order IDs.
- Preserve order IDs as text and monetary precision through aggregation; use decimal parsing and integer cents internally for money, converting to display values only at the UI boundary.
- Reject missing, unreadable, malformed, empty, or invalid files. Return actionable validation errors naming columns and example CSV row numbers where possible. Do not silently skip rows.
- Add pytest cases using small temporary CSV files for valid input and each failure category. Do not alter the supplied CSV to test errors.

**Verify:** Run `venv\Scripts\python.exe -m pytest tests/test_sales_data.py -q`. Confirm valid data loads completely and invalid data produces useful explanations.

## Step 3 [TASK-2]: Add tested summary functions and the page structure

**Files:** `sales_data.py`, `tests/test_sales_data.py`, `app.py`, `.streamlit/config.toml`.

- Add clearly named functions for KPI totals, monthly sales, sales by category, and sales by region.
- Sum `total_amount` for revenue and count transaction rows for orders. Group months by both year and month, sort chronologically, and fill missing months within the observed range with zero.
- Sort breakdowns by descending sales, then alphabetically for ties. Include every category and region present in valid data.
- Test known totals including cents, counts, multi-year grouping, missing months, breakdown totals, and stable sorting with small fixtures whose expected values are easy to calculate by hand.
- Configure the light theme and blue accent. Build the title, reporting-period caption, two KPI columns, full-width trend area, and two side-by-side breakdown areas.
- Resolve the CSV relative to the application files. Load once per run; on an expected data error, display the explanation and stop before rendering metrics or charts.

**Verify:** Run the data tests and open the page. Check the title and reporting period. Exercise the error display with a temporary invalid fixture and restore normal input afterward.

## Step 4 [TASK-3]: Render the KPI cards

**Files:** `app.py`; extend `tests/test_sales_data.py` only if a calculation gap is found.

- Connect Total Sales and Total Orders to the tested summary functions.
- Display sales with a dollar sign, thousands separators, and whole-dollar rounding; display order count as an integer with separators.
- Keep both cards prominent and omit undefined comparison percentages.

**Verify:** Compare both displayed values to the CSV totals and inspect formatting. Confirm display rounding does not affect underlying calculations.

## Step 5 [TASK-4]: Render the monthly trend

**Files:** `app.py`.

- Build the full-width Plotly line chart from the tested monthly summary.
- Use chronological month/year labels, clearly labeled axes, dollar formatting, and hover values showing cents.
- Keep styling restrained and consistent with the light theme.

**Verify:** Check plotted months and hover totals against the summary, including a fixture spanning years and containing a missing month. Confirm no months outside the observed range appear.

## Step 6 [TASK-5]: Render category and region charts

**Files:** `app.py`.

- Place horizontal bar charts side by side below the trend.
- Show every category and region, with the highest sales visibly at the top and alphabetical ordering for ties.
- Start numeric axes at zero and provide clear labels and exact currency hover values.

**Verify:** Compare both charts to the tested summaries. Check actual rendered order, readable category names, and that each breakdown sums to Total Sales.

## Step 7 [TASK-6]: Verify and refine the complete dashboard

**Files:** `app.py`, `sales_data.py`, tests as needed, `README.md`, `TASKS.md`.

- Run the complete pytest suite with `venv\Scripts\python.exe -m pytest -q` and resolve failures.
- Independently calculate sample totals from the CSV and compare every KPI and chart summary. Use the PRD's approximately $116,500, 482 orders, Electronics lead, and four regions as sanity checks; investigate discrepancies.
- Review the complete page against the approved design and all PRD acceptance criteria, including the stop-on-invalid-data behavior.
- Check modern Chrome, Firefox, Safari, and Edge. Record the browsers actually tested and any outstanding checks rather than claiming unavailable checks passed.
- Measure dashboard loading against the 5-second target and chart rendering against the 2-second target after data load. Record the environment and timing method, and distinguish a sleeping cloud app's startup from normal operation when applicable.
- Resolve errors, warnings, readability problems, or performance failures. Keep calculations separate from rendering and avoid adding unnecessary abstractions.
- Finish beginner-friendly run and test instructions and record verification results on the task board. Required unresolved checks keep the relevant milestone open.

**Verify:** All applicable acceptance criteria and the Definition of Done are satisfied, with reproducible test commands and recorded manual-check results.

## Step 8 [TASK-7]: Prepare the deployment handoff and merge-ready changes

**Files:** `README.md`, `requirements.txt`, `.streamlit/config.toml`, `TASKS.md` as needed.

- Document the deployment inputs: repository, `main` branch, `app.py` entry point, and a supported Python version matching local verification.
- Confirm the CSV and required configuration are included in the proposed changes and `venv/` is excluded. Verify dependency installation from `requirements.txt` is documented and reproducible.
- Prepare a review summary describing the dashboard behavior, tests, and any outstanding issues so the feature can be reviewed and merged into `main` before deployment.
- Keep TASK-7 In Progress: preparation alone does not satisfy its public-URL deliverable. Hand off the deployment instructions to the user.

**Verify:** The deployment instructions are complete, the feature is ready for review and merge, and the user can identify the branch and entry point. This step does not itself authorize or perform a merge.

## Step 9 [TASK-7]: User deploys from main — final handoff

**Owner: User. Execute only after the feature has been reviewed and merged into `main`.**

- Deploy the repository's `main` branch and `app.py` to Streamlit Community Cloud using the documented environment settings.
- Open the public URL and confirm the CSV loads, both KPIs are correct, all three charts render, and tooltips work without errors or warnings.
- Record the shareable URL and verification results in `TASKS.md`, then move TASK-7 to Done when its Definition of Done is met.

The assistant's implementation work stops at the handoff. Deployment is the final plan step and is executed by the user.
