from pathlib import Path
import json
import traceback

from policy_analytics_parser.reference_extraction.add_reference_list import add_ref_list
from policy_analytics_parser.entity_extraction.entities import extract_entities
from policy_analytics_parser.keyword_extraction.keywords import extract_keywords
from policy_analytics_parser.ranking.rank import add_pagerank, add_popscore
from policy_analytics_parser.topic_extraction.topics import extract_topics
from policy_analytics_parser.post_process import post_process
from policy_analytics_parser.section_parse import add_sections
from policy_analytics_parser.init_doc import (
    assign_other_fields,
    add_metadata_fields,
)

def write(out_dir="./", ex_dict={}):
    outname = Path(ex_dict["filename"]).stem + ".json"

    p = Path(out_dir)
    if not p.exists():
        p.mkdir()
    print('writing to', p.joinpath(outname))
    with open(p.joinpath(outname), "w") as fp:
        json.dump(ex_dict, fp)
    return True

def policy_text_pipeline(
    doc_dict,
    pipeline_args,
) : 
    try:
        ## text already extracted, start extra steps
        out_dir = pipeline_args['destination']

        # assign fields from meta data, already attached to doc
        add_metadata_fields(doc_dict)

        # assign other fields (defaults)
        assign_other_fields(doc_dict)

        add_ref_list(doc_dict)
        # print("ref list", doc_dict[FN.REF_LIST])

        extract_entities(doc_dict)
        # print("entities", doc_dict[FN.TOP_ENTITIES])

        extract_topics(doc_dict)
        # print("topics", doc_dict["topics_s"])

        extract_keywords(doc_dict)
        # print("keywords", doc_dict["keyw_5"])

        doc_dict["abbreviations_n"] = []
        # abbreviations.add_abbreviations_n, just returns empty list currently
        doc_dict["summary_30"] = "" 
            # summary.add_summary, just returns empty string currently

        add_pagerank(doc_dict)
        # print("pagerank", doc_dict["pagerank_r"])

        add_popscore(doc_dict)
        # print("popularity score", doc_dict["pop_score"])

        # word count - should this really be abstracted?
        doc_dict["word_count"] = len(doc_dict["text"].split(" "))
        # print("word count", doc_dict["word_count"])

        add_sections(doc_dict)
        # for title, section in doc_dict["sections"].items():
            # print(title, ':', section)

        post_process(doc_dict)

        # process_ingest_date - connects to database
        # crawler_info - connects to database

        write(out_dir=out_dir, ex_dict=doc_dict)

    except Exception as e:
        traceback.print_exc()

        


