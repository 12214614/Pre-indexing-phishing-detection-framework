from datetime import datetime
from urllib.parse import urlsplit, urlunsplit, urlparse, unquote
import re
import math
import socket
import whois
import requests
import ipaddress
from collections import Counter
from bs4 import BeautifulSoup

# -----------------------------
# Configuration Flags
# -----------------------------
ENABLE_DNS   = True
ENABLE_WHOIS = True
ENABLE_HTML  = True


# -----------------------------
# Normalization
# -----------------------------
def normalize_url(raw_url: str) -> str:
    url = str(raw_url).strip()

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parts = urlsplit(url)

    hostname = (parts.hostname or "").lower().rstrip(".")

    if hostname.startswith("www."):
        hostname = hostname[4:]

    path = re.sub(r"/{2,}", "/", parts.path or "/")

    return urlunsplit((parts.scheme, hostname, path, parts.query, ""))

# -----------------------------
# Utility Functions
# -----------------------------
def is_ip_address(domain: str) -> int:
    try:
        ipaddress.ip_address(domain)
        return 1
    except:
        return 0


def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    freq = Counter(s)
    length = len(s)
    return -sum((c / length) * math.log2(c / length) for c in freq.values())


def tokenize_url(url: str):
    return re.split(r"[./\-_=?:&]", url.lower())


def split_domain(domain: str):
    parts = domain.split(".")
    if parts and parts[0] in {"www", "m", "web"}:
        parts = parts[1:]
    return parts


def get_registered_domain(domain: str):
    parts = split_domain(domain)
    return ".".join(parts[-2:]) if len(parts) >= 2 else domain


# -----------------------------
# Keyword Sets
# -----------------------------
SUSPICIOUS_TOKENS = {
    "login", "secure", "verify", "account", "update",
    "bank", "signin", "confirm", "password"
}

BRAND_KEYWORDS = {
    "google", "facebook", "amazon", "paypal",
    "apple", "microsoft", "flipkart", "netflix",
    "instagram", "youtube"
}

DOCUMENT_TOKENS = {
    "doc", "document", "article", "paper", "abstract"
}


# -----------------------------
# Structural Domain Features
# -----------------------------
def semantic_subdomain_features(domain: str) -> dict:
    parts = split_domain(domain)
    depth = max(len(parts) - 2, 0)

    return {
        "semantic_subdomain_depth": depth,
        "has_deep_subdomain": int(depth >= 2)
    }


def brand_position_features(domain: str) -> dict:
    parts = split_domain(domain)
    registered = ".".join(parts[-2:]) if len(parts) >= 2 else domain

    brand_in_registered = 0
    brand_in_subdomain = 0

    for b in BRAND_KEYWORDS:
        if b in registered:
            brand_in_registered = 1
        elif b in domain and not domain.endswith(registered):
            brand_in_subdomain = 1

    return {
        "brand_in_registered_domain": brand_in_registered,
        "brand_in_subdomain": brand_in_subdomain,
        "brand_mismatch": int(brand_in_subdomain and not brand_in_registered)
    }


# -----------------------------
# Layer 1: Lexical + Structural
# -----------------------------
def extract_layer1_features(url: str) -> dict:
    parsed = urlparse(url)
    domain = parsed.hostname or ""
    path = parsed.path or ""
    decoded = unquote(url)

    digit_count = sum(c.isdigit() for c in decoded)
    special_chars = re.findall(r"[^\w/.:?=&%-]", decoded)

    parts = split_domain(domain)

    return {
        "url_length": len(decoded),
        "domain_length": len(domain),
        "path_length": len(path),
        "path_depth": path.count("/"),

        "digit_ratio": digit_count / max(len(decoded), 1),
        "special_char_ratio": len(special_chars) / max(len(decoded), 1),

        "dot_count": decoded.count("."),
        "hyphen_count": decoded.count("-"),

        "subdomain_count": max(len(parts) - 2, 0),

        "has_ip_address": is_ip_address(domain),
        "has_https": int(parsed.scheme == "https"),
    }


# -----------------------------
# Layer 2: Semantic + Entropy
# -----------------------------
def extract_layer2_features(url: str) -> dict:
    parsed = urlparse(url)
    domain = parsed.hostname or ""
    path = parsed.path or ""

    tokens = [t for t in tokenize_url(url) if t]
    suspicious_count = sum(t in SUSPICIOUS_TOKENS for t in tokens)
    digit_sequences = re.findall(r"\d+", url)

    features = {
        "url_entropy": shannon_entropy(url),
        "domain_entropy": shannon_entropy(domain),

        "token_count": len(tokens),
        "max_token_length": max((len(t) for t in tokens), default=0),
        "suspicious_token_ratio": suspicious_count / max(len(tokens), 1),

        "has_query_params": int(bool(parsed.query)),
        "query_param_count": parsed.query.count("&") + 1 if parsed.query else 0,

        "document_path_present": int(any(t in path.lower() for t in DOCUMENT_TOKENS)),
        "long_digit_sequence": int(any(len(seq) >= 6 for seq in digit_sequences)),
        "path_numeric_ratio": sum(c.isdigit() for c in path) / max(len(path), 1),
    }

    features.update(semantic_subdomain_features(domain))
    features.update(brand_position_features(domain))

    return features


# -----------------------------
# DNS Features
# -----------------------------
def extract_dns_features(domain: str) -> dict:
    features = {
        "dns_query_success": 0,
        "a_record_count": -1,
    }
    try:
        socket.setdefaulttimeout(3)
        records = socket.getaddrinfo(domain, None, socket.AF_INET)
        features["a_record_count"] = len(set(r[4][0] for r in records))
        features["dns_query_success"] = 1
    except:
        pass
    return features


# -----------------------------
# WHOIS Features
# -----------------------------
def extract_whois_features(domain: str) -> dict:
    features = {"domain_age_days": -1}
    try:
        w = whois.whois(domain)
        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]
        if isinstance(creation, datetime):
            age = (datetime.utcnow() - creation).days
            features["domain_age_days"] = min(age, 5000)
    except:
        pass
    return features


# -----------------------------
# HTML Features
# -----------------------------
def fetch_html(url: str):
    try:
        r = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200 and "text/html" in r.headers.get("Content-Type", ""):
            return r.text
    except:
        pass
    return None


def extract_html_features(html: str, base_domain: str) -> dict:
    features = {
        "has_form": 0,
        "password_input_present": 0,
        "external_form_action": 0,
    }

    if not html:
        return features

    soup = BeautifulSoup(html, "html.parser")
    forms = soup.find_all("form")

    if not forms:
        return features

    features["has_form"] = 1

    for form in forms:
        if form.find("input", {"type": "password"}):
            features["password_input_present"] = 1

        action = form.get("action", "")
        if action.startswith("http"):
            action_domain = urlparse(action).hostname or ""
            if action_domain and action_domain not in base_domain:
                features["external_form_action"] = 1

    return features


# -----------------------------
# Final Feature Extractor
# -----------------------------
def extract_all_features(raw_url: str) -> dict:
    url = normalize_url(raw_url)
    domain = urlparse(url).hostname or ""

    features = {}
    features.update(extract_layer1_features(url))
    features.update(extract_layer2_features(url))

    if ENABLE_DNS:
        features.update(extract_dns_features(domain))

    if ENABLE_WHOIS:
        features.update(extract_whois_features(domain))

    if ENABLE_HTML:
        html = fetch_html(url)
        features.update(extract_html_features(html, domain))

    return features
