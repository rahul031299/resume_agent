import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="IIMN Resume Agent", page_icon="📝")

# --- SECRET KEY MANAGEMENT ---
# This checks if the key is in Streamlit Secrets (for deployed app)
# If not, it asks the user for it (for local testing)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

st.title("IIM Nagpur Resume Action-Agent 🚀")
st.markdown("**Transform rough notes into IIMN-compliant CV points.**")

user_text = st.text_area("Paste your rough experience here:", height=150)

if st.button("Generate Bullet Points"):
    if not api_key:
        st.error("⚠️ API Key missing. Please contact the administrator.")
    elif not user_text:
        st.warning("Please enter some text.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Auto-detect model logic
            active_model_name = "gemini-pro"
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        active_model_name = m.name
                        break
            except:
                pass
            
            model = genai.GenerativeModel(active_model_name)
            
            # --- STRICT SYSTEM PROMPT ---
            system_prompt = f"""
            ROLE: Strict Placement Mentor at IIM Nagpur.
            TASK: Rewrite user text into 3 resume points strictly following IIMN Guidelines.
            
            RULES:
            1. Max 14 words OR 120 characters per point.
            2. STAR Format (Situation, Task, Action, Result).
            3. Start with Power Verb (e.g., Spearheaded, Orchestrated).
            4. MUST include numbers/metrics (%, $).
            5. No 'worked on' or 'helped'.
            
            INPUT: {user_text}
            
            OUTPUT:
            1. **Consulting Style**
            2. **Finance Style**
            3. **General Mgmt Style**
            """
            
            with st.spinner("Optimizing..."):
                response = model.generate_content(system_prompt)
                
            st.markdown(response.text)
            st.success("✅ Points generated following IIMN Prep Comm Guidelines.")
            
        except Exception as e:
            if "429" in str(e):
                st.error("⚠️ Too many people are using the tool right now! Please wait 1 minute and try again.")
            else:
                st.error(f"Error: {e}")
