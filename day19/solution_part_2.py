from typing import Set, List, Dict

INPUT_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day19/input.txt"


class TowelManager:
    def __init__(self):
        self.towels: List[str] = []
        self.patterns: List[str] = []
        self.options_per_pattern: Dict[str, int] = {}
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
        self.towels = towels

    def count_valid_towels(self) -> int:
        total_valid = 0
        for i, pattern in enumerate(self.patterns):
            count_valid = self._count_of_options(pattern)
            total_valid += count_valid
            print(f"[{i + 1}] out of [{len(self.patterns)}], {count_valid} options")
        return total_valid


    def _count_of_options(self, target: str) -> int:
        def find_patterns(reminder: str) -> int:
            if not reminder:
                return 1
            if reminder in self.options_per_pattern:
                return self.options_per_pattern[reminder]
            options_count = 0
            for towel in self.towels:
                if reminder.startswith(towel):
                    new_reminder = reminder[len(towel):]
                    options_count += find_patterns(new_reminder)

            self.options_per_pattern[reminder] = options_count
            return options_count

        return find_patterns(target)


def solution_1():
    towel_manager = TowelManager()
    print(towel_manager.count_valid_towels())  # 950763269786650


if __name__ == "__main__":
    solution_1()
