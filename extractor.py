import requests
import trafilatura
from urllib.parse import urlparse
from io import BytesIO
from pypdf import PdfReader
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'ai-agent/1.0 (+https://example.com)'}

def fetch_url_text(url, timeout=15):
    parsed = urlparse(url)
    # PDF handling
    if parsed.path.lower().endswith('.pdf'):
        try:
            r = requests.get(url, headers=HEADERS, timeout=timeout)
            r.raise_for_status()
            reader = PdfReader(BytesIO(r.content))
            text = [p.extract_text() or '' for p in reader.pages]
            return '\n'.join(text)
        except Exception as e:
            raise RuntimeError(f'Failed to fetch or parse PDF: {e}')
    # HTML handling
    try:
        downloaded = trafilatura.fetch_url(url)
        extracted = trafilatura.extract(downloaded)
        if extracted:
            return extracted
    except Exception:
        pass  # fallback to BeautifulSoup

    # Fallback using BeautifulSoup
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for t in soup(["script", "style", "header", "footer", "nav"]):
            t.extract()
        text = "\n".join([line.strip() for line in soup.get_text().splitlines() if line.strip()])
        if not text:
            raise RuntimeError("No extractable text found")
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to fetch or extract HTML: {e}")
