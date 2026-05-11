import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Scribacious AI", page_icon="✍️", layout="wide")

# Custom Branding for OAU ENG 102
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #002147; color: white; height: 3em; }
    h1 { color: #002147; }
    </style>
    """, unsafe_allow_html=True)

# --- API INITIALIZATION ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Missing API Key! Please add 'GOOGLE_API_KEY' to your Streamlit Secrets.")

# --- APP UI ---
st.title("🎓 Scribacious AI")
st.subheader("Your Interactive ENG 102 Writing Coach")

# Use columns for a dynamic layout
col_settings, col_input = st.columns([1, 2])

with col_settings:
    st.write("### 🛠️ Configuration")
    task_type = st.selectbox(
        "Select Module:",
        [
            "Mechanics of Writing",
            "Formal Letter",
            "Semi-Formal Letter",
            "Informal Letter",
            "Speech Writing",
            "Report Writing",
            "Internet Correspondence",
            "Register as a Tool for Literacy"
        ]
    )
    
    st.markdown(f"""
    **Current Focus:**
    The AI is currently analyzing your work based on **{task_type}** standards used in OAU ENG 102.
    """)

with col_input:
    user_text = st.text_area("✍️ Write or paste your work here:", height=400)
    
    if st.button("🚀 Analyze Writing"):
        if not user_text.strip():
            st.warning("The workspace is empty. Please enter your text.")
        else:
            with st.spinner(f"Reviewing your {task_type}..."):
                # SYSTEM PROMPT LOGIC
                # This string tells Gemini exactly how to behave for each task.
                system_instruction = f"""
                You are Scribacious AI, an expert English Grammar and Composition tutor at OAU. 
                Focus specifically on the following ENG 102 module: {task_type}.
                
                Strictly evaluate based on:
                1. Mechanics (Concord, Punctuation, Spelling).
                2. Structure (For letters: Addresses/Salutations; For reports: Heading/Findings).
                3. Register: Tone and vocabulary appropriateness for {task_type}.
                4. Literacy: How well it communicates the intended message.

                Output Format:
                # 📊 Score: [Number]/100
                ## 🔍 Detailed Analysis
                - **Mechanics:** [Comment]
                - **Register & Tone:** [Comment]
                - **Formatting:** [Comment]
                
                ## ✅ The "Gold Standard" Rewrite
                (Provide the most grammatically perfect and stylistically appropriate version of the student's text).
                """
                
                try:
                    full_prompt = f"{system_instruction}\n\nStudent Text: {user_text}"
                    response = model.generate_content(full_prompt)
                    
                    st.success("Analysis Complete!")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.balloons()
                except Exception as e:
                    st.error(f"Coding Error: {e}")

st.markdown("---")
st.caption("Developed for ENG 102 Students | Powered by Gemini 1.5 Flash")
  
