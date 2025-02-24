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
    """Extracts relevant keywords from job description while filtering out common words and numbers."""
    common_words = {"and", "or", "the", "of", "a", "to", "for", "with", "in", "on", "by", "an", "at", "as", "this", "is",
                    "must", "your", "have", "any", "within", "such", "required", "understanding", "determined", "time",
                    "details", "address", "city", "state", "name", "phone", "email", "skills", "education", "experience", "resume", "years"}

    # Clean and remove personal details like address, phone numbers, emails, etc.
    cleaned_text = re.sub(r"\d{1,5}\s\w+(\s\w+){0,2},\s\w{2,},\s?\w{2,}", "", text)  # Address
    cleaned_text = re.sub(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", "", cleaned_text)  # Phone numbers
    cleaned_text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "", cleaned_text)  # Emails

    # Extract words with 3+ characters
    words = re.findall(r"\b[a-zA-Z#.+-]{3,}\b", cleaned_text.lower())

    # Filter out common words and unwanted terms like "years"
    filtered_keywords = {word for word in words if word not in common_words and not word.isdigit()}
    return filtered_keywords

# Function to highlight only matching keywords in the resume summary
def get_highlighted_keywords(text, keywords):
    """Returns only the highlighted keywords from the resume summary."""
    highlighted_keywords = []
    # Sort keywords by length (longest first) to avoid partial overlaps
    for keyword in sorted(keywords, key=len, reverse=True):  
        match = re.findall(f"(?i)\\b{re.escape(keyword)}\\b", text)
        if match:
            highlighted_keywords.append(keyword)
            # Apply the highlighting format with HTML
            text = re.sub(f"(?i)\\b{re.escape(keyword)}\\b", 
                          rf'<span style="color:blue; font-weight:bold">{keyword}</span>', text)
    return highlighted_keywords

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

    # Ensure ranked_resumes is not empty before selecting top resumes
    if ranked_resumes:
        # Avoid min_value being greater than max_value when there's only one resume
        top_n = 1 if len(ranked_resumes) == 1 else st.slider(
            "📊 Select number of top resumes to summarize:", 
            1, len(ranked_resumes), min(3, len(ranked_resumes))
        )

        # Summary of selected top resumes
        st.subheader(f"🏆 Summary of Top {top_n} Resume{'s' if top_n > 1 else ''}")

        for i, (name, score) in enumerate(ranked_resumes[:top_n], 1):
            resume_text = processed_resumes[name]  # Full resume text
            highlighted_keywords = get_highlighted_keywords(resume_text, job_keywords)
            

            # Extract experience section (first 100 words)
            experience_section = " ".join(resume_text.split()[:100])

            st.markdown(f"### {i}. {name} - Score: `{score:.4f}`")
            st.markdown(f"📜 **Experience Summary:** {experience_section}...")
            # Display highlighted keywords
            st.write("🔍 Highlighted Keywords:", ", ".join(highlighted_keywords))

    # Allow users to download results as CSV
    st.subheader("📥 Download Results")
    csv_buffer = StringIO()
    results_df.to_csv(csv_buffer, index=False)
    st.download_button("Download CSV", data=csv_buffer.getvalue(), file_name="resume_ranking_results.csv", mime="text/csv")
