from PIL import Image
from typing import List, Set, Tuple, Optional, Dict

Coords = Tuple[int, int]

data = {
    "small": ((11, 7),
        "/Users/andreisitaev/sources/sennder/aoc2024/day14/input_small.txt"),
    "normal": ((101, 103),
        "/Users/andreisitaev/sources/sennder/aoc2024/day14/input.txt"),
    "x": ((101, 103),
        "/Users/andreisitaev/sources/sennder/aoc2024/day14/input_x.txt")
}

OUTPUT_FOLDER = "/Users/andreisitaev/sources/sennder/aoc2024/day14/images"

class Robot:
    def __init__(self, p: Coords, v: Coords):
        self.p = p
        self.v = v

    def __repr__(self):
        return f"[{self.p}] -> [{self.v}]"

    def __str__(self):
        return self.__repr__()

class TileMap:
    def __init__(self, sz: Coords, file_path: str):
        self.w = sz[0]
        self.h = sz[1]
        self.matrix: List[List[int]] = [[0 for _ in range(self.w)] for _ in range(self.h)]
        self.robots: List[Robot] = []
        self._read_robots_from_file(file_path)

    def move_robots(self) -> None:
        self.matrix = [[0 for _ in range(self.w)] for _ in range(self.h)]

        for robot in self.robots:
            robot.p = (robot.p[0] + robot.v[0], robot.p[1] + robot.v[1])
            # if robot stranded outside the map, mirror its position
            if robot.p[0] < 0:
                robot.p = self.w + robot.p[0], robot.p[1]
            if robot.p[0] >= self.w:
                robot.p = robot.p[0] - self.w, robot.p[1]
            if robot.p[1] < 0:
                robot.p = robot.p[0], self.h + robot.p[1]
            if robot.p[1] >= self.h:
                robot.p = robot.p[0], robot.p[1] - self.h
            self.matrix[robot.p[1]][robot.p[0]] = 1

    def get_largest_cluster_size(self) -> int:
        def dfs(x: int, y: int, visited: Set[Coords]) -> int:
            if x < 0 or x >= self.w or y < 0 or y >= self.h:
                return 0
            if self.matrix[y][x] == 0 or (x, y) in visited:
                return 0
            visited.add((x, y))
            return 1 + dfs(x - 1, y, visited) + dfs(x + 1, y, visited) + dfs(x, y - 1, visited) + dfs(x, y + 1, visited)

        visited: Set[Coords] = set()
        max_cluster_size = 0
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) not in visited and self.matrix[y][x] == 1:
                    cluster_size = dfs(x, y, visited)
                    max_cluster_size = max(max_cluster_size, cluster_size)
        return max_cluster_size

    def save_image(self, subfolder: str, index: int) -> None:
        path = f"{OUTPUT_FOLDER}/{subfolder}/img_{index:05d}.png"
        scale = 4  # Specify the scaling factor

        # Create a scaled image
        scaled_width = self.w * scale
        scaled_height = self.h * scale
        img = Image.new("RGB", (scaled_width, scaled_height), "black")
        pixels = img.load()

        # Draw scaled pixels for robots
        for robot in self.robots:
            x, y = robot.p
            for dx in range(scale):  # Fill in the scaled pixel block
                for dy in range(scale):
                    if 0 <= (x * scale + dx) < scaled_width and 0 <= (y * scale + dy) < scaled_height:
                        pixels[x * scale + dx, y * scale + dy] = (200, 200, 200)
        img.save(path)

    def calc_robots_per_quadrant(self) -> Tuple[int, int, int, int]:
        w2, h2 = self.w // 2, self. h // 2
        q1 = q2 = q3 = q4 = 0
        for robot in self.robots:
            if robot.p[0] < w2 and robot.p[1] < h2:
                q1 += 1
            elif robot.p[0] > w2 and robot.p[1] < h2:
                q2 += 1
            elif robot.p[0] < w2 and robot.p[1] > h2:
                q3 += 1
            elif robot.p[0] > w2 and robot.p[1] > h2:
                q4 += 1
        return q1, q2, q3, q4

    def _read_robots_from_file(self, file_path: str) -> None:
        with open(file_path) as f:
            for line in f:
                # line is "p=7,6 v=-1,-3"
                p, v = line.split(" v=")
                p = p.replace("p=", "").split(",")
                v = v.split(",")
                robot = Robot((int(p[0]), int(p[1])), (int(v[0]), int(v[1])))
                self.robots.append(robot)

    def print_tiles(self) -> None:
        robots_per_coords: Dict[Coords, int] = {}
        for robot in self.robots:
            robots_per_coords[robot.p] = robots_per_coords.get(robot.p, 0) + 1

        for y in range(self.h):
            for x in range(self.w):
                is_center_line = x == self.w // 2 or y == self.h // 2

                robots_count = robots_per_coords.get((x, y), 0)
                if robots_count > 0:
                    print(f"{robots_count}", end="")
                else:
                    if is_center_line:
                        print(" ", end="")
                    else:
                        print(".", end="")
            print()

def solution_2():
    sample = "normal"

    size, path = data[sample]
    t_map = TileMap(size, path)
    for i in range(8500):
        t_map.move_robots()
        t_map.save_image(sample, i)
        largest_cluster_size = t_map.get_largest_cluster_size()
        if largest_cluster_size > 22:
            #t_map.save_image(sample, i)
            print(f"Cluster size: {largest_cluster_size} at {i + 1}")
            break

    t_map.print_tiles()



if __name__ == "__main__":
    solution_2()
