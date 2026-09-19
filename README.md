# AI-Assisted Development Workflow Tutorial

This tutorial teaches you a professional development workflow by having you build and deploy a real project: an e-commerce sales dashboard.

You'll work through it in two parts:

| Part | What you do | Time |
|------|-------------|------|
| [Part 1: Setup](pre-work-setup.md) | Set up accounts, install tools, get your repo ready | 55–80 min |
| [Part 2: Build & Deploy](workshop-build-deploy.md) | Plan with [Superpowers](https://github.com/obra/superpowers) (a skills add-on for Claude Code), track work in `TASKS.md`, build with Claude Code, deploy live | ~3 hours |

**Your course sets the deadline and the submission channel.** Several courses use this tutorial, and it carries no due date of its own. Section 7 of Part 2 tells you what to have ready when you finish. Where to send it, by when, and how much of the tutorial is assigned all come from your course.

## Why this matters

Most working developers now build with a coding agent. In a March 2026 survey of 906 engineers by The Pragmatic Engineer, 95 percent used AI tools every week, and Claude Code was the most used. The field has settled on a name for doing this well: agentic engineering. Andrej Karpathy coined "vibe coding" for the casual version. He describes the professional one as writing a clear spec, supervising the agent's plan, reading its changes, and keeping a way to check the result. That list is this tutorial.

Claude Code, the tool you'll use throughout, is Anthropic's coding agent. Unlike a chatbot that suggests code for you to paste, it works in your terminal: it reads your project, edits files, runs commands, and debugs with you.

You're not here to become a software engineer. You're here to learn how to build things when your work calls for it: a dashboard, an automated workflow, a rough prototype. Those skills carry over whether you go into analytics, consulting, or product management.

AI is an amplifier, not a shortcut. For someone with judgment, it multiplies what they can do. For someone without it, it produces confident output with no one home to check it. The evidence is specific. In a January 2026 study, Anthropic gave 52 junior developers a new library to learn, half of them with AI help. The AI group scored 50 percent on a comprehension quiz against 67 percent for the others, and saved no time doing it. The students who kept up were the ones who asked the AI to explain, questioned its choices, and did their own debugging. The ones who fell behind handed everything over.

This tutorial is built for the first group, and every step asks you to read what the agent did, decide something, or explain it back. The workflow rewards curiosity and initiative: asking why, reading the diff, pushing back on a plan, changing your mind on the record. Bring those, and a coding agent multiplies what you can do.

Where those numbers come from: https://newsletter.pragmaticengineer.com/p/ai-tooling-2026 and https://www.anthropic.com/research/AI-assistance-coding-skills

## What you'll build

A Streamlit dashboard with KPI (key performance indicator) scorecards, a sales trend chart, and breakdowns by category and region. Streamlit is an open-source Python framework for building web apps from plain Python scripts.

```
┌─────────────────────────────────────────────────────────────┐
│                E-Commerce Sales Dashboard                    │
├────────────────────────────┬────────────────────────────────┤
│       Total Sales          │       Total Orders             │
│       $1,234,567           │       8,432                    │
├────────────────────────────┴────────────────────────────────┤
│                   Sales Trend (Line Chart)                   │
│    $                                                         │
│    │      ╱╲        ╱╲                                       │
│    │     ╱  ╲      ╱  ╲      ╱                              │
│    │    ╱    ╲    ╱    ╲    ╱                               │
│    │   ╱      ╲  ╱      ╲  ╱                                │
│    │  ╱        ╲╱        ╲╱                                 │
│    └──────────────────────────────────────────── time       │
├────────────────────────────┬────────────────────────────────┤
│    Sales by Category       │    Sales by Region             │
│    (Bar Chart)             │    (Bar Chart)                 │
└────────────────────────────┴────────────────────────────────┘
```

See the finished version: https://sales-dashboard-greg-lontok.streamlit.app/

The dashboard itself is straightforward. The point is the workflow you use to build it.

## The workflow

Every technology company uses a variation of this workflow. You'll experience the entire cycle:

```
┌─────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌────────┐
│   PRD   │ -> │   TASKS.md   │ -> │ brainstorming│ -> │writing-plans │ -> │  Code  │
│(written)│    │ (milestones) │    │ (design doc) │    │ (impl plan)  │    │(Claude)│
└─────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └────────┘
                                                                              │
┌─────────┐    ┌───────────┐    ┌─────────┐    ┌───────────────────────────────┐
│  Live!  │ <- │  Deploy   │ <- │  Push   │ <- │ executing-plans (TDD + commit)│
│(public) │    │(Streamlit)│    │(GitHub) │    │ on a feature branch           │
└─────────┘    └───────────┘    └─────────┘    └───────────────────────────────┘
```

1. **PRD** (Product Requirements Document): Start with a written specification of what to build
2. **TASKS.md**: Draft your milestones (the deliverables, with IDs like TASK-1) from the PRD into a Markdown board in your repo
3. **brainstorming**: A Superpowers skill that asks clarifying questions and produces a design document
4. **writing-plans**: A Superpowers skill that turns the design into a bite-sized implementation plan covering your milestones
5. **executing-plans**: A Superpowers skill that builds the feature with Claude Code, implementing each task (test-first where the plan flags it)
6. **Commit**: Save your changes with a meaningful message linked to the milestone ID
7. **Push**: Upload your code to GitHub
8. **Review and merge**: Read what the agent wrote, run Claude Code's `/code-review` on the branch, decide what to fix, then merge
9. **Deploy**: Make your dashboard publicly accessible

## Key concepts

**Traceability.** Every piece of code traces back to a requirement. When you commit, you include the milestone ID (like TASK-1) in the message, and because `TASKS.md` is versioned in the repo, `git log` shows the whole chain from requirement to code to deployed feature.

**Skill-driven development.** Instead of jumping straight to code, you let Claude's Superpowers skills run a structured process: brainstorming explores what to build, writing-plans turns that into a bite-sized plan, then executing-plans implements task by task, using TDD on the tasks the plan flags for it (test-driven development: write a failing test first, then the code to pass it). This prevents the most common failure mode: building the wrong thing fast.

**AI as a partner.** Claude Code isn't just a code generator. You set the direction and make the judgment calls; it supplies the speed and technical know-how, and explains its reasoning so you learn as you go. You also review what it wrote before it ships, because you own what you ship.

## What you need

- Basic Python knowledge (if you've used pandas or written a few scripts, you're fine)
- A computer running macOS or Windows
- No prior experience with Git or AI coding tools
- A Claude Pro subscription, or a ChatGPT subscription if you already have one. The tutorial is written for Claude Code. If you already pay for ChatGPT, which includes OpenAI's Codex, follow the [Codex companion](codex-companion.md) at the marked points instead of buying a second subscription. The workflow is the same on both.

## Where to start

Open [pre-work-setup.md](pre-work-setup.md) and work through it first, then continue to Part 2.

## Project materials

| Resource | Description |
|----------|-------------|
| [E-Commerce PRD](prd/ecommerce-analytics.md) | The product requirements document you'll build from |
| [Sales data](data/sales-data.csv) | Sample dataset for the dashboard |
| [Codex companion](codex-companion.md) | For students on a ChatGPT subscription: what to do differently with OpenAI's Codex at each marked point |
| [Capstone tools](capstone-tools.md) | Appendix: Granola (meeting notes into Claude Code) and Wispr Flow (dictation), for the capstone, not this tutorial |

## Run the dashboard locally

The page loads and validates the CSV, displays **ShopSmart Sales Dashboard** and
its reporting period, and provides labeled spaces for the KPIs and charts.
KPI values and chart rendering belong to TASK-3 through TASK-5 in [TASKS.md](TASKS.md).

Use Python 3.11 or newer and run commands from the project folder. This project
has been checked with Python 3.14.7 on Windows. Dependency versions are pinned
in `requirements.txt`.

### Setup (Windows PowerShell)

For a fresh checkout, create a virtual environment once:

```powershell
python --version
python -m venv venv
```

If `python` is unavailable, try `py`. If neither command is available, use the
full path to your installed Python executable. Skip environment creation when
`venv/` already exists, as it does in the current local setup.

Install and check dependencies using the environment's Python directly;
activation is not required:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m pip check
```

### Launch the dashboard

```powershell
.\venv\Scripts\python.exe -m streamlit run app.py
```

Open the URL printed in the terminal, usually `http://localhost:8501`.
Keep the terminal open while using the dashboard; press **Ctrl+C** to stop it.

### Verify and run tests

Check the page and invalid-data handling with Streamlit's built-in test runner:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_app.py -q
```

The test runner may emit a `missing ScriptRunContext` warning identified by
Streamlit as ignorable in bare mode. This is separate from warnings on the page.

Run the project test suite with:

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

The data tests cover CSV validation and exact summary calculations using temporary
files without changing the supplied dataset. To run just these tests, use:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_sales_data.py -q
```

On macOS/Linux, create the environment with `python3 -m venv venv` and replace
`.\venv\Scripts\python.exe` in the commands above with `venv/bin/python`.
Those platforms have not yet been verified for this project.

### CSV loader (Step 2)

`sales_data.load_sales_data(path)` validates the complete UTF-8 CSV and returns
a Pandas DataFrame, or raises `SalesDataError` with a correction hint. The page loads
the CSV once per run using a path relative to `app.py`. Invalid input displays the
explanation and stops before the KPI and chart areas are rendered.

The loader requires all eight columns: `date`, `order_id`, `product`, `category`,
`region`, `quantity`, `unit_price`, and `total_amount`. Required values cannot be
blank. Dates use `YYYY-MM-DD`, IDs must be unique, quantities must be whole
numbers, and numeric values must be finite. Extra columns are allowed and omitted.

Text is trimmed, IDs retain leading zeros, and dates become Python date values.
Money is stored as exact Python integers in `unit_price_cents` and
`total_amount_cents`, replacing the dollar columns. Fractions of a cent are
rejected rather than rounded. Revenue uses the supplied `total_amount` rather
than recomputing price times quantity. Dollar formatting belongs to the UI.

### Summary functions and page structure (Step 3)

The summary functions in `sales_data.py` accept the validated, nonempty DataFrame:

- `summarize_kpis(data)` returns `total_sales_cents` and `total_orders` in a dictionary.
- `monthly_sales(data)` returns a DataFrame with `month` (the first day of each
  month) and `total_amount_cents`. It separates years, sorts chronologically, and
  fills missing months with zero only between the first and last observed months.
- `sales_by_category(data)` and `sales_by_region(data)` return DataFrames with
  the grouping column and `total_amount_cents`, sorted by descending sales and
  alphabetically for ties. Every category and region is included.

All summaries retain exact integer cents. `.streamlit/config.toml` sets the light
theme and blue accent; launch from the project folder so Streamlit finds it.
For a visual check, confirm the reporting period is **Jan 03, 2024 to Dec 31, 2024**,
the two KPI areas sit side by side, Monthly Sales spans the page, and the category
and region areas sit side by side below it. Placeholder text is expected until
the later milestones add KPI values and charts.

## License

This tutorial is provided for educational purposes.
