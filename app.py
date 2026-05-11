import streamlit as st
from openai import OpenAI

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="Scribacious AI", page_icon="🎓", layout="wide")

# Custom CSS for OAU Navy/Gold Theme
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    .stButton button { background-color: #003366; color: white; border-radius: 10px; font-weight: bold; width: 100%; }
    .title-text { color: #003366; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. OPENROUTER CLIENT INITIALIZATION ---
# Accessing the secret you are about to set
if "OPENROUTER_API_KEY" in st.secrets:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"],
    )
else:
    st.error("Secret 'OPENROUTER_API_KEY' not found! Please check your Streamlit Settings.")

# --- 3. UI LAYOUT ---
st.markdown("<h1 class='title-text'>✍️ Scribacious AI: ENG 102 Coach</h1>", unsafe_allow_html=True)
st.caption("<p style='text-align: center;'>Powered by OpenRouter | Specialized for OAU Standards</p>", unsafe_allow_html=True)

col_ctrl, col_edit = st.columns([1, 2], gap="large")

with col_ctrl:
    st.subheader("Writing Module")
    writing_task = st.selectbox(
        "Select your task:",
        [
            "Mechanics of Writing",
            "Formal Letter Writing",
            "Semi-Formal Letter",
            "Informal Letter",
            "Speech Writing",
            "Report Writing",
            "Internet Correspondence",
            "Register as a Tool for Literacy"
        ]
    )
    st.info(f"AI Persona: Senior Lecturer reviewing **{writing_task}**.")

with col_edit:
    user_input = st.text_area("Paste your text here:", height=400, placeholder="Type your draft...")

    if st.button("🚀 Analyze with Scribacious"):
        if not user_input.strip():
            st.warning("Please enter text before analyzing.")
        else:
            with st.spinner("Scribacious is reviewing your work..."):
                # System instructions for high-quality feedback
                system_prompt = f"""
                You are Scribacious AI, a Senior Lecturer in English at Obafemi Awolowo University.
                Task: Evaluate this ENG 102 student's submission for: {writing_task}.
                
                Analyze based on:
                1. Mechanics (Concord, Punctuation, Spelling).
                2. Register (Tone appropriateness for {writing_task}).
                3. Structure (Standard conventions for the genre).
                
                Format:
                # 📊 Score: [X]/100
                ## 📝 Feedback
                (Detailed critique)
                ## ✅ Model Version
                (The professionally rewritten version)
                """
                
                try:
                    # Using Gemini 1.5 Flash via OpenRouter for speed and reliability
                    response = client.chat.completions.create(
                        model="google/gemini-flash-1.5",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_input}
                        ]
                    )
                    
                    st.markdown("---")
                    st.markdown(response.choices[0].message.content)
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"OpenRouter Error: {e}")

st.markdown("---")
st.caption("© 2026 Scribacious AI | Great Ife")
