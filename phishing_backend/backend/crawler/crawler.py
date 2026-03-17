import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

# Backend API endpoint (your Django API)
BACKEND_API = "http://127.0.0.1:8000/api/add-url/"

# Seed URLs to start crawling
seed_urls = [
    "https://example.com",
    "https://github.com",
    "https://news.ycombinator.com"
]

# Store visited URLs to avoid duplicates
visited = set()


# -----------------------------
# Send URL to Backend API
# -----------------------------
def send_to_backend(url):

    data = {"url": url}

    try:
        response = requests.post(BACKEND_API, json=data)

        print("Submitted:", url)
        print("Response:", response.text)

    except Exception as e:
        print("Backend connection failed:", e)


# -----------------------------
# Extract URLs from webpage
# -----------------------------
def extract_links(url):

    links = []

    try:
        response = requests.get(url, timeout=5)

        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a", href=True):

            new_url = urljoin(url, link["href"])

            # Only keep http/https URLs
            parsed = urlparse(new_url)

            if parsed.scheme in ["http", "https"]:
                links.append(new_url)

    except Exception as e:
        print("Error crawling", url, ":", e)

    return links


# -----------------------------
# Main Crawling Function
# -----------------------------
def crawl(seed_urls):

    queue = list(seed_urls)

    while queue:

        url = queue.pop(0)

        if url in visited:
            continue

        print("\nCrawling:", url)

        visited.add(url)

        # Send URL to backend for ML verification
        send_to_backend(url)

        # Extract new links
        links = extract_links(url)

        for link in links:

            if link not in visited:
                queue.append(link)

        # Delay to avoid server overload
        time.sleep(1)


# -----------------------------
# Run the crawler
# -----------------------------
if __name__ == "__main__":

    print("Starting crawler...\n")

    crawl(seed_urls)