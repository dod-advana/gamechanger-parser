import typing as t
import datetime
import pandas

from parsers.text_utils import utf8_pass, clean_text

def parse_timestamp(ts: t.Union[str, datetime.datetime], raise_parse_error: bool = False) -> t.Optional[datetime.datetime]:
    """Parse date/timestamp with no particular format
    :param ts: date/timestamp string
    :return: datetime.datetime if parsing was successful, else None
    """
    def _parse(ts):
        if isinstance(ts, datetime.datetime):
            return ts

        try:
            ts = pandas.to_datetime(ts).to_pydatetime()
            if str(ts) == 'NaT':
                return None
            else:
                return ts
        except:
            return None

    parsed_ts = _parse(ts)
    if parsed_ts is None and raise_parse_error:
        raise ValueError(f"Invalid timestamp: '{ts!r}'")
    else:
        return parsed_ts

def get_publication_date(doc_dict):
    try:
        parsed_date = parse_timestamp(doc_dict.get("publication_date", None))
        if parsed_date:
            return datetime.datetime.strftime(parsed_date, '%Y-%m-%dT%H:%M:%S')
    except:
        return ""

def get_access_timestamp(doc_dict):
    try:
        parsed_date = parse_timestamp(doc_dict.get("access_timestamp", None))
        if parsed_date:
            return datetime.datetime.strftime(parsed_date, '%Y-%m-%dT%H:%M:%S')
    except:
        return ""

def post_process(doc_dict):
    doc_dict["raw_text"] = utf8_pass(doc_dict["text"])
    doc_dict["text"] = clean_text(doc_dict["text"])

    # because an old format of the metadata could exist, we need to check if the entry exists in each assignment
    if doc_dict["meta_data"]:
        doc_dict["file_ext_s"] = doc_dict["meta_data"]["file_ext"] if "file_ext" in doc_dict["meta_data"] \
            else doc_dict["meta_data"]["downloadable_items"][0]["doc_type"]
        doc_dict["display_doc_type_s"] = doc_dict["meta_data"]["display_doc_type"] if "display_doc_type" in doc_dict["meta_data"] \
            else "Uncategorized"
        doc_dict["display_title"] = doc_dict["meta_data"]["display_title"] if "display_title" in doc_dict["meta_data"] \
            else doc_dict["meta_data"]["doc_type"] + " " + doc_dict["meta_data"]["doc_num"] + ": " + doc_dict["meta_data"]["doc_title"]
        doc_dict["display_title_s"] = doc_dict["display_title"]
        doc_dict["display_org_s"] = doc_dict["meta_data"]["display_org"] if "display_org" in doc_dict["meta_data"] \
            else "Uncategorized"
        doc_dict["source_title_s"] = doc_dict["meta_data"]["source_title"] if "source_title" in doc_dict["meta_data"] \
            else "Uncategorized"
        doc_dict["display_source_s"] = doc_dict["meta_data"]["display_source"] if "display_source" in doc_dict["meta_data"] \
            else "Uncategorized"
        doc_dict["access_timestamp_dt"] = datetime_utils.get_access_timestamp(doc_dict["meta_data"])
        doc_dict["publication_date_dt"] = datetime_utils.get_publication_date(doc_dict["meta_data"])
        doc_dict["is_revoked_b"] = False
        doc_dict["doc_name"] = doc_dict["meta_data"]["doc_name"]
    else:
        doc_dict["is_revoked_b"] = False

    to_rename = [
        ("txt_length", "text_length_r"),
        ("crawler_used", "crawler_used_s"),
        ("source_fqdn", "source_fqdn_s"),
        ("source_page_url", "source_page_url_s"),
        ("cac_login_required", "cac_login_required_b"),
        ("download_url", "download_url_s"),
        ("version_hash", "version_hash_s"),
    ]

    for current, needed in to_rename:
        try:
            doc_dict[needed] = doc_dict[current]
            del doc_dict[current]
        except KeyError:
            pass

    if doc_dict["meta_data"]:
        if "extensions" in doc_dict["meta_data"]:
            extensions = doc_dict["meta_data"]["extensions"]
            for key in extensions:
                doc_dict[key] = extensions[key]

    to_delete = [
        "meta_data",
        "access_timestamp",
        "publication_date",
        "crawler_used",
        "source_fqdn",
        "source_page_url",
        "source_title",
        "cac_login_required",
        "download_url",
        "version_hash",
        "ingest_date",
        "orgs",
        "f_name",
        "file_ext",
        "display_org",
        "display_source",
        "data_source",
        "source_title",
        "is_revoked"
    ]

    for key in to_delete:
        try:
            del doc_dict[key]
        except KeyError:
            pass

    return doc_dict