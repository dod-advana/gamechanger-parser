from collections import Counter

from flashtext import KeywordProcessor

from parsers.field_names import FieldNames
from parsers.utils import text_utils
from parsers.entity_extraction import entities_utils
from parsers.static_data.data_paths import path_for_GraphRelations_xls


# The graph relations file from gamechangerml is used as gold standard entities.
graph_relations_entities_dict = entities_utils.make_entities_lookup_dict(
    path_for_GraphRelations_xls
)

# # Used to find entities in text.
flashtext_processor = KeywordProcessor(case_sensitive=True)
for entity in graph_relations_entities_dict.keys():
    flashtext_processor.add_keyword(entity)

# # Used to rename entity types from how they exist in the graph relations file
# # to how they will exist in document dictionaries.
ENTITY_RENAME_DICT = {
    "ORG": "ORG_s",
    "GPE": "GPE_s",
    "NORP": "NORP_s",
    "LAW": "LAW_s",
    "LOC": "LOC_s",
    "PERSON": "PERSON_s",
}


def extract_entities(doc_dict: dict) -> None:
    """Extract entities from a document's text.

    Utilizes GraphRelations.xls from gamechangerml as gold standard entities.


    Adds the following new keys/ values to doc_dict:
        "entities" (list of str): Entities extracted from the document.
        "top_entities_t" (list of str): Most common entities in the document

    Also adds the following to each item of doc_dict["paragraphs"]:
        "entities" (dict): Keys (str) are entity types and values (list of str)
            are the entities extracted from the paragraph.
    Args:
        doc_dict (dict): Dictionary representation of a document. Must have
            the following keys/ values:
                "paragraphs" (list of dict): Dictionary representations of the
                    document's paragraphs. Each dict must have the key
                    "par_raw_text_t" with the corresponding value (str) being
                    the paragraph's text.
            Example:
            {
                "paragraphs": [
                    {
                        "par_raw_text_t": "hello"
                    }
                ]
            }

    Returns:
        dict: The updated document dictionary
    """
    paragraphs = doc_dict[FieldNames.PARAGRAPHS]

    all_document_entities = []

    for paragraph_dict in paragraphs:

        # use set to avoid adding duplicates
        entities_by_type = {new_name: set() for new_name in ENTITY_RENAME_DICT.values()}

        text = paragraph_dict[FieldNames.PAR_RAW_TEXT]
        if text is None:
            paragraph_dict[FieldNames.ENTITIES] = entities_by_type
            continue

        text = text_utils.simple_clean(text)
        # Remove non-alphanumeric characters in the paragraph's text since we
        # search for entities using the keys of ENTITIES_LOOKUP_DICT which also
        # have non-alphanumeric characters removed.
        text = entities_utils.replace_nonalpha_chars(text, "")

        # The flashtext KeywordProcessor (inspired by the Aho-Corasick
        # algorithm and Trie data structure) is MUCH faster than re.finditer()
        # in this case.
        extracted_keywords = flashtext_processor.extract_keywords(text, span_info=True)

        entities = []
        for keyword, span_start, span_stop in extracted_keywords:
            raw_entity_for_keyword = graph_relations_entities_dict[keyword]["raw_ent"]
            entity_type = graph_relations_entities_dict[keyword]["ent_type"]
            entities.append(
                (span_start, span_stop, raw_entity_for_keyword, entity_type)
            )

        entities = entities_utils.remove_overlapping(entities)
        for span_start, span_stop, raw_entity, entity_type in entities:
            entity_type_renamed = ENTITY_RENAME_DICT[entity_type]
            entities_by_type[entity_type_renamed].add(raw_entity)

        # convert sets of entities into a list
        entities_by_type = {k: list(v) for k, v in entities_by_type.items()}

        paragraph_dict[FieldNames.ENTITIES] = entities_by_type

        # add all entities found for each type to all document entities
        for entity_list in entities_by_type.values():
            all_document_entities += entity_list

    all_unique_entities = list(set(all_document_entities))
    doc_dict[FieldNames.ENTITIES] = all_unique_entities

    # list of tuple of (key, count) for 5 most common found
    top_counts = Counter(all_document_entities).most_common(5)
    most_common_entities = [entity for (entity, _) in top_counts]

    doc_dict[FieldNames.TOP_ENTITIES] = most_common_entities
