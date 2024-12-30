from typing import List, Set, Tuple, Optional, Dict
import heapq

Coords = Tuple[int, int]
LeapCoords = Tuple[Coords, Coords]

NO_CHEAT = ((0, 0), (0, 0))


FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day20/input.txt"


class Maze:
    def __init__(self):
        self.matrix: List[List[str]] = []
        self.w = 0
        self.h = 0
        self.start: Coords = (0, 0)
        self.end: Coords = (0, 0)
        self._read_from_file(FILE_PATH)
        self.disabled_leaps: Set[LeapCoords] = set()
        # cost from point to the end w/o leaps
        self.cost_from_point: Dict[Coords, int] = {}
        self.highest_allowed_cost = 10000000

        self.leap_vectors = [((0, 1), (0, 2)),
                             ((0, -1), (0, -2)), # up
                             ((1, 0), (2, 0)),
                             ((-1, 0), (-2, 0))]
        self.move_vectors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def fill_cost_from_point(self) -> None:
        orig_coords = self.start
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell == ".":
                    self.start = (x, y)
                    self.cost_from_point[(x, y)] = self.solve(False)
        self.start = orig_coords

    def solve(self, leaps_allowed: bool) -> int:
        # cost, current pos, leap on the route
        stack: List[Tuple[int, Coords, LeapCoords]] = [(0, self.start, NO_CHEAT)]
        visited: Set[Tuple[Coords, LeapCoords]] = set()

        while stack:
            cost, point, leap_coords = heapq.heappop(stack)
            if point == self.end:
                if leap_coords != NO_CHEAT:  # always NO_CHEAT
                    # we used this cheat - let's store it
                    self.disabled_leaps.add(leap_coords)
                return cost

            if not leaps_allowed:
                if point in self.cost_from_point:
                    cost += self.cost_from_point[point]
                    return cost

            if leaps_allowed and leap_coords != NO_CHEAT:
                if point in self.cost_from_point:
                    self.disabled_leaps.add(leap_coords)

                    cost += self.cost_from_point[point]
                    if cost > self.highest_allowed_cost:
                        continue
                    #self.disabled_leaps.add(leap_coords)
                    return cost

            x, y = point
            for dx, dy in self.move_vectors:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.w and 0 <= ny < self.h:
                    is_free = self.matrix[ny][nx] == "."
                    if is_free:
                        if ((nx, ny), leap_coords) not in visited:
                            heapq.heappush(stack, (cost + 1, (nx, ny), leap_coords))
                            visited.add(((nx, ny), leap_coords))

            if leaps_allowed and leap_coords == NO_CHEAT:
                for inter, fin in self.leap_vectors:
                    nx, ny = x + fin[0], y + fin[1]
                    if 0 <= nx < self.w and 0 <= ny < self.h:
                        # is this a leap over a wall?
                        lox, loy = x + inter[0], y + inter[1]
                        if self.matrix[loy][lox] == "#" \
                            and self.matrix[ny][nx] == ".":

                            new_leap_coords = (x, y), (nx, ny)
                            if new_leap_coords not in self.disabled_leaps:
                                if ((nx, ny), new_leap_coords) not in visited:
                                    heapq.heappush(stack, (cost + 2, (nx, ny), new_leap_coords))
                                    visited.add(((nx, ny), new_leap_coords))

        return -1

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


def solution_1():
    maze = Maze()
    #maze.print()
    base_cost = maze.solve(False)
    maze.highest_allowed_cost = base_cost - 100
    print(f"\nBase cost: {base_cost}")
    maze.fill_cost_from_point()
    print("Filled cost from point")
    assert maze.cost_from_point[maze.start] == base_cost

    counter = 0
    while True:
        cheat_cost = maze.solve(True)
        if cheat_cost == -1:
            break
        counter += 1
        cheat_profit = base_cost - cheat_cost
        print(f"[{counter}] Cheating profit: {cheat_profit}")
        if cheat_profit < 5 or counter > 1900:
            break

    print(f"Done")


if __name__ == "__main__":
    solution_1()  # 801 - too low,