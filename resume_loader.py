import os
import PyPDF2
import docx
from typing import Optional, List, Dict, Union

def extract_text_from_pdf(file) -> str:
    """
    Extracts text from a PDF file.

    Parameters:
        file (BinaryIO or str): PDF file object (for uploaded files) or file path.

    Returns:
        str: Extracted text from the PDF.
    """
    reader = PyPDF2.PdfReader(file)
    # Extract text from all pages and join with newline, ignoring pages with no text
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()]).strip()

def extract_text_from_docx(file: Union[str, object]) -> str:
    """
    Extracts text from a DOCX file.

    Parameters:
        file (str or file-like object): DOCX file path or uploaded file object.

    Returns:
        str: Extracted text from the DOCX file.
    """
    doc = docx.Document(file)
    # Extract all paragraph texts and join with newline
    return "\n".join([para.text for para in doc.paragraphs]).strip()

def load_resumes(
    uploaded_files: Optional[List[object]] = None,
    from_directory: bool = False,
    resume_dir: str = "resumes"
) -> Dict[str, str]:
    """
    Loads resumes from uploaded files or from a local directory.

    Parameters:
        uploaded_files (list, optional): List of uploaded file objects (e.g., Streamlit upload).
        from_directory (bool): If True, load resumes from the local directory specified by resume_dir.
        resume_dir (str): Path to the directory containing resumes.

    Returns:
        dict: Dictionary with filenames as keys and extracted text as values.
    """
    resumes = {}

    if uploaded_files:
        # Process uploaded files (Streamlit or similar)
        for file in uploaded_files:
            file_name = file.name
            if file_name.endswith(".pdf"):
                resumes[file_name] = extract_text_from_pdf(file)
            elif file_name.endswith(".docx"):
                resumes[file_name] = extract_text_from_docx(file)

    elif from_directory:
        # Process files from a local directory (CLI)
        if not os.path.exists(resume_dir):
            print(f"⚠️ Directory '{resume_dir}' does not exist.")
            return resumes

        for filename in os.listdir(resume_dir):
            file_path = os.path.join(resume_dir, filename)
            if filename.endswith(".pdf"):
                with open(file_path, "rb") as f:
                    resumes[filename] = extract_text_from_pdf(f)
            elif filename.endswith(".docx"):
                resumes[filename] = extract_text_from_docx(file_path)

    return resumes
