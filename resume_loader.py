import os
import PyPDF2
import docx

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    reader = PyPDF2.PdfReader(file)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()]).strip()

def extract_text_from_docx(file):
    """Extract text from a DOCX file."""
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

def load_resumes(uploaded_files=None, from_directory=False, resume_dir="resumes"):
    resumes = {}

    if uploaded_files:
        # Read uploaded files (Streamlit)
        for file in uploaded_files:
            file_name = file.name
            if file_name.endswith(".pdf"):
                resumes[file_name] = extract_text_from_pdf(file)
            elif file_name.endswith(".docx"):
                resumes[file_name] = extract_text_from_docx(file)

    elif from_directory:
        # Read from local "resumes" directory (CLI)
        for filename in os.listdir(resume_dir):
            file_path = os.path.join(resume_dir, filename)
            if filename.endswith(".pdf"):
                with open(file_path, "rb") as f:
                    resumes[filename] = extract_text_from_pdf(f)
            elif filename.endswith(".docx"):
                resumes[filename] = extract_text_from_docx(file_path)

    return resumes
