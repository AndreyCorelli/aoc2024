import os
from typing import List, Set, Tuple, Optional, Dict
import heapq

Coords = Tuple[int, int]


FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day20/input.txt"

MAX_CHEAT = 20


class CheatTrack:
    def __init__(self, p: Coords):
        self.a = p
        self.b = p
        self.length = 1

    def create_new_track(self, p: Coords) -> "CheatTrack":
        t = CheatTrack(p)
        t.length = self.length + 1
        t.a = self.a
        return t

    def __str__(self) -> str:
        return f"{self.a}>{self.b}:{self.length}"

    def __repr__(self) -> str:
        return self.__str__()

    def __gt__(self, other):
        return self.length > other.length

    def __lt__(self, other):
        return self.length < other.length

    def __eq__(self, other):
        return self.length == other.length and self.a == other.a and self.b == other.b


PSEUDO_TRACK = CheatTrack((0, 0))


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
        # cost, current pos, leap on the route
        stack: List[Tuple[int, Coords, CheatTrack]] = [(0, self.start, PSEUDO_TRACK)]
        visited: Set[str] = set()
        solutions_total = 0

        while stack:
            cost, point, cheat_track = heapq.heappop(stack)

            if point == self.end:
                # we moved here w/o leaps, the highest_allowed_cost is not exceeded
                # should not be feasible, as the shortest path is already found
                solutions_total += 1
                continue

            x, y = point
            # try move without leaps
            if cheat_track == PSEUDO_TRACK and cost < self.highest_allowed_cost:
                for dx, dy in self.move_vectors:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.w and 0 <= ny < self.h:
                        is_free = self.matrix[ny][nx] == "."
                        if is_free:
                            move_key = f"{nx},{ny}"
                            if move_key not in visited:
                                heapq.heappush(stack, (cost + 1, (nx, ny), PSEUDO_TRACK))
                                visited.add(move_key)

            # can we finish the track?
            if cheat_track != PSEUDO_TRACK:
                for dx, dy in self.move_vectors:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.w and 0 <= ny < self.h:
                        if self.matrix[ny][nx] == ".":
                            move_key = f"{cheat_track}_{nx},{ny}"
                            if move_key not in visited:
                                total_cost = cost + 1 + self.cost_from_point[(nx, ny)]
                                # acceptable solution?
                                if total_cost <= self.highest_allowed_cost:
                                    solutions_total += 1
                                visited.add(move_key)

            # try starting or continuing a track
            if cheat_track.length < MAX_CHEAT and cost < self.highest_allowed_cost:
                for dx, dy in self.move_vectors:
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.w and 0 <= ny < self.h) and (self.matrix[ny][nx] == "#"):
                        # can we start or continue the track?
                        if cheat_track == PSEUDO_TRACK:
                            new_track = CheatTrack((nx, ny))
                        else:
                            new_track = cheat_track.create_new_track((nx, ny))
                        new_key = str(new_track)
                        if new_key not in visited:
                            visited.add(new_key)
                            heapq.heappush(stack, (cost + 1, (nx, ny), new_track))

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
    solution_2()
