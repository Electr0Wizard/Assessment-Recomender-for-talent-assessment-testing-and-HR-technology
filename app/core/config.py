import os
from dotenv import load_dotenv

# Load the hidden variables from your .env file
load_dotenv() 

# Grab the key securely
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Using a powerful free model on OpenRouter
LLM_MODEL = "meta-llama/llama-3.3-70b-instruct"
# LLM_MODEL = "meta-llama/llama-3.1-8b-instruct" 
# LLM_MODEL = "google/gemini-2.0-flash-lite-preview-02-05"
# LLM_MODEL = "mistralai/mistral-7b-instruct"
# LLM_MODEL = "huggingfaceh4/zephyr-7b-beta"
VECTORSTORE_PATH = "app/data_pipeline/vectorstore"
CATALOG_PATH = "data/shl_product_catalog.json"