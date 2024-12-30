import heapq
from typing import List, Set, Tuple, Optional, Dict

Coords = Tuple[int, int]

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day15/input.txt"


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
        for y, line in enumerate(map_lines):
            for x, cell in enumerate(line):
                if cell == "@":
                    self.robot = (x, y)

        self.matrix = [list(line) for line in map_lines]
        self.matrix[self.robot[1]][self.robot[0]] = "."
        self.w = len(self.matrix[0])
        self.h = len(self.matrix)
        self.moves = movements

    def print_map(self):
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if (x, y) == self.robot:  # print a red symbol
                    print("\033[91m" + "@" + "\033[0m", end="")
                else:
                    print(cell, end="")
            print()

    def get_boxes_hashes(self) -> int:
        b_hash = 0
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell == "O":
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
        if self.matrix[new_pos[1]][new_pos[0]] == ".":
            self.robot = new_pos
            self.next_move_index += 1
            return
        # there's a box - move the box until it's pressed
        # against the wall. If it's pressed against another box,
        # move them all, until the last one is pressed against the wall
        boxes = [new_pos]  # the line of boxes
        line_ends_with = ""
        while True:
            new_box_pos = (boxes[-1][0] + v[0], boxes[-1][1] + v[1])
            if self.matrix[new_box_pos[1]][new_box_pos[0]] == "#":
                line_ends_with = "#"
                break
            if self.matrix[new_box_pos[1]][new_box_pos[0]] == ".":
                line_ends_with = "."
                break
            boxes.append(new_box_pos)
        if line_ends_with == "#":
            # nowhere to move the boxes
            self.next_move_index += 1
            return
        # move the boxes and the robot
        self.matrix[self.robot[1]][self.robot[0]] = "."
        self.robot = new_pos
        self.matrix[self.robot[1]][self.robot[0]] = "."
        for box in boxes:
            new_pos = box[0] + v[0], box[1] + v[1]
            self.matrix[new_pos[1]][new_pos[0]] = "O"
        self.next_move_index += 1

def solution_1():
    t_map = TileMap(FILE_PATH)
    t_map.print_map()
    while t_map.next_move_index < len(t_map.moves):
        t_map.move_robot()
        #t_map.print_map()
        #print("\n\n")
    print(f"Result = {t_map.get_boxes_hashes()}")


if __name__ == "__main__":
    solution_1()
