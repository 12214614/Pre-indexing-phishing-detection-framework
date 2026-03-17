from bs4 import BeautifulSoup, Comment


def clean_html(html: str) -> bytes:
    soup = BeautifulSoup(html, "lxml")

    for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()

    for tag in soup.find_all(True):
        tag.attrs = {}

    for t in soup.find_all(string=True):
        if t.strip():
            t.replace_with("")

    return soup.prettify().encode("utf-8")