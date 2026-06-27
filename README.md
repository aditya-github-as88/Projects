---
title: SkyWings AI Airline Customer Support
emoji: ✈️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# ✈️ SkyWings AI-Powered Airline Customer Support System

An end-to-end AI customer support system for airline queries, built with:

- **LangChain + LangGraph** — Orchestration and ReAct agent
- **Groq LLM** — Fast inference (Llama/GPT models)
- **Pinecone** — Vector store for RAG (policy/FAQ retrieval)
- **PostgreSQL (Supabase)** — Structured flight schedule data
- **FastAPI** — REST API backend
- **Streamlit** — Interactive chat frontend

## System Architecture

```
User Query
    │
    ▼
[Input Guardrail] ── UNSAFE ──► Blocked
    │ SAFE
    ▼
[Classifier LLM]
    ├── need_sql  ──► [SQL Gen] ──► [SQL Guardrail] ──► [AI Agent + PostgreSQL]
    ├── non_sql   ──► [RAG Chain (Pinecone)]
    └── out_of_context ──► [Fallback LLM]
                              │
                    [Output Guardrail]
                              │
                        Response to User
```

## Environment Variables Required

Set these in Hugging Face Spaces → Settings → Secrets:

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Groq API key for LLM |
| `PINECONE_API_KEY` | Pinecone API key |
| `PINECONE_INDEX` | Pinecone index name |
| `DB_HOST` | Supabase PostgreSQL host |
| `DB_PORT` | Database port (5432) |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |
