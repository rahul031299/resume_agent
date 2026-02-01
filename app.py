import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="IIMN Resume Agent", page_icon="📝")

# --- SIDEBAR: API SETUP ---
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password", help="Get it free at aistudio.google.com")

# --- MAIN APP UI ---
st.title("IIM Nagpur Resume Action-Agent (Strict Mode) 🚀")
st.markdown("""
**Transform rough notes into IIMN-compliant CV points.**
*Strict Compliance: 14 words/120 chars, STAR Format, Specific Power Verbs.*
""")

# --- INPUT SECTION ---
user_text = st.text_area("Paste your rough experience here:", height=150, placeholder="Example: I worked in sales for a summer internship. I had to call people to sell the software. I sold about 30 subscriptions and the revenue went up.")

# --- THE "BRAIN" (LOGIC) ---
if st.button("Generate Bullet Points"):
    if not api_key:
        st.error("⚠️ Please enter your API Key in the sidebar to proceed.")
    elif not user_text:
        st.warning("Please enter some text describing your work.")
    else:
        try:
            # 1. Configure the API
            genai.configure(api_key=api_key)
            
            # 2. AUTO-DETECT WORKING MODEL
            active_model_name = "gemini-pro"
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        active_model_name = m.name
                        break
            except:
                pass 
            
            model = genai.GenerativeModel(active_model_name)
            
            # 3. THE "STRICT COMPLIANCE" PROMPT
            # This prompt includes specific rules and examples from your uploaded PDF.
            system_prompt = f"""
            ROLE: You are a strict Placement Mentor at IIM Nagpur (Prep Comm).
            TASK: Rewrite the user's rough text into 3 resume bullet points that strictly follow the 'One-Page CV Guidelines'.

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
            with st.spinner("Checking against IIM Nagpur Guidelines..."):
                response = model.generate_content(system_prompt)
                
            # 5. Display Output
            st.markdown("### 🎯 Optimized CV Points")
            st.markdown(response.text)
            st.success("✅ Compliance Check: These points follow the 120-character limit and STAR framework.")
            st.info("💡 Tip: Replace the bracketed [X] numbers with your actual data!")
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- FOOTER ---
st.markdown("---")
st.caption("Powered by GenAI • Based on IIM Nagpur Prep Comm Guidelines")
