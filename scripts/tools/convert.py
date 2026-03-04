import sys
from core.converter import pdf_to_epub, epub_to_pdf

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Použití:")
        print("pdf2epub input.pdf output.epub")
        print("epub2pdf input.epub output.pdf")
        sys.exit(1)

    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if mode == "pdf2epub":
        pdf_to_epub(input_file, output_file, metadata={"title": "Converted"})
    elif mode == "epub2pdf":
        epub_to_pdf(input_file, output_file)