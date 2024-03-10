# Vector Search RAG

This is a simple Python project that demonstrates how to create a RESTful API using FastAPI.

## Requirements

- Python 3.7+
- Pip (Python Package Installer)

## Installation

1. Clone the repository:
3. Install the required dependencies: pip install -r requirements.txt


## Running the Server

To start the server, run the following command:
`uvicorn main:app --reload`

The server will start and listen on `http://localhost:8000` by default.


## Endpoints

### Search Endpoint

This endpoint allows users to search for information based on company and topic.

#### Request Body

- `company` (text): The name of the company to search for.
- `topic` (text): The topic related to the search.

#### Response

- Status: 200
- Content-Type: application/json

##### Example Response:

```json
{
    "keywords": {
        "1": [""],
        "2": [""],
        "3": [""],
        "4": [""],
        "5": [""]
    },
    "summary": ""
}

