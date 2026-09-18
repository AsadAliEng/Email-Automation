# Debugged n8n workflow

Import `email-automation-debugged.json` for the short Task 2 demonstration flow.

## Fixes included

- Disabled source rows are filtered before HTTP requests. A row with `Enabled = FALSE` is never fetched or appended.
- Source URLs are retained when emails are extracted.
- Boolean values such as `false`, `FALSE`, and `0` are treated consistently.
- The Gmail reply search is narrowed to the current contact and the last day, excluding sent mail and including delivery-daemon messages for bounce detection.
- The stop gate ignores unrelated Gmail results and stops only when the current contact appears in a reply or bounce result.
- Email 2 receives the original contact item directly and logs its message ID.

## Import and test order

1. Import `email-automation-debugged.json` as a new workflow.
2. Re-select the existing Google Sheets and Gmail credentials on the imported nodes.
3. Set the Sheet ID in all Google Sheets nodes.
4. Keep only a valid, accessible test mailbox with `Status = New` in `Contacts`.
5. Keep the Django source disabled (`Enabled = FALSE`).
6. Set `delay_hours_1` to `0.0167` for the short demonstration wait.
7. Execute from `Manual Start`, not from `Send Email 2`.

Expected successful path:

`Email 1 → Log Email 1 → Wait → Check Replies (0 relevant items) → Stop gate → Email 2 → Log Email 2`

Expected bounce/reply path:

`Email 1 → Log Email 1 → Wait → Check Replies (matching bounce/reply) → Stop gate with 0 output → Email 2 skipped`
