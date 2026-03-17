from ncd_engine import ncd
from config import NCD_THRESHOLD


def extract_prototypes(samples):
    prototypes = []
    distances = [float("inf")] * len(samples)

    while max(distances) > NCD_THRESHOLD:
        idx = distances.index(max(distances))
        proto = samples[idx]
        prototypes.append(proto)

        for i, s in enumerate(samples):
            d = ncd(s, proto)
            if d < distances[i]:
                distances[i] = d

        distances[idx] = 0.0

    return prototypes