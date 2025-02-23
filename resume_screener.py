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

# Function to extract meaningful keywords from job description
def extract_keywords(text):
    """Extracts relevant keywords from job description while filtering out common words."""
    common_words = {"and", "or", "the", "of", "a", "to", "for", "with", "in", "on", "by", "an", "at", "as", "this", "is"}
    words = re.findall(r"\b[a-zA-Z0-9#.+-]+\b", text.lower())  # Extract words and keep programming terms
    filtered_keywords = {word for word in words if word not in common_words}
    return filtered_keywords

# Function to highlight only matching keywords in the resume summary
def highlight_keywords(text, keywords):
    """Highlights only relevant keywords in resume summaries."""
    for keyword in sorted(keywords, key=len, reverse=True):  # Sort to avoid partial overlaps
        text = re.sub(f"(?i)\\b{re.escape(keyword)}\\b", 
                      rf'<span style="color:blue; font-weight:bold">{keyword}</span>', text)
    return text

if uploaded_files and job_description:
    st.write("🔍 **Processing Resumes...**")

    # Load resumes
    processed_resumes = load_resumes(uploaded_files=uploaded_files)  

    # Rank resumes
    ranked_resumes = rank_resumes(job_description, processed_resumes)

    # Extract filtered keywords from job description
    job_keywords = extract_keywords(job_description)
    st.write("🔹 **Filtered Keywords for Matching:**", ", ".join(sorted(job_keywords)))

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
        summary_text = processed_resumes[name][:500]  # Limit summary length
        highlighted_text = highlight_keywords(summary_text, job_keywords)
        
        st.markdown(f"**{i}. {name}** - Score: `{score:.4f}`", unsafe_allow_html=True)
        st.markdown(f"📜 **Key Details:** {highlighted_text}...", unsafe_allow_html=True)

    # Allow users to download results as CSV
    st.subheader("📥 Download Results")
    csv_buffer = StringIO()
    results_df.to_csv(csv_buffer, index=False)
    st.download_button("Download CSV", data=csv_buffer.getvalue(), file_name="resume_ranking_results.csv", mime="text/csv")
