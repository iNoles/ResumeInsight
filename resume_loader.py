import os
import PyPDF2
import docx

# Path to the resumes folder
RESUME_DIR = "resumes"

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

def load_resumes():
    """Load and extract text from all resumes in the 'resumes' folder."""
    resumes = {}
    
    for filename in os.listdir(RESUME_DIR):
        file_path = os.path.join(RESUME_DIR, filename)
        
        if filename.endswith(".pdf"):
            resumes[filename] = extract_text_from_pdf(file_path)
        elif filename.endswith(".docx"):
            resumes[filename] = extract_text_from_docx(file_path)
    
    return resumes

if __name__ == "__main__":
    all_resumes = load_resumes()
    
    for name, content in all_resumes.items():
        print(f"\n===== {name} =====")
        print(content[:500])  # Print first 500 characters for preview
        print("... (truncated)\n")
