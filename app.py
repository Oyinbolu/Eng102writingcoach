import streamlit as st
import google.generativeai as genai

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="Scribacious AI", page_icon="🎓", layout="wide")

# Custom CSS for OAU aesthetic
st.markdown("""
    <style>
    .main { background-color: #fdfdfd; }
    .stTextArea textarea { font-size: 1.1rem !important; border: 1px solid #003366; }
    .stButton button { background-color: #003366; color: white; border-radius: 10px; height: 3em; font-weight: bold; }
    .title-text { color: #003366; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API CONFIGURATION & ERROR HANDLING ---
# Accessing the key from Streamlit Cloud Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # We use 'gemini-1.5-flash' which is the current stable name
    # Fallback to 'gemini-pro' if 'flash' is unavailable in your region
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('gemini-pro')
else:
    st.error("API Key missing! Please add 'GOOGLE_API_KEY' to your Streamlit Secrets.")

# --- 3. UI LAYOUT ---
st.markdown("<h1 class='title-text'>✍️ Scribacious AI: ENG 102 Coach</h1>", unsafe_allow_html=True)
st.caption("<p style='text-align: center;'>Interactive Writing Assistant for Obafemi Awolowo University Students</p>", unsafe_allow_html=True)

col_ctrl, col_edit = st.columns([1, 2], gap="large")

with col_ctrl:
    st.subheader("Target Module")
    writing_task = st.selectbox(
        "What are you writing?",
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
    
    st.info(f"Focusing on: **{writing_task}**")
    st.markdown("""
    **Evaluation Criteria:**
    *   **Mechanics:** Punctuation/Concord.
    *   **Register:** Appropriate tone.
    *   **Format:** Structural accuracy.
    """)

with col_edit:
    user_input = st.text_area("Type or paste your work below:", height=450, placeholder="Example: Dear Sir, I am writing to...")

    if st.button("🚀 Run Scribacious Analysis"):
        if not user_input.strip():
            st.warning("Please provide some text to analyze.")
        else:
            with st.spinner("Reviewing against OAU ENG 102 standards..."):
                
                # The System Instruction is injected into the prompt
                system_prompt = f"""
                You are Scribacious AI, an expert Senior Lecturer in the English Department at OAU.
                Analyze this student's submission for the ENG 102 module: {writing_task}.
                
                Strictly assess:
                1. Mechanics: Check for concord errors, punctuation, and spelling.
                2. Register: Ensure the tone matches {writing_task} requirements.
                3. Structure: Verify if letters/reports/speeches follow standard formats.
                4. Literacy: Evaluate clarity and expression.

                Format your response exactly as:
                # 📊 Overall Score: [X]/100
                
                ## ✅ Strengths
                (What was done well)
                
                ## ⚠️ Corrections & Feedback
                (Specific errors found in mechanics or register)
                
                ## 💡 The Model Version
                (Provide a professionally rewritten version of their text)
                """
                
                try:
                    # Combining system prompt with student content
                    response = model.generate_content(system_prompt + "\n\nStudent Work:\n" + user_input)
                    
                    st.markdown("---")
                    st.markdown(response.text)
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Coding Error: {e}")
                    st.info("Check your Streamlit Secrets and ensure the library version is updated in requirements.txt.")

# --- 4. FOOTER ---
st.markdown("---")
st.center = st.write("© 2026 Scribacious AI | Introduction to English Grammar and Composition")
