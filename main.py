import ssl
from fastapi import FastAPI
from src.search import search_service
from dotenv import load_dotenv
from src.search.model import Search
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

# Load environment variables from .env file
load_dotenv()

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

app = FastAPI()

@app.get("/")
async def root():
    return {
        "success": True
    }


@app.post("/search")
async def search(request: Search):
    print("here",request)
    extracted_text = await search_service.Search_Service().search(company=request.company, topic=request.topic, question=request.question)
    return extracted_text

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

