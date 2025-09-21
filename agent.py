import os
import requests
import json
from extractor import fetch_url_text
from db import save_report
import google.generativeai as genai

SERPAPI_KEY = os.getenv('SERPAPI_API_KEY')
GEMINI_KEY = os.getenv('GOOGLE_API_KEY')

if not GEMINI_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set in environment")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def search_serpapi(query, num_results=3):
    if not SERPAPI_KEY:
        raise RuntimeError('SERPAPI_API_KEY not set')
    params = {
        'q': query,
        'engine': 'google',
        'api_key': SERPAPI_KEY,
        'num': num_results
    }
    resp = requests.get('https://serpapi.com/search', params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    results = []
    for r in data.get('organic_results', [])[:num_results]:
        link = r.get('link') or r.get('url')
        title = r.get('title')
        snippet = r.get('snippet')
        if link:
            results.append({'url': link, 'title': title, 'snippet': snippet})
    return results


def summarize_text_with_gemini(query, sources_texts):
    system = (
        "You are an assistant that reads multiple documents and produces a short "
        "structured report: title, 3-6 key points, summary, and links to sources. Keep it concise."
    )
    combined = '\n\n'.join([f"SOURCE {i+1}:\n{t[:4000]}" for i, t in enumerate(sources_texts)])
    user_prompt = (
        f"{system}\n\nQuery: {query}\n\n{combined}\n\n"
        "Format the output as JSON with fields: title, key_points (list), summary, sources (list)."
    )

    response = model.generate_content(user_prompt)
    text = response.text.strip()

    # Remove Markdown ```json wrapper if present
    if text.startswith("```json"):
        text = text[len("```json"):].rstrip("```").strip()

    try:
        parsed = json.loads(text)
        return parsed
    except Exception:
        # fallback if model output isn't valid JSON
        return {"title": query, "key_points": [], "summary": text, "sources": []}

def run_query(query):
    texts = []
    sources = []

    # Check if the query is a URL (PDF or webpage)
    if query.lower().startswith("http"):
        try:
            txt = fetch_url_text(query)
            texts.append(txt)
            sources.append(query)
        except Exception as e:
            texts.append(f"[Could not fetch {query}: {e}]")
            sources.append(query)
    else:
        # Normal search via SerpAPI
        results = search_serpapi(query, num_results=3)
        for r in results:
            url = r['url']
            try:
                txt = fetch_url_text(url)
                texts.append(txt)
                sources.append(url)
            except Exception as e:
                texts.append(f"[Could not fetch {url}: {e}]")
                sources.append(url)

    # Summarize using Gemini
    llm_out = summarize_text_with_gemini(query, texts)

    # Fallback to fetched URLs if model doesn't provide sources
    if not llm_out.get('sources'):
        llm_out['sources'] = sources

    # Clean JSON (no ```json wrappers)
    summary_clean = json.dumps(llm_out, ensure_ascii=False, indent=2)

    # Save in DB
    report_id = save_report(query, summary_clean, json.dumps(sources))
    return report_id
