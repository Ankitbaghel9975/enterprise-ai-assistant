import time
import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from google import genai

from pdf_processor import extract_text_from_pdf, create_chunks
from metrics import (
    PDF_UPLOADS,
    TOTAL_QUESTIONS,
    QUESTION_RESPONSE_TIME,
    APPLICATION_ERRORS,
    start_metrics_server
)

load_dotenv()

st.set_page_config(
    page_title="Enterprise AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

start_metrics_server()

st.title("🤖 Enterprise AI Knowledge Assistant")

st.write(
    "Upload company PDF documents and ask questions "
    "about their contents."
)

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = None

if api_key:
    client = genai.Client(api_key=api_key)

else:
    st.warning("Please configure GEMINI_API_KEY in your .env file.")

st.header("1. Upload PDF Documents")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file:

    if st.button("Process PDF"):

        with st.spinner("Reading and processing PDF..."):

            try:
                with tempfile.NamedTemporaryFile(
                    suffix=".pdf",
                    delete=False
                ) as temp_file:

                    temp_file.write(uploaded_file.getvalue())
                    pdf_path = temp_file.name

                try:
                    pages = extract_text_from_pdf(pdf_path)

                    chunks = create_chunks(pages)

                    count = store_documents(
                        chunks,
                        uploaded_file.name
                    )

                    st.success(
                      f"Successfully processed {count} chunks!"
                   )

                    PDF_UPLOADS.inc()

                finally:
                    os.remove(pdf_path)

            except Exception as error:
                st.error(f"PDF processing failed: {error}")


st.divider()

st.header("2. Ask Questions")

question = st.text_input(
    "Enter your question about the uploaded documents"
)

if st.button("Get Answer"):
    if not client:
        st.error("Configure your Gemini API key first.")

    elif not question.strip():
        st.warning("Please enter a question.")

    else:
        TOTAL_QUESTIONS.inc()
        try:
            with st.spinner("Searching documents and generating answer..."):

                retrieved_chunks = search_documents(question)

                if not retrieved_chunks:
                    st.warning("No documents found. Upload a PDF first.")

                else:
                    context = "\n\n".join([
                        f"Source: {item['filename']}, "
                        f"Page: {item['page']}\n{item['text']}"
                        for item in retrieved_chunks
                    ])

                    prompt = f"""
                    You are an enterprise knowledge assistant.

                    Answer the question using ONLY the provided context.

                    If the answer is not available in the context,
                    clearly say that the uploaded documents do not
                    contain enough information.

                    Context:
                    {context}

                    Question:
                    {question}
                    """

                    start_time = time.time()

                    response = client.interactions.create(
                        model=model_name,
                        input=prompt
                    )

                    QUESTION_RESPONSE_TIME.observe(
                        time.time() - start_time
                    )

                    st.subheader("AI Answer")
                    st.write(response.output_text)

                    st.subheader("Retrieved Sources")

                    for item in retrieved_chunks:
                        st.caption(
                            f"{item['filename']} | Page {item['page']}"
                        )

        except Exception as error:
            APPLICATION_ERRORS.inc()
            st.error(f"Question answering failed: {error}")
