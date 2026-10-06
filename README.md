# YouTube Summarizer

A Streamlit application that summarizes YouTube videos using a Kaggle API endpoint.

## Requirements

- Python 3.10 or later
- Streamlit
- Requests
- python-dotenv

## Installation

```bash
cd /Users/alisaid/PythonProjects/youtubesummarizer
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

Environment Configuration
Create a .env file in the project directory:


Replace the API URL and key with the values provided by your API.

Run the Application

streamlit run app.py

Then open:

http://localhost:8501

Usage
Enter a valid YouTube video URL.
Click Generate Summary.
View the generated summary.
API Response
The API should return JSON similar to:
{
  "success": true,
  "summary": "The summary of the video."
}

Project Files
app.py — Streamlit interface and API request logic.
requirements.txt — Python dependencies.
.env — API configuration.
.gitignore — Files excluded from Git.
Notes
Never commit .env to Git.
Never share your API key.
The API must be running and accessible.