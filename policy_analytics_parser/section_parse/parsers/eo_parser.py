from policy_analytics_parser.field_names import FieldNames
from .parser_definition import ParserDefinition

class EOParser(ParserDefinition):
    """Section parser for Executive Order (EO) documents.
    
    Child of ParserDefinition.
    """

    SUPPORTED_DOC_TYPES = ["eo"]

    def __init__(self, doc_dict: dict, test_mode: bool = False):
        super().__init__(doc_dict, test_mode)
        self._title = self.doc_dict[FieldNames.TITLE]

    @property
    def purpose(self):
        return [self._title]

