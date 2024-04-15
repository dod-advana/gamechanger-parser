import sys
import os
import re
from pathlib import Path
import json
import typing
from datetime import datetime
import traceback

from parsers import paragraphs, pages, pdf_reader

from parsers.field_names import FieldNames as FN
from parsers.ocr_utils import OCRError, UnparseableDocument, PageCountParse
from parsers.file_utils import coerce_file_to_pdf
from parsers.ocr import get_ocr_filename
from parsers.reference_extraction.add_reference_list import add_ref_list
from parsers.entity_extraction.entities import extract_entities
from parsers.keyword_extraction.keywords import extract_keywords
from parsers.ranking.rank import add_pagerank, add_popscore
from parsers.topic_extraction.topics import extract_topics
from parsers.post_process import post_process
from parsers.init_doc import (
    assign_f_name_fields,
    assign_other_fields,
    add_metadata_fields,
)
from parsers.section_parse import add_sections


def write(out_dir="./", ex_dict={}):
    outname = Path(ex_dict["filename"]).stem + ".json"

    p = Path(out_dir)
    if not p.exists():
        p.mkdir()

    with open(p.joinpath(outname), "w") as fp:
        json.dump(ex_dict, fp)
    return True


def parse(
    f_name,
    out_dir,
):
    print("running policy_analyics.parse on", f_name)
    try:
        meta_dict = {}
        doc_dict = {}

        add_metadata_fields(doc_dict, meta_dict)
        assign_f_name_fields(f_name, doc_dict)
        assign_other_fields(doc_dict)

        if not str(f_name).endswith(".pdf"):
            f_name = coerce_file_to_pdf(f_name)
            doc_dict[FN.FILENAME] = re.sub(r"\.[^.]+$", ".pdf", doc_dict[FN.FILENAME])

        doc_obj = pdf_reader.get_fitz_doc_obj(f_name)
        pages.handle_pages(doc_obj, doc_dict)
        doc_obj.close()

        paragraphs.add_paragraphs(doc_dict)

        ## text extracted, start extra steps

        add_ref_list(doc_dict)
        print("ref list", doc_dict[FN.REF_LIST])

        extract_entities(doc_dict)
        print("entities", doc_dict[FN.TOP_ENTITIES])

        extract_topics(doc_dict)
        print("topics", doc_dict["topics_s"])

        extract_keywords(doc_dict)
        print("keywords", doc_dict["keyw_5"])

        doc_dict["abbreviations_n"] = []
        # abbreviations.add_abbreviations_n, just returns empty list currently
        doc_dict["summary_30"] = "" 
         # summary.add_summary, just returns empty string currently
        

        add_pagerank(doc_dict)
        print("pagerank", doc_dict["pagerank_r"])

        add_popscore(doc_dict)
        print("popularity score", doc_dict["pop_score"])

        # word count - should this really be abstracted?
        doc_dict["word_count"] = len(doc_dict["text"].split(" "))
        print("word count", doc_dict["word_count"])

        # # TODO: add sections
        add_sections(doc_dict)
        for title, section in doc_dict["sections"].items():
            print(title, ':', section)

        post_process(doc_dict)

        # process_ingest_date - connects to database
        # crawler_info - connects to database

        write(out_dir=out_dir, ex_dict=doc_dict)
    except Exception as e:
        print("ERROR in policy_analytics.parse:", repr(e))
        traceback.print_exc()


def process_directory(
    source: str,
    destination: str,
) -> None:
    """
    Converts input pdf file to json
    Args:
        source: A source directory to be processed.
        destination: A destination directory to be processed
    """
    if not Path(source).is_dir:
        print("A directory of files to parse is required")
        exit(1)

    print("processing files in", source)

    filepath = Path(source).glob("**/*")
    to_process = []
    excluded = []

    for path_item in filepath:
        if not path_item.is_file():
            excluded.append(path_item)
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

    print(f"{len(to_process)} items to process")
    print(f"{len(excluded)} items were excluded")

    for f_name in to_process:
        parse(f_name=f_name, out_dir=destination)
