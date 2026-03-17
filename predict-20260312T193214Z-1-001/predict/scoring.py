def weighted_score(dists):
    if not dists:
        return 1.0

    weights = [1 / (i + 1) for i in range(len(dists))]
    return sum(w * d for w, d in zip(weights, dists)) / sum(weights)