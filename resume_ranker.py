import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume_loader import load_resumes

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """Cleans and preprocesses text using spaCy."""
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

def rank_resumes(job_description, resumes):
    """Ranks resumes based on similarity to the job description using TF-IDF."""
    processed_resumes = {name: preprocess_text(content) for name, content in resumes.items()}
    
    documents = [preprocess_text(job_description)] + list(processed_resumes.values())
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    job_vector = tfidf_matrix[0]  # Job description vector
    resume_vectors = tfidf_matrix[1:]  # Resume vectors
    
    similarities = cosine_similarity(job_vector, resume_vectors).flatten()
    
    ranked_resumes = sorted(zip(processed_resumes.keys(), similarities), key=lambda x: x[1], reverse=True)
    
    return ranked_resumes

if __name__ == "__main__":
    # Example job description
    job_desc = """Looking for a software engineer with experience in Python, machine learning, and NLP."""
    
    all_resumes = load_resumes()
    ranked_results = rank_resumes(job_desc, all_resumes)
    
    print("\n🔹 Resume Ranking Results:")
    for rank, (name, score) in enumerate(ranked_results, 1):
        print(f"{rank}. {name} - Score: {score:.4f}")
