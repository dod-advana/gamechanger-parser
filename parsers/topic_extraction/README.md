# Topic Model
This topic model setup expects the folder `model/` to have these files:
- bigrams.phr
- tfidf.model
- tfidf_dictionary.dic

See gamechanger-ml for information about training a topic model

# Retreiving model
- Activate BIG-IP VPN
- Activate AWS SAML app and set token
- `python config/get_topic_model.py`
- verify topic_extraction/model has bigrams, model, and dictionary files