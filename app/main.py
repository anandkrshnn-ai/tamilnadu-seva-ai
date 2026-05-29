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
        
        # 3. Inject matching schemes list
        scheme_names = [scheme.get("name") for scheme in matched_schemes if scheme.get("name")]
        response_data["matched_schemes"] = scheme_names
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")
