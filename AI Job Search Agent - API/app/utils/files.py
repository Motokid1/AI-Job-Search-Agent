from io import BytesIO

from docx import Document
from pypdf import PdfReader


def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            pages.append(text)
    return "\n".join(pages)


def extract_text_from_docx(file_bytes: bytes) -> str:
    document = Document(BytesIO(file_bytes))
    paragraphs = [para.text for para in document.paragraphs if para.text.strip()]
    return "\n".join(paragraphs)


def extract_text_from_resume(filename: str, file_bytes: bytes) -> str:
    lowered = filename.lower()

    if lowered.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    if lowered.endswith(".docx"):
        return extract_text_from_docx(file_bytes)

    raise ValueError("Unsupported file format. Only PDF and DOCX are allowed.")