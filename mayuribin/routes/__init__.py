from .get_document import GetDocument
from .index_page import IndexPage
from .raw_document import RawDocument
from .save_document import SaveDocument
from .serve_document import ServeDocument

class Routes(
    GetDocument,
    IndexPage,
    RawDocument,
    SaveDocument,
    ServeDocument
):
    def __init__(self, *args, **kwargs):
        pass
