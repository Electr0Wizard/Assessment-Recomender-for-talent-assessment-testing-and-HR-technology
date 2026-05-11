import json
from langchain_core.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.core.config import VECTORSTORE_PATH

# Initialize embeddings globally so it doesn't reload on every request
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# embeddings = HuggingFaceEmbeddings(model_name="intfloat/e5-base-v2")

@tool
def search_catalog(query: str, k: int = 15) -> str:
    """
    Search the SHL assessment catalog. 
    Pass a descriptive query like 'senior full stack java engineer' or 'safety personality test'.
    Returns a JSON string of matching assessments with highly specific keywords like 'Java Advanced', 'OPQ32r', 'Dependability', 'SVAR' along with their names, descriptions, and URLs.
    """
    try:
        vectorstore = FAISS.load_local(
            VECTORSTORE_PATH, 
            embeddings, 
            allow_dangerous_deserialization=True 
        )
        
        query = f"query: {query}"
        
        results = vectorstore.similarity_search(query, k=k)
        
        extracted_results = []
        for doc in results:
            extracted_results.append({
                "name": doc.metadata.get("name"),
                "url": doc.metadata.get("url"),
                "description": doc.metadata.get("description"),
                "test_type": doc.metadata.get("test_type", "K") 
            })
            
        return json.dumps(extracted_results)
    except Exception as e:
        return f"Error searching catalog: {str(e)}. (Ensure vectorstore is generated)"