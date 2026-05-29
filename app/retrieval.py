import json
import re
from typing import List, Dict, Any
from app.config import DATA_PATH

def load_schemes() -> List[Dict[str, Any]]:
    """Loads verified schemes from local JSON file."""
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def tokenize(text: str) -> set:
    """Tokenizes text into a set of lowercased alphanumeric words."""
    if not text:
        return set()
    text = text.lower()
    # Simple alphanumeric split
    words = re.findall(r"\w+", text)
    # Exclude common English stop words
    stop_words = {
        "is", "the", "a", "an", "and", "or", "in", "on", "at", "to", "for", "of",
        "with", "about", "by", "what", "how", "where", "who", "which", "explain",
        "tell", "me", "about", "show", "get", "details", "scheme", "schemes",
        "government", "tamil", "nadu", "tn", "state", "central"
    }
    return {w for w in words if w not in stop_words and len(w) > 1}

def retrieve_relevant_schemes(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Ranks schemes by keyword overlap with the user query.
    Scrutinizes: name, category, summary, eligibility, benefits, and keywords.
    """
    schemes = load_schemes()
    query_tokens = tokenize(query)
    
    if not query_tokens:
        # Return first top_k schemes if query is empty or has no meaningful tokens
        return schemes[:top_k]
    
    scored_schemes = []
    for scheme in schemes:
        score = 0
        # 1. Match in Name (weight: 3)
        name_tokens = tokenize(scheme.get("name", ""))
        score += 3 * len(query_tokens.intersection(name_tokens))
        
        # 2. Match in Keywords list (weight: 2)
        keywords_text = " ".join(scheme.get("keywords", []))
        kw_tokens = tokenize(keywords_text)
        score += 2 * len(query_tokens.intersection(kw_tokens))
        
        # 3. Match in Category and Summary (weight: 1)
        cat_sum_text = f"{scheme.get('category', '')} {scheme.get('summary', '')}"
        cat_sum_tokens = tokenize(cat_sum_text)
        score += len(query_tokens.intersection(cat_sum_tokens))
        
        # 4. Match in Eligibility list (weight: 1)
        eligibility_text = " ".join(scheme.get("eligibility", []))
        elig_tokens = tokenize(eligibility_text)
        score += len(query_tokens.intersection(elig_tokens))
        
        # 5. Match in Benefits list (weight: 1)
        benefits_text = " ".join(scheme.get("benefits", []))
        ben_tokens = tokenize(benefits_text)
        score += len(query_tokens.intersection(ben_tokens))

        if score > 0:
            scored_schemes.append((score, scheme))
            
    # Sort descending by score
    scored_schemes.sort(key=lambda x: x[0], reverse=True)
    
    # Extract scheme objects
    results = [scheme for _, scheme in scored_schemes]
    
    # If no matches are found, return the top_k default schemes
    if not results:
        return schemes[:top_k]
        
    return results[:top_k]
