from typing import List, Set, Tuple, Dict, Iterator

Coords = Tuple[int, int]

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day10/input.txt"


class HeightMap:
    def __init__(self, file_path: str):
        self.heights: List[List[int]] = self._read_heights(file_path)
        self.w = len(self.heights[0])
        self.h = len(self.heights)
        self.total_score = 0

    def calc_trail_scores_total(self) -> int:
        self.total_score = 0
        for y, row in enumerate(self.heights):
            for x, height in enumerate(row):
                if height > 0:
                    continue
                self._calc_trail_score(x, y, {(x, y)})
        return self.total_score

    def _calc_trail_score(
            self,
            x: int,
            y: int,
            trail: Set[Coords]) -> None:
        if self.heights[y][x] == 9:
            # self._print_trail(trail)
            self.total_score += 1
            return
        # find all possible directions
        directions: List[Coords] = []
        if x > 0:
            directions.append((x - 1, y))
        if x < self.w - 1:
            directions.append((x + 1, y))
        if y > 0:
            directions.append((x, y - 1))
        if y < self.h - 1:
            directions.append((x, y + 1))

        # check possible directions: filter out those that are already in the trail
        # and those that are not current height + 1
        current_height = self.heights[y][x]
        filtered_directions = []
        for dx, dy in directions:
            if self.heights[dy][dx] != current_height + 1:
                continue
            if (dx, dy) in trail:
                continue
            filtered_directions.append((dx, dy))

        # if no possible directions, return current score
        if not filtered_directions:
            return

        # build N-1 alternative trails for filtered_directions[1:]
        for dx, dy in filtered_directions[1:]:
            new_trail = trail
            # SIC: we'd copy if the trails are allowed to cross
            new_trail = trail.copy()
            new_trail.add((dx, dy))
            self._calc_trail_score(dx, dy, new_trail)

        trail.add(filtered_directions[0])
        self._calc_trail_score(filtered_directions[0][0], filtered_directions[0][1], trail)

    def _print_trail(self, trail: Set[Coords]):
        for y, row in enumerate(self.heights):
            for x, height in enumerate(row):
                if (x, y) in trail:
                    # print red letter to indicate the trail
                    print(f"\033[91m{height}\033[0m", end="")
                else:
                    print(height, end="")
            print()
        print()


    @classmethod
    def _read_heights(cls, file_path: str) -> List[List[int]]:
        with open(file_path, "r") as f:
            return [[int(c) for c in line.strip()] for line in f.readlines()]


def solution_1():
    map = HeightMap(FILE_PATH)
    print(map.calc_trail_scores_total())


if __name__ == "__main__":
    solution_1()  # 816
