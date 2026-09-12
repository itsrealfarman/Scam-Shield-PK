# 🛡️ Scam Shield PK

**AI-powered scam / fraud message detector for SMS, WhatsApp and email — built for Pakistan.**

Fake bank SMS, lottery "you won!" texts, fake job offers, and OTP-phishing messages
are one of the most common ways people in Pakistan get defrauded. Most people can't
quickly tell a real bank message from a fake one. Scam Shield PK pastes any message
into an LLM (via **Groq**, running the GPT-OSS 120B model) and gets back a clear
verdict, the specific red flags, and a plain-language explanation — in seconds.

## How it works

1. User pastes a suspicious SMS / WhatsApp / email message (English, Urdu, or Roman Urdu).
2. The app sends it to Groq's `openai/gpt-oss-120b` model with a fraud-analysis system prompt.
3. The model returns a structured verdict: scam or safe, confidence %, risk level,
   the specific red flags it found, a short explanation, and a safety tip.
4. The Streamlit UI renders this as a clear, color-coded result.

No training data or model training required — this is a prompt-engineered LLM
application, which is why it can be built and deployed in a few hours.

## Tech stack

- **LLM inference:** Groq API (`openai/gpt-oss-120b`)
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

## Limitations

This is an **awareness tool, not a guaranteed verdict**. Since it relies on an LLM's
judgement rather than a fixed rule set:

- Confidence scores are the model's own estimate, not a mathematically calibrated probability.
- Genuinely new or unusual scam wording it hasn't "seen" the pattern of before can be missed.
- Legitimate urgent messages (real sales, real deadlines) can occasionally be flagged
  as suspicious (false positive).
- It judges the text only — it cannot verify sender numbers, check if a link's
  domain is real, or confirm anything outside the message itself.

The app is meant to help a user make a more informed judgement call, not replace it.

## Notes

- No personal data is stored; each message is analysed per-request and not logged.
- Groq's model naming changes over time (models get deprecated) — if you see a
  `model_not_found` error, check console.groq.com/docs/models for the current
  recommended model and update MODEL_NAME in app.py.

## Roadmap ideas

- Multi-message batch check (paste a whole chat log)
- Browser extension / share-sheet integration for one-tap checking
- Community-reported scam pattern database to keep the prompt current
