from pydantic import BaseModel

class Search(BaseModel):
    company: str
    topic: str

class SearchResult(BaseModel):
    keywords: object
    summary: str