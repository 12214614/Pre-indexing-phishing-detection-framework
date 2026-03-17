import lzma
from functools import lru_cache


@lru_cache(maxsize=4096)
def compressed_size(data: bytes) -> int:
    return len(lzma.compress(data))