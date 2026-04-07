# ✉️ OutreachAI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Generative AI](https://img.shields.io/badge/Generative_AI-Enabled-brightgreen?style=for-the-badge)

**OutreachAI** is a personalized mass email generator designed to scale one-on-one communication without sacrificing individual context. It bridges the gap between generic bulk emails and time-consuming manual composing.

By leveraging artificial intelligence (Large Language Models), the tool digests tabular data (CSV) detailing recipient-specific context and dynamically injects those contexts into a generic base template, creating highly tailored drafts.

## ✨ Features
- **Scalable Personalization:** Iterates through thousands of rows of data instantaneously.
- **Context Awareness:** Automatically adjusts email tone based on specific student factors (e.g. positive framing for good grades, encouraging framing for poor performance).
- **Interactive UI:** Built using `Streamlit` to provide a seamless, local-hosted web application layout.
- **Selective Sending Checkboxes:** Review the AI-generated drafts in an interactive table, uncheck recipients you wish to exclude, and dispatch the rest.
- **Automated Dispatching Engine:** Mock SMTP integration to batch-send the curated list exactly as reviewed.

## 🚀 Getting Started

### Installation
Clone this repository and set up your python virtual environment:
```bash
git clone https://github.com/ymbawa26/OutreachAI.git
cd OutreachAI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the App
Spin up the local Streamlit server:
```bash
streamlit run app.py
```
*The UI will pop open in your browser automatically at `http://localhost:8501`. A dataset (`sample_students.csv`) is provided in the repository to test out the features!*

## 🤖 The AI Engine (`ai_engine.py`)
Currently, the repo features a **Mock AI Engine** which leverages powerful string manipulation to mimic true LLM behavior. This allows developers to thoroughly test the loop architecture locally for free.

To connect this to a real GenAI backend (OpenAI, Gemini, HuggingFace), replace `mock_ai_generate()` with your respective API call (example structure for OpenAI currently exists but is commented out within the engine file).
