from parsers.topic_extraction.custom_stopwords import custom_stopwords

import gensim
from gensim.models.tfidfmodel import TfidfModel
from gensim import corpora
from gensim.models.phrases import Phraser


import os
import logging

logger = logging.getLogger("gamechanger")

# turn off gensim logging for lifecycle events like loading etc
logging.getLogger(gensim.__name__).setLevel(logging.ERROR)


class Topics(object):
    """
    TF-iDF topic model wrapper class.

    This class is written to be processing pipeline agnostic, but
    because of that be sure that you track your own pipeline for
    training and inference otherwise results may vary.

    Also note that this class will allow you to perform topic modeling
    on out of corpus documents.  Be sure to monitor the number of
    documents being processed out of corpus to ensure that the model
    still reflects the statistics of the corpus.  When this is no longer
    the case you can either retrain from scatch. TODO: Implement an
    update function to update the model on only the new documents.

    Class requirements:
        from gensim.models.tfidfmodel import TfidfModel
        from gensim import corpora
    """

    def __init__(self, directory=None, verbose=False, status=None):

        self.status = status

        try:
            if directory is not None:
                self.load(directory)
        except Exception as e:
            logger.warning("Could not load topics model")
            logger.warning(e)

    def load(self, directory):
        """
        load - class function to load the required files from a
            directory.
        Args:
            directory (str): Path to where `tfidf_dictionary.dic`
                and `tfidf.model` are located.
        Returns:
            None
        """
        logger.info(f"Topics loading from {directory}")

        dictionary_path = os.path.join(directory, "tfidf_dictionary.dic")
        tfidf_path = os.path.join(directory, "tfidf.model")
        bigrams_path = os.path.join(directory, "bigrams.phr")
        self.dictionary = corpora.Dictionary.load(dictionary_path)
        self.tfidf = TfidfModel.load(tfidf_path)
        self.bigrams = Phraser.load(bigrams_path)


    def get_topics(self, tokens, topn=5):
        """
        get_topics - given a tokenized text, get a list of the topn topics
            with their scores
        Args:
            tokens (list): A tokenized text list.
            topn (int): the number of topic to be returned
        Returns:
            topics (list|tuple): a list of (score, topic) pairs
        """
        doc_term_matrix = [self.dictionary.doc2bow(tokens)]
        doc_tfidf = self.tfidf[doc_term_matrix]

        word = []
        doc = doc_tfidf[0]
        for id, value in doc:
            if self.dictionary.get(id) not in custom_stopwords:
                word.append((value, self.dictionary.get(id)))
        word.sort(reverse=True)
        return word[:topn]
