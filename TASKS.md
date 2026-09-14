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

### TASK-1: Set up the environment and project (M1)

Initialize the Python 3.11+ project, declare Streamlit, Pandas, and Plotly dependencies, and document how to install dependencies and run the dashboard locally.

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
