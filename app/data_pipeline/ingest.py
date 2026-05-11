import json
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain.docstore.document import Document
from langchain_core.documents import Document
from app.core.config import CATALOG_PATH, VECTORSTORE_PATH

def get_test_types(keys):
    mapping = {
        "Knowledge & Skills": "K",
        "Personality & Behavior": "P",
        "Ability & Aptitude": "A",
        "Simulations": "S",
        "Competencies": "C",
        "Biodata & Situational Judgment": "B",
        "Development & 360": "D"
    }
    types = [mapping.get(k) for k in keys if mapping.get(k)]
    return ",".join(types) if types else "K"

def ingest_catalog():
    print("Loading catalog...")
    # with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    # catalog = json.load(f)
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.loads(f.read(), strict=False)

    documents = []
    for item in catalog:
        test_type = get_test_types(item.get('keys', []))
        content = (
            # f"Name: {item.get('name', '')}\n"
            f"passage: Name: {item.get('name', '')}\n"
            f"Description: {item.get('description', '')}\n"
            f"Keys: {', '.join(item.get('keys', []))}\n"
            f"Job Levels: {', '.join(item.get('job_levels', []))}\n"
            f"Languages: {item.get('languages_raw', '')}"
        )
        
        # metadata = {
        #     "name": item.get('name', ''),
        #     "url": item.get('link', ''),
        #     "description": item.get('description', ''),
        #     "keys": item.get('keys', [])
        # }
        metadata = {
            "name": item.get('name', ''),
            "url": item.get('link', ''),
            "description": item.get('description', ''),
            "test_type": test_type
        }
        documents.append(Document(page_content=content, metadata=metadata))

    print("Generating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    # embeddings = HuggingFaceEmbeddings(model_name="intfloat/e5-base-v2")
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    os.makedirs(os.path.dirname(VECTORSTORE_PATH), exist_ok=True)
    vectorstore.save_local(VECTORSTORE_PATH)
    print("Ingestion complete!")

if __name__ == "__main__":
    ingest_catalog()