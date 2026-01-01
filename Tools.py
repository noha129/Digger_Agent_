# tools.py
import json, requests
from io import BytesIO
from bs4 import BeautifulSoup
import PyPDF2, docx
from langchain_core.tools import tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import YouTubeSearchTool






# -------------------------
ddg = DuckDuckGoSearchAPIWrapper()

@tool
def duckduckgo_search(query: str) -> str:
    """Search DuckDuckGo and return formatted results."""
    results = ddg.results(query, max_results=5)
    return json.dumps(
        [
            {
                "title": r.get("title", ""),
                "url": r.get("link", ""),
                "snippet": r.get("snippet", "")
            }
            for r in results
        ],
        indent=2
    )

@tool
def youtube_search_tool(query: str) -> str:
    """Search YouTube and return results."""
    yt = YouTubeSearchTool()
    return yt.run(query)

@tool
def fetch_url(url: str) -> str:
    """Fetch readable text from a webpage."""
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    return text[:5000]

@tool
def extract_pdf_text(path: str) -> str:
    """Extract text from PDF (local or URL)."""
    pdf = BytesIO(requests.get(path).content) if path.startswith("http") else open(path, "rb")
    reader = PyPDF2.PdfReader(pdf)
    pages = [p.extract_text() for p in reader.pages if p.extract_text()]
    return "\n\n".join(pages)[:15000]

@tool
def extract_docx_text(path: str) -> str:
    """Extract text from DOCX (local or URL)."""
    doc_file = BytesIO(requests.get(path).content) if path.startswith("http") else path
    doc = docx.Document(doc_file)
    return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())[:15000]

TOOLS = [
    duckduckgo_search,
    youtube_search_tool,
    fetch_url,
    extract_pdf_text,
    extract_docx_text,
]
