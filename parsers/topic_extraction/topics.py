
from gensim.utils import simple_preprocess

try:
    from parsers.topic_extraction.tfidf import bigrams_phraser, tfidf_model
except ImportError:
    print("[IMPORT ERROR]: No Topic Models, skipping extract_topics")
    tfidf_model = bigrams_phraser = None

def extract_topics(doc_dict):
    """
    This function takes in a document dictionary, checks if it is
    longer than 1 page, and if it is extracts up to 5 topics from
    the text of the document.
    Args:
        doc_dict (dict): A dictionary containing document data.
            Note that `page_count` and `text` must be present in
            the dictionary.
    Returns:
        doc_dict (dict): The output dict differs from the input
            only in that it now includes `topics_rs` as a key.
    """

    doc_dict["topics_s"] = []

    # the topic model may be missing, returns empty topics_rs
    if tfidf_model is None:
        return

    MIN_TOKEN_LEN = 300  # tokens, this turns out to be roughly a half page

    tokens = doc_dict["text"].split()

    if len(tokens) > MIN_TOKEN_LEN:
        preprocessed_text = simple_preprocess(doc_dict["text"], min_len=4, max_len=15)
        phrases = bigrams_phraser[preprocessed_text]
        topics = tfidf_model.get_topics(phrases, topn=5)

        doc_dict['topics_s'] = [topic[1].replace("_", " ") for topic in topics]

