import streamlit as st
from openai import OpenAI

# --- 1. CONFIGURATION & UI ---
st.set_page_config(page_title="Scribacious AI", page_icon="🎓")

st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    .stButton button { background-color: #003366; color: white; width: 100%; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE DIAGNOSTIC INITIALIZATION ---
if "OPENROUTER_API_KEY" in st.secrets:
    # We .strip() the key to remove accidental spaces from copy-pasting
    raw_key = st.secrets["OPENROUTER_API_KEY"].strip()
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=raw_key,
    )
else:
    st.error("No API Key found in Streamlit Secrets.")
    st.stop()

# --- 3. APP INTERFACE ---
st.title("✍️ Scribacious AI")
writing_task = st.selectbox("Module:", ["Mechanics of Writing", "Formal Letter", "Speech Writing", "Report Writing"])
user_input = st.text_area("Input text:", height=300)

if st.button("🚀 Analyze"):
    if not user_input.strip():
        st.warning("Please enter text first.")
    else:
        with st.spinner("Communicating with OpenRouter..."):
            try:
                # Try a very common model to ensure it's not a model-access issue
                response = client.chat.completions.create(
                    model="google/gemini-flash-1.5", 
                    messages=[
                        {"role": "system", "content": f"You are an OAU Lecturer. Review this {writing_task}."},
                        {"role": "user", "content": user_input}
                    ]
                )
                st.success("Analysis Complete!")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error("⚠️ Connection Error")
                # This detailed message helps us debug the 401
                st.write(f"Server Response: {e}")
                
                st.info("""
                **Possible Fixes:**
                1. **Credits:** OpenRouter requires a small balance ($1) for some models. Check your OpenRouter Credits.
                2. **New Key:** Try generating a fresh key on OpenRouter.
                3. **Format:** Ensure your secret is exactly: `OPENROUTER_API_KEY = "sk-or-v1-..."`
                """)
                
