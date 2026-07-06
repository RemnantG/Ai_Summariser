import streamlit as st
from backend import DocumentAssistant  # Our separated logic brain

# 1. Page Configuration for a dark, immersive feel
st.set_page_config(
    page_title="DocuMind Seer's Sanctum",
    page_icon="🔮",
    layout="centered"  # Keeps the focus centralized on the crystal ball
)

# 2. Inject Custom CSS for Theme and Crystal Ball Visualization
st.markdown("""
<style>
    /* 1. Global Page Background (Deep Obsidian/Velvet Purple) */
    .stApp {
        background: radial-gradient(circle at center, #11052C 0%, #05010B 100%);
        color: #E6E1F1 !important;
        font-family: 'Garamond', serif;
    }

    /* 2. Mystical Header Styling */
    .witch-title {
        color: #B298E6;
        font-family: 'Garamond', serif;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        text-shadow: 0px 0px 15px rgba(178, 152, 230, 0.6);
        margin-bottom: -15px;
    }
    .witch-subtitle {
        color: #8C6FD1;
        text-align: center;
        font-style: italic;
        margin-bottom: 2rem;
    }

    /* 3. THE CRYSTAL BALL VISUALIZATION */
    .crystal-ball-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: -30px;
        margin-bottom: 30px;
    }
    .crystal-ball {
        width: 320px;
        height: 320px;
        background: radial-gradient(circle at 30% 30%, #4C1D95 0%, #1D0A3D 60%, #0A0214 100%);
        border-radius: 50%;
        box-shadow: 
            0 0 40px rgba(178, 152, 230, 0.6), /* Outer Glow */
            inset 0 0 30px rgba(255, 255, 255, 0.1); /* Inner Reflection */
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        overflow: hidden; /* Contains the text within the ball */
        border: 2px solid #2D1452;
    }
    /* Pulsing Light inside the ball */
    .crystal-ball::before {
        content: '';
        position: absolute;
        width: 150%;
        height: 150%;
        background: radial-gradient(circle, rgba(178, 152, 230, 0.2) 0%, rgba(0,0,0,0) 70%);
        animation: pulse 4s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); opacity: 0.5; }
    }

    /* Text displayed *inside* the crystal ball */
    .ball-content {
        color: #FFFFFF;
        font-size: 0.9rem;
        padding: 40px;
        text-align: center;
        z-index: 1; /* Puts text above the pulse effect */
        font-family: 'Garamond', serif;
        overflow-y: auto; /* Adds scroll if summary is long */
        max-height: 80%; /* Limits text height */
    }

    /* 4. Thematic Inputs and Text */
    .stTextInput>div>div>input {
        background-color: #1A0B35;
        color: #FFFFFF;
        border: 1px solid #6B21A8;
        border-radius: 20px;
        font-family: 'Garamond', serif;
    }
    stMarkdown, stCaption {
        color: #B298E6;
        font-family: 'Garamond', serif;
    }

</style>
""", unsafe_allow_html=True)

# Instantiate the backend brain
seer = DocumentAssistant()

# 3. Main Sanctum Layout
st.markdown('<div class="witch-title">🔮 The All-Knowing Seer</div>', unsafe_allow_html=True)
st.markdown('<div class="witch-subtitle">Feed manuscripts into the void; peer deep into their contained truths.</div>', unsafe_allow_html=True)
st.write("---")

# The Altar (File Input)
with st.sidebar:
    st.markdown("### 📜 The Sacrificial Altar")
    st.caption("Place your mundane document upon the altar to initiate the ritual.")
    uploaded_file = st.file_uploader("", type=["txt", "pdf"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### ⚙️ Dark Arcane Settings")
    st.caption("Powered by the Whispering Gemini Matrix.")

# Logic flow remains clean because we separated it!
if uploaded_file is None:
    # Empty State with visual pointer
    st.markdown(
        "<div style='text-align: center; color: #6B21A8; font-style: italic; margin-top: 5rem;'>"
        "👈 The crystal sits dark. Place your manuscript upon the sidebar altar."
        "</div>", 
        unsafe_allow_html=True
    )
else:
    # Read text using backend brain
    with st.spinner("🔄 Chanting incantations to read the runes..."):
        document_text = seer.extract_text_from_stream(uploaded_file, uploaded_file.type)

    if document_text:
        # Success status
        st.toast(f"The text has been consumed by the entity.", icon="👁️")
        
        # 4. Peer into the Crystal Ball (Summary)
        st.subheader("📋 Glimpse the Essence (Summary)")

        # Generate (and cache) summary using backend brain
        @st.cache_data
        def get_cached_summary(text):
            # We slightly alter the *voice* instructions right here in app.py
            witch_voice_prompt = f"""
            You are an all-knowing ancient witch speaking through a glowing crystal ball. 
            Summarize the core truth of the following context precisely but with a slightly cryptic, elite, mystical tone.
            Use labels like '🌙 The Core Intentions' and '✨ Key Strategic Manifestations'.
            
            Context: {text}
            """
            # Pass the themed prompt into our modular brain's API method
            return seer.generate_summary(witch_voice_prompt)

        summary_text = get_cached_summary(document_text)

        # RENDER THE CRYSTAL BALL and inject the summary text inside it
        st.markdown(f"""
            <div class="crystal-ball-container">
                <div class="crystal-ball">
                    <div class="ball-content">
                        {summary_text}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.write("---")

        # 5. Question & Answer Interface
        st.subheader("💬 Speak into the Void (Q&A)")
        user_question = st.text_input("Whisper your query:", placeholder="e.g., What are the core conclusions?")
        
        if user_question:
            # Re-theme the QA prompt to maintain the voice
            witch_qa_prompt = f"""
            You are an all-knowing ancient witch. Answer the user's question using ONLY the facts present in the text context. 
            Speak with precise, elite, and slightly mystical language. If the answer is missing, state that the spirits are silent on that matter.
            
            Context: {document_text}
            Question: {user_question}
            """
            
            with st.spinner("Scrying the temporal mists..."):
                answer = seer.answer_question(document_text, witch_qa_prompt)
                
                with st.chat_message("assistant", avatar="🧙‍♀️"):
                    st.write(answer)