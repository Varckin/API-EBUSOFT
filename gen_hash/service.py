from typing import List
import hashlib
from gen_hash.settings import CONFIG


def compute_hashes(data: bytes, algorithms: List[str]) -> dict:
    """
    Generate hashes for the given data (bytes) using the specified list of algorithms.
    """
    hashes = {}
    for algo in algorithms:
        algo_lower = algo.lower()
        if algo_lower not in CONFIG.supported_algorithms:
            raise ValueError(f"Unsupported algorithm: {algo}")
        hasher = hashlib.new(algo_lower)
        hasher.update(data)
        hashes[algo_lower] = hasher.hexdigest()
    return hashes
