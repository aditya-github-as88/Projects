#!/bin/bash
# start.sh — Starts both FastAPI backend and Streamlit frontend
# Used inside Docker container and for local testing

set -e

echo "============================================"
echo "  SkyWings AI Airline Customer Support"
echo "============================================"

# ── Start FastAPI backend (background) ────────────────────────────────────────
echo "▶ Starting FastAPI backend on port 8000..."
uvicorn airline_api:app --host 0.0.0.0 --port 8000 --workers 1 &
BACKEND_PID=$!
echo "  Backend PID: $BACKEND_PID"

# ── Wait for backend to be ready ──────────────────────────────────────────────
echo "⏳ Waiting for backend to initialize..."
sleep 10

# Health check loop (up to 60 seconds)
MAX_WAIT=60
WAITED=0
until curl -sf http://localhost:8000/health > /dev/null 2>&1; do
    if [ $WAITED -ge $MAX_WAIT ]; then
        echo "❌ Backend failed to start within ${MAX_WAIT}s"
        exit 1
    fi
    echo "  Still waiting... (${WAITED}s)"
    sleep 5
    WAITED=$((WAITED + 5))
done
echo "✅ Backend is ready!"

# ── Start Streamlit frontend (foreground, main process) ───────────────────────
echo "▶ Starting Streamlit frontend on port 7860..."
streamlit run airline_ui.py \
    --server.port 7860 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --browser.gatherUsageStats false
