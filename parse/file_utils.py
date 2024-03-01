import typing as t
from pathlib import Path
import fitz
import os
import PyPDF2
from PyPDF2.utils import PdfReadError


def walk_files(src: t.Union[Path, str]) -> t.Iterable[Path]:
    src_path = Path(src)
    if not src_path.is_dir():
        raise ValueError(f"Given src is not a dir {src!s}")
    for p in src_path.rglob("*"):
        if p.is_dir():
            continue
        yield p


def ensure_dir(path: t.Union[Path, str]) -> Path:
    """Ensure given directory path exists"""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def is_pdf(file: t.Union[Path, str]) -> bool:
    """Check if given file is a readable PDF file"""
    file_path = Path(file).resolve()

    try:
        doc = fitz.open(file_path)
        doc.close()
    except RuntimeError as e:
        if "no objects found" in e.args:
            return False
    except:
        return False

    return True


def is_ocr_pdf(file: t.Union[Path, str], error_char_threshold=0.2) -> bool:
    """Check if given pdf file is OCR'ed"""
    file_path = Path(file).resolve()
    try:
        with fitz.open(str(file_path)) as doc:
            for page_num in range(doc.pageCount):
                page_text = doc.getPageText(page_num).strip()
                # if there is ocr'd text present
                if page_text:
                    # check to see if the OCR font (or char encodings) are problematic, and the PDF does need OCR
                    # character 65533 is the 'replace'/'unknown' character. If the percentage of error characters is
                    # greater than the error_char_threshold, the document requires "
                    if [ord(char) for char in page_text].count(65533) / len(
                        page_text
                    ) > error_char_threshold:
                        return False
                    # This document contains well suited OCR already
                    else:
                        return True
            return False
    except Exception as e:
        print(f"Unexpected error while trying to open {file_path}")
        print(e)
        return False


def check_ocr_status_job_type(file: t.Union[Path, str], error_char_threshold=0.2):
    """Check if given pdf file is OCR'ed"""
    file_path = Path(file).resolve()
    bad_page_nums = ""  # the page number (index + 1) of pages that need to be OCRed
    try:
        with fitz.open(str(file_path)) as doc:
            total_pages = doc.pageCount
            missing_text_page_count = 0
            for page_num in range(total_pages):
                page_text = doc.getPageText(page_num).strip()
                # if there is ocr'd text present
                if page_text:
                    pass
                    # check to see if the OCR font (or char encodings) are problematic, and the PDF does need OCR
                    # character 65533 is the 'replace'/'unknown' character. If the percentage of error characters is
                    # greater than the error_char_threshold, the document requires "
                    # if [ord(char) for char in page_text].count(65533) / len(page_text) > error_char_threshold:
                    #    return False, 'force-ocr'#OCRJobType.FORCE_OCR
                else:
                    bad_page_nums = bad_page_nums + str(page_num + 1) + " "
                    missing_text_page_count += 1
            # if there are missing text pages, and none of the pages contain erroneous glyph/text, then redo OCR - else
            # skip OCRing all together
            if missing_text_page_count > 0:
                return {
                    "successful_ocr": False,
                    "ocr_job_type": "redo-ocr",
                    "bad_page_nums": bad_page_nums,
                }  # OCRJobType.REDO_OCR
            else:
                return {
                    "successful_ocr": True,
                    "ocr_job_type": "skip-text",
                    "bad_page_nums": None,
                }  # OCRJobType.SKIP_TEXT
    except Exception as e:
        print(f"Unexpected error while trying to open {file_path}")
        print(e)
        return {"successful_ocr": False, "ocr_job_type": None, "bad_page_nums": None}


def is_encrypted_pdf(file: t.Union[Path, str]) -> bool:
    """Check if pdf file is encrypted"""
    file_path = Path(file).resolve()

    try:
        pdf_reader = PyPDF2.PdfFileReader(str(file_path))
        return pdf_reader.isEncrypted
    except PdfReadError as e:
        print(f"PdfReadError error while trying to open {file_path.name}")
        print(e)
        return True  # err on a side of caution
    except Exception as e:
        print(f"Unexpected error while trying to open {file_path.name}")
        print(e)
        return True  # err on a side of caution


from parse.html_utils import (
    convert_html_file_to_pdf,
    convert_html_to_pdf,
    convert_text_to_html,
)
from parse.reading_in import read_plain_text


def coerce_file_to_pdf(filepath: t.Union[Path, str]) -> str:
    """Attempts to convert the given file to a pdf and returns the pdf filepath."""
    filepath = Path(filepath)
    filetype = filepath.suffix
    if filetype == ".pdf" or filetype == ".PDF":
        return str(filepath)
    elif filetype == ".html":
        return convert_html_file_to_pdf(filepath)
    elif filetype == ".txt":
        text = read_plain_text(filepath)
        html = convert_text_to_html(text)
        return convert_html_to_pdf(filepath, html)
    else:
        raise ValueError(f"unsupported filetype {filetype}")
