

import fitz


def extract_text_from_pdf(pdf_path):
    """
    Extract text from every page of a PDF.
    """

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")

        if text.strip():
            pages.append({
                "page": page_number,
                "text": text
            })

    document.close()

    return pages


def create_chunks(pages, chunk_size=800, overlap=150):
    """
    Divide page text into smaller overlapping chunks.
    """

    chunks = []

    for page_data in pages:

        text = page_data["text"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "page": page_data["page"]
                })

            start += chunk_size - overlap

    return chunks
