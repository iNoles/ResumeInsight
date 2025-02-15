from resume_loader import load_resumes
from resume_ranker import rank_resumes

def main():
    print("\n📄 ResumeInsight - AI Resume Screener")
    
    # Get job description from user
    job_description = input("\nEnter the job description: ")
    
    # Load resumes
    resumes = load_resumes()
    if not resumes:
        print("No resumes found in the 'resumes' folder.")
        return
    
    # Rank resumes
    ranked_resumes = rank_resumes(job_description, resumes)
    
    print("\n🔹 Resume Ranking Results:")
    for rank, (name, score) in enumerate(ranked_resumes, 1):
        print(f"{rank}. {name} - Score: {score:.4f}")

if __name__ == "__main__":
    main()
