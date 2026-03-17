#!/usr/bin/env python3
import gzip
import io
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

SOURCES = [
    "https://epgshare01.online/epgshare01/epg_ripper_DE1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_IT1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_IL1.xml.gz",
]

OUT_DIR = Path("docs")
OUT_DIR.mkdir(exist_ok=True)
OUT_XML = OUT_DIR / "epg_de_it_il.xml"
OUT_GZ = OUT_DIR / "epg_de_it_il.xml.gz"

def fetch_xml(url: str) -> ET.Element:
    with urllib.request.urlopen(url, timeout=60) as resp:
        raw = resp.read()
    if url.endswith(".gz"):
        raw = gzip.decompress(raw)
    return ET.fromstring(raw)

def main() -> int:
    tv = ET.Element("tv")
    seen_channels = set()
    total_programmes = 0

    for url in SOURCES:
        root = fetch_xml(url)

        for channel in root.findall("channel"):
            cid = channel.get("id")
            if cid and cid not in seen_channels:
                tv.append(channel)
                seen_channels.add(cid)

        for programme in root.findall("programme"):
            tv.append(programme)
            total_programmes += 1

    tree = ET.ElementTree(tv)
    tree.write(OUT_XML, encoding="utf-8", xml_declaration=True)

    with open(OUT_XML, "rb") as f_in, gzip.open(OUT_GZ, "wb", compresslevel=9) as f_out:
        f_out.write(f_in.read())

    print(f"Created {OUT_GZ} with {len(seen_channels)} channels and {total_programmes} programmes")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
