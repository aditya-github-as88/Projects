"""
airline_ui.py — Streamlit Frontend
AI-Powered Airline Customer Support System
"""

import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# When running inside Docker, FastAPI runs on localhost:8000 (same container)
API_URL = os.getenv("API_URL", "http://localhost:8000")

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SkyWings AI Support",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/airplane-mode-on.png", width=70)
    st.title("✈️ SkyWings Support")
    st.markdown("---")

    # API health check
    try:
        r = requests.get(f"{API_URL}/health", timeout=3)
        if r.status_code == 200:
            st.success("🟢 Backend: Online")
        else:
            st.error("🔴 Backend: Error")
    except Exception:
        st.warning("🟡 Backend: Connecting...")

    st.markdown("---")
    st.markdown("### 📋 Sample Queries")

    sample_groups = {
        "🛫 Flight Queries": [
            "What is the status of flight AI695?",
            "Show flights from Mumbai to Bengaluru.",
            "List flights delayed by more than 60 minutes.",
            "How many seats are available on flight 6E815?",
        ],
        "📦 Baggage Policy": [
            "How much free baggage is allowed?",
            "Can I carry a power bank in cabin?",
            "What are excess baggage charges?",
            "Do you allow musical instruments?",
        ],
        "💳 Cancellation & Refund": [
            "What is the cancellation policy?",
            "How do I request a refund?",
            "What happens if I miss my flight?",
            "Can I reschedule after confirmation?",
        ],
        "♿ Special Assistance": [
            "How do I request wheelchair assistance?",
            "Can expectant mothers fly?",
            "What documents are needed for domestic travel?",
        ],
    }

    for group, samples in sample_groups.items():
        with st.expander(group):
            for s in samples:
                if st.button(s, key=s, use_container_width=True):
                    st.session_state["prefill"] = s

    st.markdown("---")
    st.caption(f"API: `{API_URL}`")

# ── Main Content ──────────────────────────────────────────────────────────────
st.title("✈️ SkyWings AI Customer Support")
st.markdown(
    "Welcome! Ask me anything about **flights, baggage, cancellations, or airline policies**."
)
st.markdown("---")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

CATEGORY_LABELS = {
    "need_sql"      : "🗄️ Flight Data (Database)",
    "non_sql"       : "📖 Policy Info (RAG)",
    "out_of_context": "❓ Out of Scope",
    "blocked"       : "🛡️ Blocked by Guardrail",
}

# Display conversation history
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "✈️"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg.get("category"):
            label = CATEGORY_LABELS.get(msg["category"], msg["category"])
            st.caption(f"Routed via: {label}")

# Chat input
prefill    = st.session_state.pop("prefill", "")
user_input = st.chat_input("Type your airline question here...") or prefill

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Call API and show response
    with st.chat_message("assistant", avatar="✈️"):
        with st.spinner("Looking up your information..."):
            try:
                resp = requests.post(
                    f"{API_URL}/ask",
                    json={"query": user_input},
                    timeout=60
                )
                if resp.status_code == 200:
                    data     = resp.json()
                    response = data["response"]
                    category = data.get("category", "")
                else:
                    response = f"⚠️ API Error {resp.status_code}: {resp.text}"
                    category = ""
            except requests.exceptions.ConnectionError:
                response = (
                    "⚠️ Cannot connect to the backend API. "
                    "Please ensure the FastAPI server is running."
                )
                category = ""
            except requests.exceptions.Timeout:
                response = "⚠️ Request timed out. The backend may be processing. Please try again."
                category = ""
            except Exception as e:
                response = f"⚠️ Unexpected error: {e}"
                category = ""

        st.markdown(response)
        if category:
            label = CATEGORY_LABELS.get(category, category)
            st.caption(f"Routed via: {label}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "category": category
    })

# Clear chat
if st.session_state.messages:
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.caption("Powered by **LangChain** · **LangGraph** · **Pinecone** · **PostgreSQL (Supabase)** · **Groq LLM**")
