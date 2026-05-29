#!/bin/bash
echo "Testing backend health..."
curl -s http://127.0.0.1:8000/health
echo -e "\n\nTesting retrieval and API generation..."
curl -s -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Explain Pudhumai Penn in Tamil","language":"ta"}'
echo -e "\n"
