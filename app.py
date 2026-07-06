import streamlit as st
import pypdf
from google import genai

# Page Configuration & Theme Match
st.set_page_config(
    page_title="DocuMind AI", 
    page_icon="🤖",
    layout="centered" # Clean, focused reading layout
)

# Custom Styling for polished elements
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F8FAFC;
        border-radius: 4px 4px 0px 0px;
        padding-left: 16px;
        padding-right: 16px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #EFF6FF !important;
        border-bottom: 2px solid #3B82F6 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main Title Headers
st.markdown("# 🧠 DocuMind AI")
st.markdown("##### *Your Intelligent Document Workspace*")
st.write("---")

# 1. File Upload Area (Now with a progress/status indicator)
uploaded_file = st.file_uploader("📂 Drop your PDF or TXT document here", type=["txt", "pdf"])

if uploaded_file is not None:
    # Extract text based on file type
    document_text = ""
    with st.spinner("🔄 Reading document layers..."):
        if uploaded_file.type == "text/plain":
            document_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            reader = pypdf.PdfReader(uploaded_file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    document_text += page_text + "\n"

    if document_text:
        # Success pill with file statistics
        st.toast(f"Successfully loaded {uploaded_file.name}!", icon="✅")
        
        # 2. Modern Tabbed Workspace Layout
        tab1, tab2 = st.tabs(["📋 Executive Summary", "💬 Interactive Chat Explorer"])

        # --- TAB 1: EXECUTIVE SUMMARY ---
        with tab1:
            st.markdown("### Document Summary")
            
            @st.cache_data
            def generate_summary(text):
                prompt = f"""
                You are an elite research analyst. Provide a beautifully structured, executive summary of this document.
                Include:
                - **The Big Picture:** A brief 2-sentence overview.
                - **Key Strategic Insights:** 3-5 high-impact bullet points.
                Context: {text}
                """
                client = genai.Client()
                response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                return response.text

            with st.spinner("Analyzing text patterns..."):
                summary_text = generate_summary(document_text)
                st.markdown(summary_text)
            
            st.write("---")
            # Added Feature: Export/Download Summary Utility
            st.download_button(
                label="📥 Download Summary as .txt",
                data=summary_text,
                file_name=f"Summary_{uploaded_file.name}.txt",
                mime="text/plain"
            )

        # --- TAB 2: INTERACTIVE CHAT EXPLORER ---
        with tab2:
            st.markdown("### Conversational Engine")
            st.caption("Ask specific questions, cross-examine data, or request translations of sections.")
            
            # Text input for user query
            user_question = st.text_input("Ask a question about this document:", placeholder="What are the main metrics or conclusions?")
            
            if user_question:
                # Render the user's message using Streamlit's native chat bubble UI
                with st.chat_message("user"):
                    st.write(user_question)
                
                # Generate and render AI response
                with st.chat_message("assistant"):
                    with st.spinner("Scanning file matrix..."):
                        qa_prompt = f"""
                        Answer the user's question using only the facts present in the text context.
                        Context: {document_text}
                        Question: {user_question}
                        """
                        client = genai.Client()
                        response = client.models.generate_content(model='gemini-2.5-flash', contents=qa_prompt)
                        st.write(response.text)
else:
    # Onboard screen when no file is present
    st.info("👋 Welcome! To begin, please drag and drop or upload a document file above.")