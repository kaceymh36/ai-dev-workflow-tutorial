# Repository Guidelines

## Project Structure & Module Organization

`app.py` builds the Streamlit page and Plotly charts. `sales_data.py` loads, validates, and summarizes the CSV; keep calculations there and presentation in `app.py`. The sample dataset is `data/sales-data.csv`, and the light theme is configured in `.streamlit/config.toml`. Tests live in `tests/test_sales_data.py` and `tests/test_app.py`. `verify_dashboard.py` independently audits sample totals. Product requirements are in `prd/ecommerce-analytics.md`; the design and implementation plan are in `docs/superpowers/`. Track milestone status and evidence in `TASKS.md`.

## Build, Test, and Development Commands

Use Python 3.11 or newer and the local `venv/`. From the repository root on Windows:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m streamlit run app.py
.\venv\Scripts\python.exe -m pytest -q
.\venv\Scripts\python.exe verify_dashboard.py
```

The first two commands prepare dependencies; Streamlit starts the local dashboard. Pytest runs the full suite. The audit script checks the supplied CSV's totals and reports Python-side timings, which do not measure browser rendering.

## Coding Style & Naming Conventions

Use four spaces for Python indentation, descriptive `snake_case` names for functions and files, and small functions with comments where the intent is not obvious. Preserve money as integer cents during calculations; format it only for display. Follow the surrounding code style. No formatter or linter is configured in this repository.

## Testing Guidelines

Use pytest. Name test files `test_*.py` and test functions `test_*`. Add small temporary CSV fixtures for validation and aggregation cases; do not edit the supplied sample CSV to test failures. Run the full suite before recording milestone verification, and distinguish automated checks from browser observations.

## Commit & Pull Request Guidelines

Commits start with a milestone ID, for example `TASK-6: Add dashboard verification audit and guidance`. Keep code changes and the subsequent `TASKS.md` completion update traceable; record the code commit hash and verification evidence on the board. Before a pull request or merge, review the diff, report tests run and known limitations, and include screenshots when the dashboard appearance changes. Review the feature branch before merging to `main` for deployment.

## Lessons

- Commit completed milestone work with its `TASK-n` ID before recording the hash in `TASKS.md`.
- Reuse the existing `venv/` and check CSV facts, including reporting dates, before setting test expectations.
- Treat server health as an availability check; record visual checks separately.
- Mark unavailable browser checks as untested. State timing limits plainly, and use the PRD and plan to distinguish requirements from suggested methods.
