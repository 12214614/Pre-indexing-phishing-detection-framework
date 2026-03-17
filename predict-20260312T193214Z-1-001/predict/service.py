from html_cleaner import clean_html
from javascript_extractor import extract_js
from classifier import classify


def predict(html, legit_store, phish_store):
    html_b = clean_html(html)
    js_b = extract_js(html)
    return classify(html_b, js_b, legit_store, phish_store)