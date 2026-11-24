"""Download one day of IESO's Generator Output and Capability report (XML)."""

import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import requests

from ingest import EST

BASE_URL = "https://reports-public.ieso.ca/public/GenOutputCapability"
RAW_DIR = Path("data/raw")


def report_filename(day: date) -> str:
    # The dated file (no _vN suffix) is the latest version for that day.
    return f"PUB_GenOutputCapability_{day:%Y%m%d}.xml"


def fetch_report(day: date) -> bytes:
    url = f"{BASE_URL}/{report_filename(day)}"
    print("Fetching", url)
    # Give up after 30 seconds, so a stuck website can't freeze the robot forever.
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()  # Stop with an error if the download failed
    return resp.content


def yesterday_est() -> date:
    return datetime.now(EST).date() - timedelta(days=1)


def main() -> None:
    if len(sys.argv) > 1:
        day = date.fromisoformat(sys.argv[1])
    else:
        day = yesterday_est()

    xml = fetch_report(day)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out = RAW_DIR / report_filename(day)
    out.write_bytes(xml)
    print(f"Saved {out} ({len(xml) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()