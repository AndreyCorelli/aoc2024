from typing import List

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day22/input.txt"


def read_file() -> List[int]:
    with open(FILE_PATH, "r") as file:
        return [int(line.strip()) for line in file.readlines() if line.strip()]


def hash_number(x: int) -> int:
    y = x * 64
    x = x ^ y
    x = x % 16777216

    y = x // 32
    x = x ^ y
    x = x % 16777216

    y = x * 2048
    x = x ^ y
    x = x % 16777216

    return x


def preprocess_data() -> None:
    nums = read_file()
    out_path = FILE_PATH + ".pre"
    with open(out_path, "w") as file:
        for n in nums:
            for _ in range(2000):
                n = hash_number(n)
                d = str(n)[-1]
                file.write(d)
            file.write("\n")


def solution():
    preprocess_data()
    return
    nums = read_file()
    total = 0
    for n in nums:
        for _ in range(2000):
            n = hash_number(n)
        total += n
    print(total)

if __name__ == "__main__":
    solution()
