from pydantic import BaseModel, Field
from typing import List, Literal

class AskRequest(BaseModel):
    question: str = Field(..., description="The user's query about a scheme")
    language: Literal["en", "ta", "hi"] = Field("en", description="The language code (en=English, ta=Tamil, hi=Hindi)")

class SourceItem(BaseModel):
    title: str = Field(..., description="Title of the source official website/document")
    url: str = Field(..., description="Official URL of the welfare scheme")

class AskResponse(BaseModel):
    answer: str = Field(..., description="Concise paragraph answering the user's query in the requested language")
    language: Literal["en", "ta", "hi"] = Field(..., description="The language of the response")
    eligibility: List[str] = Field(default=[], description="Extracted eligibility rules from matched schemes")
    benefits: List[str] = Field(default=[], description="Extracted benefits/entitlements from matched schemes")
    how_to_apply: List[str] = Field(default=[], description="Extracted step-by-step application instructions")
    why_this_answer: str = Field(..., description="Brief reasoning of why this scheme matches the user query")
    sources: List[SourceItem] = Field(default=[], description="List of official source titles and URLs")
    confidence: Literal["high", "medium", "low"] = Field(..., description="AI confidence rating of correctness based on grounding")
    matched_schemes: List[str] = Field(default=[], description="List of matched scheme IDs or names")
