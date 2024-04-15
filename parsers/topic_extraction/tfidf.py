from gensim.models.phrases import Phraser
from parsers.topic_extraction.topic_modeling import Topics
import os

base = os.path.dirname(os.path.realpath(__file__))
model_dir = os.path.join(base, 'model')

try:
    tfidf_model = Topics(model_dir, False)
    bigrams_phraser = Phraser.load(os.path.join(model_dir, 'bigrams.phr'))
except Exception as e:
    tfidf_model = None
    bigrams_phraser = None
    print(e)
    print("failed to load tfidf")
