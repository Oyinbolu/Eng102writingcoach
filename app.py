import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & BRANDING ---
st.set_page_config(page_title="Scribacious AI", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    .stButton button { background-color: #003366; color: white; border-radius: 10px; font-weight: bold; width: 100%; }
    .title-text { color: #003366; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DYNAMIC MODEL INITIALIZATION ---
def get_working_model():
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("API Key missing! Add it to Streamlit Secrets.")
        return None
    
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Logic to find a model that supports 'generateContent'
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini-1.5-flash' in m.name:
                    return genai.GenerativeModel(m.name)
        # Fallback to any gemini-pro model if flash isn't found
        return genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"Failed to list models: {e}")
        return None

model = get_working_model()

# --- 3. UI LAYOUT ---
st.markdown("<h1 class='title-text'>✍️ Scribacious AI: ENG 102 Coach</h1>", unsafe_allow_html=True)

col_settings, col_input = st.columns([1, 2], gap="large")

with col_settings:
    st.subheader("Module Selection")
    writing_task = st.selectbox(
        "Focus Area:",
        ["Mechanics of Writing", "Formal Letter", "Semi-Formal Letter", 
         "Informal Letter", "Speech Writing", "Report Writing", 
         "Internet Correspondence", "Register for Literacy"]
    )
    st.info(f"Targeting OAU standards for: {writing_task}")

with col_input:
    user_text = st.text_area("Paste your work:", height=400)

    if st.button("🚀 Analyze with Scribacious"):
        if not user_text.strip():
            st.warning("Please enter text first.")
        elif model is None:
            st.error("AI Model not initialized. Check API key.")
        else:
            with st.spinner("Scribacious is reviewing your work..."):
                system_prompt = f"""
                You are Scribacious AI, an OAU English Lecturer. 
                Evaluate this {writing_task} for ENG 102.
                Check: Mechanics (Concord/Punctuation), Register, and Format.
                
                Format:
                # 📊 Score: [X]/100
                ## 📝 Feedback
                ## ✅ Model Version
                """
                
                try:
                    # Combining prompt and text
                    response = model.generate_content(f"{system_prompt}\n\nStudent Work: {user_text}")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.balloons()
                except Exception as e:
                    st.error(f"API Error: {e}")
                    st.info("Try refreshing the page or checking your API key quota.")

st.markdown("---")
st.caption("© 2026 Scribacious AI | OAU ENG 102 Project")
