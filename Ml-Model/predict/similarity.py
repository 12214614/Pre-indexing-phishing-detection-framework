from ncd_engine import ncd


def top_k(sample, prototypes, k):
    dists = sorted(ncd(sample, p) for p in prototypes)
    return dists[:k]