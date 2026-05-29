#!/bin/bash
# Run backend API server
uvicorn app.main:app --reload --port 8000
