from syntok import segmenter

from parsers.field_names import FieldNames as FN
from parsers.text_utils import utf8_pass
from parsers.utils.dod_text import normalize_dod


def tokens_to_str(tokens):
    """Convert tokens to strings.

    Also removes whitespace formatting (e.g., newlines).

    Args:
        tokens (output of syntok.segmenter.process())

    Returns:
        str
    """
    return " ".join(
        [
            " ".join([token.spacing + token.value for token in sentence])
            for sentence in tokens
        ]
    )


def make_paragraph_id(filename, par_count_i):
    """Make the "id" field for a paragraph.

    Args:
        filename (str): File name of the document that the paragraph is from.
        par_count_i (int): Paragraph index within the given page

    Returns:
        str
    """
    if filename is None:
        filename = ""
    if par_count_i is None:
        par_count_i = ""

    return f"{filename}_{str(par_count_i)}"


def add_paragraphs(doc_dict):
    """Split the document into dictionary representations of its paragraphs.

    Each dict will have the following keys and values:
        FieldNames.TYPE: str
        FieldNames.FILENAME: str (File name of the document that the paragraph is from)
        FieldNames.PAR_INC_COUNT: int (paragraph index within the entire document)
        FieldNames.ID: str (paragraph ID)
        FieldNames.PAR_COUNT: int (paragraph index within the given page)
        FieldNames.PAGE_NUM: int (page number of the paragraph)
        FieldNames.PAR_RAW_TEXT: str (paragraph raw text)
        FieldNames.ENTITIES: empty list (see entities.py for entity extraction)

    Returns:
        None - modifies input dict to add paragraphs: List[dict]
    """

    pages = doc_dict.get(FN.PAGES)
    if pages is None:
        return []

    filename = doc_dict.get(FN.FILENAME, "")

    total_paragraph_count = 0
    paragraph_dicts = []

    for page in pages:
        raw_text = page[FN.PAGE_RAW_TEXT]
        page_num = page['p_page']

        segmented_text = segmenter.process(raw_text)

        for page_paragraph_num, tokens in enumerate(segmented_text):
            token_string = tokens_to_str(tokens)
            dod_normalized_text = normalize_dod(token_string)
            paragraph_text = utf8_pass(dod_normalized_text)

            paragraph_dict = {
                FN.TYPE: FN.PARAGRAPH_TYPE,
                FN.FILENAME: filename,
                FN.PAR_INC_COUNT: total_paragraph_count,
                FN.ID: make_paragraph_id(filename, total_paragraph_count),
                FN.PAR_COUNT: page_paragraph_num,
                FN.PAGE_NUM: page_num,
                FN.PAR_RAW_TEXT: paragraph_text,  # not in fact the raw text, very cleaned
                FN.ENTITIES: []

            }
            paragraph_dicts.append(paragraph_dict)
            total_paragraph_count += 1

    doc_dict[FN.PAR_COUNT] = total_paragraph_count
    doc_dict[FN.PARAGRAPHS] = paragraph_dicts
