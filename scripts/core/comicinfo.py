import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
import zipfile


def _prettify_xml(elem: ET.Element) -> str:
    """Return pretty formatted XML string."""
    rough_string = ET.tostring(elem, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# ComicInfo.xml generation and embedding
def generate_comicinfo_xml(metadata: dict) -> str:
    """
    Generate ComicInfo.xml content from metadata dict.

    Expected metadata keys:
        title
        series
        volume
        number
        summary
        writers (list or str)
        publisher
        year
        month
        day
        genres (list or str)
        tags (list or str)
        age_rating
    """

    comic = ET.Element("ComicInfo")

    def add(tag, value):
        if value:
            el = ET.SubElement(comic, tag)
            el.text = str(value)

    # Basic
    add("Title", metadata.get("title"))
    add("Series", metadata.get("series"))
    add("Volume", metadata.get("volume"))
    add("Number", metadata.get("number"))

    # Summary
    add("Summary", metadata.get("summary"))

    # Writers
    writers = metadata.get("writers")
    if isinstance(writers, list):
        writers = ", ".join(writers)
    add("Writer", writers)

    # Publisher
    add("Publisher", metadata.get("publisher"))

    # Date
    add("Year", metadata.get("year"))
    add("Month", metadata.get("month"))
    add("Day", metadata.get("day"))

    # Genre
    genres = metadata.get("genres")
    if isinstance(genres, list):
        genres = ", ".join(genres)
    add("Genre", genres)

    # Tags
    tags = metadata.get("tags")
    if isinstance(tags, list):
        tags = ", ".join(tags)
    add("Tags", tags)

    # Age Rating
    add("AgeRating", metadata.get("age_rating"))

    return _prettify_xml(comic)


def save_comicinfo_file(output_path: Path, metadata: dict):
    """Save ComicInfo.xml next to file."""
    xml_content = generate_comicinfo_xml(metadata)

    output_file = output_path.parent / "ComicInfo.xml"
    output_file.write_text(xml_content, encoding="utf-8")


def embed_comicinfo_into_cbz(cbz_path: Path, metadata: dict):
    """
    Embed ComicInfo.xml into existing CBZ archive.
    """

    xml_content = generate_comicinfo_xml(metadata)

    with zipfile.ZipFile(cbz_path, "a", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("ComicInfo.xml", xml_content)