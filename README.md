# AI Agent

This project is an **AI-powered research assistant** that can fetch online sources, extract content (HTML/PDF), summarize it, and save structured reports in a database. Users can view past reports through a web interface.

---

## Features

- **Query the AI agent**: Ask about any topic, e.g., "Impact of Mediterranean diet on heart health."
- **Web search**: Uses SerpAPI to find 2–3 relevant sources online.
- **Content extraction**: Extracts text from HTML pages and PDF files using `trafilatura` and `pypdf`.
- **LLM-based summarization**: Uses Google Gemini to generate structured summaries with:
  - Title  
  - Key points (3–6 bullets)  
  - Short summary (2–3 sentences)  
  - List of source URLs
- **Database storage**: Reports are saved in SQLite for later retrieval.
- **Web interface**:  
  - Home page to enter queries  
  - History page to see past reports  
  - Report page to view structured summary  
  - Clear history functionality
- **Error handling**: Gracefully handles blocked pages, fetch errors, and unsupported content types.

---

## Tech Stack

- **Backend**: Python, Flask  
- **LLM**: Google Gemini API  
- **Web search**: SerpAPI  
- **Content extraction**: `trafilatura` for HTML, `pypdf` for PDFs  
- **Database**: SQLite  
- **Frontend**: HTML templates with Jinja2  

---

## Setup & Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/sandalinatekarr/ai-agent.git
    cd ai-agent
    ```

2. **Create and activate a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Mac/Linux
    venv\Scripts\activate     # Windows
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set environment variables**
    ```bash
    export SERPAPI_API_KEY="your_serpapi_key"
    export GOOGLE_API_KEY="your_google_gemini_key"
    ```

5. **Run the app**
    ```bash
    python app.py
    ```

6. **Open in browser**
    ```
    http://127.0.0.1:5050
    ```

---

## Example Queries

- `"Impact of Mediterranean diet on heart health"`  
- `"Latest AI research in education"`  
- `"Benefits of intermittent fasting"`

---

## Demo

**Inline GIF Preview (optional)**:  
![Demo GIF](demo.gif)



## Notes

- Supports both HTML and PDF extraction.  
- If a source cannot be fetched, it is skipped with a warning.  
- History can be cleared from the web interface.  

---

## License

MIT License
