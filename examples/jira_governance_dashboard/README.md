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

## Exactly where to replace the sample CSV later

You have two simple options. Use **Option A** if you do not want to edit any files. Use **Option B** if you want your Jira export to become the default dataset every time the app opens.

### Option A: Upload your Jira CSV inside the dashboard, no code changes

1. Export your issues from Jira as a CSV file.
2. Start the dashboard with:

   ```bash
   streamlit run examples/jira_governance_dashboard/app.py
   ```

3. In the left sidebar, find **Optional: upload your Jira CSV later**.
4. Click **Browse files** and select your Jira CSV export.
5. The dashboard will use your uploaded CSV for that browser session. The original mock CSV file remains untouched.

### Option B: Replace the default sample CSV file

1. Save a backup copy of the current sample file if you want to keep it:

   ```bash
   cp examples/jira_governance_dashboard/sample_jira_tickets.csv examples/jira_governance_dashboard/sample_jira_tickets.backup.csv
   ```

2. Copy your real Jira export into this exact location and filename:

   ```text
   examples/jira_governance_dashboard/sample_jira_tickets.csv
   ```

3. Restart the dashboard. The app loads that file by default because `app.py` points to:

   ```python
   SAMPLE_DATA_PATH = APP_DIR / "sample_jira_tickets.csv"
   ```

4. If you prefer to keep your export under a different filename, place it in the same folder and change only the filename in `SAMPLE_DATA_PATH` inside `examples/jira_governance_dashboard/app.py`.

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
