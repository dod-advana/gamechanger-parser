import filetype
from pathlib import Path
import re
import traceback
import typing
import json

from text_extraction import pdf_reader
from text_extraction.file_utils import coerce_file_to_pdf
from text_extraction import pages, paragraphs

def read_metadata(meta_data_path) -> dict:
    try:
        with open(Path(meta_data_path)) as f_in:
            data = json.load(f_in)
    except:
        print("Failed to load metadata, attempted at path:", meta_data_path)
        return {}

    return data

def assign_f_name_fields(f_name, doc_dict):
    filename = (
        f_name.absolute().name
        if isinstance(f_name, Path)
        else Path(str(f_name)).name
    )
    doc_dict['filename'] = filename
    doc_dict['f_name'] = filename
    doc_dict["id"] = filename + "_0"
    doc_dict["group_s"] = filename + "_0"

    meta_data = doc_dict.get("meta_data", {})

    doc_dict["doc_type"] = meta_data.get("doc_type", str(f_name).split(" ")[0])
    doc_dict["doc_num"] = meta_data.get(
        "doc_num", str(f_name).split(",")[0].split(" ")[-1])

def extract_text(
    filepath: Path
):
    print("running extract_text on", filepath)
    try:
        metadata_path = Path(str(filepath) + '.metadata')

        meta_dict = read_metadata(metadata_path)
        doc_dict = {}
        doc_dict['meta_data'] = meta_dict 

        assign_f_name_fields(filepath, doc_dict)

        if not str(filepath).endswith(".pdf"):
            filepath = coerce_file_to_pdf(filepath)
            doc_dict["filename"] = re.sub(r"\.[^.]+$", ".pdf", doc_dict["filename"])

        doc_obj = pdf_reader.get_fitz_doc_obj(filepath)
        pages.handle_pages(doc_obj, doc_dict)
        doc_obj.close()

        paragraphs.add_paragraphs(doc_dict)

        return doc_dict

    except Exception as e:
        print("ERROR in policy_analytics.parse:", repr(e))
        traceback.print_exc()



def generate_extracted_text_from_directory(
    source: str,
) -> typing.Iterator[dict] :

    if not Path(source).is_dir() or not Path(source).exists():
        raise Exception("A directory of files to parse is required")

    print("Extracting text from the files in", source)

    filepaths = Path(source).glob("**/*")
    to_process = []
    metadata_files = []
    excluded = []


    for path_item in filepaths:
        if not path_item.is_file():
            excluded.append(path_item)
            continue

        if path_item.suffix == ".metadata":
            metadata_files.append(path_item)
            continue

        if path_item.suffix.lower() in (".pdf", ".html", ".txt"):
            to_process.append(path_item)
            continue

        filetype_guess = filetype.guess(str(path_item))
        if filetype_guess is not None and filetype_guess.mime in [
            "pdf",
            "application/pdf",
        ]:
            to_process.append(path_item)
            continue

        excluded.append(path_item)

    print(f"{len(to_process)} items to extract text from")
    print(f"{len(metadata_files)} metadata files identified")
    print(f"{len(excluded)} items were excluded, probably not of filetypes: .pdf, .html, .txt")
    if excluded:
        print([f.stem+f.suffix for f in excluded])

    for filepath in to_process:
        extracted_text_dict = extract_text(filepath=filepath)
        yield extracted_text_dict

            
