# Google Sheets Schema

Create these four tabs in one spreadsheet.

## Config

Columns: `Key`, `Value`

Required keys: `control_mode`, `sender_name`, `sender_email`, `subject_1`, `subject_2`, `subject_3`, `template_1`, `template_2`, `template_3`, `delay_hours_1`, `delay_hours_2`, `quiet_start`, `quiet_end`, `stop_words`, `max_attempts`.

`control_mode` values are `Run`, `Pause`, or `Restart`. `stop_words` is a comma-separated list such as `unsubscribe,stop,remove,no thanks`.

## Sources

Columns: `Source_URL`, `Enabled`, `Last_Fetched`, `Fetch_Status`, `Error`

Use 5–7 public pages that visibly contain test or business contact emails and that you are permitted to fetch.

## Contacts

Columns: `Contact_Email`, `Source_URL`, `Status`, `Sequence`, `Last_Message_ID`, `Last_Sent_At`, `Reply_Detected`, `Unsubscribe_Detected`, `Attempts`, `Updated_At`

Valid statuses: `New`, `Sent_1`, `Sent_2`, `Sent_3`, `Replied`, `Unsubscribed`, `Bounced`, `Stopped`, `Error`.

## Logs

Columns: `Timestamp`, `Event`, `Contact_Email`, `Source_URL`, `Sequence`, `Message_ID`, `Status`, `Attempts`, `Details`
