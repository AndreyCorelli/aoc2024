from typing import List, Set, Tuple, Dict, Iterator

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day11/input.txt"


# class Stone:
#     def __init__(self, value: int, power: int = 1) -> None:
#         self.value = value
#         self.power = power
#
#     def __str__(self) -> str:
#         return f"{self.value}^{self.power}"
#
#     def __repr__(self) -> str:
#         return f"{self.value}^{self.power}"


class StoneLine:
    def __init__(self, file_path: str) -> None:
        self.stones = self._read_input(file_path)

    @classmethod
    def _read_input(cls, file_path: str) -> Dict[int, int]:
        with open(file_path, "r") as f:
            line = f.read().strip()

        return {int(x): 1 for x in line.split(" ")}

    def blink(self) -> None:
        resulted: Dict[int, int] = {}

        for stone, quantity in self.stones.items():
            if stone == 0:
                new_stones = (1,)
            else:
                stone_str = str(stone)
                if len(stone_str) % 2 == 1:
                    new_stones = (2024 * stone,)
                else:
                    # split number in 2
                    middle = len(stone_str) // 2
                    a_str, b_str = stone_str[:middle], stone_str[middle:].lstrip("0")
                    new_stones = int(a_str), int(b_str) if b_str else 0

            for new_stone in new_stones:
                existing = resulted.get(new_stone, 0)
                resulted[new_stone] = existing + quantity
        self.stones = resulted

    def calc_stones_count(self) -> int:
        total = 0
        for _, value in self.stones.items():
            total += value
        return total



def solution_1():
    map = StoneLine(FILE_PATH)
    for i in range(75):
        print(f"[{i+1}] Blink")
        map.blink()
    print(map.calc_stones_count())


if __name__ == "__main__":
    solution_1()  # 221280540398419
