# Portfolio IQ — Intelligence Dashboard

A professional, enterprise-style dashboard for tracking a portfolio of projects:
their health, budgets, risks, and milestones. It's built to *look and feel like
a real SaaS product* — but it stays deliberately simple under the hood.

> **This iteration uses sample data only.** There is no database, no login, no
> external APIs, and no paid services. Everything runs inside a single file.

---

## What the application does

**Navigation (left sidebar)** — click to move between seven sections:
Dashboard, Portfolio, Projects, Risks & Issues, Financials, Reports, Settings.

- **Dashboard** — the executive view. Six headline numbers (Total Projects, On
  Track, At Risk, Delayed, Total Portfolio Budget, Actual Spend), a **Portfolio
  Health** donut using Red / Amber / Green indicators, a **Financial Overview**
  (budget vs actual), the **Top 5 Risks**, and **Upcoming Milestones** (next 90 days).
- **Portfolio** — portfolio health and the full **Project Portfolio table**
  (Project Name, Project Manager, Business Unit, Status, % Complete, Budget,
  Actual Spend, Target Completion Date) across 8 sample projects.
- **Projects** — the same projects as cards, with a working **search box** and
  **status filters** (All / On Track / At Risk / Delayed).
- **Risks & Issues** — the full risk register, ranked by priority.
- **Financials** — budget vs actual spend, remaining budget, and utilization %.
- **Reports** — generate an on-screen **preview** of a report, or **Print /
  Export to PDF** (uses your browser's built-in print).
- **Settings** — change the organization name, accent color, and table density.
  Your choices are remembered by the browser.

**Interactive touches:** clicking any project (row or card) opens a **detail
panel** with its risks and milestones. Clicking the "At Risk" or "Delayed" tiles
on the Dashboard jumps to a filtered project list.

---

## How to preview it

The whole app is one file — **`index.html`** — with nothing to install:

1. Open the `portfolio-dashboard` folder.
2. Double-click **`index.html`** — it opens in your web browser.

(While we work together, there is also a live hosted preview link in the chat.)

---

## How the code is organized

Everything lives in **`index.html`**, split into three clearly-labeled parts:

1. **STYLING (CSS)** — the visual design. All colors and spacing come from a set
   of "design tokens" (the `--variables` at the top), so the look stays
   consistent and is easy to re-theme.
2. **STRUCTURE (HTML)** — the fixed frame: the sidebar, the top bar, and the
   empty main area that each screen is drawn into.
3. **BEHAVIOR (JavaScript)** — the "brain", organized into numbered sections:
   1. **Sample data** — the single source of truth (projects, risks, milestones).
      *Change a number here and every screen updates automatically.*
   2. **Settings** — small preferences saved in the browser.
   3. **Helpers** — formatting money/dates and calculating portfolio totals.
   4. **Icons** — small inline SVGs (no icon library needed).
   5. **Navigation** — the menu and the "router" that swaps between screens.
   6. **The views** — one function builds each screen from the data.
   7. **Interactions** — search, filters, the detail panel, report previews.
   8. **Start-up** — the code that runs once when the page loads.

### The key idea
The screen is always **built from the data**, never hand-typed. The KPI totals,
the health donut, and the charts are all *calculated* from the project list. That
single principle is what makes this a real dashboard rather than a static mock-up
— and it's exactly how professional business-intelligence tools work.

### A note on dates
So the demo always looks populated, "today" is fixed to **8 August 2026**
(`REFERENCE_DATE` in the code). The "next 90 days" milestones are measured from
that date.
