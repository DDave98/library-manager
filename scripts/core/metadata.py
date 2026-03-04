import pikepdf

# Funkce pro čtení a zápis metadat PDF souborů pomocí knihovny pikepdf
def read_pdf_metadata(file_path):
    try:
        with pikepdf.open(file_path) as pdf:
            meta = pdf.docinfo
            return {
                "title": str(meta.get("/Title", "")),
                "author": str(meta.get("/Author", "")),
                "producer": str(meta.get("/Producer", "")),
                "creator": str(meta.get("/Creator", "")),
            }
    except Exception as e:
        return {"error": str(e)}

# Funkce pro zápis metadat do PDF souboru
def write_pdf_metadata(file_path, metadata):
    with pikepdf.open(file_path, allow_overwriting_input=True) as pdf:
        meta = pdf.docinfo

        if "title" in metadata:
            meta["/Title"] = metadata["title"]

        if "author" in metadata:
            meta["/Author"] = metadata["author"]

        pdf.save()