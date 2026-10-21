import random
from .base import run_attack


def random_failure(G, seed=42):
    rng = random.Random(seed)

    def pick_random(H):
        return rng.choice(list(H.nodes))

    return run_attack(G, pick_random)