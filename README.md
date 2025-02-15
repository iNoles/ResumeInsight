# ResumeInsight

ResumeInsight is an AI-powered resume screening tool that analyzes and ranks resumes based on job descriptions. It utilizes NLP techniques to extract relevant information from resumes and compare them to job requirements.

## Features

- Parses resumes in PDF and DOCX formats
- Extracts key information like skills, experience, and education
- Uses NLP to rank candidates based on job descriptions
- Provides insights into resume relevance

## Installation

1. Clone the repository:
```bash
git clone https://github.com/iNoles/ResumeInsight.git
cd ResumeInsight
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place resumes in the ```resumes/``` directory.

2. Run the script with a job description:
```bash
python resume_insight.py --job "Software Engineer with Python and ML experience"
```
3. View ranked candidates in the output.

## Dependencies

- python-docx (for parsing DOCX files)
- pdfminer.six (for extracting text from PDFs)
- spacy (for NLP processing)
- numpy & pandas (for data handling)

## Contributing

1. Fork the repository
2. Create a new branch (```feature-branch```)
3. Commit your changes
4. Push to your fork
5. Submit a pull request
