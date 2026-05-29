from .get_document import GetDocument
from .index_page import IndexPage
from .raw_document import RawDocument
from .save_document import SaveDocument
from .serve_document import ServeDocument
from .static import Static

class Routes(
    GetDocument,
    IndexPage,
    RawDocument,
    SaveDocument,
    ServeDocument,
    Static
):
    def __init__(self, *args, **kwargs):
        pass
