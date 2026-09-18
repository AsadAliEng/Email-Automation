"""Local dry-run of the Task 2 extraction and stop/retry rules.

This script does not send email. It is a safe way to test the data logic before
connecting n8n credentials and a real test mailbox.
"""
import re
import time
from urllib.request import Request, urlopen

EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
STOP_WORDS = {"unsubscribe", "stop", "remove", "no thanks"}


def fetch(url, attempts=3):
    for attempt in range(1, attempts + 1):
        try:
            request = Request(url, headers={"User-Agent": "Task2-verification/1.0"})
            with urlopen(request, timeout=15) as response:
                return response.read().decode("utf-8", errors="ignore")
        except Exception:
            if attempt == attempts:
                raise
            time.sleep(2 ** (attempt - 1))


def extract(html, source_url):
    return [{"Contact_Email": email.lower(), "Source_URL": source_url, "Status": "New"}
            for email in sorted(set(EMAIL_RE.findall(html)))]


def should_stop(status, reply_text=""):
    text = reply_text.lower()
    return status in {"Replied", "Bounced", "Unsubscribed", "Stopped"} or any(word in text for word in STOP_WORDS)


if __name__ == "__main__":
    urls = ["https://example.com", "https://www.iana.org/domains/example"]
    contacts = {}
    for url in urls:
        try:
            for row in extract(fetch(url), url):
                contacts.setdefault(row["Contact_Email"], row)
        except Exception as exc:
            print(f"FETCH_ERROR {url}: {exc}")
    print(f"Unique contacts: {len(contacts)}")
    print(*contacts.values(), sep="\n")
    print("Stop simulation:", should_stop("Sent_1", "Please stop and unsubscribe me"))
