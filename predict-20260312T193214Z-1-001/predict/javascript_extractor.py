from bs4 import BeautifulSoup
import re


def normalize_js(js: str) -> str:
    js = js.lower()
    js = re.sub(r"//.*?$|/\*.*?\*/", "", js, flags=re.S)
    js = re.sub(r"\s+", " ", js)
    js = re.sub(r"[a-zA-Z_]\w*", "VAR", js)
    return js


def extract_js(html: str) -> bytes:
    soup = BeautifulSoup(html, "lxml")
    scripts = []

    for s in soup.find_all("script"):
        if s.string:
            scripts.append(normalize_js(s.string))

    return "\n".join(scripts).encode("utf-8")