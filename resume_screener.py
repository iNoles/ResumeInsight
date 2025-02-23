import streamlit as st
import pandas as pd
import re
from io import StringIO
from resume_loader import load_resumes
from resume_ranker import rank_resumes

# Streamlit UI
st.set_page_config(page_title="ResumeInsight - AI Resume Screener", layout="wide")

st.title("📄 ResumeInsight - AI Resume Screener")
st.write("Upload resumes and enter a job description to rank candidates based on relevance.")

# Sidebar for job description input
with st.sidebar:
    st.header("📝 Job Description")
    job_description = st.text_area("Enter the job description:", height=200)

# File uploader for resumes
uploaded_files = st.file_uploader("📂 Upload resumes (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

# Function to extract only relevant keywords (excluding common words)
def extract_relevant_keywords(job_description):
    """Extracts relevant technical skills and terms from the job description."""
    common_words = {
        "and", "or", "the", "to", "of", "in", "with", "for", "a", "your", "must", "have", 
        "years", "experience", "as", "on", "by", "at", "an", "is", "that", "this", "are"
    }  # Expand this list if needed
    words = set(job_description.lower().split())
    return {word for word in words if word not in common_words and len(word) > 2}

# Function to highlight keywords in text
def highlight_keywords(text, keywords):
    """Highlights matching keywords in text using blue color."""
    for keyword in sorted(keywords, key=len, reverse=True):  # Sort to avoid substring conflicts
        text = re.sub(f"(?i)\\b{re.escape(keyword)}\\b", r'<span style="color:blue; font-weight:bold">\g<0></span>', text)
    return text

if uploaded_files and job_description:
    st.write("🔍 **Processing Resumes...**")

    # Extract relevant keywords from job description
    job_keywords = extract_relevant_keywords(job_description)
    st.write("🔹 **Filtered Keywords for Matching:**", ", ".join(job_keywords))  # Debugging output

    # Load and process resumes
    processed_resumes = load_resumes(uploaded_files=uploaded_files)

    # Rank resumes based on job description
    ranked_resumes = rank_resumes(job_description, processed_resumes)

    # Convert results to DataFrame
    results_df = pd.DataFrame(ranked_resumes, columns=["Resume Name", "Score"])

    # Display ranking results
    st.subheader("🔹 Resume Ranking Results")
    st.dataframe(results_df.style.format({"Score": "{:.4f}"}))

    # User selects number of top resumes to display
    top_n = st.slider("📊 Select number of top resumes to summarize:", 1, len(ranked_resumes), 3)

    # Summary of selected top resumes with highlighted keywords
    st.subheader(f"🏆 Summary of Top {top_n} Resumes")
    for i, (name, score) in enumerate(ranked_resumes[:top_n], 1):
        highlighted_text = highlight_keywords(processed_resumes[name][:500], job_keywords)
        st.markdown(f"**{i}. {name}** - Score: `{score:.4f}`", unsafe_allow_html=True)
        st.markdown(f"📜 **Key Details:** {highlighted_text}...", unsafe_allow_html=True)

    # Allow users to download results as CSV
    st.subheader("📥 Download Results")
    csv_buffer = StringIO()
    results_df.to_csv(csv_buffer, index=False)
    st.download_button("Download CSV", data=csv_buffer.getvalue(), file_name="resume_ranking_results.csv", mime="text/csv")
