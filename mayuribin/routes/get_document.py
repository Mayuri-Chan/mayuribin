from fastapi import Request, HTTPException, Query
from pydantic import BaseModel
from mayuribin.route import Route

class GetDocumentResult(BaseModel):
    key: str
    content: str

class GetDocumentResponse(BaseModel):
    ok: bool
    result: GetDocumentResult

class GetDocument:
    @Route.get('/api/v1/documents', response_model=GetDocumentResponse, summary="Get a document from the bin")
    async def get_document(self, key: str = Query(..., description="The key of the document")):
        if not key:
            raise HTTPException(status_code=400, detail="Document Key is required")
            
        document = await self.db.fetchrow("SELECT content FROM documents WHERE key = $1", key)
        if not document and key != "about.md":
            raise HTTPException(status_code=404, detail="Document not found")
            
        if key == "about.md":
            content = open("mayuribin/assets/about.md", "r").read()
        else:
            content = document['content']
            
        return {'ok': True, 'result': {'key': key, 'content': content}}
