import heapq
from typing import List, Set, Tuple, Optional, Dict

Coords = Tuple[int, int]

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day15/input.txt"


class Box:
    def __init__(self, coords: Coords):
        self.coords = coords

    def __repr__(self):
        return f"Box({self.coords})"

    def __str__(self):
        return f"Box({self.coords})"

    def get_front(self, v: Coords) -> Set[Coords]:
        return {
            (self.coords[0] + v[0], self.coords[1] + v[1]),
            (self.coords[0] + v[0] + 1, self.coords[1] + v[1])}


class TileMap:
    MOVE_VECTOR = {
        "^": (0, -1),
        "v": (0, 1),
        "<": (-1, 0),
        ">": (1, 0)
    }

    def __init__(self, file_path: str):
        self.matrix: List[List[str]] = []
        self.w = 0
        self.h = 0
        self.boxes: List[Box] = []
        self.box_areas: Dict[Coords, Box] = {}
        self.moves: str = ""
        self.next_move_index = 0
        self.robot: Coords = (0, 0)  # x, y
        self._read_file(file_path)

    def _read_file(self, file_path: str):
        map_lines: List[str] = []
        movements = ""
        line_type = "map"
        with open(file_path) as file:
            for line in file:
                line = line.strip("\n")
                if line == "":
                    line_type = "moves"
                    continue
                if line_type == "map":
                    map_lines.append(line)
                else:
                    movements += line

        # preprocess map lines
        new_lines = []
        for y, line in enumerate(map_lines):
            new_line = ""
            for x, c in enumerate(line):
                if c == "@":
                    self.robot = (x * 2, y)
                    new_line += ".."
                elif c == "#":
                    new_line += "##"
                elif c == ".":
                    new_line += ".."
                elif c == "O":
                    new_line += ".."
                    self.boxes.append(Box((x * 2, y)))
                    self.box_areas[(x * 2, y)] = self.boxes[-1]
                    self.box_areas[(x * 2 + 1, y)] = self.boxes[-1]
            new_lines.append(new_line)
        map_lines = new_lines

        self.matrix = [list(line) for line in map_lines]
        self.w = len(self.matrix[0])
        self.h = len(self.matrix)
        self.moves = movements

    def print_map(self):
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if (x, y) == self.robot:  # print a red symbol
                    robot_smb = self.moves[self.next_move_index] if self.next_move_index < len(self.moves) else "@"
                    print("\033[91m" + robot_smb + "\033[0m", end="")
                elif (x, y) in self.box_areas:
                    box = self.box_areas[(x, y)]
                    smb = "[" if (x, y) == box.coords else "]"
                    print("\033[32m" + smb + "\033[0m", end="")
                else:
                    print(cell, end="")
            print()

    def get_boxes_hashes(self) -> int:
        b_hash = 0
        for box in self.boxes:
            x, y = box.coords
            b_hash += (x + y * 100)
        return b_hash

    def move_robot(self) -> None:
        move = self.moves[self.next_move_index]
        v = self.MOVE_VECTOR[move]
        new_pos = (self.robot[0] + v[0], self.robot[1] + v[1])
        # if wall, do nothing
        if self.matrix[new_pos[1]][new_pos[0]] == "#":
            self.next_move_index += 1
            return
        # if empty cell, move
        box = self.box_areas.get(new_pos)
        if not box:
            self.robot = new_pos
            self.next_move_index += 1
            return
        # found boxes, that would be moved as a bunch
        # found an obstacle ahead of the boxes, if any
        pack = {box}
        hit_obstacle = self._update_boxes_pack(v, pack)
        if hit_obstacle:
            self.next_move_index += 1
            return
        # move the robot and the pack
        self.robot = new_pos
        for box in pack:
            box.coords = (box.coords[0] + v[0], box.coords[1] + v[1])

        self.box_areas = {}
        for box in self.boxes:
            self.box_areas[box.coords] = box
            self.box_areas[(box.coords[0] + 1, box.coords[1])] = box
        self.next_move_index += 1

    def _update_boxes_pack(self, v: Coords, pack: Set[Box]) -> bool:
        new_front = set()
        for box in pack:
            new_front |= box.get_front(v)

        # check if new_front hits the wall or another box
        while True:
            added_front_points = set()
            for p in new_front:
                if self.matrix[p[1]][p[0]] == "#":
                    return True  # here we stop
                box = self.box_areas.get(p)
                if box and box not in pack:
                    pack.add(box)
                    added_front_points |= box.get_front(v)
            if not added_front_points:
                break
            new_front |= added_front_points

        return False


def solution_2():
    t_map = TileMap(FILE_PATH)
    t_map.print_map()
    print("\n---->\n")
    while t_map.next_move_index < len(t_map.moves):
        t_map.move_robot()
        # t_map.print_map()
        # print("\n\n")
    print(f"Result = {t_map.get_boxes_hashes()}")


if __name__ == "__main__":
    solution_2()
