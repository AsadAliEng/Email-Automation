# Restartable Email Automation with n8n

## Project Document

**Project:** Automation Engineer Task 2  
**Platform:** n8n  
**Email:** Gmail or Outlook through n8n credentials  
**Storage:** Google Sheets  
**Workflow export:** `workflows/email-automation-complete.json`

---

## 1. Project Overview

This project provides a reusable, restartable email automation workflow. It fetches permitted public webpages, extracts visible email addresses, validates and deduplicates them, stores contacts in Google Sheets, and sends a maximum of three configured email messages.

The sequence is controlled through a Config tab. It supports pause/run/restart behavior, configurable templates and delays, retry handling, logging, and stop conditions for replies, bounces, and unsubscribe signals.

---

## 2. Objectives

- Use n8n to build a restartable automation workflow.
- Fetch public webpages using HTTP Request nodes.
- Extract and validate visible email addresses.
- Deduplicate contacts before logging.
- Store contact state and message history in Google Sheets.
- Send up to three sequenced messages.
- Stop on reply, bounce, or unsubscribe.
- Retry failed fetches and sends up to three times.
- Keep credentials outside the exported workflow.

---

## 3. Workflow Architecture

```text
Manual Start
     |
     v
Read Config -> Run/Pause/Restart Gate
     |
     v
Read Sources -> Split Sources -> HTTP Request
     |
     v
Extract -> Validate -> Deduplicate -> Contacts Sheet
     |
     v
Read Eligible Contacts -> One Contact at a Time
     |
     v
Send Email 1 -> Log -> Update Contacts -> Wait
     |
     v
Search Replies -> Stop Gate
     |
     v
Send Email 2 -> Log -> Update Contacts -> Wait
     |
     v
Search Replies -> Stop Gate
     |
     v
Send Email 3 -> Log -> Update Contacts
```

---

## 4. Google Sheets Tabs

### Config

Stores sender details, subject lines, templates, delay hours, quiet hours, stop words, retry count, and control mode.

Important values:

```text
control_mode: Run / Pause / Restart
delay_hours_1: 24
delay_hours_2: 48
max_attempts: 3
stop_words: unsubscribe,stop,remove,no thanks
```

### Sources

Stores enabled public webpage URLs and fetch status.

### Contacts

Stores current contact state:

```text
Contact_Email
Source_URL
Status
Sequence
Last_Message_ID
Last_Sent_At
Reply_Detected
Unsubscribe_Detected
Attempts
Updated_At
```

### Logs

Append-only history of fetches, sends, retries, errors, and stop events.

---

## 5. Workflow Nodes

### Input and control

- Manual Start
- Read Config
- Run Pause Restart Gate

### Email extraction

- Read Sources
- Fetch Each Source
- HTTP Request
- Extract Validate Deduplicate
- Append Contacts

### Contact processing

- Read Eligible Contacts
- Filter Active Contacts
- One Contact Per Run

### Email sequence

- Send Email 1
- Wait Before Email 2
- Search Replies 1
- Stop If Reply Or Unsubscribe
- Send Email 2
- Wait Before Email 3
- Search Replies 2
- Stop Before Final Email
- Send Email 3

### Logging and persistence

- Log Email 1
- Update Contact After Email 1
- Log Email 2
- Update Contact After Email 2
- Log Email 3
- Update Contact After Email 3

---

## 6. Extraction and Deduplication

The Code node uses a conservative email pattern to identify visible addresses in fetched page content. Each address is converted to lowercase and stored only once per run.

Example normalized record:

```json
{
  "Contact_Email": "person@example.com",
  "Source_URL": "https://example.com/contact",
  "Status": "New",
  "Sequence": 0,
  "Attempts": 0
}
```

Only public pages that are permitted to be fetched should be used. The Sources tab must contain 5–7 approved test URLs for the final demonstration.

---

## 7. Sequence and Stop Rules

The workflow sends no more than three emails per contact:

1. Email 1 is sent immediately.
2. Configured delay 1 is applied.
3. Reply search and stop-word check run.
4. Email 2 is sent only if no stop signal exists.
5. Configured delay 2 is applied.
6. Reply search and stop-word check run again.
7. Email 3 is sent only if no stop signal exists.

