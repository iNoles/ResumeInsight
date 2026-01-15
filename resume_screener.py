import streamlit as st
import pandas as pd
import re
from io import StringIO
from resume_loader import load_resumes
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Set

# -----------------------------
# Load NLP model with word vectors
# -----------------------------
nlp = spacy.load("en_core_web_md")  # Use medium model with embeddings

st.set_page_config(page_title="ResumeInsight - AI Resume Screener", layout="wide")
st.title("📄 ResumeInsight - AI Resume Screener")
st.write("Upload resumes and enter a job description to rank candidates semantically.")

# Sidebar job description input
with st.sidebar:
    st.header("📝 Job Description")
    job_description = st.text_area("Enter the job description:", height=200)

# File uploader
uploaded_files = st.file_uploader("📂 Upload resumes (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

# -----------------------------
# Keyword extraction functions
# -----------------------------
def extract_keywords(text: str) -> Set[str]:
    """Extract relevant keywords from job description."""
    common_words = {"and","or","the","of","a","to","for","with","in","on","by","an","at","as","this","is",
                    "must","your","have","any","within","such","required","understanding","experience","skills"}
    # Remove personal info
    cleaned_text = re.sub(r"\d{1,5}\s\w+(\s\w+){0,2},\s\w{2,},\s?\w{2,}", "", text)
    cleaned_text = re.sub(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", "", cleaned_text)
    cleaned_text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "", cleaned_text)
    words = re.findall(r"\b[a-zA-Z#.+-]{3,}\b", cleaned_text.lower())
    return {word for word in words if word not in common_words}

def highlight_keywords(text: str, keywords: Set[str]) -> str:
    """Highlight keywords in the resume text."""
    for kw in sorted(keywords, key=len, reverse=True):
        text = re.sub(f"(?i)\\b{re.escape(kw)}\\b", 
                      f'<span style="color:blue; font-weight:bold">{kw}</span>', text)
    return text

# -----------------------------
# Semantic ranking function
# -----------------------------
def rank_resumes_semantic(job_desc: str, resumes: dict) -> List[tuple]:
    """
    Rank resumes using spaCy embeddings (semantic similarity).
    """
    job_vec = nlp(job_desc).vector.reshape(1, -1)
    scores = []
    for name, content in resumes.items():
        resume_vec = nlp(content).vector.reshape(1, -1)
        sim = cosine_similarity(job_vec, resume_vec)[0][0]
        scores.append((name, sim))
    # Sort descending
    return sorted(scores, key=lambda x: x[1], reverse=True)

# -----------------------------
# Experience section extraction
# -----------------------------
def extract_experience(text: str) -> str:
    """Extract text under common experience section headings."""
    patterns = [r"(experience|work history|professional background)(:|\n)", r"(projects)(:|\n)"]
    for pat in patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            start = match.end()
            snippet = text[start:start+500]  # Grab next 500 chars
            return snippet.replace("\n", " ")
    # fallback: first 100 words
    return " ".join(text.split()[:100])

# -----------------------------
# Main Processing
# -----------------------------
if uploaded_files and job_description:
    st.write("🔍 **Processing Resumes...**")
    resumes = load_resumes(uploaded_files=uploaded_files)
    ranked = rank_resumes_semantic(job_description, resumes)
    job_keywords = extract_keywords(job_description)
    
    # Display top results
    st.subheader("🔹 Resume Ranking Results")
    df = pd.DataFrame(ranked, columns=["Resume Name", "Score"])
    st.dataframe(df.style.format({"Score": "{:.4f}"}))
    
    # Top N resumes summary
    top_n = min(3, len(ranked))
    st.subheader(f"🏆 Summary of Top {top_n} Resume{'s' if top_n>1 else ''}")
    for i, (name, score) in enumerate(ranked[:top_n],1):
        resume_text = resumes[name]
        exp_summary = extract_experience(resume_text)
        highlighted_text = highlight_keywords(exp_summary, job_keywords)
        st.markdown(f"### {i}. {name} - Score: `{score:.4f}`")
        st.markdown(f"📜 **Experience Summary:** {highlighted_text}", unsafe_allow_html=True)
        st.write("🔍 Highlighted Keywords:", ", ".join(job_keywords.intersection(set(resume_text.lower().split()))))
    
    # Download CSV
    csv_buf = StringIO()
    df.to_csv(csv_buf, index=False)
    st.download_button("Download CSV", csv_buf.getvalue(), "semantic_resume_ranking.csv", "text/csv")
