from similarity import top_k
from scoring import weighted_score
from config import HTML_WEIGHT, JS_WEIGHT, TOP_K


def classify(html_b, js_b, legit, phish):
    ph = HTML_WEIGHT * weighted_score(top_k(html_b, phish.html, TOP_K)) + \
         JS_WEIGHT * weighted_score(top_k(js_b, phish.js, TOP_K))

    lg = HTML_WEIGHT * weighted_score(top_k(html_b, legit.html, TOP_K)) + \
         JS_WEIGHT * weighted_score(top_k(js_b, legit.js, TOP_K))

    return "PHISHING" if ph < lg else "LEGITIMATE", ph, lg