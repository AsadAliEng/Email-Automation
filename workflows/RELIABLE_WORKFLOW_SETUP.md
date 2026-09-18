# Reliable Task 2 Workflow

Use `email-automation-reliable.json` for the end-to-end demonstration. It deliberately has one straight execution path and does not depend on webpage email extraction or a Gmail inbox search.

## Why the previous workflow appeared to stop

The source-ingestion branch could legitimately produce zero extracted email addresses. n8n does not run a downstream node when it receives zero input items, so `Append Contacts` was labelled `Node was not executed`. This is normal n8n behavior, but it made the workflow confusing to test. Separately, the inbox search returned historical Gmail delivery-failure messages; those messages caused the follow-up safety rule to stop Email 2.

## Before execution

1. In `Contacts`, retain one real test address that you can receive, with `Status` set to `New`, `Reply_Detected` set to `FALSE`, and `Unsubscribe_Detected` set to `FALSE`.
2. Set `Config > control_mode` to `Run`.
3. For the demonstration, set `Config > delay_hours_1` to `0.0167`. The workflow converts this to one minute.
4. Import `email-automation-reliable.json` into n8n.
5. For all Sheets nodes, select the same Google Sheets credential and this document URL:
   `https://docs.google.com/spreadsheets/d/10JqFBPtTNr_V-ZtHTkt06Zwrvr6PPbMRi1_ZWiK8DSY/edit`
6. Select the Gmail credential in the two Gmail nodes.

## Sheet names by node

| Node | Operation | Sheet by name |
| --- | --- | --- |
| Read Config | Get Row(s) | Config |
| Read Contacts | Get Row(s) | Contacts |
| Log Email 1 | Append Row | Logs |
| Log Email 2 | Append Row | Logs |

Run from `Manual Start`. Do not execute Email 2 directly because it needs the eligible contact item from earlier nodes.

If a recipient replies or unsubscribes, set `Reply_Detected` or `Unsubscribe_Detected` to `TRUE` in `Contacts` before a follow-up run. The safety node then intentionally sends no Email 2.
