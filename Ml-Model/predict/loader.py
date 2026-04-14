import pickle
from store import PrototypeStore


def load_prototypes():
    with open("models/phish.pkl", "rb") as f:
        ph_html, ph_js = pickle.load(f)

    with open("models/legit.pkl", "rb") as f:
        lg_html, lg_js = pickle.load(f)

    return PrototypeStore(ph_html, ph_js), PrototypeStore(lg_html, lg_js)