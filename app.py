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

st.title("Prepco Resume Agent 🚀")
st.markdown("**Transform rough notes into IIMN-compliant CV points**")

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
            ROLE: IIM Nagpur Resume Optimization Engine.
            TASK: Convert the input text into 3 high-impact resume bullet points.

            --- IIM NAGPUR GUIDELINES (NON-NEGOTIABLE) ---
            1. LENGTH: Max 14 words OR 120 characters per point. [Strict Constraint]
            2. SYNTAX: Start with a strong POWER VERB. Use Active Voice. Use Past Tense.
            3. STAR FRAMEWORK: Context (Situation) -> Action -> Result (Impact).
            4. QUANTIFICATION: You MUST include numbers/metrics (%, $, time saved). If missing, use placeholders like [X]%.
            5. FORBIDDEN WORDS: Never use 'worked on', 'helped', 'responsible for', 'managed team' (unless specific).
            
            --- TRAINING EXAMPLES (FROM OFFICIAL GUIDE) ---
            * BAD: "Worked on a sales project."
            * GOOD (Sales): "Converted 30+ B2B leads via cold calls, achieving 20% monthly revenue growth."
            * GOOD (Marketing): "Boosted Meta Ads ROAS by 2.1x using A/B tested creatives and landing pages."
            * GOOD (Consulting): "Analysed 5 client portfolios, recommended 3 strategy shifts, boosting efficiency by 12%."
            * GOOD (Ops): "Automated purchase order flow, reducing manual effort by 8 hours/week using workflow tools."
            * GOOD (Finance): "Reconciled financial data of 3 quarters, identifying errors worth 5L in reporting."

            --- USER INPUT ---
            {user_text}

            --- OUTPUT INSTRUCTIONS ---
            Provide 3 variations. Ensure every point is under 120 characters.
            
            1. **Consulting/Strategy Style** (Focus: Efficiency, Analysis, Recommendations)
            2. **Finance/Analytical Style** (Focus: Accuracy, Audit, Numbers, Budget)
            3. **General Mgmt/Ops Style** (Focus: Leadership, Execution, Timelines, Stakeholders)
            """
            # 4. Generate Response
            with st.spinner("Optimizing..."):
                response = model.generate_content(system_prompt)
                
            st.markdown(response.text)
            st.success("✅ Points generated following IIMN Prep Comm Guidelines.")
            
        except Exception as e:
            if "429" in str(e):
                st.error("⚠️ Too many people are using the tool right now! Please wait 1 minute and try again.")
            else:
                st.error(f"Error: {e}")



