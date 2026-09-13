import json
import re

import streamlit as st
from groq import Groq

# ============================================
# PAGE SETUP
# ============================================
st.set_page_config(page_title="Scam Shield PK", page_icon="🛡️", layout="wide")

MODEL_NAME = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """You are a fraud-detection assistant specialised in scam messages
that circulate in Pakistan (fake bank SMS, lottery/prize scams, fake job offers,
investment/crypto fraud, OTP-phishing, courier/parcel scams, romance scams, etc).
Messages may be in English, Urdu, or Roman Urdu (Urdu written in Latin script).

Analyse the message the user gives you and respond with ONLY a valid JSON object,
no markdown fences, no extra commentary, in exactly this shape:

{
  "is_scam": true or false,
  "confidence": <integer 0-100, how confident you are in the verdict>,
  "risk_level": "Safe" | "Low" | "Medium" | "High" | "Critical",
  "red_flags": ["short phrase", "short phrase", ...],
  "explanation": "2-3 sentence explanation in simple Roman Urdu + English mix, aimed at a non-technical reader",
  "safety_tip": "one short actionable safety tip"
}

Guidelines:
- If the message is ordinary/benign, set is_scam to false, risk_level "Safe", and
  red_flags can be an empty list.
- Look for classic red flags: urgency ("abhi karein", "24 hours mein"), requests
  for OTP/PIN/CNIC/card number, suspicious/shortened links, too-good-to-be-true
  prizes, impersonation of banks/govt/couriers, pressure to keep it secret,
  unknown sender claiming to be a relative in an emergency, asking to install an app/APK.
- Keep the explanation short, clear, and non-technical.
- Never include anything outside the JSON object.
"""

EXAMPLES = {
    "Choose an example…": "",
    "📱 Fake bank SMS": (
        "Dear customer, your ABC Bank account will be BLOCKED today. "
        "Verify your account immediately by sharing OTP sent to your number "
        "or click http://abcbank-verify.tk to avoid suspension."
    ),
    "💼 Fake job offer": (
        "Congratulations! You have been selected for a Work From Home job at "
        "Amazon Pakistan, salary 80,000/month. Send Rs. 2500 registration fee "
        "via Easypaisa to confirm your seat within 2 hours."
    ),
    "🎉 Lottery scam (Roman Urdu)": (
        "Mubarak ho! Aap ne Jazz lucky draw mein 1,500,000 rupay jeetay hain. "
        "Apna prize claim karne ke liye apna CNIC number aur OTP is number par "
        "bhejein warna prize cancel ho jayega."
    ),
    "✅ Normal message": (
        "Assalam-o-alaikum, kal ki meeting 3 baje reschedule ho gayi hai, "
        "office aa jayen agenda file ke saath."
    ),
}

# ============================================
# SIDEBAR
# ============================================
# API key is read silently from Streamlit secrets — never shown in the UI.
api_key = st.secrets.get("GROQ_API_KEY", "")

with st.sidebar:
    st.markdown(
        "**Scam Shield PK** analyses SMS / WhatsApp / email text using an LLM "
        "(via Groq) to flag likely fraud common in Pakistan, and explains *why*."
    )
    if not api_key:
        st.warning(
            "⚠️ No Groq API key configured. Add GROQ_API_KEY under "
            "Streamlit Cloud → App settings → Secrets."
        )

# ============================================
# TITLE
# ============================================
st.title("🛡️ Scam Shield PK")
st.markdown("### Paste any suspicious SMS, WhatsApp or email message — get an instant fraud check")
st.markdown("---")

example_choice = st.selectbox("Try an example (optional):", list(EXAMPLES.keys()))
default_text = EXAMPLES[example_choice]

message_text = st.text_area(
    "📩 Message to check",
    value=default_text,
    height=150,
    placeholder="Paste the SMS / WhatsApp / email text here...",
)

check_clicked = st.button("🔍 Check Message", use_container_width=True, type="primary")


def extract_json(raw_text: str):
    """Parse the model's JSON reply, tolerating stray text/markdown fences."""
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


def analyze_message(client: Groq, text: str):
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Message to analyse:\n\n{text}"},
        ],
        temperature=0.2,
        max_tokens=600,
    )
    raw = completion.choices[0].message.content
    return extract_json(raw)


RISK_COLOR = {
    "Safe": "🟢",
    "Low": "🟡",
    "Medium": "🟠",
    "High": "🔴",
    "Critical": "🚨",
}

if check_clicked:
    if not api_key:
        st.error("❌ Groq API key not configured. Please contact the app owner.")
    elif not message_text.strip():
        st.warning("⚠️ Please paste a message to analyse.")
    else:
        try:
            with st.spinner("Analysing message..."):
                client = Groq(api_key=api_key)
                result = analyze_message(client, message_text)

            st.markdown("---")
            col1, col2 = st.columns(2)

            is_scam = bool(result.get("is_scam", False))
            confidence = int(result.get("confidence", 0))
            risk_level = result.get("risk_level", "Unknown")

            with col1:
                if is_scam:
                    st.error("### ❌ LIKELY SCAM")
                else:
                    st.success("### ✅ LOOKS SAFE")
                st.metric("Confidence", f"{confidence}%")

            with col2:
                emoji = RISK_COLOR.get(risk_level, "⚪")
                st.markdown(f"### {emoji} Risk Level: {risk_level}")

            st.progress(min(max(confidence, 0), 100) / 100)

            red_flags = result.get("red_flags", [])
            if red_flags:
                st.markdown("#### 🚩 Red flags detected")
                for flag in red_flags:
                    st.markdown(f"- {flag}")

            st.markdown("#### 💬 Explanation")
            st.write(result.get("explanation", "—"))

            st.markdown("#### 🛡️ Safety tip")
            st.info(result.get("safety_tip", "Never share OTP, CNIC, or card details over SMS/WhatsApp."))

        except json.JSONDecodeError:
            st.error("⚠️ Couldn't parse the model's response. Please try again.")
        except Exception as e:  # noqa: BLE001
            st.error(f"⚠️ Something went wrong: {e}")
else:
    st.info("👆 Paste a message (or pick an example) and click **Check Message**.")

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:gray;'>🛡️ Scam Shield PK — powered by Groq (Llama 3.3) "
    "| For awareness only, not a legal or financial verdict</div>",
    unsafe_allow_html=True,
)
