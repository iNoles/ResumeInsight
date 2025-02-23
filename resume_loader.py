import os
import PyPDF2
import docx

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file."""
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

def load_resumes(uploaded_files=None, from_directory=False, resume_dir="resumes"):
    resumes = {}

    if uploaded_files:
        # Streamlit: Read uploaded files
        for file in uploaded_files:
            file_name = file.name
            file_bytes = file.read()

            if file_name.endswith(".pdf"):
                resumes[file_name] = extract_text_from_pdf(file_bytes)
            elif file_name.endswith(".docx"):
                resumes[file_name] = extract_text_from_docx(file_bytes)

    elif from_directory:
        # CLI: Read from the "resumes/" folder
        for filename in os.listdir(resume_dir):
            file_path = os.path.join(resume_dir, filename)
            if filename.endswith(".pdf"):
                with open(file_path, "rb") as f:
                    resumes[filename] = extract_text_from_pdf(f)
            elif filename.endswith(".docx"):
                resumes[filename] = extract_text_from_docx(file_path)

    return resumes

if __name__ == "__main__":
    all_resumes = load_resumes(from_directory=True)
    
    for name, content in all_resumes.items():
        print(f"\n===== {name} =====")
        print(content[:500])  # Print first 500 characters for preview
        print("... (truncated)\n")
