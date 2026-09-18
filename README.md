# Restartable Email Automation (n8n)

This folder contains the local, importable assets for Task 2. The workflow uses n8n credential-based Google Sheets, Gmail/Outlook, HTTP Request, Code, Wait, and error-handling nodes. No credentials or API keys are stored in this repository.

## Files

- `workflows/email-automation.json` — n8n workflow export template.
- `Sources.csv`, `Config.csv`, `Contacts.csv`, `Logs.csv` — Google Sheets tab templates.
- `GOOGLE_SHEETS_SCHEMA.md` — exact columns and setup instructions.
- `REPORT.md` — implementation report and walkthrough script.
- `scripts/simulate_workflow.py` — local dry-run for extraction, validation, deduplication, retries, and stop conditions.

## Setup in n8n

1. Create one Google Sheet with tabs named `Config`, `Sources`, `Contacts`, and `Logs`.
2. Import the CSV headers/data from this folder into the matching tabs.
3. Import `workflows/email-automation.json` into n8n.
4. Attach credential-based Google Sheets and Gmail/Outlook credentials to the relevant nodes.
5. Replace the `GOOGLE_SHEET_ID` value in the `Read Config`, `Read Sources`, `Append Contacts`, `Read New Contacts`, `Log Send`, `Read Stop Signals`, and `Log Error` nodes.
6. Set the sender email and test recipient policy in `Config`. Use a test account and only contacts for which outreach is permitted.
7. Run manually. The workflow reads the Config control (`Run`, `Pause`, `Restart`) at the start and before each sequence step.

## Local dry run

This safe simulation validates extraction, email validation, deduplication, retries, and stop-word handling without sending email:

``powershell
cd E:\PF\chatbot\Task2
python scripts\simulate_workflow.py
``

If `python` is not available on Windows, use:

``powershell
py -3 scripts\simulate_workflow.py
``

The bundled Sources.csv contains documentation/example URLs, so a result of Unique contacts: 0 is expected until you replace them with 5–7 permitted public pages that visibly publish testable email addresses.

## Safety and restart behavior

The workflow defaults new contacts to `New`, records every fetch/send/error event in `Logs`, skips contacts marked `Replied`, `Unsubscribed`, `Bounced`, or `Stopped`, and uses a per-contact sequence number. A configured quiet-hours check prevents sending during the configured window. Changing templates or delays affects the next run.

The JSON is intentionally a credential-free template. Credentials, sheet IDs, and live URLs must be configured in n8n rather than committed here.

## Recommended import

Use workflows/email-automation-complete.json for the final sequence. It includes Email 1, Email 2, Email 3, configured waits, Gmail reply searches, stop gates, and three-attempt retry settings. The earlier email-automation.json is the compact reference workflow.
