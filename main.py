from resume_loader import load_resumes
from resume_ranker import rank_resumes

def main():
    print("\n📄 ResumeInsight - AI Resume Screener")
    
    # Get job description from user
    while True:
        job_description = input("\nEnter the job description: ").strip()
        if job_description:
            break
        print("⚠️ Job description cannot be empty. Please enter a valid description.")

    print("\n🔍 Loading resumes...")
    
    # Load resumes from directory
    resumes = load_resumes(from_directory=True)
    
    if not resumes:
        print("❌ No resumes found in the 'resumes' folder. Please add some resumes and try again.")
        return
    
    print(f"✅ Loaded {len(resumes)} resumes successfully!")

    # Rank resumes
    print("\n🔹 Ranking resumes based on relevance...")
    ranked_resumes = rank_resumes(job_description, resumes)

    # Display ranking results
    print("\n📊 Resume Ranking Results:")
    print("=" * 40)
    for rank, (name, score) in enumerate(ranked_resumes, 1):
        print(f"{rank}. {name} - Score: {score:.4f}")
    print("=" * 40)

if __name__ == "__main__":
    main()
