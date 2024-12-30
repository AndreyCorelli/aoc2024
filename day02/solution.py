from typing import List


def read_levels(file_path) -> List[List[int]]:
    levels = []
    with open(file_path, "r") as file:
        for line in file.readlines():
            line = line.strip()
            if not line:
                continue
            levels.append([int(l) for l in line.split()])
    return levels

def check_are_safe(levels: List[List[int]]) -> int:
    safe_levels = 0
    for level in levels:
        first, last = level[0], level[-1]
        is_asc = first < last
        is_safe = True
        for i in range(1, len(level)):
            delta = level[i] - level[i - 1]
            if (is_asc and delta <= 0) or (not is_asc and delta >= 0):
                is_safe = False
                break
            if abs(delta) > 3:
                is_safe = False
                break
        if is_safe:
            safe_levels += 1
    return safe_levels


def are_in_order(level: List[int], skip_index: int) -> bool:
    first, last = level[0], level[-1]
    if skip_index == 0:
        first = level[1]
    if skip_index == len(level) - 1:
        last = level[-2]
    if first == last:
        return False
    is_asc = first < last
    for i in range(1, len(level)):
        if i == skip_index:
            continue
        delta = level[i] - level[i - 1] if i - 1 != skip_index else level[i] - level[i - 2] if i - 2 >= 0 else None
        if delta is None:
            continue
        if (is_asc and delta <= 0) or (not is_asc and delta >= 0):
            return False
        if abs(delta) > 3:
            return False
    return True


def check_are_almost_safe(levels: List[List[int]]) -> int:
    safe_levels = 0
    for level in levels:
        for i in range(len(level)):
            if are_in_order(level, i):
                safe_levels += 1
                break
    return safe_levels


def test_levels():
    path = "/Users/andreisitaev/sources/sennder/aoc2024/day02/input.txt"
    levels = [
      # [1, 2, 3, 4],
      # [5, 2, 0],
      # [8, 1, 2, 3],
      # [1, 2, 3, 3, 5],
      # [1, 2, 3, 3, 3, 5],
      # [5, 1, 6, 8],
      [73, 75, 78, 81, 80]
    ]
    levels = read_levels(path)
    print(check_are_almost_safe(levels))


if __name__ == "__main__":
    test_levels()
