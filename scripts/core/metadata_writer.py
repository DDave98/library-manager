import pikepdf
from lxml import etree
from datetime import datetime

# Funkce pro zápis metadat do PDF souboru, využívající knihovnu pikepdf a lxml pro XMP
def write_pdf_metadata(file_path, metadata):
    """
    Zapíše metadata do:
    1) Document Info
    2) XMP (Dublin Core)
    """

    with pikepdf.open(file_path, allow_overwriting_input=True) as pdf:

        # -----------------------
        # 1️⃣ Document Info
        # -----------------------
        info = pdf.docinfo

        info["/Title"] = metadata.get("title", "")
        info["/Author"] = metadata.get("author", "")
        info["/Subject"] = metadata.get("summary", "")
        info["/Keywords"] = ", ".join(metadata.get("tags", []))
        info["/CreationDate"] = datetime.now().strftime("D:%Y%m%d%H%M%S")

        # -----------------------
        # 2️⃣ XMP Metadata
        # -----------------------
        rdf = etree.Element("rdf:RDF",
                            nsmap={
                                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                                "dc": "http://purl.org/dc/elements/1.1/"
                            })

        desc = etree.SubElement(rdf, "rdf:Description")

        # Title
        title = etree.SubElement(desc, "dc:title")
        title_seq = etree.SubElement(title, "rdf:Alt")
        li = etree.SubElement(title_seq, "rdf:li")
        li.text = metadata.get("title", "")

        # Author
        creator = etree.SubElement(desc, "dc:creator")
        creator_seq = etree.SubElement(creator, "rdf:Seq")
        li = etree.SubElement(creator_seq, "rdf:li")
        li.text = metadata.get("author", "")

        # Genre / Subjects
        subject = etree.SubElement(desc, "dc:subject")
        bag = etree.SubElement(subject, "rdf:Bag")

        for tag in metadata.get("genres", []):
            li = etree.SubElement(bag, "rdf:li")
            li.text = tag

        xmp_xml = etree.tostring(rdf, pretty_print=True, encoding="utf-8")

        pdf.open_metadata(set_pikepdf_as_editor=False).load_from_bytes(xmp_xml)

        pdf.save()

# Funkce pro zápis metadat do EPUB souboru, využívající knihovnu ebooklib
def write_epub_metadata(epub_path, metadata):
    from ebooklib import epub

    book = epub.read_epub(epub_path)

    book.set_title(metadata.get("title", ""))
    book.set_language(metadata.get("language", "cs"))

    if "author" in metadata:
        book.add_author(metadata["author"])

    if "publisher" in metadata:
        book.add_metadata("DC", "publisher", metadata["publisher"])

    if "summary" in metadata:
        book.add_metadata("DC", "description", metadata["summary"])

    if "genres" in metadata:
        for g in metadata["genres"]:
            book.add_metadata("DC", "subject", g)

    epub.write_epub(epub_path, book)