from typing import List, Set, Tuple, Dict

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day12/input.txt"


def count_polygon_sides(region: Set[Tuple[int, int]]) -> int:
    # edges = vertices
    # a point is a vertex if it has 1 or 3 adjacent region's dots
    vertex_neighbours = {
        (-0.5, -0.5): [(0, -1), (-1, 0), (-1, -1)],  # top left
        (0.5, -0.5): [(0, -1), (1, 0), (1, -1)],  # top right
        (0.5, 0.5): [(1, 0), (0, 1), (1, 1)],  # bottom right
        (-0.5, 0.5): [(-1, 0), (0, 1), (-1, 1)],  # bottom left
    }

    vertices: Set[Tuple[float, float]] = set()

    for x, y in region:
        for v, v_n in vertex_neighbours.items():
            count = 1
            for dx, dy in v_n:
                nx, ny = x + dx, y + dy
                if (nx, ny) in region:
                    count += 1
            if count == 1 or count == 3:
                vertices.add((x + v[0], y + v[1]))

    count_neighbours = 0
    for x, y in region:
        if (x + 1, y + 1) in region:
            if (x + 1, y) not in region and (x, y + 1) not in region:
                count_neighbours += 1
        if (x - 1, y + 1) in region:
            if (x - 1, y) not in region and (x, y + 1) not in region:
                count_neighbours += 1

    return len(vertices) + count_neighbours * 2


class RegionMap:
    def __init__(self, file_path: str):
        self.matrix = self._read_from_file(file_path)
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0]) if self.rows > 0 else 0
        self.visited = set()  # To track visited coordinates
        self.regions = []  # List of regions, each region is a set of (x, y) coordinates

    @classmethod
    def _read_from_file(cls, file_path: str) -> List[List[str]]:
        with open(file_path, "r") as f:
            return [list(line.strip()) for line in f]

    def find_regions(self) -> List[Set[Tuple[int, int]]]:
        self.visited.clear()
        self.regions.clear()

        for x in range(self.rows):
            for y in range(self.cols):
                if (x, y) not in self.visited:
                    region = self._explore_region(x, y)
                    if region:
                        self.regions.append(region)

        return self.regions

    def get_total_regions_score(self) -> int:
        score = 0
        for r in self.regions:
            edges = count_polygon_sides(r)
            score += edges * len(r)
        return score

    def print_matrix(self):
        # colors, that are used for colorful printing
        color_codes: List[str] = [
            '\033[31m',  # red
            '\033[32m',  # green
            '\033[33m',  # yellow
            '\033[34m',  # blue
            '\033[35m',  # purple
            '\033[36m',  # cyan
            '\033[37m',  # white
        ]
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                color = ''
                for rn, region in enumerate(self.regions):
                    if (x, y) in region:
                        color = color_codes[rn % len(color_codes)]
                        break
                if not color:
                    print(cell, end='')
                else:
                    print(f"{color}{cell}\033[0m", end='')
            print()

    def _explore_region(self, start_x: int, start_y: int) -> Set[Tuple[int, int]]:
        char = self.matrix[start_x][start_y]
        region = set()
        stack = [(start_x, start_y)]

        while stack:
            x, y = stack.pop()
            if (x, y) in self.visited:
                continue

            self.visited.add((x, y))
            region.add((x, y))

            # Check 4 neighbors
            for dx, dy in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.rows and 0 <= ny < self.cols:
                    if self.matrix[nx][ny] == char and (nx, ny) not in self.visited:
                        stack.append((nx, ny))
        return region


def solution_2():
    region_map = RegionMap(FILE_PATH)
    regions = region_map.find_regions()
    region_map.print_matrix()
    print("\n")

    print(f"Number of regions: {len(regions)}")
    score = region_map.get_total_regions_score()
    print(f"Total score: {score}")


if __name__ == "__main__":
    solution_2()  # 902760 - too low, 1005616 - too high, 909564
    #region = {(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)}
    #region = {(0, 0), (0, 1), (0, 2),
    #          (1, 0),         (1, 2),
    #          (2, 0), (2, 1), (2, 2)}
    #region = {(0, 0), (1, 1)}
    #print(count_polygon_sides(region))
