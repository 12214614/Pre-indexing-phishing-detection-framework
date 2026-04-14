import requests
import warnings
from loader import load_prototypes
from service import predict
from config import HEADERS

warnings.filterwarnings("ignore")

# Load prototypes only once
legit_store, phish_store = load_prototypes()


def stage3_decision(url: str) -> dict:
    """
    Stage-3 NCD similarity classifier
    1 = PHISHING
    0 = LEGITIMATE
    """

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15,
            verify=False
        )
        response.raise_for_status()
        html = response.text

        decision_label, ph_score, lg_score = predict(
            html,
            legit_store,
            phish_store
        )

        decision = 1 if decision_label == "PHISHING" else 0

        return {
            "stage": 3,
            "url": url,
            "decision": decision,
            "label": decision_label,
            "phish_score": round(ph_score, 4),
            "legit_score": round(lg_score, 4)
        }

    except Exception as e:
        return {
            "stage": 3,
            "url": url,
            "error": str(e)
        }