from resume_loader import load_resumes
from resume_ranker import rank_resumes

def main():
    """
    Main function to run the ResumeInsight AI Resume Screener.

    Workflow:
    1. Prompt the user to enter a job description.
    2. Load resumes from the 'resumes' folder.
    3. Rank resumes based on relevance to the job description.
    4. Display the ranking results.
    """
    print("\n📄 ResumeInsight - AI Resume Screener")
    
    # Prompt user for job description until a non-empty input is provided
    while True:
        job_description = input("\nEnter the job description: ").strip()
        if job_description:
            break
        print("⚠️ Job description cannot be empty. Please enter a valid description.")

    print("\n🔍 Loading resumes...")
    
    # Load resumes from the directory
    resumes = load_resumes(from_directory=True)
    
    # Handle the case where no resumes are found
    if not resumes:
        print("❌ No resumes found in the 'resumes' folder. Please add some resumes and try again.")
        return
    
    print(f"✅ Loaded {len(resumes)} resumes successfully!")

    # Rank resumes based on relevance to the job description
    print("\n🔹 Ranking resumes based on relevance...")
    ranked_resumes = rank_resumes(job_description, resumes)

    # Display ranking results in a readable format
    print("\n📊 Resume Ranking Results:")
    print("=" * 40)
    for rank, (name, score) in enumerate(ranked_resumes, 1):
        print(f"{rank}. {name} - Score: {score:.4f}")
    print("=" * 40)

if __name__ == "__main__":
    main()
