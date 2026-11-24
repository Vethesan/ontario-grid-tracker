"""Read one IESO report file and pull out clean numbers."""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Every label in IESO's file has a hidden "last name" (a namespace).
# This tells Python what that last name is, so it can find the labels.
NS = {"imo": "http://www.theIMO.com/schema"}


def main() -> None:
    path = Path(sys.argv[1])
    root = ET.fromstring(path.read_bytes())

    report_date = root.find(".//imo:Date", NS).text
    generators = root.findall(".//imo:Generator", NS)

    print(f"Report date: {report_date}")
    print(f"Generators found: {len(generators)}")

    for gen in generators:
        name = gen.find(".//imo:GeneratorName", NS).text
        fuel = gen.find(".//imo:FuelType", NS).text

        
        if name != "DARLINGTON-G1":
            continue

        for out in gen.findall(".//imo:Output", NS):
            hour = out.find(".//imo:Hour", NS).text
            mw = out.find(".//imo:EnergyMW", NS).text
            print(name, fuel, hour, mw)


if __name__ == "__main__":
    main()