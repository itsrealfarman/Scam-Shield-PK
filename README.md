# 🛡️ Scam Shield PK

**AI-powered scam / fraud message detector for SMS, WhatsApp and email — built for Pakistan.**

Fake bank SMS, lottery "you won!" texts, fake job offers, and OTP-phishing messages
are one of the most common ways people in Pakistan get defrauded. Most people can't
quickly tell a real bank message from a fake one. Scam Shield PK pastes any message
into an LLM (via **Groq**, running Llama 3.3) and gets back a clear verdict, the
specific red flags, and a plain-language explanation — in seconds.

## How it works

1. User pastes a suspicious SMS / WhatsApp / email message (English, Urdu, or Roman Urdu).
2. The app sends it to Groq's Llama 3.3 70B model with a fraud-analysis system prompt.
3. The model returns a structured verdict: scam or safe, confidence %, risk level,
   the specific red flags it found, a short explanation, and a safety tip.
4. The Streamlit UI renders this as a clear, color-coded result.

No training data or model training required — this is a prompt-engineered LLM
application, which is why it can be built and deployed in a few hours.

## Tech stack

- **LLM inference:** Groq API (`llama-3.3-70b-versatile`)
- **Interface:** Streamlit
- **Deployment:** Streamlit Community Cloud

## Run locally

```bash
git clone <your-repo-url>
cd scam-detector
pip install -r requirements.txt

# add your key
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edit .streamlit/secrets.toml and paste your real Groq API key

streamlit run app.py
```

Get a free Groq API key at [console.groq.com](https://console.groq.com).

## Deploy on Streamlit Community Cloud

1. Push this folder to a GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app** → pick the repo → set main file to `app.py`.
3. In **App settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = "your_real_key_here"
   ```
4. Deploy. The app will pick up the key automatically (the sidebar field auto-fills from `st.secrets`).

## Notes / limitations

- This is a fraud-*awareness* tool, not a legal or financial verdict — always mentioned in the app footer.
- Model can occasionally misjudge ambiguous messages; the confidence score and explanation
  are there so the user can use their own judgement too.
- No personal data is stored; each message is analysed per-request and not logged.

## Roadmap ideas

- Multi-message batch check (paste a whole chat log)
- Browser extension / share-sheet integration for one-tap checking
- Community-reported scam pattern database to keep the prompt current
