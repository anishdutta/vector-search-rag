from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

engine= 'text-davinci-003'
max_tokens= 150
temperature= 0.7
number_of_completions= 1
api_key= os.getenv("API_KEY")
