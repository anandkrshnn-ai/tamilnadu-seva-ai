from typing import List, Dict, Any

def get_system_prompt() -> str:
    return (
        "You are 'TamilNadu Seva AI', a trustworthy, professional, and empathetic public-service assistant. "
        "Your objective is to help citizens understand and apply for welfare schemes in Tamil Nadu and selected central government initiatives. "
        "You MUST respond ONLY using the verified scheme contexts provided. Do not assume, extrapolate, or hallucinate parameters. "
        "If the contexts do not contain enough information to answer a question, state clearly in the selected language "
        "that the information is not fully clear in our database, and advise checking the official website.\n\n"
        "Your output must be formatted as a JSON object matching this schema:\n"
        "{\n"
        '  "answer": "A concise paragraph answering the question directly in the requested language.",\n'
        '  "eligibility": ["List of eligibility criteria directly from context in the requested language"],\n'
        '  "benefits": ["List of benefits directly from context in the requested language"],\n'
        '  "how_to_apply": ["List of application steps directly from context in the requested language"],\n'
        '  "why_this_answer": "Explanation of which retrieved information supported this conclusion in the requested language.",\n'
        '  "sources": [{"title": "Official Portal Name", "url": "Official URL"}],\n'
        '  "confidence": "high|medium|low"\n'
        "}\n\n"
        "Ensure the entire response is valid JSON. Do not wrap it in markdown code blocks like ```json ... ```."
    )

def build_user_prompt(question: str, language: str, contexts: List[Dict[str, Any]]) -> str:
    context_str = ""
    for idx, ctx in enumerate(contexts):
        context_str += (
            f"--- Context {idx + 1} ---\n"
            f"Scheme ID: {ctx.get('id')}\n"
            f"Scheme Name: {ctx.get('name')}\n"
            f"Category: {ctx.get('category')}\n"
            f"Department: {ctx.get('department')}\n"
            f"Summary: {ctx.get('summary')}\n"
            f"Eligibility: {', '.join(ctx.get('eligibility', []))}\n"
            f"Benefits: {', '.join(ctx.get('benefits', []))}\n"
            f"How to Apply: {', '.join(ctx.get('how_to_apply', []))}\n"
            f"Language Notes: {ctx.get('language_notes', '')}\n"
            f"Official URL: {ctx.get('official_url', '')}\n"
            f"Source Type: {ctx.get('source_type', '')}\n"
            "\n"
        )
        
    lang_mapping = {
        "en": "English",
        "ta": "Tamil (தமிழ்)",
        "hi": "Hindi (हिन्दी)"
    }
    target_lang = lang_mapping.get(language, "English")
    
    return (
        f"Verified Scheme Contexts:\n{context_str}\n"
        f"User Question: {question}\n"
        f"Requested Response Language: {target_lang}\n\n"
        f"Generate the grounded response in {target_lang} adhering strictly to the system schema rules."
    )
