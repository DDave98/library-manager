import os
from pathlib import Path
from pdfminer.high_level import extract_text
from ebooklib import epub
import weasyprint
import tempfile

# Funkce pro převod PDF → EPUB a naopak, využívající knihovny pdfminer, ebooklib a weasyprint
def pdf_to_epub(pdf_path, output_path, metadata=None):
    """
    Převod PDF → EPUB (text-only verze)
    """
    text = extract_text(pdf_path)

    book = epub.EpubBook()

    if metadata:
        book.set_title(metadata.get("title", "Untitled"))
        book.add_author(metadata.get("author", "Unknown"))
        book.set_language(metadata.get("language", "cs"))

    chapter = epub.EpubHtml(title="Content", file_name="chap_01.xhtml")
    chapter.content = f"<h1>{metadata.get('title','')}</h1><p>{text.replace('\n','<br/>')}</p>"

    book.add_item(chapter)
    book.toc = (chapter,)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.spine = ["nav", chapter]

    epub.write_epub(output_path, book)
    return output_path

# Funkce pro převod EPUB → PDF (render přes HTML)
def epub_to_pdf(epub_path, output_path):
    """
    Převod EPUB → PDF (render přes HTML)
    """
    from ebooklib import epub

    book = epub.read_epub(epub_path)

    html_content = ""

    for item in book.get_items():
        if item.get_type() == epub.ITEM_DOCUMENT:
            html_content += item.get_content().decode("utf-8")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        tmp.write(html_content.encode("utf-8"))
        tmp_path = tmp.name

    weasyprint.HTML(tmp_path).write_pdf(output_path)

    os.remove(tmp_path)
    return output_path