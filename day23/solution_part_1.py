from typing import Tuple, List, Set, Dict

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day23/input.txt"

def read_input() -> List[Tuple[str, str]]:
    """
    content:
    tb-vc
    td-yn
    ...
    """
    with open(FILE_PATH, "r") as file:
        return [tuple(line.strip().split("-")) for line in file.readlines() if line.strip()]


def find_triplets():
    pairs = read_input()
    triplets: Set[Tuple[str, str, str]] = set()
    keys = {k[0] for k in pairs if k[0]}.union({k[1] for k in pairs if k[1]})

    k_affinity: Dict[str, List[str]] = {}

    for i, j in [(0, 1), (1, 0)]:
        for p in pairs:
            if p[i] in k_affinity:
                k_affinity[p[i]].append(p[j])
            else:
                k_affinity[p[i]] = [p[j]]

    t_keys = [tk for tk in keys if tk[0].startswith("t")]
    for k in t_keys:
        affinity = k_affinity[k]
        for i, b in enumerate(affinity):
            for j in range(i+1, len(affinity)):
                c = affinity[j]
                # is c in affinity of b?
                if c in k_affinity[b]:
                    triplet = tuple(sorted([k, b, c]))
                    triplets.add(triplet)

    print(triplets)
    print(len(triplets))


if __name__ == "__main__":
    find_triplets()
