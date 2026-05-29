from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import AskRequest, AskResponse
from app.retrieval import retrieve_relevant_schemes
from app.gemini_client import generate_grounded_answer

app = FastAPI(
    title="TamilNadu Seva AI API",
    description="Trustworthy multilingual AI assistant for Tamil Nadu welfare schemes",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy"}

@app.post("/ask", response_model=AskResponse, tags=["AI Assistant"])
def ask_question(request: AskRequest):
    """
    Retrieves matching schemes from the local dataset, runs grounded Gemini analysis,
    and returns a structured, trustworthy response in the requested language.
    """
    try:
        # 1. Retrieve top 3 relevant schemes
        matched_schemes = retrieve_relevant_schemes(request.question, top_k=3)
        
        # 2. Run Gemini Generation
        response_data = generate_grounded_answer(
            question=request.question,
            language=request.language,
            contexts=matched_schemes
        )
        
        # 3. Sanitize responses to prevent Pydantic serialization validation errors
        if not isinstance(response_data, dict):
            response_data = {"answer": str(response_data)}
            
        response_data["language"] = response_data.get("language") or request.language
        response_data["confidence"] = response_data.get("confidence") or "medium"
        response_data["why_this_answer"] = response_data.get("why_this_answer") or "Extracted from verified local documentation."
        
        # Standardize lists
        for list_field in ["eligibility", "benefits", "how_to_apply"]:
            if not isinstance(response_data.get(list_field), list):
                response_data[list_field] = []
                
        # Clean up sources
        sources_list = []
        for src in response_data.get("sources", []):
            if isinstance(src, dict) and src.get("title") and src.get("url"):
                sources_list.append({"title": src["title"], "url": src["url"]})
            elif isinstance(src, str):
                sources_list.append({"title": "Official Link", "url": src})
                
        if not sources_list:
            for scheme in matched_schemes:
                sources_list.append({
                    "title": scheme.get("name", "Official Portal"),
                    "url": scheme.get("official_url", "")
                })
        response_data["sources"] = sources_list

        # Inject matching schemes list
        scheme_names = [scheme.get("name") for scheme in matched_schemes if scheme.get("name")]
        response_data["matched_schemes"] = scheme_names
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")
