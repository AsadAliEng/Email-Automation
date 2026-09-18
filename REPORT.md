# Task 2 Report

## Objective

Build a restartable n8n email sequence that fetches permitted public pages, extracts and deduplicates visible email addresses, records them in Google Sheets, sends up to three configured messages, and stops on reply, bounce, or unsubscribe.

## Workflow design

1. Manual trigger starts a run.
2. Google Sheets Config is read and the control mode is checked. `Pause` exits safely; `Restart` resets eligible sequence state on the next run.
3. Enabled Sources rows are split, fetched with HTTP Request, and processed by a Code node using a conservative email regex.
4. Valid lower-case emails are deduplicated and appended to Contacts with `New` status.
5. Contacts are re-read. Only eligible records are sent through the configured Gmail/Outlook node.
6. Every send records the provider message ID and timestamp in Contacts and Logs.
7. Wait applies the configured delay. A reply/stop-signal check runs before the next message.
8. A stop condition changes status to `Replied`, `Unsubscribed`, `Bounced`, or `Stopped`; no later message is sent.
9. Retryable HTTP/email errors use up to three attempts with backoff and are logged in Logs.

## Data model

The Google Sheets tab structure and columns are documented in `GOOGLE_SHEETS_SCHEMA.md`. `Contacts` is the current state; `Logs` is append-only history.

## Security and compliance

Credentials are n8n credentials only. The repository contains no passwords or tokens. The workflow has explicit unsubscribe/stop words and should be used only for permitted, relevant outreach with a test mailbox during demonstration.

## Verification checklist

- Import JSON and attach credentials.
- Populate 5–7 permitted public test URLs.
- Confirm at least five valid emails appear in Contacts.
- Run a test contact through sequence 1 and 2 and verify Message IDs/timestamps in Logs.
- Set `control_mode` to `Pause`, run again, and confirm no send.
- Simulate a reply or stop word and confirm status changes and later sends are skipped.
- Force one HTTP/send error and confirm retries plus an Error log row.

## Loom outline

Show the sheet tabs, imported workflow, one full run, the log rows, a simulated reply/unsubscribe, and a restart using the Config toggle. Add the Loom link here before PDF conversion.
