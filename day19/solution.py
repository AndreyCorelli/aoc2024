from typing import Set, List

INPUT_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day19/input.txt"


class TowelManager:
    def __init__(self):
        self.towels: Set[str] = set()
        self.patterns: List[str] = []
        self._read_towels_and_patterns()

    def _read_towels_and_patterns(self) -> None:
        towels = []
        with open(INPUT_PATH) as f:
            for line in f:
                line = line.strip()
                if not line:
                    break
                towels += line.split(", ")
            for line in f:
                line = line.strip()
                if not line:
                    break
                self.patterns.append(line)
        self.towels = set(towels)

    def count_valid_towels(self) -> int:
        return sum(1 for pattern in self.patterns if self._is_valid_towel(pattern))

    def _is_valid_towel(self, pattern: str) -> bool:
        stack = [(pattern)]
        tried_patterns = set()

        while stack:
            reminder = stack.pop()
            if not reminder:
                return True
            if reminder in self.towels:
                return True
            for towel in self.towels:
                if reminder.startswith(towel):
                    new_reminder = reminder[len(towel):]
                    if new_reminder in tried_patterns:
                        continue
                    stack.append(new_reminder)
                    tried_patterns.add(new_reminder)

        return False




def solution_1():
    towel_manager = TowelManager()
    print(towel_manager.count_valid_towels())


if __name__ == "__main__":
    solution_1()
