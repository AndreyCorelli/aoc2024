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
        self.visited: Dict[Tuple[Coords, Coords], int] = {}
        # to recollect paths: (current position, velocity) -> [(previous position, velocity, score), ...]
        self.paths: Dict[Tuple[Coords, Coords], List[Tuple[Coords, Coords, int]]] = {}

    def solve(self) -> int:
        # score - next move - current position - cur velocity
        moves: List[Tuple[int, int, Coords, Coords]] = []
        heapq.heappush(moves, (0, self.deer, self.v))

        min_final_score = float("inf")
        while moves:
            score, pos, v = heapq.heappop(moves)
            if pos == self.end:
                if score < min_final_score:
                    min_final_score = score
                continue
            self.visited[(pos, v)] = score

            for move in ALL_MOVES:
                new_pos, new_v = pos, v
                if move == ADVANCE:
                    new_pos = (pos[0] + v[0], pos[1] + v[1])
                    if self.matrix[new_pos[1]][new_pos[0]] == "#":
                        continue
                else:
                    new_v = self._rotate(v, move)
                position_key = (new_pos, new_v)
                stored_score = self.visited.get(position_key)
                new_score = score + MOVE_COST[move]
                if stored_score is not None and stored_score < new_score:
                    continue
                existing_paths = self.paths.get(position_key, [])
                if not existing_paths:
                    self.paths[position_key] = [(pos, v, new_score)]
                else:
                    existing_paths.append((pos, v, new_score))

                heapq.heappush(moves, (new_score, new_pos, new_v))
        return min_final_score

    def backtrack(self, max_score: int) -> int:
        end_points = [(self.end, (1, 0)), (self.end, (-1, 0)), (self.end, (0, 1)), (self.end, (0, -1))]
        stack: List[Tuple[Coords, Coords, int]] = []
        for ep in end_points:
            stack += [p for p in self.paths.get(ep, []) if p[2] <= max_score]

        all_points: Set[Coords] = {self.end}
        visited: Set[Tuple[Coords, Coords, int]] = set()
        while stack:
            pos, v, score = stack.pop()
            # if pos == (3, 9):
            #     print("here")
            if pos == self.start:
                all_points.add(pos)
                continue
            all_points.add(pos)
            stored_paths = self.paths.get((pos, v), [])
            if not stored_paths:
                continue
            min_score = min([p[2] for p in stored_paths])
            if min_score >= score:
                continue
            stored_paths = [p for p in stored_paths if p[2] == min_score and p not in visited]
            visited.update(stored_paths)
            stack += stored_paths

        self.print({"o": all_points})
        return len(all_points)

        # # from the end to the start go following the
        # # self.visited cells:
        # # - the direction should be the opposite
        # # - the number should decrease by
        # def find_best_visited(pos: Coords, cur_score: int) -> Set[Tuple[int, Coords, Coords]]:
        #     if pos == (128, 13):
        #         all_spot = [(k, v) for k, v in self.visited.items() if k[0] == pos]
        #         lef_spot = [(k, v) for k, v in self.visited.items() if k[0] == (127, 13)]
        #         print("here")
        #
        #     best_score_pos: List[Tuple[int, Coords, Coords]] = []
        #     options = [((pos[0] - 1, pos[1]), (1, 0)),
        #                ((pos[0], pos[1] + 1), (0, -1)),
        #                ((pos[0] + 1, pos[1]), (-1, 0)),
        #                ((pos[0], pos[1] - 1), (0, 1)),
        #                (pos, (1, 0)), (pos, (-1, 0)), (pos, (0, 1)), (pos, (0, -1))]
        #
        #     for new_cell, new_v in options:
        #         if self._is_occupied(new_cell):
        #             continue
        #
        #         visited_score = self.visited.get((new_cell, new_v))
        #         if visited_score is not None:
        #             if visited_score < cur_score:
        #                 best_score_pos.append((visited_score, new_cell, new_v))
        #
        #     return set(best_score_pos)
        #
        # # score, pos, vector
        # visited_states = set()
        # tracks: Set[Tuple[int, Coords, Coords]] = find_best_visited(self.end, float('inf'))
        # all_points: Set[Coords] = {t[1] for t in tracks}
        #
        # while tracks:
        #     score, pos, v = tracks.pop()
        #     if (score, pos, v) in visited_states:
        #         continue
        #     visited_states.add((score, pos, v))
        #
        #     if pos == self.start:
        #         continue
        #
        #     next_points = find_best_visited(pos, score)
        #     for next_point in next_points:
        #         if next_point not in visited_states:
        #             tracks.add(next_point)
        #             all_points.add(next_point[1])
        #
        # self.print({"o": all_points})
        #
        # return len(all_points)

    def print(
            self,
            extra_points: Optional[Dict[str, Set[Coords]]] = None
    ) -> None:
        extra_points = extra_points or {}
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
                    cell_smb = cell
                    for s_extra, extra in extra_points.items():
                        if (x, y) in extra:
                            cell_smb = f"\033[95m{s_extra}\033[0m"
                            break
                    print(cell_smb, end="")
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

    def _is_occupied(self, p: Coords) -> bool:
        return self.matrix[p[1]][p[0]] == "#"


def solution_2():
    maze = Maze(FILE_PATH)
    # maze.print()
    solution = maze.solve()
    print(f"\nSolution: {solution}\n\n")
    best_points = maze.backtrack(solution)
    print(f"\nBacktrack: {best_points}\n\n")
    # 586 -> too high, 576 -> too high


if __name__ == "__main__":
    solution_2()
