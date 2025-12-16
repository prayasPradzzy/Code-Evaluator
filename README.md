# 🔍 Parallel Code Evaluator with LangGraph & Google Gemini

A Streamlit application that evaluates C++ code snippets using AI. It leverages **LangGraph** to orchestrate a workflow of multiple evaluator agents (Time Complexity, Space Complexity, and Readability) powered by **Google Gemini** (Free Tier).

## 🚀 Features

- **Multi-Perspective Evaluation**: Analyzes code from three distinct angles:
  - ⏱️ **Time Complexity**: Big O analysis and performance feedback.
  - 💾 **Space Complexity**: Memory usage analysis.
  - 📖 **Readability**: Code structure, naming conventions, and clarity.
- **AI-Powered**: Uses Google's `gemini-2.5-flash` model for high-quality, fast analysis.
- **LangGraph Workflow**: Orchestrates the evaluation steps in a structured graph.
- **Clean UI**: Minimalist interface built with Streamlit.
- **Aggregated Scoring**: Computes a final average score based on individual metrics.

## 🛠️ Tech Stack

- **Python**: Core programming language.
- **Streamlit**: Web interface.
- **LangGraph**: State-based orchestration for the AI workflow.
- **Google Generative AI SDK**: Connection to Gemini models.
- **Python-Dotenv**: Environment variable management.

## 📋 Prerequisites

- Python 3.9 or higher
- A Google Cloud Project with the **Gemini API** enabled.
- A valid **Google API Key**. [Get one here](https://aistudio.google.com/app/apikey).

## 🔧 Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Mac/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add your API key:
   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

## ▶️ Usage

1. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser:**
   The app usually runs at `http://localhost:8501`.

3. **Evaluate Code:**
   - Paste your C++ code snippet into the text area.
   - Click **"🚀 Evaluate Code"**.
   - View detailed feedback and scores for each category.

## 📂 Project Structure

```
├── app.py               # Main application logic (Streamlit UI + LangGraph)
├── requirements.txt     # Python dependencies
├── .env                 # API keys (not committed to git)
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open-source and available under the MIT License.
