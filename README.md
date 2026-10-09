# ☁️ CloudLLM Explorer

A beginner-friendly Streamlit application demonstrating **cloud-based Large Language Model inference** through a hosted API.

Built for a college presentation on *Cloud Computing Behind Large Language Models*.

> **Important:** This project does **not** train or host its own LLM. It consumes Google's Gemini model as a cloud service through the Gemini API — just like calling any other web API.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 Chat interface | Ask any question and receive an AI-generated answer |
| 🌐 Hosted LLM API | Uses Google Gemini API — no local GPU required |
| 📜 Conversation history | Maintains context within the current session |
| ⏱️ Latency measurement | Shows how long each API round-trip takes |
| 📊 Session statistics | Tracks question count and average response time |
| ℹ️ "How does this work?" | Expandable explanation of the request lifecycle |
| 🏗️ Architecture diagram | Visual overview of the cloud request flow |
| ⏳ Loading indicator | Clear spinner while the model is processing |
| ⚠️ Error handling | Friendly messages for invalid keys, quota limits, network errors |
| 🗑️ Clear conversation | One-click button to reset the session |
| 📱 Responsive design | Clean layout suitable for a live classroom demo |
| 📝 Honest footer | States that the model is accessed via API, not self-hosted |

---

## 🛠️ Technology Stack

- **Python 3.10+**
- **[Streamlit](https://streamlit.io/)** — rapid web-app framework for data/ML apps
- **[Google GenAI SDK](https://pypi.org/project/google-genai/)** (`google-genai`) — official Python client for the Gemini API
- **Git / GitHub** — version control and source hosting
- **[Streamlit Community Cloud](https://streamlit.io/cloud)** — free deployment platform

---

## 🏗️ Architecture / Request Flow

```
┌──────────┐    HTTPS     ┌───────────────────┐    API call    ┌──────────────┐
│   User   │ ──────────▶ │  Streamlit App     │ ────────────▶ │  Gemini API  │
│ (Browser)│ ◀────────── │  (Cloud-hosted)    │ ◀──────────── │  (Google     │
└──────────┘   response   └───────────────────┘   LLM output   │   Cloud)     │
                                                                └──────────────┘
```

1. The user types a question in the browser.
2. Streamlit sends the prompt to the **Google Gemini API** over HTTPS.
3. Google's infrastructure runs the LLM and returns the generated text.
4. The app displays the answer and the round-trip latency.

---

## 📂 Repository Structure

```
cloudllm-explorer/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .gitignore              # Files excluded from Git
└── .streamlit/
    └── secrets.toml        # API key (git-ignored, never committed)
```

---

## 🚀 Local Setup (Windows)

### Prerequisites

- **Python 3.10 or later** installed ([python.org](https://www.python.org/downloads/))
- A **Google Gemini API key** (see below)

### 1. Clone the repository

```bash
git clone https://github.com/kevaljatakia/cloudllm-explorer.git
cd cloudllm-explorer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get a Gemini API key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey).
2. Sign in with your Google account.
3. Click **"Create API key"** and copy the generated key.
4. The free tier provides generous usage limits for demos. Check [Google's pricing page](https://ai.google.dev/pricing) for current details.

### 5. Configure the secret

Edit `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "paste-your-actual-key-here"
```

> ⚠️ **Never commit this file.** It is listed in `.gitignore`.

### 6. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## ☁️ Deploy on Streamlit Community Cloud

1. Push this repository to GitHub (public repo).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
3. Click **"Create app"** → select the `cloudllm-explorer` repo, `main` branch, `app.py`.
4. Click **"Advanced settings"** → paste your secret:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```
5. Click **"Deploy"**.
6. The app will be live at a `*.streamlit.app` URL.

Any push to the `main` branch auto-redeploys the app.

---

## 🔒 Security Notes

- The Gemini API key is **never** committed to Git or exposed in source code.
- Secrets are stored in Streamlit's secure secrets manager (locally in `.streamlit/secrets.toml`, on the cloud in the deployment settings).
- The app never prints or logs the full API key.
- Error messages are user-friendly and do not leak credentials.

---

## ⚠️ Known Limitations

- **No persistent storage** — conversation is lost when the page is refreshed.
- **API usage limits** — the Gemini free tier has rate limits; heavy use may require a paid plan.
- **Single session** — each browser tab runs its own session.
- **No authentication** — anyone with the URL can use the app (within API quota).
- **Model availability** — the specific model (`gemini-2.0-flash`) must be available in your Google Cloud region.

---

## 🔗 Links

- **GitHub Repository:** [github.com/kevaljatakia/cloudllm-explorer](https://github.com/kevaljatakia/cloudllm-explorer)
- **Deployed App:** *(URL will be added after deployment)*

---

## 📄 License

This project is created for educational purposes as part of a college presentation on cloud computing and Large Language Models.
