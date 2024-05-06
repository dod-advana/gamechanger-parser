import pandas as pd

from policy_analytics_parser.static_data.data_paths import path_for_Corpus_Meta_csv, path_for_Popular_Documents_csv

try:
    corpus_meta_df = pd.read_csv(path_for_Corpus_Meta_csv)
    corpus_meta_df.orgs.replace({"'": '"'}, regex=True, inplace=True)

    popular_docs_df = pd.read_csv(path_for_Popular_Documents_csv)
except Exception as e:
    print("Error reading static files for corpus meta or popular docs ", e)

""" retrieve pre-generated features from corpus
    - pr: pagerank
    - orgs: organization importance
    - kw_in_doc_score: keyword in doc score historically 
"""

rank_min = 0.00001

def get_pr(docId: str) -> float:
    try:
        if docId in list(corpus_meta_df.id):
            return corpus_meta_df[corpus_meta_df.id == docId].pr.values[0]
        else:
            return rank_min
    except Exception as e:
        print("get pr error", e)
        return rank_min


def get_pop_score(docId: str) -> float:
    try:
        if docId in list(popular_docs_df.doc):
            return float(popular_docs_df[popular_docs_df.doc == docId].pop_score.values[0])
        else:
            return 0.0
    except Exception as e:
        print("get get_pop_score error", e)
        return 0.0

def add_pagerank(doc_dict):
    doc_dict["pagerank_r"] = get_pr(doc_dict["id"])

def add_popscore(doc_dict):
    doc_dict["pop_score"] = get_pop_score(doc_dict["filename"])





