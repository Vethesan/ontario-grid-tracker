"""Read one IESO report file and pull out clean numbers."""

import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

from ingest import EST

# Every label in IESO's file has a hidden "last name" (a namespace).
# This tells Python what that last name is, so it can find the labels.
NS = {"imo": "http://www.theIMO.com/schema"}


def main() -> None:
    path = Path(sys.argv[1])
    root = ET.fromstring(path.read_bytes())

    report_date = root.find(".//imo:Date", NS).text
    generators = root.findall(".//imo:Generator", NS)

    # Midnight at the start of the report's day, on IESO's clock (EST, all year).
    midnight = datetime.fromisoformat(report_date).replace(tzinfo=EST)

    print(f"Report date: {report_date}")
    print(f"Generators found: {len(generators)}")

    rows = []  # an empty stack of cards

    for gen in generators:
        name = gen.find(".//imo:GeneratorName", NS).text
        fuel = gen.find(".//imo:FuelType", NS).text

        for out in gen.findall(".//imo:Output", NS):
            hour = int(out.find(".//imo:Hour", NS).text)

            mw_label = out.find(".//imo:EnergyMW", NS)
            if mw_label is None:
                mw = None
            else:
                mw = float(mw_label.text)

            # Hour 1 means midnight to 1 AM, so it STARTS at midnight + 0 hours.
            start = midnight + timedelta(hours=hour - 1)

            # Make one card for this generator + hour, and add it to the stack.
            rows.append({"generator": name, "fuel": fuel, "interval_start": start, "output_mw": mw})

    print(f"Rows: {len(rows)}")

    first = rows[0]
    last = rows[23]
    print(first["generator"], first["interval_start"], first["output_mw"])
    print(last["generator"], last["interval_start"], last["output_mw"])


if __name__ == "__main__":
    main()