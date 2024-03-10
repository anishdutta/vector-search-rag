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

##### cURL:
```
curl --location 'http://localhost:8000/search' \
--header 'Content-Type: application/json' \
--data '{
    "company":"TTKPRESTIG",
    "topic":"RISK MANAGEMENT"
}'
```

##### Example Response:

```json
{
    "keywords": {
        "1": [
            "Risk identification",
            "risk management framework",
            "external risks",
            "internal risks",
            "extreme risks",
            "calamities",
            "disasters",
            "business strategy",
            "business continuity",
            "contingency plans"
        ],
        "2": [
            "operations",
            "transactions",
            "statutory compliance",
            "legal compliance",
            "financial reporting",
            "information technology system",
            "cyber security",
            "internal control framework",
            "SEBI (LODR) Regulations",
            "sustainability factors"
        ],
        "3": [
            "environment",
            "social",
            "governance",
            "independent professional management auditors",
            "risk assessment",
            "risk status",
            "risk management committee",
            "risk policy",
            "board report",
            "composition"
        ],
        "4": [
            "members",
            "chairperson",
            "attendance",
            "EBITDA levels",
            "general economic risks",
            "risk management policy",
            "risk identification",
            "risk management framework",
            "market risk",
            "fair value"
        ],
        "5": [
            "cash flows",
            "financial instruments",
            "market prices",
            "foreign currency exchange rates",
            "interest rates",
            "credit",
            "liquidity",
            "market changes",
            "price risk."
        ]
    },
    "summary": "\nTitle: Risk Management in TTK Prestige Limited\n\nIntroduction:\nThe document provides information on the risk management practices of TTK Prestige Limited, a company listed on the stock exchange. It includes details on the Risk Management Committee, its composition and responsibilities, as well as the company's risk management policy and framework.\n\nSummary:\n1. The Risk Management Committee of TTK Prestige Limited is responsible for identifying and assessing risks related to various aspects of the company's operations, including strategy, operations, compliance, financials, sustainability, and cyber security.\n2. The committee met thrice and all members attended the meetings.\n3. The committee's details are provided in the Board's Report.\n4. The company has a Risk Management Policy in place, which includes identifying potential risks that may threaten the company's existence.\n5. The policy is available on the company's website.\n6. The company has a risk identification and management framework appropriate to its size and operating environment.\n7. Risks are continuously identified in relation to business strategy, operations, compliance, financial reporting, and IT systems.\n8. The company utilizes the services of independent professional management auditors for risk management.\n9. The scope of risk management also includes sustainability factors.\n10. The company is exposed to market"
}

