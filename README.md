# TamilNadu Seva AI

TamilNadu Seva AI is a trustworthy, multilingual AI assistant designed to help citizens learn about and apply for welfare schemes in Tamil Nadu and selected central government initiatives. Users can ask questions in English, Tamil, or Hindi, and receive simple, grounded answers complete with eligibility criteria, benefits, step-by-step instructions on how to apply, reasoning details, and links to official portals.

This prototype was developed for the **Google Cloud Gen AI Academy APAC Meet the Builders** event.

---

## 🏛️ Local Problem & Why Trustworthy AI Matters
Welfare schemes are crucial for uplifting citizens, but accessing scheme information presents major hurdles:
- **Language Barriers**: Many government portals are in English, which excludes a large segment of the population.
- **Complex Specifications**: Scheme guidelines are often written in legal or administrative language.
- **Hallucination Risks in LLMs**: General AI systems might invent critical facts, dates, or eligibility requirements, creating confusion.

**TamilNadu Seva AI** solves this by using **Retrieval-Augmented Generation (RAG)** grounded entirely on a verified, local dataset. Every answer contains a "Why this answer?" reasoning section, direct source citations, and a disclaimer to ensure complete transparency.

---

## 🛠️ Google AI Tools & Tech Stack
- **FastAPI**: Lightweight, high-performance web API framework for routing.
- **Streamlit**: Beautiful, responsive, multilingual frontend UI.
- **Google GenAI SDK (`google-genai`)**: The official SDK used to access the Gemini API.
- **Gemini 2.5 Flash**: Multi-language generation optimized for low latency and robust structured JSON output formatting.
- **Token Overlap Scoring Retrieval**: Clean local scoring algorithm with no complex database prerequisites.

---

## 📁 Repository Structure

```
tamilnadu-seva-ai/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── PROMPT.md
├── BLOG_DRAFT.md
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── retrieval.py
│   ├── prompts.py
│   ├── gemini_client.py
│   ├── main.py
│   └── data/
│       └── schemes_data.json
├── frontend/
│   └── streamlit_app.py
├── tests/
│   ├── test_health.py
│   └── test_retrieval.py
├── cloudrun/
│   ├── Dockerfile.api
│   ├── Dockerfile.ui
│   └── service.yaml
└── scripts/
    ├── run_api.sh
    ├── run_ui.sh
    └── smoke_test.sh
```

---

## 🚀 Local Setup & Run Instructions

### 1. Clone & Initialize Environment
```bash
python -m venv .venv
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```
*Edit `.env` and configure your `GEMINI_API_KEY`.*

### 2. Start Backend API
```bash
uvicorn app.main:app --reload --port 8000
```
API is available at `http://127.0.0.1:8000/docs`.

### 3. Start Frontend Dashboard
```bash
streamlit run frontend/streamlit_app.py --server.port 8501
```
UI dashboard is available at `http://127.0.0.1:8501`.

### 4. Run Smoke Test
Ensure the backend API is running and execute:
```bash
sh scripts/smoke_test.sh
```

---

## 📡 API Contract

### `GET /health`
Verifies that the server is online.
**Response:**
```json
{
  "status": "healthy"
}
```

### `POST /ask`
Submit a user question about a scheme.
**Request Schema:**
```json
{
  "question": "Explain Pudhumai Penn in Tamil",
  "language": "ta"
}
```

**Response Schema:**
```json
{
  "answer": "...",
  "language": "ta",
  "eligibility": ["..."],
  "benefits": ["..."],
  "how_to_apply": ["..."],
  "why_this_answer": "...",
  "sources": [{"title": "...", "url": "..."}],
  "confidence": "high",
  "matched_schemes": ["Pudhumai Penn Scheme..."]
}
```

---

## ☁️ Google Cloud Run Deployment

To build containers and deploy directly:

### 1. Deploy Backend API
```bash
gcloud run deploy tamilnadu-seva-api \
  --source . \
  --dockerfile cloudrun/Dockerfile.api \
  --region asia-south1 \
  --set-env-vars GEMINI_API_KEY=your-actual-api-key \
  --allow-unauthenticated
```
*Note down the backend service URL generated (e.g. `https://tamilnadu-seva-api-xxxxx.a.run.app`).*

### 2. Deploy Frontend UI
```bash
gcloud run deploy tamilnadu-seva-ui \
  --source . \
  --dockerfile cloudrun/Dockerfile.ui \
  --region asia-south1 \
  --set-env-vars BACKEND_API_URL=https://tamilnadu-seva-api-xxxxx.a.run.app \
  --allow-unauthenticated
```

---

## ⚠️ Disclaimer
This assistant summarizes official information for convenience. Final eligibility and benefits should be verified on the official government website.