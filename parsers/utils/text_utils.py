import re
import typing as t

def translate_to_ascii_string(_s: t.Union[str, bytes]) -> str:
    """
    Translates utf-8 byte sequence to ASCII string
    The point is to approximately translate foreign characters rather than
    deleting them
    Args:
        _s (str|bytes: string to translate

    Returns:
        str

    Raises:
        UnicodeDecodeError if decoding fails

    """
    _str_bytes = _s if isinstance(_s, bytes) else _s.encode("utf-8", "ignore")
    return _str_bytes.decode("ascii", errors="ignore")

def simple_clean(text: str) -> str:
    """
    Performs a simple text cleaning: removes newline characters, square and
    curly braces, insures `utf-8` encoding, and reduces inter-word spacing to
    a single space.

    Args:
        text (str): text to be cleaned

    Returns:
        str

    Raises:
        UnicodeDecodeError if an illegal Unicode code-point is encountered

    """
    try:
        text = re.sub("[\\n\\t\\r]+", " ", text)
        text = re.sub("[" + re.escape("][}{)\\/") + "]+", " ", text)
        text = re.sub("\\s{2,}", " ", text)
        text = translate_to_ascii_string(text)
        return text.strip()
    except UnicodeDecodeError as e:
        print("{}: {}".format(type(e), str(e)), exc_info=True)
        raise

def replace_nonalpha_chars(text, replace_char=""):
    """Replace non-alphanumeric characters in the text.

    Args:
        text (str)
        replace_char (str, optional): The character(s) to replace 
            non-alphanumeric characters with. Defaults to "".

    Returns:
        str: The text with non-alphanumeric characters replaced.
    """
    text = re.sub("[^a-zA-Z0-9\s]+", replace_char, text)
    
    return re.sub("\\s{2,}", " ", text)