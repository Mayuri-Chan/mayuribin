import uuid
from time import time
from typing import Optional
from fastapi import Request
from pydantic import BaseModel, Field
from mayuribin.route import Route

class SaveDocumentRequest(BaseModel):
    content: str = Field(..., description="The content of the document")

class SaveDocumentResult(BaseModel):
    key: str
    title: Optional[str] = None
    author: Optional[str] = None
    date: float
    views: int
    length: int
    content: str

class SaveDocumentResponse(BaseModel):
    ok: bool
    result: SaveDocumentResult

class SaveDocument:
    @Route.post('/api/v1/documents', response_model=SaveDocumentResponse, summary="Save a document to the bin")
    async def save_document(self, body: SaveDocumentRequest):
        key = ''.join(str(uuid.uuid4()).split("-"))[:10]
        content = body.content
        now = time()
        _ = await self.db.execute(
            "INSERT INTO documents (key, content, date) VALUES ($1, $2, $3) ON CONFLICT (key) DO UPDATE SET content = EXCLUDED.content, date = EXCLUDED.date",
            key, content, now
        )
        return {
            'ok': True,
            'result': {
                'key': key,
                'title': None,
                'author': None,
                'date': now,
                'views': 0,
                'length': len(content),
                'content': content
            }
        }
