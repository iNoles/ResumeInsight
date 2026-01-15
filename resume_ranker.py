import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume_loader import load_resumes
from typing import Dict, List, Tuple

# Load English NLP model from spaCy
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text: str) -> str:
    """
    Cleans and preprocesses text using spaCy.

    Steps:
    1. Convert text to lowercase.
    2. Tokenize using spaCy.
    3. Lemmatize words.
    4. Remove stopwords and punctuation.

    Parameters:
        text (str): Input text to preprocess.

    Returns:
        str: Preprocessed and cleaned text.
    """
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

def rank_resumes(job_description: str, resumes: Dict[str, str]) -> List[Tuple[str, float]]:
    """
    Ranks resumes based on similarity to the job description using TF-IDF and cosine similarity.

    Parameters:
        job_description (str): The job description text.
        resumes (dict): Dictionary of resumes with filenames as keys and text content as values.

    Returns:
        list of tuples: Ranked list of tuples (resume_name, similarity_score) in descending order of relevance.
    """
    # Preprocess all resumes
    processed_resumes = {name: preprocess_text(content) for name, content in resumes.items()}

    # Preprocess job description and combine with resumes
    documents = [preprocess_text(job_description)] + list(processed_resumes.values())

    # Vectorize documents using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Separate job description vector and resume vectors
    job_vector = tfidf_matrix[0]
    resume_vectors = tfidf_matrix[1:]

    # Compute cosine similarity between job description and each resume
    similarities = cosine_similarity(job_vector, resume_vectors).flatten()

    # Rank resumes based on similarity score
    ranked_resumes = sorted(zip(processed_resumes.keys(), similarities), key=lambda x: x[1], reverse=True)

    return ranked_resumes

if __name__ == "__main__":
    # Example usage
    job_desc = """Looking for a software engineer with experience in Python, machine learning, and NLP."""

    # Load resumes from local directory
    all_resumes = load_resumes(from_directory=True)

    # Rank resumes based on job description
    ranked_results = rank_resumes(job_desc, all_resumes)

    # Display ranking results
    print("\n🔹 Resume Ranking Results:")
    for rank, (name, score) in enumerate(ranked_results, 1):
        print(f"{rank}. {name} - Score: {score:.4f}")
