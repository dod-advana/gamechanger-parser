from os.path import split
from parsers.field_names import FieldNames
from .parser_definition import ParserDefinition
from .dod_parser import DoDParser
from .navy_parser import NavyParser
from .cjcs_parser import CJCSParser
from .eo_parser import EOParser
from .uscode_parser import USCodeParser

class ParserFactory:
    """Create a parser for a specific document type."""

    @staticmethod
    def create(doc_dict: dict) -> ParserDefinition:
        """Create a parser for the document type defined in the document
        dictionary.

        Args:
            doc_dict (dict): JSON representation of the document.

        Returns:
            ParserDefinition
        """
        doc_type = split(doc_dict[FieldNames.DOC_TYPE])[1].lower()
        if doc_type in DoDParser.SUPPORTED_DOC_TYPES:
            return DoDParser(doc_dict)
        elif doc_type in NavyParser.SUPPORTED_DOC_TYPES:
            return NavyParser(doc_dict)
        elif doc_type in CJCSParser.SUPPORTED_DOC_TYPES:
            return CJCSParser(doc_dict)
        elif doc_type in EOParser.SUPPORTED_DOC_TYPES:
            return EOParser(doc_dict)
        elif doc_type in USCodeParser.SUPPORTED_DOC_TYPES:
            return USCodeParser(doc_dict)
        else:
            return ParserDefinition(doc_dict)
