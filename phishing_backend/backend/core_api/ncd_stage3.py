"""
NCD Stage 3 — DOM structure + JavaScript similarity-based phishing detection.

Uses pre-built phishing/legitimate prototype sets (models/phish.pkl, models/legit.pkl)
from the predict folder. No external module dependencies — all NCD logic is inlined here.
"""

import os
import re
import lzma
import pickle
import glob
import warnings
import requests
from functools import lru_cache
from bs4 import BeautifulSoup, Comment

warnings.filterwarnings("ignore")

# -----------------------------------------------------------------------
# Paths — prototypes in predict-*/predict/models (auto-discovered)
# -----------------------------------------------------------------------
def _find_predict_models_dir() -> str:
    workspace_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )
    candidates = glob.glob(os.path.join(workspace_root, "predict-*", "predict", "models"))
    if candidates:
        candidates.sort(key=os.path.getmtime, reverse=True)
        return candidates[0]

    # Fallback to backend/ml/models if future project layout changes.
    return os.path.join(workspace_root, "ml", "models")


_PREDICT_MODELS_DIR = _find_predict_models_dir()

# -----------------------------------------------------------------------
# NCD core (LZMA-based)
# -----------------------------------------------------------------------

@lru_cache(maxsize=4096)
def _compressed_size(data: bytes) -> int:
    return len(lzma.compress(data))


def _ncd(x: bytes, y: bytes) -> float:
    if not x or not y:
        return 1.0
    cx  = _compressed_size(x)
    cy  = _compressed_size(y)
    cxy = _compressed_size(x + y)
    return (cxy - min(cx, cy)) / max(cx, cy)


# -----------------------------------------------------------------------
# HTML structural fingerprint (strip text/attrs, keep tag skeleton)
# -----------------------------------------------------------------------

def _clean_html(html: str) -> bytes:
    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        soup = BeautifulSoup(html, "html.parser")

    # remove HTML comments
    for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()

    # strip all attributes and visible text — keep only tag structure
    for tag in soup.find_all(True):
        tag.attrs = {}
    for t in soup.find_all(string=True):
        if t.strip():
            t.replace_with("")

    return soup.prettify().encode("utf-8")


# -----------------------------------------------------------------------
# JS extraction + normalization (variable names → VAR)
# -----------------------------------------------------------------------

def _extract_js(html: str) -> bytes:
    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        soup = BeautifulSoup(html, "html.parser")

    scripts = []
    for s in soup.find_all("script"):
        if s.string:
            js = s.string.lower()
            js = re.sub(r"//.*?$|/\*.*?\*/", "", js, flags=re.S)
            js = re.sub(r"\s+", " ", js)
            js = re.sub(r"[a-zA-Z_]\w*", "VAR", js)
            scripts.append(js)

    return "\n".join(scripts).encode("utf-8")


# -----------------------------------------------------------------------
# Similarity scoring
# -----------------------------------------------------------------------

_HTML_WEIGHT = 0.6
_JS_WEIGHT   = 0.4
_TOP_K       = 5


def _top_k_ncd(sample: bytes, prototypes: list, k: int) -> list:
    dists = sorted(_ncd(sample, p) for p in prototypes)
    return dists[:k]


def _weighted_score(dists: list) -> float:
    if not dists:
        return 1.0
    weights = [1 / (i + 1) for i in range(len(dists))]
    return sum(w * d for w, d in zip(weights, dists)) / sum(weights)


# -----------------------------------------------------------------------
# Prototype store (loaded once at first use)
# -----------------------------------------------------------------------

_phish_prototypes = None   # (html_protos, js_protos)
_legit_prototypes = None


def _load_prototypes():
    global _phish_prototypes, _legit_prototypes
    if _phish_prototypes is not None:
        return  # already loaded

    phish_path = os.path.join(_PREDICT_MODELS_DIR, "phish.pkl")
    legit_path  = os.path.join(_PREDICT_MODELS_DIR, "legit.pkl")

    with open(phish_path, "rb") as f:
        ph_html, ph_js = pickle.load(f)

    with open(legit_path, "rb") as f:
        lg_html, lg_js = pickle.load(f)

    _phish_prototypes = (ph_html, ph_js)
    _legit_prototypes  = (lg_html, lg_js)


# -----------------------------------------------------------------------
# NCD classifier
# -----------------------------------------------------------------------

def _classify_ncd(html_b: bytes, js_b: bytes) -> tuple:
    ph_html, ph_js = _phish_prototypes
    lg_html, lg_js = _legit_prototypes

    ph_score = (
        _HTML_WEIGHT * _weighted_score(_top_k_ncd(html_b, ph_html, _TOP_K))
        + _JS_WEIGHT * _weighted_score(_top_k_ncd(js_b,   ph_js,   _TOP_K))
    )
    lg_score = (
        _HTML_WEIGHT * _weighted_score(_top_k_ncd(html_b, lg_html, _TOP_K))
        + _JS_WEIGHT * _weighted_score(_top_k_ncd(js_b,   lg_js,   _TOP_K))
    )

    # Lower NCD score = more structurally similar = same class
    label = "phishing" if ph_score < lg_score else "legitimate"
    return label, round(ph_score, 4), round(lg_score, 4)


# -----------------------------------------------------------------------
# Public API
# -----------------------------------------------------------------------

_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
_TIMEOUT = 10


def run_ncd_stage3(url: str) -> dict:
    """
    Fetch the URL's HTML, run NCD Stage-3 classification.

    Returns:
        {
            "ncd_available": True,
            "ncd_prediction": "phishing" | "legitimate",
            "ncd_phish_score": float,   # lower = more similar to phishing
            "ncd_legit_score": float,   # lower = more similar to legitimate
        }

    On any failure:
        {"ncd_available": False, "ncd_prediction": None, "ncd_error": "..."}
    """
    try:
        _load_prototypes()

        resp = requests.get(url, headers=_HEADERS, timeout=_TIMEOUT, verify=False)
        html = resp.text

        html_b = _clean_html(html)
        js_b   = _extract_js(html)

        label, ph_score, lg_score = _classify_ncd(html_b, js_b)

        # Only trust NCD when there is a clear structural gap between classes.
        # If both scores are near 1.0 and close together, the page structure
        # doesn't resemble any prototype well — result is inconclusive.
        score_gap = abs(ph_score - lg_score)
        ncd_confident = score_gap >= 0.05

        return {
            "ncd_available":   True,
            "ncd_confident":   ncd_confident,
            "ncd_prediction":  label if ncd_confident else None,
            "ncd_phish_score": ph_score,
            "ncd_legit_score": lg_score,
            "ncd_score_gap":   round(score_gap, 4),
        }

    except Exception as e:
        return {
            "ncd_available":  False,
            "ncd_prediction": None,
            "ncd_error":      str(e),
        }
