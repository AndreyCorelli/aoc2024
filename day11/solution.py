from typing import List, Set, Tuple, Dict, Iterator

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day11/input.txt"


class StoneLine:
    def __init__(self, file_path: str) -> None:
        self.stones = self._read_input(file_path)

    @classmethod
    def _read_input(cls, file_path: str) -> List[int]:
        with open(file_path, "r") as f:
            line = f.read().strip()

        return [int(x) for x in line.split(" ")]

    def blink(self) -> None:
        resulted: List[int] = []
        for stone in self.stones:
            if stone == 0:
                resulted.append(1)
                continue
            stone_str = str(stone)
            if len(stone_str) % 2 == 1:
                resulted.append(2024 * stone)
                continue
            # split number in 2
            middle = len(stone_str) // 2
            a, b = stone_str[:middle], stone_str[middle:].lstrip("0")
            resulted.append(int(a))
            resulted.append(int(b) if b else 0)
        self.stones = resulted


def solution_1():
    map = StoneLine(FILE_PATH)
    for i in range(25):
        print(f"[{i+1}] Blink")
        map.blink()
    print(len(map.stones))


if __name__ == "__main__":
    solution_1()  # 816
