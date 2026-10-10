"""
CloudLLM Explorer — Cloud-Powered AI Question Answering
========================================================
A beginner-friendly Streamlit application that demonstrates cloud-based
Large Language Model inference through Google's Gemini API.

This application does NOT train or host its own model.  It sends prompts
to a hosted LLM via an API and displays the generated response along with
latency measurements.
"""

import time
import streamlit as st

# ---------------------------------------------------------------------------
# Page configuration (must be the first Streamlit command)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="CloudLLM Explorer",
    page_icon="☁️",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MODEL_ID = "gemini-2.0-flash"  # Fast, capable, widely available model


# ---------------------------------------------------------------------------
# Helper — initialise the Gemini client (cached so we only do it once)
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_gemini_client():
    """Return a configured Gemini client, or None with an error message."""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None, (
            "🔑 **Gemini API key not found.**\n\n"
            "Add GEMINI_API_KEY in Streamlit Community Cloud → "
            "App settings → Secrets."
        )

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as exc:
        return None, f"❌ **Failed to initialise Gemini client:** {exc}"
# ---------------------------------------------------------------------------
# Helper — call the model and return (response_text, elapsed_seconds)
# ---------------------------------------------------------------------------
def ask_gemini(client, conversation_messages: list[dict]) -> tuple[str, float]:
    """Send the full conversation to Gemini and return the assistant reply + latency."""
    # Build contents list for the API call
    contents = []
    for msg in conversation_messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    start = time.perf_counter()
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=contents,
    )
    elapsed = time.perf_counter() - start
    return response.text, elapsed


# ---------------------------------------------------------------------------
# Session-state initialisation
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {"role": ..., "content": ...}
if "latencies" not in st.session_state:
    st.session_state.latencies = []  # list of floats (seconds)
if "question_count" not in st.session_state:
    st.session_state.question_count = 0


# ---------------------------------------------------------------------------
# Custom CSS for a cleaner look
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Subtle card-like chat bubbles */
    .stChatMessage { border-radius: 0.75rem; }
    /* Footer styling */
    .footer-text {
        text-align: center;
        font-size: 0.78rem;
        color: #888;
        margin-top: 2rem;
        padding: 1rem 0;
        border-top: 1px solid #e0e0e0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("☁️ CloudLLM Explorer")
st.caption(
    "A cloud-powered AI question-answering app — ask anything and see "
    "how a hosted Large Language Model responds in real time."
)

# ---------------------------------------------------------------------------
# Sidebar — stats, info, controls
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("📊 Session Statistics")
    q_count = st.session_state.question_count
    avg_lat = (
        sum(st.session_state.latencies) / len(st.session_state.latencies)
        if st.session_state.latencies
        else 0.0
    )
    col1, col2 = st.columns(2)
    col1.metric("Questions", q_count)
    col2.metric("Avg latency", f"{avg_lat:.2f} s" if q_count else "— s")

    st.divider()

    # --- Clear conversation button ---
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.latencies = []
        st.session_state.question_count = 0
        st.rerun()

    st.divider()

    # --- How does this work? ---
    with st.expander("ℹ️ How does this work?"):
        st.markdown(
            """
**Request lifecycle:**

1. You type a question in the chat box.
2. The Streamlit app sends your prompt to Google's
   **Gemini API** over HTTPS.
3. The Gemini model (hosted on Google Cloud) generates
   a response.
4. The response is streamed back and displayed here,
   along with the time the round-trip took.

**Key point:** We do **not** train or host the model.
We consume it as a *cloud service* through an API — the
same way you might call a weather API or a payments API.
"""
        )

    # --- Architecture diagram ---
    with st.expander("🏗️ Architecture"):
        st.markdown(
            """
```
┌──────────┐    HTTPS     ┌───────────────────┐    API call    ┌──────────────┐
│  You     │ ──────────▶ │  Streamlit App     │ ────────────▶ │  Gemini API  │
│ (Browser)│ ◀────────── │  (Cloud-hosted)    │ ◀──────────── │  (Google     │
└──────────┘   response   └───────────────────┘   LLM output   │   Cloud)     │
                                                                └──────────────┘
```

- **Streamlit App** — our Python code, deployed on Streamlit Community Cloud.
- **Gemini API** — Google's hosted Large Language Model endpoint.
- **No GPU, no training, no custom infrastructure.**
"""
        )

    st.divider()
    st.markdown(
        f"<div style='font-size:0.75rem;color:#999;'>Model: <code>{MODEL_ID}</code></div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Main chat area
# ---------------------------------------------------------------------------

# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "latency" in msg:
            st.caption(f"⏱️ Response time: {msg['latency']:.2f} s")

# Chat input
if prompt := st.chat_input("Ask me anything about cloud computing, AI, or any topic…"):
    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Try to get the client
    client, err = get_gemini_client()
    if err:
        with st.chat_message("assistant"):
            st.warning(err)
    else:
        # Call the model with a spinner
        with st.chat_message("assistant"):
            with st.spinner("Thinking… (calling the hosted Gemini API)"):
                try:
                    reply, elapsed = ask_gemini(client, st.session_state.messages)
                    st.markdown(reply)
                    st.caption(f"⏱️ Response time: {elapsed:.2f} s")

                    # Persist
                    st.session_state.messages.append(
                        {"role": "assistant", "content": reply, "latency": elapsed}
                    )
                    st.session_state.latencies.append(elapsed)
                    st.session_state.question_count += 1

                except Exception as exc:
                    error_text = str(exc)
                    # Provide user-friendly messages for common errors
                    if "API_KEY_INVALID" in error_text or "401" in error_text:
                        friendly = (
                            "🔒 **Invalid API key.** Please check your "
                            "`GEMINI_API_KEY` in Streamlit secrets."
                        )
                    elif "quota" in error_text.lower() or "429" in error_text:
                        friendly = (
                            "⏳ **Rate limit or quota exceeded.** "
                            "Please wait a moment and try again."
                        )
                    elif "404" in error_text or "not found" in error_text.lower():
                        friendly = (
                            f"🔍 **Model `{MODEL_ID}` not found.** "
                            "It may not be available for your API key or region."
                        )
                    elif "timeout" in error_text.lower() or "deadline" in error_text.lower():
                        friendly = (
                            "⏰ **Request timed out.** The model took too long. "
                            "Please try again."
                        )
                    else:
                        friendly = f"❌ **Error:** {error_text}"
                    st.error(friendly)

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="footer-text">
        <strong>CloudLLM Explorer</strong> — College presentation demo<br>
        The language model is accessed through the
        <a href="https://ai.google.dev/" target="_blank">Google Gemini API</a>,
        a hosted cloud service.<br>
        We have <em>not</em> trained or hosted the model ourselves.
        All inference runs on Google's infrastructure.
    </div>
    """,
    unsafe_allow_html=True,
)
