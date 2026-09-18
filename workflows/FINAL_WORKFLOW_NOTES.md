# Final Task 2 workflow

Import `email-automation-final.json` for the repaired short demonstration flow.

## Why this version fixes the failed path

- The Contacts branch is independent from source extraction, so an empty/disabled source list cannot prevent existing test contacts from reaching Email 1.
- `Enabled = FALSE` source rows are filtered before any HTTP request.
- Gmail reply lookup is limited to the current contact, the last day, and excludes sent mail. Mail-delivery-daemon messages remain available for bounce detection.
- The stop node passes the contact forward when no matching reply/bounce is found; it returns zero items only for a matching message.
- Email 2 and its log node receive the original contact item directly.

Source extraction appends new contacts for the next run. The current run processes contacts already present in the Contacts tab, which makes the flow deterministic and restartable.

## Test sequence

1. Import this JSON as a new n8n workflow.
2. Re-select the Google Sheets and Gmail credentials.
3. Replace `GOOGLE_SHEET_ID` in every Google Sheets node.
4. Keep one valid, accessible test mailbox as `New` in Contacts.
5. Keep invalid/bounced contacts as `Bounced` and the Django source as `FALSE`.
6. Set `delay_hours_1` to `0.0167` for a short wait.
7. Execute from `Manual Start`.

Success path:

`Send Email 1 → Log Email 1 → Wait → Check Replies (no matching item) → Stop gate → Send Email 2 → Log Email 2`

Stop path:

`Check Replies (matching reply/bounce) → Stop gate with no output → Email 2 is correctly skipped`
