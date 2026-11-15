
import streamlit as st
from prometheus_client import Counter, Histogram, start_http_server

# Count successfully processed PDF documents
PDF_UPLOADS = Counter(
    "total_pdf_uploads",
    "Total number of successfully processed PDF documents"
)

# Count questions submitted
TOTAL_QUESTIONS = Counter(
    "total_questions",
    "Total number of questions submitted"
)

# Measure AI question-answering duration
QUESTION_RESPONSE_TIME = Histogram(
    "question_response_time_seconds",
    "Time taken to generate AI answers"
)

# Count application errors
APPLICATION_ERRORS = Counter(
    "application_errors",
    "Total number of application errors"
)

# Start the Prometheus metrics endpoint only once
@st.cache_resource
def start_metrics_server():
    start_http_server(8000)
    return True
