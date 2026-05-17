"""Streamlit prototype for a Jira Managed Services Governance Dashboard.

This app ships with realistic sample Jira data and also supports replacing the
sample records with a CSV export from Jira later.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

APP_DIR = Path(__file__).parent
SAMPLE_DATA_PATH = APP_DIR / "sample_jira_tickets.csv"
TODAY = date(2026, 5, 17)
STATUS_ORDER = ["To Do", "In Progress", "Blocked", "In Review", "Done"]
PRIORITY_ORDER = ["Critical", "High", "Medium", "Low"]

st.set_page_config(
    page_title="Jira Managed Services Governance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_sample_data() -> pd.DataFrame:
    """Load the bundled sample Jira dataset."""
    return pd.read_csv(SAMPLE_DATA_PATH)


def normalise_jira_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Prepare either sample data or a Jira CSV export for dashboard reporting."""
    df = raw_df.copy()
    df.columns = [column.strip().lower().replace(" ", "_") for column in df.columns]

    required_columns = {
        "issue_key": "Issue Key",
        "summary": "Summary",
        "status": "Status",
        "priority": "Priority",
        "assignee": "Assignee",
        "created": "Created",
        "due_date": "Due Date",
        "resolved": "Resolved",
        "estimated_hours": "Estimated Hours",
        "actual_hours": "Actual Hours",
        "response_hours": "Response Hours",
        "sla_target_hours": "SLA Target Hours",
        "escalated": "Escalated",
        "blocked": "Blocked",
        "action_item": "Action Item",
    }

    missing = [source_name for column, source_name in required_columns.items() if column not in df.columns]
    if missing:
        st.error(
            "Your CSV is missing columns needed by this prototype: " + ", ".join(missing)
        )
        st.stop()

    for column in ["created", "due_date", "resolved"]:
        df[column] = pd.to_datetime(df[column], errors="coerce")

    numeric_columns = ["estimated_hours", "actual_hours", "response_hours", "sla_target_hours"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    for column in ["escalated", "blocked", "action_item"]:
        df[column] = df[column].astype(str).str.strip().str.lower().isin(["true", "yes", "1", "y"])

    df["is_completed"] = df["status"].eq("Done") | df["resolved"].notna()
    df["active"] = ~df["is_completed"]
    df["age_days"] = (pd.Timestamp(TODAY) - df["created"]).dt.days.clip(lower=0)
    df["is_delayed"] = df["active"] & df["due_date"].notna() & (df["due_date"].dt.date < TODAY)
    df["due_this_week"] = (
        df["active"]
        & df["due_date"].notna()
        & (df["due_date"].dt.date >= TODAY)
        & (df["due_date"].dt.date <= TODAY + timedelta(days=7))
    )
    df["sla_met"] = df["response_hours"] <= df["sla_target_hours"]
    df["aging_ticket"] = df["active"] & (df["age_days"] >= 14)
    df["aging_critical"] = df["active"] & df["priority"].isin(["Critical", "High"]) & (df["age_days"] >= 10)
    df["workload_variance"] = df["actual_hours"] - df["estimated_hours"]
    return df


def metric_card(label: str, value: int | float | str, help_text: str | None = None) -> None:
    st.metric(label, value, help=help_text)


def chart_template(fig):
    fig.update_layout(
        margin=dict(l=10, r=10, t=45, b=10),
        legend_title_text="",
        font=dict(size=13),
    )
    return fig


def show_ticket_table(df: pd.DataFrame, title: str, limit: int | None = None) -> None:
    st.subheader(title)
    columns = [
        "issue_key",
        "summary",
        "status",
        "priority",
        "assignee",
        "due_date",
        "age_days",
        "estimated_hours",
        "actual_hours",
    ]
    table_df = df[columns].copy()
    table_df["due_date"] = table_df["due_date"].dt.strftime("%Y-%m-%d").fillna("Not set")
    if limit:
        table_df = table_df.head(limit)
    st.dataframe(
        table_df.rename(
            columns={
                "issue_key": "Issue",
                "summary": "Summary",
                "status": "Status",
                "priority": "Priority",
                "assignee": "Assignee",
                "due_date": "Due Date",
                "age_days": "Age (Days)",
                "estimated_hours": "Est. Hours",
                "actual_hours": "Actual Hours",
            }
        ),
        hide_index=True,
        use_container_width=True,
    )


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.title("Governance Filters")
    st.sidebar.caption("Use these filters for an executive review by client, status, priority, or owner.")

    uploaded_file = st.sidebar.file_uploader(
        "Optional: upload your Jira CSV later",
        type=["csv"],
        help="For now, leave this blank to use the bundled sample Jira data.",
    )
    if uploaded_file is not None:
        df = normalise_jira_data(pd.read_csv(uploaded_file))
        st.sidebar.success("Using uploaded Jira CSV")
    else:
        st.sidebar.info("Using realistic sample Jira data")

    client_options = sorted(df["client"].dropna().unique()) if "client" in df.columns else []
    selected_clients = st.sidebar.multiselect("Client", client_options, default=client_options)
    selected_statuses = st.sidebar.multiselect("Status", STATUS_ORDER, default=STATUS_ORDER)
    selected_priorities = st.sidebar.multiselect("Priority", PRIORITY_ORDER, default=PRIORITY_ORDER)
    assignee_options = sorted(df["assignee"].dropna().unique())
    selected_assignees = st.sidebar.multiselect("Assignee", assignee_options, default=assignee_options)

    filtered = df[
        df["status"].isin(selected_statuses)
        & df["priority"].isin(selected_priorities)
        & df["assignee"].isin(selected_assignees)
    ]
    if client_options:
        filtered = filtered[filtered["client"].isin(selected_clients)]

    st.sidebar.divider()
    st.sidebar.caption(
        "Prototype date anchor: 2026-05-17. Replace sample data and this anchor when moving to production."
    )
    return filtered


def executive_dashboard(df: pd.DataFrame) -> None:
    st.header("1. Executive Dashboard")
    active = df[df["active"]]
    completed = df[df["is_completed"]]

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        metric_card("Total Active Tickets", len(active), "Open tickets that are not marked Done")
    with kpi_cols[1]:
        metric_card("Delayed Tickets", int(df["is_delayed"].sum()), "Active tickets past due date")
    with kpi_cols[2]:
        metric_card("Due This Week", int(df["due_this_week"].sum()), "Active tickets due in the next 7 days")
    with kpi_cols[3]:
        metric_card("Completed Tickets", len(completed), "Tickets marked Done or resolved")

    chart_cols = st.columns(2)
    with chart_cols[0]:
        status_counts = df["status"].value_counts().reindex(STATUS_ORDER, fill_value=0).reset_index()
        status_counts.columns = ["Status", "Tickets"]
        fig = px.bar(status_counts, x="Status", y="Tickets", color="Status", title="Tickets by Status")
        st.plotly_chart(chart_template(fig), use_container_width=True)
    with chart_cols[1]:
        priority_counts = df["priority"].value_counts().reindex(PRIORITY_ORDER, fill_value=0).reset_index()
        priority_counts.columns = ["Priority", "Tickets"]
        fig = px.pie(priority_counts, names="Priority", values="Tickets", title="Tickets by Priority", hole=0.45)
        st.plotly_chart(chart_template(fig), use_container_width=True)

    chart_cols = st.columns(2)
    with chart_cols[0]:
        by_assignee = df.groupby("assignee", as_index=False).size().rename(columns={"size": "Tickets"})
        fig = px.bar(by_assignee, x="assignee", y="Tickets", color="Tickets", title="Tickets by Assignee")
        st.plotly_chart(chart_template(fig), use_container_width=True)
    with chart_cols[1]:
        aging = active.sort_values("age_days", ascending=False).head(10)
        fig = px.bar(aging, x="issue_key", y="age_days", color="priority", title="Top Aging Active Tickets")
        st.plotly_chart(chart_template(fig), use_container_width=True)

    show_ticket_table(df[df["due_this_week"]].sort_values("due_date"), "Due This Week")


def sla_tracking(df: pd.DataFrame) -> None:
    st.header("2. SLA Tracking")
    active = df[df["active"]]
    sla_missed = df[~df["sla_met"]]
    overdue = df[df["is_delayed"]]
    escalated = df[df["escalated"]]

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        metric_card("SLA Met", int(df["sla_met"].sum()))
    with kpi_cols[1]:
        metric_card("SLA Missed", len(sla_missed))
    with kpi_cols[2]:
        metric_card("Avg Response Time", f"{df['response_hours'].mean():.1f} hrs")
    with kpi_cols[3]:
        metric_card("Escalated Tickets", len(escalated))

    chart_cols = st.columns(2)
    with chart_cols[0]:
        sla_summary = pd.DataFrame(
            {"SLA Result": ["Met", "Missed"], "Tickets": [int(df["sla_met"].sum()), len(sla_missed)]}
        )
        fig = px.bar(sla_summary, x="SLA Result", y="Tickets", color="SLA Result", title="SLA Met vs Missed")
        st.plotly_chart(chart_template(fig), use_container_width=True)
    with chart_cols[1]:
        response_by_priority = df.groupby("priority", as_index=False)["response_hours"].mean()
        fig = px.bar(
            response_by_priority,
            x="priority",
            y="response_hours",
            category_orders={"priority": PRIORITY_ORDER},
            color="priority",
            title="Average Response Time by Priority",
        )
        st.plotly_chart(chart_template(fig), use_container_width=True)

    show_ticket_table(overdue.sort_values("due_date"), "Overdue Tickets")
    show_ticket_table(active[active["escalated"]].sort_values("priority"), "Escalated Active Tickets")


def capacity_view(df: pd.DataFrame) -> None:
    st.header("3. Capacity View")
    resource_capacity = st.slider("Weekly capacity per resource (hours)", min_value=20, max_value=60, value=40, step=5)
    active = df[df["active"]]
    workload = (
        active.groupby("assignee", as_index=False)
        .agg(tickets=("issue_key", "count"), estimated_hours=("estimated_hours", "sum"), actual_hours=("actual_hours", "sum"))
        .sort_values("estimated_hours", ascending=False)
    )
    workload["capacity_hours"] = resource_capacity
    workload["overallocated"] = workload["estimated_hours"] > workload["capacity_hours"]

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        metric_card("Active Resources", workload["assignee"].nunique())
    with kpi_cols[1]:
        metric_card("Estimated Hours", f"{workload['estimated_hours'].sum():.0f}")
    with kpi_cols[2]:
        metric_card("Actual Hours", f"{active['actual_hours'].sum():.0f}")
    with kpi_cols[3]:
        metric_card("Overallocated", int(workload["overallocated"].sum()))

    fig = px.bar(
        workload,
        x="assignee",
        y=["estimated_hours", "actual_hours", "capacity_hours"],
        barmode="group",
        title="Resource Workload: Estimated vs Actual vs Capacity",
    )
    st.plotly_chart(chart_template(fig), use_container_width=True)

    st.subheader("Resource Workload Detail")
    st.dataframe(
        workload.rename(
            columns={
                "assignee": "Resource",
                "tickets": "Active Tickets",
                "estimated_hours": "Estimated Hours",
                "actual_hours": "Actual Hours",
                "capacity_hours": "Capacity Hours",
                "overallocated": "Overallocated",
            }
        ),
        hide_index=True,
        use_container_width=True,
    )

    overallocated_resources = workload[workload["overallocated"]]["assignee"].tolist()
    if overallocated_resources:
        st.warning("Capacity concern: " + ", ".join(overallocated_resources) + " exceed selected weekly capacity.")
    else:
        st.success("No resources are overallocated under the selected capacity threshold.")


def risk_escalation_view(df: pd.DataFrame) -> None:
    st.header("4. Risk & Escalation View")
    active = df[df["active"]]
    high_priority = active[active["priority"].isin(["Critical", "High"])]
    blocked = active[active["blocked"]]
    escalated = active[active["escalated"]]
    aging_critical = active[active["aging_critical"]]

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        metric_card("High Priority", len(high_priority))
    with kpi_cols[1]:
        metric_card("Blocked", len(blocked))
    with kpi_cols[2]:
        metric_card("Escalated", len(escalated))
    with kpi_cols[3]:
        metric_card("Aging Critical", len(aging_critical))

    risk_df = pd.DataFrame(
        {
            "Risk Type": ["High Priority", "Blocked", "Escalated", "Aging Critical"],
            "Tickets": [len(high_priority), len(blocked), len(escalated), len(aging_critical)],
        }
    )
    fig = px.bar(risk_df, x="Risk Type", y="Tickets", color="Risk Type", title="Risk and Escalation Summary")
    st.plotly_chart(chart_template(fig), use_container_width=True)

    show_ticket_table(high_priority.sort_values(["priority", "age_days"], ascending=[True, False]), "High Priority Tickets")
    show_ticket_table(blocked.sort_values("age_days", ascending=False), "Blocked Tickets")
    show_ticket_table(aging_critical.sort_values("age_days", ascending=False), "Aging Critical Items")


def weekly_governance_review(df: pd.DataFrame) -> None:
    st.header("5. Weekly Governance Review")
    week_start = pd.Timestamp(TODAY - timedelta(days=7))
    active = df[df["active"]]
    new_tickets = df[df["created"] >= week_start]
    delayed = df[df["is_delayed"]]
    risks = active[active["priority"].isin(["Critical", "High"]) | active["blocked"] | active["aging_critical"]]
    escalations = active[active["escalated"]]
    action_items = active[active["action_item"]]

    st.info("Use this page as a ready-made agenda for a weekly managed services governance meeting.")
    agenda_cols = st.columns(3)
    with agenda_cols[0]:
        metric_card("New Tickets", len(new_tickets))
        metric_card("Delayed Tickets", len(delayed))
    with agenda_cols[1]:
        metric_card("Risks", len(risks))
        metric_card("Escalations", len(escalations))
    with agenda_cols[2]:
        capacity_by_resource = active.groupby("assignee")["estimated_hours"].sum()
        metric_card("Capacity Concerns", int((capacity_by_resource > 40).sum()))
        metric_card("Open Action Items", len(action_items))

    tabs = st.tabs(["New Tickets", "Delayed", "Risks", "Escalations", "Capacity", "Actions"])
    with tabs[0]:
        show_ticket_table(new_tickets.sort_values("created", ascending=False), "New Tickets This Week")
    with tabs[1]:
        show_ticket_table(delayed.sort_values("due_date"), "Delayed Tickets")
    with tabs[2]:
        show_ticket_table(risks.sort_values("age_days", ascending=False), "Risks")
    with tabs[3]:
        show_ticket_table(escalations.sort_values("age_days", ascending=False), "Escalations")
    with tabs[4]:
        capacity = active.groupby("assignee", as_index=False)["estimated_hours"].sum()
        capacity["Concern"] = capacity["estimated_hours"].apply(lambda hours: "Review" if hours > 40 else "OK")
        st.dataframe(capacity.rename(columns={"assignee": "Resource", "estimated_hours": "Estimated Hours"}), hide_index=True, use_container_width=True)
    with tabs[5]:
        show_ticket_table(action_items.sort_values("due_date"), "Open Action Items")


def main() -> None:
    st.title("📊 Jira Managed Services Governance Dashboard")
    st.caption(
        "Executive-friendly Streamlit prototype using realistic mock Jira data. "
        "Upload your Jira CSV later from the sidebar when it becomes available."
    )

    base_df = normalise_jira_data(load_sample_data())
    df = apply_filters(base_df)

    if df.empty:
        st.warning("No tickets match the selected filters. Adjust the sidebar filters to see dashboard data.")
        return

    pages = {
        "Executive Dashboard": executive_dashboard,
        "SLA Tracking": sla_tracking,
        "Capacity View": capacity_view,
        "Risk & Escalation View": risk_escalation_view,
        "Weekly Governance Review": weekly_governance_review,
    }
    selected_page = st.sidebar.radio("Dashboard Page", list(pages.keys()))
    pages[selected_page](df)

    st.divider()
    st.caption("Prototype only: validate field mappings, SLA logic, and capacity assumptions before operational use.")


if __name__ == "__main__":
    main()
