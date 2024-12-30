from distutils.command.build_clib import build_clib
from typing import Tuple, List, Set, Dict

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day23/input.txt"

def read_input() -> List[Tuple[str, str]]:
    with open(FILE_PATH, "r") as file:
        return [tuple(line.strip().split("-")) for line in file.readlines() if line.strip()]


def build_affinity(pairs: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    k_affinity: Dict[str, List[str]] = {}

    for i, j in [(0, 1), (1, 0)]:
        for p in pairs:
            if p[i] in k_affinity:
                k_affinity[p[i]].append(p[j])
            else:
                k_affinity[p[i]] = [p[j]]
    return k_affinity


def clusterize_greedy():
    pairs = read_input()
    keys = {k[0] for k in pairs if k[0]}.union({k[1] for k in pairs if k[1]})
    affinity = build_affinity(pairs)
    clusters: List[Set[str]] = []

    def build_cluster(k: str) -> Set[str]:
        cluster = {k}
        while True:
            new_keys = set()
            # find all values in keys, that are connected to all keys in cluster
            for b in keys:
                should_add = None
                for a in cluster:
                    if b not in affinity[a]:
                        should_add = False
                        break
                    else:
                        should_add = True
                if should_add:
                    new_keys.add(b)
                    break
            if not new_keys:
                break
            cluster.update(new_keys)

        return cluster

    while keys:
        k = keys.pop()
        cluster = build_cluster(k)
        clusters.append(cluster)
        keys = keys.difference(cluster)

    longest = max(clusters, key=len)
    longest_list = sorted(list(longest))
    title = ",".join(longest_list)
    print(title)


if __name__ == "__main__":
    clusterize_greedy()  # co,de,ka,ta.
