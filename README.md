# OutreachAI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LLM Workflow](https://img.shields.io/badge/Workflow-AI%20assisted-brightgreen?style=for-the-badge)

OutreachAI is a personalized outreach generator that turns a CSV and a base message into individual email drafts.

It is designed for cases where one message template needs to adapt to many recipients without losing individual context.

[Try the browser demo](https://ymbawa26.github.io/OutreachAI/)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ymbawa26/OutreachAI)

## What It Does

- loads recipient data from a CSV file
- blends each row into a reusable base template
- generates tailored email drafts for each person
- lets the user review drafts before selecting which ones to send
- includes a mock sending flow so the product can be demonstrated safely

## How To Try It

### Option 1: Run locally

```bash
git clone https://github.com/ymbawa26/OutreachAI.git
cd OutreachAI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501`.

### Option 2: Run in Codespaces

1. Click the Codespaces badge above.
2. Wait for the workspace to open.
3. Install the dependencies with `pip install -r requirements.txt`.
4. Start the app with `streamlit run app.py`.
5. Open the forwarded Streamlit port.

### Option 3: Use the browser demo

If you just want to understand the product quickly from another computer, use the public browser demo above.

The hosted demo is intentionally client-side and uses the same mock generation logic as the local Python version. It is meant for product exploration, not real SMTP sending.

## Included Demo Data

The repo includes `sample_students.csv`, which gives the app a ready-to-use dataset for testing the personalization flow.

## How The AI Layer Works

The current repo uses a mock generation engine in [`ai_engine.py`](./ai_engine.py) so the end-to-end workflow can be tested without requiring a paid LLM API key.

That means the product architecture is real, while the generation backend is intentionally lightweight and easy to swap.

## Tech Stack

- Python
- Streamlit
- CSV-based input workflow
- Mock AI generation layer for safe local demos

## Repo Layout

- `app.py` Streamlit UI and app flow
- `ai_engine.py` draft generation logic
- `sample_students.csv` demo dataset
- `test_email.py` mock email testing helper
- `requirements.txt` Python dependencies

## Status

This is a working demoable prototype.

It now has a lightweight public browser demo for quick evaluation, while the full Streamlit flow is still available locally and in Codespaces.
