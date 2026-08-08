# My First App

A very simple web application built with plain HTML, CSS, and JavaScript.
No database, no accounts, no extra software to install — just one file.

## What it does
1. Shows a professional home page with a heading and welcome message.
2. Has a **Get Started** button.
3. Clicking **Get Started** reveals a short form (Name and Email).
4. Clicking **Submit** saves your details and shows them back in a summary card.
5. The app **remembers you**: refresh or reopen the page and your details are
   still there. A **Start over** button clears them and returns to the start.
6. The form **checks your input** before saving: it asks for a name if the
   field is empty, and a valid email address if the email looks wrong, showing
   a friendly message under the field (no browser pop-ups).

### How it "remembers" without a database
It uses `localStorage` — a small notepad built into every web browser. Nothing
is sent anywhere; the data stays only inside your own browser. No database, no
server, no accounts, no extra software.

## How to preview it
The easiest way — **just open the file**:

1. Open the `my-first-app` folder on your computer.
2. Double-click `index.html`.
3. It opens in your web browser. That's it!

There is nothing to install and nothing to run in a terminal.

## The one file, explained
Everything lives in `index.html`, split into three clearly-labeled sections:
- **STRUCTURE (HTML)** — what's on the page.
- **STYLING (CSS)** — how it looks.
- **BEHAVIOR (JavaScript)** — what happens when you click.
