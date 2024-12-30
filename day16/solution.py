from typing import List, Set, Tuple, Optional, Dict
import heapq

Coords = Tuple[int, int]

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day16/input.txt"

ADVANCE = 1
RCW = 2
RCCW = 3

ALL_MOVES = [ADVANCE, RCW, RCCW]

MOVE_COST = {
    ADVANCE: 1,
    RCW: 1000,
    RCCW: 1000
}


class Maze:
    def __init__(self, file_path: str):
        self.matrix: List[List[str]] = []
        self.w = 0
        self.h = 0
        self.start: Coords = (0, 0)
        self.deer: Coords = (0, 0)
        self.v: Coords = (1, 0)
        self.end: Coords = (0, 0)
        self._read_from_file(file_path)
        self.visited: Dict[Tuple[int, Coords, Coords], int] = {}

    def solve(self) -> int:
        # score - next move - current position - cur velocity
        moves: List[Tuple[int, int, Coords, Coords]] = []
        for move in ALL_MOVES:
            heapq.heappush(moves, (0, move, self.deer, self.v))

        while moves:
            score, move, pos, v = heapq.heappop(moves)
            if pos == self.end:
                return score
            score += MOVE_COST[move]

            new_pos, new_v = pos, v
            if move == ADVANCE:
                new_pos = (pos[0] + v[0], pos[1] + v[1])
                if self.matrix[new_pos[1]][new_pos[0]] == "#":
                    continue
            else:
                new_v = self._rotate(v, move)

            for move in ALL_MOVES:
                position_key = (move, new_pos, new_v)
                stored_score = self.visited.get(position_key)
                if stored_score is not None and stored_score <= score:
                    continue
                heapq.heappush(moves, (score, move, new_pos, new_v))
                self.visited[position_key] = score


    def print(self) -> None:
        dir_to_smb = {
            (1, 0): ">",
            (-1, 0): "<",
            (0, 1): "v",
            (0, -1): "^"
        }

        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if (x, y) == self.deer:
                    smb = dir_to_smb[self.v]
                    # print a red symbol
                    print(f"\033[91m{smb}\033[0m", end="")
                elif (x, y) == self.start:
                    print("S", end="")
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
                    self.deer = (row.index("S"), self.h - 1)
                    self.start = self.deer
                    row[row.index("S")] = "."
                if "E" in row:
                    self.end = (row.index("E"), self.h - 1)
                    row[row.index("E")] = "."

    def _rotate(self, v: Coords, direction: int) -> Coords:
        if direction == RCW:
            if v == (1, 0):
                return (0, 1)
            if v == (0, 1):
                return (-1, 0)
            if v == (-1, 0):
                return (0, -1)
            return (1, 0)
        if direction == RCCW:
            if v == (1, 0):
                return (0, -1)
            if v == (0, -1):
                return (-1, 0)
            if v == (-1, 0):
                return (0, 1)
            return (1, 0)
        return v


def solution_1():
    maze = Maze(FILE_PATH)
    maze.print()
    solution = maze.solve()
    print(f"\nSolution: {solution}")  # full = 89460 - OK


if __name__ == "__main__":
    solution_1()
