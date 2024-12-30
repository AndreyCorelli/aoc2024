import heapq
from typing import List, Set, Tuple, Optional

Coords = Tuple[int, int]

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day13/input.txt"


class RoutingTask:
    BUTTON_COST = (3, 1)

    def __init__(self):
        self.a: Coords = (0, 0)
        self.b: Coords = (0, 0)
        self.prize: Coords = (0, 0)

    def __repr__(self) -> str:
        return f"Task: {self.a}, {self.b} -> {self.prize}"

    def __str__(self) -> str:
        return self.__repr__()

    def solve(self) -> Optional[int]:
        # cost, current point, Na, Nb
        solutions_ordered_stack: List[Tuple[int, Coords, int, int]] = []
        solutions_ordered_stack.append((0, (0, 0), 0, 0))

        min_cost: Optional[int] = None
        iterations = 0

        visited: Set[Coords] = set()

        while solutions_ordered_stack:
            cost, current_point, na, nb = solutions_ordered_stack.pop()
            iterations += 1
            if current_point == self.prize:
                if not min_cost or cost < min_cost:
                    min_cost = cost
                continue

            if current_point[0] >= self.prize[0] or current_point[1] >= self.prize[1]:
                continue
            for dcost, da, db, vector in [
                (self.BUTTON_COST[0], na + 1, nb, self.a),
                (self.BUTTON_COST[1], na, nb + 1, self.b)]:

                path_key = (da, db)
                if path_key in visited:
                    continue

                new_coords = (current_point[0] + vector[0], current_point[1] + vector[1])
                if new_coords[0] > self.prize[0] or new_coords[1] > self.prize[1]:
                    continue
                heapq.heappush(
                    solutions_ordered_stack,
                    (cost + dcost, new_coords, da, db))
                visited.add(path_key)

        return min_cost


    @classmethod
    def read_from_file(cls, file_path: str) -> List["RoutingTask"]:
        tasks = []
        with open(file_path, "r") as f:
            lines = f.readlines()
            for i in range(0, len(lines), 4):
                task = RoutingTask()
                task.a = cls._parse_coords(lines[i])
                task.b = cls._parse_coords(lines[i + 1])
                task.prize = cls._parse_prize(lines[i + 2])
                tasks.append(task)
        return tasks

    @classmethod
    def _parse_coords(cls, line: str) -> Coords:
        line = line[len("Button A: X+"):]
        parts = [p.strip("+") for p in line.split(", Y")]
        x = int(parts[0])
        y = int(parts[1])
        return x, y

    @classmethod
    def _parse_prize(cls, line: str) -> Coords:
        line = line[len("Prize: X="):]
        parts = [p.strip("Y=") for p in line.split(", ")]
        x = int(parts[0])
        y = int(parts[1])
        return x, y


def solution_1():
    tasks = RoutingTask.read_from_file(FILE_PATH)
    total_cost = 0
    for task in tasks:
        cost = task.solve()
        total_cost += (cost or 0)
    print(total_cost)


if __name__ == "__main__":
    solution_1()  # 30973
