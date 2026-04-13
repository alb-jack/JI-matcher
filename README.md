# ResuMatch

An AI-powered web application that analyzes job descriptions against a candidate's resume 
and provides honest hiring feedback.

## What it does
- Upload your resume as a PDF
- Paste any job description
- Get an AI-generated analysis including interview likelihood, resume strengths and gaps, 
  and an optional cover letter
- Session history lets you compare multiple roles side by side

## Tech Stack
- Python, Flask, Javascript, HTML, CSS, Bootstrap 5
- Anthropic Claude API
- PyMuPDF (PDF parsing)

## Setup
1. Clone the repo
2. Create a virtual environment and install dependencies: `pip install -r requirements.txt`
3. Add your Anthropic API key to a `.env` file: `ANTHROPIC_API_KEY=your_key_here`
4. Run: `python3 app.py`
5. Visit `http://127.0.0.1:5001`
