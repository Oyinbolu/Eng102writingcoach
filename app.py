import streamlit as st
from google import genai

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="Scribacious AI", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    .stTextArea textarea { font-size: 1.1rem !important; border: 1px solid #003366; }
    .stButton button { background-color: #003366; color: white; border-radius: 10px; height: 3em; font-weight: bold; width: 100%; }
    .title-text { color: #003366; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. NEW SDK CONFIGURATION ---
# We now use the 'Client' method which is more stable
if "GOOGLE_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key missing! Please add 'GOOGLE_API_KEY' to your Streamlit Secrets.")

# --- 3. UI LAYOUT ---
st.markdown("<h1 class='title-text'>✍️ Scribacious AI: ENG 102 Coach</h1>", unsafe_allow_html=True)
st.caption("<p style='text-align: center;'>Specialized for OAU: Mechanics, Letters, Reports, and Register</p>", unsafe_allow_html=True)

col_ctrl, col_edit = st.columns([1, 2], gap="large")

with col_ctrl:
    st.subheader("Module Settings")
    writing_task = st.selectbox(
        "Select Writing Task:",
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
    
    st.info(f"Goal: Professional **{writing_task}** mastery.")

with col_edit:
    user_input = st.text_area("Type your work here:", height=400, placeholder="Example: To the Registrar, I am writing to apply for...")

    if st.button("🚀 Analyze with Scribacious"):
        if not user_input.strip():
            st.warning("Please enter your text to receive feedback.")
        else:
            with st.spinner("Connecting to Gemini 2.0 Flash..."):
                
                # System instructions embedded in the request
                system_prompt = f"""
                You are Scribacious AI, a Senior Lecturer in the English Department at OAU.
                Analyze this student's work for the ENG 102 module: {writing_task}.
                
                Critically evaluate:
                1. Mechanics (Concord, Punctuation, Spelling).
                2. Register (Tone appropriateness for {writing_task}).
                3. Structure (Standard conventions for the chosen genre).
                4. Literacy (Clarity and effectiveness).

                Format:
                # 📊 Score: [X]/100
                ## 📝 Detailed Critique
                (Breakdown of errors and strengths)
                ## 💡 The 'Great Ife' Standard Version
                (A perfectly rewritten version)
                """
                
                try:
                    # New SDK method: client.models.generate_content
                    response = client.models.generate_content(
                        model='gemini-2.0-flash', 
                        contents=system_prompt + "\n\nStudent Work:\n" + user_input
                    )
                    
                    st.markdown("---")
                    st.markdown(response.text)
                    st.balloons()
                    
                except Exception as e:
                    # If 2.0 fails, it usually means the key doesn't have access yet, 
                    # so we try the 1.5-flash as a fallback.
                    try:
                        response = client.models.generate_content(
                            model='gemini-1.5-flash', 
                            contents=system_prompt + "\n\nStudent Work:\n" + user_input
                        )
                        st.markdown("---")
                        st.markdown(response.text)
                        st.balloons()
                    except Exception as e2:
                        st.error(f"Critical Connection Error: {e2}")

st.markdown("---")
st.caption("Built for OAU ENG 102 | © 2026 Scribacious AI")
