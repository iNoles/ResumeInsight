# ResumeInsight

ResumeInsight is a console-based and web-based AI resume screening tool that ranks resumes based on their relevance to a given job description. Using NLP, TF-IDF, and cosine similarity, this tool helps recruiters and hiring managers quickly identify the most relevant candidates.

## Features

- Parses resumes in PDF and DOCX formats
- Two Modes: Console & Web UI – Use via the terminal or a browser-based interface with Streamlit
- Extracts key information like skills, experience, and education
- Uses NLP to rank candidates based on job descriptions
- Provides insights into resume relevance
- Performance Optimization with Watchdog – Monitors file changes for efficient reloading
- Downloadable CSV Reports – Export ranked results for easy review

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

### Run the Console Version
```bash
python main.py
```

### Run the Web App
```bash
streamlit run app.py
```

## Dependencies

- python-docx (for parsing DOCX files)
- pdfminer.six (for extracting text from PDFs)
- spacy (for NLP processing)
- numpy & pandas (for data handling)
- Streamlit – For interactive web-based UI
- Watchdog – For performance optimization and real-time file monitoring

## Contributing

1. Fork the repository
2. Create a new branch (```feature-branch```)
3. Commit your changes
4. Push to your fork
5. Submit a pull request
