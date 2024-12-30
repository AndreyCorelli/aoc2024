from typing import List

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day25/input.txt"


def read_file(file_path: str, locks: List[List[int]], keys: List[List[int]]) -> None:
    lines = open(file_path).read().strip().split("\n")

    for start in range(0, len(lines) - 1, 8):
        block = [list(l) for l in lines[start:start + 7]]
        is_lock = block[0][0] == "#"

        if not is_lock:
            block.reverse()

        lst: List[int] = []
        for x in range(len(block[0])):
            count = 0
            for row in range(1, len(block)):
                if block[row][x] == "#":
                    count += 1
            lst.append(count)

        if is_lock:
            locks.append(lst)
        else:
            keys.append(lst)


def is_match(lock: List[int], key: List[int]) -> bool:
    for i in range(len(lock)):
        if lock[i] + key[i] > 5:
            return False
    return True


def solve():
    locks, keys = [], []
    read_file(FILE_PATH, locks, keys)

    count_matched = 0

    for lock in locks:
        for key in keys:
            if is_match(lock, key):
                count_matched += 1

    print(count_matched)


if __name__ == "__main__":
    solve()
