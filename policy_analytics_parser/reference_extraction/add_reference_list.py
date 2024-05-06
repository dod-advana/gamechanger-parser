import re
import typing as t

from policy_analytics_parser.field_names import FieldNames as FN
from policy_analytics_parser.reference_extraction.reference_regexes import get_reference_regex_dict


reference_regex_dict = get_reference_regex_dict()


def add_found_references(
    text: str,
    found_references_accumulator: set,
    pattern: t.Pattern,
    doc_type_prefix: str,
) -> None:

    matches = pattern.findall(text)

    for match in matches:
        if type(match) == tuple:
            values = [x for x in match if x != ""]
            if len(values) != 1:
                print(
                    f"ERR: Patterns in `ref_regex` should only have exactly 1 "
                    f"non-empty capture group each. Check the pattern for {doc_type_prefix}"
                )
                print("text was:", text)
                print("match was:", match)
                continue
            match = values[0]
        elif match == "":
            continue

        if doc_type_prefix == "Title":
            try:
                num = int(match.strip())
            except:
                continue
            else:
                if num > 53 or num == 0:
                    continue
        elif doc_type_prefix == "CFR Title":
            try:
                num = int(match.strip())
            except:
                continue
            else:
                if num > 50 or num == 0:
                    continue

        ref = (doc_type_prefix + " " + match).strip()
        found_references_accumulator.add(ref)


def preprocess_text(text: str) -> str:
    # Interpret the unicode as a -
    text = text.replace("\u2013", "-")
    # Remove parenthesis
    text = re.sub(r"[()]", "", text)
    # Normalize whitespace to make regex simpler
    text = " ".join(text.split())

    return text


def add_ref_list(doc_dict: dict) -> None:

    preprocessed_text = preprocess_text(doc_dict[FN.TEXT])
    found_references_accumulator = set()

    for doc_type_prefix, reference_finding_pattern in reference_regex_dict.items():
        add_found_references(
            preprocessed_text,
            found_references_accumulator,
            reference_finding_pattern,
            doc_type_prefix,
        )

    doc_dict[FN.REF_LIST] = list(found_references_accumulator)
