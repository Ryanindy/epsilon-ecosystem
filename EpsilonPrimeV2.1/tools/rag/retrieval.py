import os
import logging
import chromadb
from chromadb.utils import embedding_functions
from concurrent.futures import ThreadPoolExecutor, TimeoutError

# --- PROJECT ROOT ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- LOGGING ---
logger = logging.getLogger("RAGRetrieval")

# Configuration (ABSOLUTE PATH)
CHROMA_PATH = os.path.join(PROJECT_ROOT, "rag", ".chromadb")
# Threshold for relevance. 
# ChromaDB by default uses squared L2 distance.
# 0.0 is exact match. 
# We interpret 0.25 similarity as a distance threshold.
MIN_SIMILARITY_THRESHOLD = 0.10 

def query_collection(client, ef, coll_name, query_text, top_k):
    """Worker function for parallel querying."""
    try:
        collection = client.get_collection(name=coll_name, embedding_function=ef)
        results = collection.query(
            query_texts=[query_text],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        if not results['ids'] or not results['ids'][0]:
            return []

        coll_results = []
        for i in range(len(results['ids'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            dist = results['distances'][0][i]

            # Heuristic: convert L2 distance to a 0-1 similarity score
            similarity = 1.0 / (1.0 + dist)

            if similarity >= MIN_SIMILARITY_THRESHOLD:
                coll_results.append({
                    "content": doc,
                    "metadata": meta,
                    "similarity": similarity,
                    "collection": coll_name
                })
        return coll_results
    except Exception as e:
        logger.debug(f"Collection {coll_name} query failed: {e}")
        return []

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# ... (keep existing imports) ...

def expand_query_hyde(query_text):
    """Generates a hypothetical response to expand the query (HyDE). Enforces failover."""
    models = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']
    for model in models:
        try:
            llm = ChatGoogleGenerativeAI(
                model=model, 
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                max_retries=0
            )
            system_prompt = "You are a RAG Expansion engine. Generate a concise, information-dense hypothetical paragraph that answers the user's query. Do not include preambles."
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=query_text)]
            response = llm.invoke(messages)
            return f"{query_text}\n\n{response.content}"
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                continue
            logger.debug(f"HyDE expansion failed for {model}: {e}")
            continue
    return query_text

def get_rag_context(query_text, top_k=5, use_hyde=True):
    """
    Queries the hierarchical RAG across multiple collections.
    Now supports HyDE expansion for improved semantic matching.
    """
    if not os.path.exists(CHROMA_PATH):
        return "RAG Index not found."

    search_text = expand_query_hyde(query_text) if use_hyde else query_text

    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        ef = embedding_functions.DefaultEmbeddingFunction()
    except Exception as e:
        return f"Error connecting to RAG: {e}"
    
    # ... (rest of the parallel query logic) ...
    
    collections = [
        "epsilon_collection", 
        "legal_collection", 
        "business_collection",
        "decisions_collection",
        "engineering_collection",
        "media_collection",
        "tools_collection",
        "malware_intel_collection",
        "identity_collection"
    ]
    
    all_results = []
    
    # Limit thread pool to prevent resource exhaustion
    max_workers = min(len(collections), 4)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(query_collection, client, ef, name, search_text, top_k) for name in collections]
        for future in futures:
            try:
                result = future.result(timeout=30)  # 30 second timeout per collection
                all_results.extend(result)
            except TimeoutError:
                logger.warning("Collection query timed out")
            except Exception as e:
                logger.error(f"Collection query error: {e}")

    # Sort by similarity descending
    all_results.sort(key=lambda x: x['similarity'], reverse=True)
    
    # Top K overall
    final_results = all_results[:top_k]
    
    if not final_results:
        return "INSUFFICIENT_EVIDENCE: No high-confidence matches found in RAG."

    context_blocks = []
    for res in final_results:
        meta = res['metadata']
        source = meta.get('source', 'Unknown')
        level = meta.get('level', 'document')
        parent = meta.get('parent_id', 'None')
        
        block = f"### SOURCE: {source} [{level.upper()}]\n"
        if level == "chunk" and parent != "None":
            block += f"**Parent Doc**: {parent}\n"
        block += f"**Relevance**: {res['similarity']:.4f}\n"
        block += f"**Collection**: {res['collection']}\n\n"
        block += f"{res['content']}\n"
        context_blocks.append(block)
        
    return "## RAG KNOWLEDGE RETRIEVAL\n\n" + "\n---\n\n".join(context_blocks)

if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Epsilon Man Core Principles"
    print(get_rag_context(query))