The sequence stops when a contact is marked or detected as:

- Replied
- Unsubscribed
- Bounced
- Stopped

Stop words are configured through the Config tab and are not hard-coded into the email templates.

---

## 8. Retry and Error Handling

HTTP Request and email nodes are configured for up to three attempts with a backoff delay. Errors should be recorded in the Logs tab with:

- Timestamp
- Event
- Contact email
- Source URL
- Sequence
- Attempt count
- Error details

The workflow should be tested with one simulated fetch or send error to confirm retry behavior.

---

## 9. Security and Compliance

- No passwords, tokens, or API keys are stored in the JSON export.
- Gmail/Outlook and Google Sheets authentication uses n8n credentials.
- A test mailbox should be used for demonstration.
- Only permitted public pages should be fetched.
- Outreach should be relevant and compliant with applicable email rules.
- Every message includes a clear stop/unsubscribe instruction.

---

## 10. Setup Instructions

1. Create a Google Sheet with tabs: `Config`, `Sources`, `Contacts`, and `Logs`.
2. Import the CSV templates from this folder.
3. Add 5–7 permitted public URLs to `Sources`.
4. Import `workflows/email-automation-complete.json` into n8n.
5. Configure the Google Sheets credential.
6. Configure the Gmail or Outlook test credential.
7. Replace `GOOGLE_SHEET_ID` in Google Sheets nodes.
8. Set sender and test mailbox values in `Config`.
9. Set `control_mode` to `Run`.
10. Execute the workflow manually.

---

## 11. Testing Checklist

- [ ] At least 5 valid email addresses extracted.
- [ ] Duplicate email addresses removed.
- [ ] New contacts added with `New` status.
- [ ] Email 1 sent and logged with Message ID.
- [ ] Email 2 sent after configured delay.
- [ ] Email 3 sent only when no stop signal exists.
- [ ] Reply simulation stops the next email.
- [ ] Unsubscribe-word simulation stops the next email.
- [ ] Pause mode prevents sending.
- [ ] Restart mode reprocesses eligible state.
- [ ] Failed fetch/send retries up to three times.
- [ ] Error event is logged.
- [ ] Contact status and sequence update after each send.

### Screenshot Placeholders

Add screenshots below before converting to PDF:

1. Google Sheets tabs: `![Sheets tabs](screenshots/sheets-tabs.png)`
2. Config tab: `![Config](screenshots/config.png)`
3. n8n workflow canvas: `![Workflow](screenshots/workflow.png)`
4. Contacts tab: `![Contacts](screenshots/contacts.png)`
5. Logs tab: `![Logs](screenshots/logs.png)`
6. Reply/stop simulation: `![Stop simulation](screenshots/stop-simulation.png)`

---

## 12. Local Dry-Run

The local script can verify extraction and stop logic without sending email:

```powershell
cd E:\PF\chatbot\Task2
python -m py_compile scripts/simulate_workflow.py
python scripts/simulate_workflow.py
```

The script does not replace the n8n run. It is only a safe local verification of the code-based data logic.

---

## 13. Loom Walkthrough

The 5–7 minute video should show:

- Google Sheets tabs and Config values
- Imported n8n workflow
- HTTP extraction run
- Contacts created and deduplicated
- Email 1 and Email 2 logs
- Reply or unsubscribe simulation
- Sequence stopping correctly
- Pause/restart control
- Retry/error demonstration

**Clickable Loom URL:** [Add Loom URL here](https://www.loom.com/)

---

## 14. Known Limitations

- Live n8n credentials are not included in the export.
- A live Google Sheet ID must be configured after import.
- Test URLs must be replaced with permitted pages that contain visible test emails.
- Email provider behavior, reply search syntax, and message ID fields may require minor adjustment for the selected Gmail/Outlook node version.
- Screenshots, public links, Loom URL, and Google Drive link must be added before final submission.

---

## 15. Final Submission Checklist

- [ ] Google Sheet shared publicly
- [ ] n8n workflow JSON uploaded to Google Drive
- [ ] Workflow export link added
- [ ] Loom URL added inside this document
- [ ] Loom URL added to submission form
- [ ] Screenshots added
- [ ] PDF exported
- [ ] PDF uploaded to Google Drive
- [ ] Google Drive links made public
