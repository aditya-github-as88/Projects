# ── Dockerfile ────────────────────────────────────────────────────────────────
# AI-Powered Airline Customer Support System
# Runs FastAPI (port 8000, internal) + Streamlit (port 7860, public)

# Use slim Python 3.11 image for smaller size
FROM python:3.11-slim

# ── System dependencies ────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ── Set working directory ──────────────────────────────────────────────────────
WORKDIR /app

# ── Install Python dependencies ────────────────────────────────────────────────
# Copy requirements first (better Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Copy application files ─────────────────────────────────────────────────────
COPY airline_api.py .
COPY airline_ui.py .
COPY start.sh .
COPY data/ ./data/

# ── Make startup script executable ────────────────────────────────────────────
RUN chmod +x start.sh

# ── Create non-root user for security ─────────────────────────────────────────
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# ── Expose ports ──────────────────────────────────────────────────────────────
# 7860 = Streamlit (HuggingFace Spaces default, public)
# 8000 = FastAPI   (internal only)
EXPOSE 7860
EXPOSE 8000

# ── Health check ──────────────────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# ── Start both services ────────────────────────────────────────────────────────
CMD ["./start.sh"]
