import json
import re
import logging
from typing import List, Dict, Any, Tuple
from google import genai
from google.genai.errors import APIError
from app.config import settings

logger = logging.getLogger("app.retrieval")

# In-memory cache for scheme documents and their embeddings
_SCHEME_CACHE: List[Dict[str, Any]] = []
_EMBEDDING_CACHE: List[List[float]] = []

def load_schemes() -> List[Dict[str, Any]]:
    """Loads verified schemes from local JSON file."""
    if not settings.DATA_PATH.exists():
        logger.error(f"Verified dataset path {settings.DATA_PATH} does not exist.")
        return []
    try:
        with open(settings.DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to read schemes JSON: {e}")
        return []

def get_scheme_document_text(scheme: Dict[str, Any]) -> str:
    """Concatenates scheme metadata and text fields to build a robust grounding document."""
    fields = [
        scheme.get("name", ""),
        scheme.get("category", ""),
        scheme.get("summary", ""),
        " ".join(scheme.get("eligibility", [])),
        " ".join(scheme.get("benefits", [])),
        " ".join(scheme.get("keywords", []))
    ]
    return " ".join([f for f in fields if f])

def tokenize(text: str) -> set:
    """Tokenizes text into alphanumeric tokens for keyword matching."""
    if not text:
        return set()
    text = text.lower()
    words = re.findall(r"\w+", text)
    stop_words = {
        "is", "the", "a", "an", "and", "or", "in", "on", "at", "to", "for", "of",
        "with", "about", "by", "what", "how", "where", "who", "which", "explain",
        "tell", "me", "about", "show", "get", "details", "scheme", "schemes",
        "government", "tamil", "nadu", "tn", "state", "central"
    }
    return {w for w in words if w not in stop_words and len(w) > 1}

def calculate_keyword_score(query_tokens: set, scheme: Dict[str, Any]) -> float:
    """Calculates term-overlap score for keyword fallback."""
    score = 0.0
    name_tokens = tokenize(scheme.get("name", ""))
    score += 3.0 * len(query_tokens.intersection(name_tokens))
    
    keywords_text = " ".join(scheme.get("keywords", []))
    kw_tokens = tokenize(keywords_text)
    score += 2.0 * len(query_tokens.intersection(kw_tokens))
    
    cat_sum_text = f"{scheme.get('category', '')} {scheme.get('summary', '')}"
    cat_sum_tokens = tokenize(cat_sum_text)
    score += 1.0 * len(query_tokens.intersection(cat_sum_tokens))
    
    eligibility_text = " ".join(scheme.get("eligibility", []))
    elig_tokens = tokenize(eligibility_text)
    score += 1.0 * len(query_tokens.intersection(elig_tokens))
    
    benefits_text = " ".join(scheme.get("benefits", []))
    ben_tokens = tokenize(benefits_text)
    score += 1.0 * len(query_tokens.intersection(ben_tokens))
    
    return score

def get_embeddings_for_schemes(client: genai.Client, schemes: List[Dict[str, Any]]) -> List[List[float]]:
    """Generates and caches embeddings for all schemes using text-embedding-004."""
    global _EMBEDDING_CACHE, _SCHEME_CACHE
    
    # If cache is already populated, return it
    if _EMBEDDING_CACHE and len(_EMBEDDING_CACHE) == len(schemes):
        return _EMBEDDING_CACHE
        
    logger.info(f"Computing semantic embeddings for {len(schemes)} schemes...")
    embeddings = []
    
    for scheme in schemes:
        doc_text = get_scheme_document_text(scheme)
        try:
            response = client.models.embed_content(
                model=settings.EMBEDDING_MODEL,
                contents=doc_text
            )
            # Response format from google-genai SDK contains list of embeddings
            emb_values = response.embeddings[0].values
            embeddings.append(emb_values)
        except Exception as e:
            logger.error(f"Failed to generate embedding for scheme {scheme.get('id')}: {e}")
            # Fallback with dummy vector if single one fails
            embeddings.append([0.0] * 768)
            
    _EMBEDDING_CACHE = embeddings
    _SCHEME_CACHE = schemes
    return embeddings

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calculates dot product similarity of normalized vectors."""
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot_product = sum(a * b for a, b in zip(v1, v2))
    # Gemini embeddings are unit normalized by default, so dot product matches cosine similarity
    return dot_product

def retrieve_relevant_schemes(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Retrieves matching schemes using hybrid semantic search.
    If API Key is missing or service is offline, falls back to token overlap.
    """
    schemes = load_schemes()
    if not schemes:
        return []
        
    query_tokens = tokenize(query)
    
    # Check if we should attempt semantic search
    if settings.GEMINI_API_KEY:
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            
            # Populate scheme embedding cache
            scheme_embeddings = get_embeddings_for_schemes(client, schemes)
            
            # Generate query embedding
            query_response = client.models.embed_content(
                model=settings.EMBEDDING_MODEL,
                contents=query
            )
            query_vector = query_response.embeddings[0].values
            
            # Compute semantic score & merge with keyword score
            scored_schemes = []
            for idx, scheme in enumerate(schemes):
                semantic_score = cosine_similarity(query_vector, scheme_embeddings[idx])
                keyword_score = calculate_keyword_score(query_tokens, scheme)
                
                # Normalize keyword score roughly (e.g. capped contribution of 0.2)
                normalized_keyword = min(keyword_score / 10.0, 1.0) * 0.2
                
                # Final hybrid score
                hybrid_score = (semantic_score * 0.8) + normalized_keyword
                
                # Only keep matches that show positive affinity
                if hybrid_score > 0.1:
                    scored_schemes.append((hybrid_score, scheme))
                    
            if scored_schemes:
                scored_schemes.sort(key=lambda x: x[0], reverse=True)
                return [scheme for _, scheme in scored_schemes][:top_k]
                
        except Exception as e:
            logger.warning(f"Semantic search failed, falling back to keyword overlap: {e}")
            
    # Fallback/Keyword scoring logic
    logger.info("Executing keyword overlap fallback retrieval.")
    scored_schemes = []
    for scheme in schemes:
        score = calculate_keyword_score(query_tokens, scheme)
        if score > 0:
            scored_schemes.append((score, scheme))
            
    if scored_schemes:
        scored_schemes.sort(key=lambda x: x[0], reverse=True)
        return [scheme for _, scheme in scored_schemes][:top_k]
        
    # Ultimate default if no score matches
    return schemes[:top_k]
