import fitz
from parse.ocr_utils import PageCountParse

def get_fitz_doc_obj(f_name):
    doc = fitz.open(f_name)
    if doc.page_count < 1:
        doc.close()
        raise PageCountParse(
            f"Could not parse the doc, failed page count check: {f_name}")
    else:
        return doc
