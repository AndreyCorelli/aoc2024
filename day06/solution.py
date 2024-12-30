from typing import Tuple, Set, List


class Map:
    def __init__(self, map_data: List[Tuple[int, ...]]):
        self.map_data = map_data
        self.width = len(map_data[0]) if map_data else 0
        self.height = len(map_data)
        self.guard_coords = (0, 0)
        self.guard_vector = (1, 1)
        self.waypoints: Set[Tuple[int, int], Tuple[int, int]] = set()

    def print_map(self):
        def guard_vector_to_symbol() -> str:
            x, y = self.guard_vector
            if x == 0 and y == 0:
                return "X"
            if x == 0:
                return "↑" if y < 0 else "↓"
            if y == 0:
                return "←" if x < 0 else "→"
            if x < 0:
                return "↖" if y < 0 else "↙"
            return "↗" if y < 0 else "↘"

        for y, line in enumerate(self.map_data):
            for x, c in enumerate(line):
                if (x, y) == self.guard_coords:
                    print(guard_vector_to_symbol(), end="")
                else:
                    print("#" if c == 1 else ".", end="")
            print("")

    def guide_guard_through_map(self) -> Tuple[str, int]:
        while True:
            move_result = self._move_guard()
            if move_result != "moved":
                break
        return move_result, len(self.waypoints)

    def _move_guard(self) -> str:
        while True:
            x, y = self.guard_coords
            dx, dy = self.guard_vector
            x += dx
            y += dy
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return "gone"

            # check obstacle
            if self.map_data[y][x] == 1:
                # turn 90 degrees clockwise
                self._turn_guard()
                continue
            self.guard_coords = x, y
            # check if we've been here before with the same vector
            if (self.guard_coords, self.guard_vector) in self.waypoints:
                return "loop"

            #self.waypoints.add(self.guard_coords)
            self.waypoints.add((self.guard_coords, self.guard_vector))
            return "moved"

    def _turn_guard(self):
        x, y = self.guard_vector
        if x == 0 and y == -1:
            self.guard_vector = (1, 0)
        elif x == 1 and y == 0:
            self.guard_vector = (0, 1)
        elif x == 0 and y == 1:
            self.guard_vector = (-1, 0)
        elif x == -1 and y == 0:
            self.guard_vector = (0, -1)


def load_map(file_path: str) -> Map:
    # read a file, containing lines like "....#.....", "# .........#", etc.
    # "#" means 1, "." means 0
    map = Map([])
    field = []

    with open(file_path, 'r') as file:
        content = file.read().strip()
        for y, line in enumerate(content.split("\n")):
            field_line = []
            for x, c in enumerate(line):
                if c == "#":
                    field_line.append(1)
                else:
                    field_line.append(0)
                if c != "." and c != "#":
                    map.guard_coords = x, y

                if c == "^":
                    map.guard_vector = 0, -1
                elif c == ">":
                    map.guard_vector = 1, 0
                elif c == "<":
                    map.guard_vector = -1, 0
                elif c == "V":
                    map.guard_vector = 0, 1
            field.append(field_line)

    map.map_data = [tuple(f) for f in field]
    map.width = len(map.map_data[0])
    map.height = len(map.map_data)
    map.waypoints.add(map.guard_coords)
    return map


def solution_1() -> int:
    map = load_map("/Users/andreisitaev/sources/sennder/aoc2024/day06/input.txt")
    return map.guide_guard_through_map()


def solution_2() -> int:
    map = load_map("/Users/andreisitaev/sources/sennder/aoc2024/day06/input.txt")

    orig_guard_coords = map.guard_coords
    orig_guard_vector = map.guard_vector

    solutions_count = 0

    lines_count = len(map.map_data)

    for y in range(map.height):
        print(f"Line [{y}/{lines_count}]")
        for x in range(map.width):
            if map.map_data[y][x] == 1:
                continue
            if (x, y) == orig_guard_coords:
                continue
            # set an obstacle
            map.map_data[y] = map.map_data[y][:x] + (1,) + map.map_data[y][x + 1:]
            # check if the guard is stuck
            move_outcome, _ = map.guide_guard_through_map()
            is_stuck = move_outcome == "loop"
            if is_stuck:
                solutions_count += 1
            # clean up
            map.map_data[y] = map.map_data[y][:x] + (0,) + map.map_data[y][x + 1:]
            map.guard_coords = orig_guard_coords
            map.guard_vector = orig_guard_vector
            map.waypoints = {(orig_guard_coords, orig_guard_vector)}
    return solutions_count


if __name__ == "__main__":
    print(solution_2())
