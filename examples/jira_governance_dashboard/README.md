# Jira Managed Services Governance Dashboard Prototype

This is a beginner-friendly Streamlit prototype for an executive Jira Managed Services Governance Dashboard. It uses realistic mock Jira data now and includes a sidebar upload control so you can replace the sample data with your own Jira CSV export later.

## What the dashboard includes

- **Executive Dashboard**: active tickets, delayed tickets, status, priority, assignee workload, aging tickets, due-this-week tickets, and completed tickets.
- **SLA Tracking**: SLA met/missed, overdue tickets, average response time, and escalated tickets.
- **Capacity View**: tickets by resource, estimated hours, actual hours, workload chart, and overallocated resources.
- **Risk & Escalation View**: high-priority tickets, blocked tickets, escalated items, and aging critical items.
- **Weekly Governance Review**: new tickets, delayed tickets, risks, escalations, capacity concerns, and open action items.

## Folder contents

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit application. |
| `sample_jira_tickets.csv` | Mock Jira data used by default. |
| `requirements.txt` | Python packages needed to run the app. |

## How to run it

You do not need coding experience. Follow these steps from the repository root.

### 1. Open a terminal

Make sure you are in the main `Flowise` repository folder.

### 2. Create a Python virtual environment

```bash
python -m venv .venv-jira-dashboard
```

### 3. Activate the virtual environment

On macOS or Linux:

```bash
source .venv-jira-dashboard/bin/activate
```

On Windows PowerShell:

```powershell
.venv-jira-dashboard\Scripts\Activate.ps1
```

### 4. Install the required packages

```bash
pip install -r examples/jira_governance_dashboard/requirements.txt
```

### 5. Start the dashboard

```bash
streamlit run examples/jira_governance_dashboard/app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`. Open that URL in your browser.

## How to use your own Jira export later

1. Export your Jira issues as a CSV file.
2. Start the Streamlit app.
3. Use the sidebar field named **Optional: upload your Jira CSV later**.
4. Upload your CSV.

For the first prototype, your CSV should contain these columns:

- `issue_key`
- `summary`
- `status`
- `priority`
- `assignee`
- `created`
- `due_date`
- `resolved`
- `estimated_hours`
- `actual_hours`
- `response_hours`
- `sla_target_hours`
- `escalated`
- `blocked`
- `action_item`

The app also supports an optional `client` column for filtering by customer or business unit.

## Notes for production use

- The prototype uses a fixed reporting date of **2026-05-17** so the sample data remains stable.
- Before using this operationally, confirm your Jira field names, SLA rules, capacity assumptions, and priority definitions.
- If your Jira CSV has different column names, update the `required_columns` mapping in `app.py`.
