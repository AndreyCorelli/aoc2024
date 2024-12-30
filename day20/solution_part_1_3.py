from typing import List, Set, Tuple, Optional, Dict
import heapq

Coords = Tuple[int, int]


FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day20/input.txt"


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
                    self.cost_from_point[(x, y)] = self.solve_wo_leaps()
                    if (x, y) == orig_coords:
                        self.base_cost = self.cost_from_point[(x, y)]
                        self.highest_allowed_cost = self.base_cost - 100
                        print(f"Base cost: {self.base_cost}")
        self.start = orig_coords
        
    def solve_wo_leaps(self) -> int:
        # cost, current pos, leap on the route
        stack: List[Tuple[int, Coords]] = [(0, self.start)]
        visited: Set[Coords] = set()

        while stack:
            cost, point = heapq.heappop(stack)
            if point == self.end:
                return cost

            #if point in self.cost_from_point:
            #    cost += self.cost_from_point[point]
            #    return cost  # this won't work

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
        # cost, current pos, leap on the route
        stack: List[Tuple[int, Coords]] = [(0, self.start)]
        visited: Set[str] = set()
        solutions_total = 0

        while stack:
            cost, point = heapq.heappop(stack)

            if point == self.end:
                # we moved here w/o leaps, the highest_allowed_cost is not exceeded
                # should not be feasible, as the shortest path is already found
                solutions_total += 1
                continue

            x, y = point
            # try move without leaps
            if cost < self.highest_allowed_cost:
                for dx, dy in self.move_vectors:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.w and 0 <= ny < self.h:
                        is_free = self.matrix[ny][nx] == "."
                        if is_free:
                            move_key = f"{nx},{ny}"
                            if move_key not in visited:
                                heapq.heappush(stack, (cost + 1, (nx, ny)))
                                visited.add(move_key)

            # try leap
            for inter, fin in self.leap_vectors:
                nx, ny = x + fin[0], y + fin[1]
                if 0 <= nx < self.w and 0 <= ny < self.h:
                    # is this a leap over a wall?
                    lox, loy = x + inter[0], y + inter[1]
                    if self.matrix[loy][lox] == "#" \
                        and self.matrix[ny][nx] == ".":
                        move_key = f"{x},{y},{nx},{ny}"
                        if move_key not in visited:
                            # leap to the point & calc total cost
                            total_cost = cost + 2 + self.cost_from_point[(nx, ny)]
                            # acceptable solution?
                            if total_cost <= self.highest_allowed_cost:
                                solutions_total += 1
                                visited.add(move_key)

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


def solution_1():
    maze = Maze()
    #maze.print()
    maze.fill_cost_from_point()
    print("Filled cost from point")
    solution = maze.solve()
    print(f"Total solutions: {solution}")


if __name__ == "__main__":
    solution_1()  # 1355
