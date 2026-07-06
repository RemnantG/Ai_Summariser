import pypdf
from google import genai

class DocumentAssistant:
    def __init__(self):
        # Automatically draws GEMINI_API_KEY from environment/secrets
        self.client = genai.Client()

    def extract_text_from_stream(self, file_buffer, file_type: str) -> str:
        """
        Parses raw text data from file byte buffers.
        Completely agnostic of the UI platform.
        """
        text = ""
        if "text/plain" in file_type or file_type == "txt":
            text = file_buffer.read().decode("utf-8")
        elif "application/pdf" in file_type or file_type == "pdf":
            reader = pypdf.PdfReader(file_buffer)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def generate_summary(self, text: str) -> str:
        """Sends document string data to Gemini for structured summarization."""
        prompt = f"""
        You are an elite research analyst. Provide a beautifully structured executive summary of this document.
        Include:
        - **The Big Picture:** A brief 2-sentence overview.
        - **Key Strategic Insights:** 3-5 high-impact bullet points.
        
        Context: {text}
        """
        response = self.client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text

    def answer_question(self, text: str, question: str) -> str:
        """Answers contextual queries based on the provided text base."""
        prompt = f"""
        Answer the user's question using only the facts present in the context below.
        Context: {text}
        Question: {question}
        """
        response = self.client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text