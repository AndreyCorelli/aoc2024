from typing import List, Set, Tuple, Dict

Coords = Tuple[int, int]

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day08/input.txt"


class Map:
    def __init__(self, file_path: str):
        self.map = self._read_map(file_path)
        self.focals: Set[Coords] = set()

    @classmethod
    def _read_map(cls, file_path: str) -> List[str]:
        with open(file_path, 'r') as file:
            content = file.read()
        lines = content.strip().split("\n")
        return lines

    def locate_focals(self) -> int:
        antennas: List[Tuple[str, Coords]] = []
        for y, line in enumerate(self.map):
            for x, cell in enumerate(line):
                if cell != ".":
                    antennas.append((cell, (x, y)))
        antennas_by_type: Dict[str, List[Coords]] = {}
        for antenna in antennas:
            antennas_by_type[antenna[0]] = antennas_by_type.get(antenna[0], []) + [antenna[1]]

        # within the same "type" category check each antennas' pair
        for antenna_type, coords in antennas_by_type.items():
            for i, coord in enumerate(coords):
                for j in range(i + 1, len(coords)):
                    self._check_pair_of_antennas(coord, coords[j])
                    self._check_pair_of_antennas(coords[j], coord)

        return len(self.focals)

    def draw_map(self) -> None:
        for y, line in enumerate(self.map):
            for x, cell in enumerate(line):
                if (x, y) in self.focals:
                    print("#", end="")
                else:
                    print(cell, end="")
            print()

    def _check_pair_of_antennas(self, a: Coords, b: Coords) -> None:
        # the method searches for only 1 focal point f, that's closer to a than to b
        dx, dy = b[0] - a[0], b[1] - a[1]

        for k in range(10000):
            x = a[0] - k * dx
            y = a[1] - k * dy
            if x < 0 or y < 0 or x >= len(self.map[0]) or y >= len(self.map):
                break
            self.focals.add((x, y))
        """
        update: no need for equations: Manhattan distance is 2 times higher
                in case focal point is shifted by the same dx, dy
        K = (by - ay)/(bx - ax)
        x = ax + A * (ax - bx)
        y = ay + A * K * (ay - by)
        
        Case 1: dx > 0, dy > 0
        2 * (x - ax + y - ay) = x - bx + y - by
        x + y = 2ax + 2ay - bx - by
        
        / y = 2ax + 2ay - bx - by - x        
        { x = ax + A * (ax - bx)
        \ y = ay + A * K * (ay - by)
        
        2ax + 2ay - bx - by - ax + A * (ax - bx) = ay + A * K * (ay - by)
        A * (ax - bx) - A * K * (ay - by) = ay - (2ax + 2ay - bx - by - ax)
        A = (ay - 2*ax - 2*ay + bx + by + ax) / (ax - bx - K * (ay - by))  (=1)

        ax, ay = 4, 3
        bx, by = 5, 5
        dx, dy = bx - ax, by - ay
        K = dy / dx
        A = (ay - 0.5*bx - 0.5*by) / (K*(ay - by) + ax - bx)
        K, A = 2, 0.4
        x = ax - A * (ax - bx)
        y = ay - A * K * (ay - by)
        """


def solution_1():
    map = Map(FILE_PATH)
    print(map.locate_focals())
    map.draw_map()


if __name__ == "__main__":
    solution_1()
