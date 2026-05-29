import json
import logging
from typing import List, Dict, Any
from google import genai
from google.genai import types
from google.genai.errors import APIError

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.prompts import get_system_prompt, build_user_prompt

logger = logging.getLogger("app.gemini_client")

def generate_grounded_answer(question: str, language: str, contexts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Interfaces with the Google GenAI SDK to generate a grounded, multilingual response.
    """
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not found in environment variables. Running in mock/offline mode.")
        # Provide a helpful grounded offline response based directly on context
        first_scheme = contexts[0] if contexts else {}
        return {
            "answer": (
                f"[Offline Mode - No API Key Set] Found relevant scheme: {first_scheme.get('name', 'Unknown')}. "
                f"Please set GEMINI_API_KEY to enable full conversational AI."
            ),
            "language": language,
            "eligibility": first_scheme.get("eligibility", []),
            "benefits": first_scheme.get("benefits", []),
            "how_to_apply": first_scheme.get("how_to_apply", []),
            "why_this_answer": "Direct retrieval match of scheme ID: " + str(first_scheme.get("id", "none")),
            "sources": [{"title": first_scheme.get("name", "Official Portal"), "url": first_scheme.get("official_url", "")}] if first_scheme else [],
            "confidence": "medium"
        }
        
    try:
        # Initialize client using the new google-genai SDK format
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        system_instruction = get_system_prompt()
        user_prompt = build_user_prompt(question, language, contexts)
        
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                temperature=0.1,  # Keep temperature low for grounding correctness
            )
        )
        
        # Parse the JSON response
        result = json.loads(response.text)
        return result
        
    except APIError as e:
        logger.error(f"Google GenAI API error: {e}")
        raise RuntimeError(f"Gemini API invocation failed: {str(e)}")
    except json.JSONDecodeError:
        logger.error("Gemini returned invalid JSON.")
        raise RuntimeError("Failed to decode response from Gemini model.")
    except Exception as e:
        logger.error(f"Unexpected error calling Gemini API: {e}")
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")
