import ssl
from fastapi import FastAPI
from src.search import search_service
from dotenv import load_dotenv
from src.search.model import Search

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
async def search(request:Search):
    # Assuming you have a function named `extract` within `extractor_service`
    extracted_text = search_service.Search_Service().search(company=request.company, topic=request.topic)
    return extracted_text
