from collections import Counter
from typing import List

from policy_analytics_parser.keyword_extraction.rake import Rake

kw_alg = Rake(stop_words="smart")


def get_keywords(text: str, amount: int = 2) -> List[str]:
    """
    This function is used to extract keywords.
    """
    try:
        key_w = kw_alg.rank(text, ngram=(1, 2), topn=amount, clean=True)
        return key_w
    except ValueError:
        raise

def extract_keywords(doc_dict: dict) -> None:
    keyword_counts = Counter()

    for page in doc_dict['pages']:
        raw_page_text = page['p_raw_text']
        page_keywords = get_keywords(raw_page_text)
        for keyword in page_keywords:
            keyword_counts[keyword] += 1

    doc_dict["keyw_5"] = [kw for (kw, _) in keyword_counts.most_common(10)]