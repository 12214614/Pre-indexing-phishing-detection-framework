from ncd import compressed_size


def ncd(x: bytes, y: bytes) -> float:
    if not x or not y:
        return 1.0

    cx = compressed_size(x)
    cy = compressed_size(y)
    cxy = compressed_size(x + y)

    return (cxy - min(cx, cy)) / max(cx, cy)