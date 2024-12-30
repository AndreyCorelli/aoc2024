import heapq
from typing import List, Set, Tuple, Optional, Dict

Coords = Tuple[int, int]

data = {
    "small": ((11, 7),
        "/Users/andreisitaev/sources/sennder/aoc2024/day14/input_small.txt"),
    "normal": ((101, 103),
        "/Users/andreisitaev/sources/sennder/aoc2024/day14/input.txt")
}

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
        self.robots: List[Robot] = []
        self._read_robots_from_file(file_path)

    def move_robots(self) -> None:
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

def solution_1():
    size, path = data["normal"]
    t_map = TileMap(size, path)
    for i in range(100):
        t_map.move_robots()

    t_map.print_tiles()
    q1, q2, q3, q4 = t_map.calc_robots_per_quadrant()
    result = q1 * q2 * q3 * q4
    print(result)


if __name__ == "__main__":
    solution_1()
