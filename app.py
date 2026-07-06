import streamlit as st
import pypdf
from google import genai

# Page Configuration
st.set_page_config(page_title="PDF Assistant", layout="centered")
st.title("📚 PDF Summarizer & Q&A Assistant")

# Initialize Gemini Client
# Streamlit Cloud will securely inject this environment variable for us later!
client = genai.Client()

# 1. File Uploader Component
uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])

if uploaded_file is not None:
    # 2. Extract text based on file type
    file_details = uploaded_file.name
    st.success(f"Loaded: {file_details}")
    
    document_text = ""
    
    if uploaded_file.type == "text/plain":
        document_text = uploaded_file.read().decode("utf-8")
        
    elif uploaded_file.type == "application/pdf":
        # Pass the file buffer straight into pypdf
        reader = pypdf.PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                document_text += page_text + "\n"

    # 3. Trigger Initial Summary (Using Streamlit cache so it doesn't re-run on every click)
    @st.cache_data
    def generate_summary(text):
        prompt = f"Provide a clean, bulleted summary of the following text:\n\n{text}"
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text

    if document_text:
        st.subheader("📋 Document Summary")
        summary = generate_summary(document_text)
        st.write(summary)
        
        st.write("---")
        
        # 4. Interactive Q&A Box
        st.subheader("🙋 Ask a Question")
        user_question = st.text_input("What would you like to know about this document?")
        
        if st.button("Ask Gemini"):
            if user_question:
                with st.spinner("Analyzing document..."):
                    qa_prompt = f"Answer the question based strictly on this document:\n\n{document_text}\n\nQuestion: {user_question}"
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=qa_prompt)
                    st.markdown(f"**🤖 Answer:**\n{response.text}")
            else:
                st.warning("Please enter a question first!")