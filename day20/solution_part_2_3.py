import os
from typing import List, Set, Tuple, Optional, Dict
import heapq

Coords = Tuple[int, int]


FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day20/input.txt"

MAX_CHEAT = 20

EMPTY_COORDS = (-1, -1)


class Maze:
    def __init__(self):
        self.matrix: List[List[str]] = []
        self.w = 0
        self.h = 0
        self.start: Coords = (0, 0)
        self.end: Coords = (0, 0)
        self._read_from_file(FILE_PATH)
        # cost from point to the end w/o leaps
        self.cost_from_point: Dict[Coords, int] = {}
        self.highest_allowed_cost = 10000000
        self.base_cost = -1
        self.move_vectors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        # cache in the same dir, as FILE_PATH
        self.cache_path = FILE_PATH + ".cache.txt"

    def _try_load_from_cache(self) -> bool:
        if not os.path.exists(self.cache_path):
            return False
        # load base_cost from the first line and cost_from_point from the rest
        with open(self.cache_path) as f:
            self.base_cost = int(f.readline())
            for line in f:
                x, y, cost = map(int, line.strip().split())
                self.cost_from_point[(x, y)] = cost
        self.highest_allowed_cost = self.base_cost - 100
        return True

    def _save_to_cache(self) -> None:
        with open(self.cache_path, "w") as f:
            f.write(f"{self.base_cost}\n")
            for (x, y), cost in self.cost_from_point.items():
                f.write(f"{x} {y} {cost}\n")

    def fill_cost_from_point(self) -> None:
        if self._try_load_from_cache():
            return

        orig_coords = self.start
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell == ".":
                    self.start = (x, y)
                    self.cost_from_point[(x, y)] = self.solve_wo_leaps()
                    if (x, y) == orig_coords:
                        self.base_cost = self.cost_from_point[(x, y)]
                        self.highest_allowed_cost = self.base_cost - 100
                        print(f"Base cost: {self.base_cost}")
        self.start = orig_coords
        # cache
        self._save_to_cache()
        
    def solve_wo_leaps(self) -> int:
        # cost, current pos, leap on the route
        stack: List[Tuple[int, Coords]] = [(0, self.start)]
        visited: Set[Coords] = set()

        while stack:
            cost, point = heapq.heappop(stack)
            if point == self.end:
                return cost

            x, y = point
            for dx, dy in self.move_vectors:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.w and 0 <= ny < self.h:
                    is_free = self.matrix[ny][nx] == "."
                    if is_free:
                        if (nx, ny) not in visited:
                            heapq.heappush(stack, (cost + 1, (nx, ny)))
                            visited.add((nx, ny))            

        return -1

    def solve(self) -> int:
        # cost, current pos
        stack: List[Tuple[int, Coords]] = [(0, self.start)]
        visited: Set[str] = set()
        used_leaps: Set[str] = set()
        solutions_total = 0

        while stack:
            cost, point = heapq.heappop(stack)

            # if point == self.end:  # should not be feasible
            if cost >= self.highest_allowed_cost:
                continue

            x, y = point
            for dx, dy in self.move_vectors:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < self.w and 0 <= ny < self.h):
                    continue
                if self.matrix[ny][nx] == "#":
                    continue
                move_key = f"{nx},{ny}"
                if move_key not in visited:
                    heapq.heappush(stack, (cost + 1, (nx, ny)))
                    visited.add(move_key)

            # try to cheat: move to any point with Manhattan distance <= MAX_CHEAT
            for leap_x in range(0, MAX_CHEAT + 1):
                # sum(|nx - x| + |ny - y|) <= MAX_CHEAT
                for leap_y in range(0, MAX_CHEAT - leap_x + 1):
                    leap_range = leap_x + leap_y
                    if leap_range == 0:
                        continue

                    new_points = [(x + leap_x, y + leap_y), (x + leap_x, y - leap_y),
                                  (x - leap_x, y + leap_y), (x - leap_x, y - leap_y)]
                    for nx, ny in new_points:
                        if not (0 <= nx < self.w and 0 <= ny < self.h):
                            continue
                        is_free = self.matrix[ny][nx] == "."
                        if not is_free:
                            continue
                        # can we reach the end without cheating?
                        total_cost = cost + leap_range + self.cost_from_point[(nx, ny)]
                        if total_cost <= self.highest_allowed_cost:
                            leap_key = f"{x},{y}:{nx},{ny}"
                            if leap_key not in used_leaps:
                                used_leaps.add(leap_key)
                                solutions_total += 1

        return solutions_total

    def print(self) -> None:
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if (x, y) == self.start:
                    print(f"\033[96mS\033[0m", end="")
                elif (x, y) == self.end:
                    # print a blue symbol
                    print(f"\033[94mE\033[0m", end="")
                else:
                    print(cell, end="")
            print()
        print()

    def _read_from_file(self, file_path: str) -> None:
        with open(file_path) as f:
            for line in f:
                row = list(line.strip())
                self.matrix.append(row)
                self.w = max(self.w, len(row))
                self.h += 1
                if "S" in row:
                    self.start = (row.index("S"), self.h - 1)
                    row[row.index("S")] = "."
                if "E" in row:
                    self.end = (row.index("E"), self.h - 1)
                    row[row.index("E")] = "."


def solution_2():
    maze = Maze()
    #maze.print()
    maze.fill_cost_from_point()
    print("Filled cost from point")
    solution = maze.solve()
    print(f"Total solutions: {solution}")


if __name__ == "__main__":
    solution_2()  # 1051681 - too high, 1007335 - OK
