from pathlib import Path
import gzip
import urllib.request
import xml.etree.ElementTree as ET

SOURCES = [
    "https://epgshare01.online/epgshare01/epg_ripper_DE1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_IT1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_IL1.xml.gz",
]

KEEP_CHANNEL_IDS = {
    # Germany
    "Das.Erste.de","ZDF.de","3sat.de","ARD.alpha.de","ARTE.de","DELUXE.MUSIC.de",
    "KIKA.de","ONE.de","PHOENIX.de","tagesschau24.de","WELT.de","ZDFinfo.de","ZDFneo.de",
    "BR.de","HR.de","MDR.de","NDR.de","RBB.de","SWR/SR.de","WDR.de",

    # Italy
    "Rai1.it","Rai2.it","Rai3.it","Rete.4.it","Canale.5.it","Italia.1.it","LA7.HD.it",
    "TV8.HD.it","Nove.it","20.it","Rai4.it","Iris.it","Rai5.it","RaiMovie.it","RaiPremium.it",
    "cielo.it","27.Twentyseven.it","QVC.it","Food.Network.it","Giallo.TV.it","K2.it",
    "RaiGulp.it","RaiYoyo.it","Frisbee.it","RaiNews24.it","RaiStoria.it","RaiScuola.it",
    "RaiSport.it","Sportitalia.it","SuperTennis.HD.it","Deejay.TV.it","Radio.Italia.TV.HD.it",
    "RADIONORBA.TV.it","R101tv.it","RMC.it","Virgin.Radio.it","TRM.h24.it","TG.NORBA.24.it",
    "GoldTV.it","7Gold.it","TelecolorLombardia.it","Telenova.it",

    # Israel
    "Kan11.il","Channel13.il",

    # Keshet 12 - multiple likely IDs included as fallback
    "Keshet12.il","Keshet.12.il","Keshet12.2018.il","קשת.il","קשת.12.il","ערוץ.12.il","Channel12.il",
}

def fetch_xml_root(url: str) -> ET.Element:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        raw = resp.read()
    if url.endswith(".gz"):
        raw = gzip.decompress(raw)
    return ET.fromstring(raw)

def main():
    out_root = ET.Element("tv", attrib={"generator-info-name": "filtered-epg-builder"})
    added_channels = set()

    for src in SOURCES:
        root = fetch_xml_root(src)

        for channel in root.findall("channel"):
            cid = channel.attrib.get("id")
            if cid in KEEP_CHANNEL_IDS and cid not in added_channels:
                out_root.append(channel)
                added_channels.add(cid)

        for programme in root.findall("programme"):
            cid = programme.attrib.get("channel")
            if cid in KEEP_CHANNEL_IDS:
                out_root.append(programme)

    xml_bytes = ET.tostring(out_root, encoding="utf-8", xml_declaration=True)
    Path("epg_de_it_il.xml").write_bytes(xml_bytes)
    with gzip.open("epg_de_it_il.xml.gz", "wb") as f:
        f.write(xml_bytes)

    print("Channels kept:", len(added_channels))
    print("Kept IDs:", sorted(added_channels))

if __name__ == "__main__":
    main()
