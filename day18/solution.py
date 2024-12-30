import heapq
from typing import Tuple, List, Dict

Coords = Tuple[int, int]

INPUT = {
    "small": {
        "path": "/Users/andreisitaev/sources/sennder/aoc2024/day18/input_small.txt",
        "size": (7, 7)
    },
    "normal": {
        "path": "/Users/andreisitaev/sources/sennder/aoc2024/day18/input.txt",
        "size": (71, 71)
    }
}


class MemoryMap:
    def __init__(self, input_key: str):
        self.w = INPUT[input_key]["size"][0]
        self.h = INPUT[input_key]["size"][1]
        self.start: Coords = (0, 0)
        self.end: Coords = (self.w - 1, self.h - 1)
        self.byte_coords: List[Coords] = []
        self.matrix: List[List[str]] = []

        self._read_file(INPUT[input_key]["path"])

    def solve(self, bytes_limit: int) -> None:
        self._build_matrix(bytes_limit)
        self._find_path()

    def print(self) -> None:
        if not self.matrix:
            for y in range(self.h):
                for x in range(self.w):
                    if (x, y) in self.byte_coords:
                        print("#", end="")
                    else:
                        print(".", end="")
                print()
            return
        # print matrix
        for y in range(self.h):
            for x in range(self.w):
                print(self.matrix[y][x], end="")
            print()

    def _find_path(self) -> None:
        visited: Dict[Coords, int] = {}
        stack: List[Tuple[int, Coords]] = [(0, self.start)]

        while stack:
            length, coords = heapq.heappop(stack)
            if coords == self.end:
                print(f"Shortest path: {length}")
                return
            if coords in visited and visited[coords] <= length:
                continue
            visited[coords] = length
            x, y = coords
            for x_offset, y_offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_x, new_y = x + x_offset, y + y_offset
                if 0 <= new_x < self.w and 0 <= new_y < self.h:
                    if self.matrix[new_y][new_x] == '.':
                        stack.append((length + 1, (new_x, new_y)))

    def _build_matrix(self, bytes_limit: int) -> None:
        self.matrix = []
        selected_bytes = set(self.byte_coords[:bytes_limit])
        for y in range(self.h):
            row = []
            for x in range(self.w):
                if (x, y) in selected_bytes:
                    row.append("#")
                else:
                    row.append(".")
            self.matrix.append(row)

    def _read_file(self, path: str) -> None:
        """
        Read byte_coords from a multiline file with records like "x,y"
        """
        with open(path) as f:
            for line in f:
                x, y = line.strip().split(",")
                self.byte_coords.append((int(x), int(y)))


def solution_1():
    memory_map = MemoryMap("normal")
    memory_map.solve(1024)
    memory_map.print()


if __name__ == "__main__":
    solution_1()