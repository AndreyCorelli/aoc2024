from typing import List, Tuple, Optional, Set

Operation = Tuple[int, int]

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day17/input.txt"


class Computer:
    def __init__(self):
        self.program = [2,4,1,2,7,5,0,3,4,7,1,7,5,5,3,0]
        self.min_a = 8**17
        self.cache: Set[Tuple[int, int]] = set()

    def calc_output(self, a: int) -> Optional[int]:
        b = a % 8         # 2, 4
        b = b ^ 2         # 1, 2
        c = a // (2 ** b) # 7, 5
        a = a // 8        # 0, 3
        b = b ^ c         # 4, 7
        b = b ^ 7         # 1, 7
        output = b % 8    # 5, 5
        # 3, 0 is the loop's exit condition, don't need to check it
        return output

    def dfs(self, a: int, step: int) -> None:
        if (a, step) in self.cache:
            return
        a = a * 8
        cur_output = self.program[step]

        for i in range(8):
            new_a = a + i
            output = self.calc_output(new_a)
            if output == cur_output:
                if step == 0:
                    print(f"Found A: {new_a}")
                    if new_a < self.min_a:
                        self.min_a = new_a
                else:
                    self.dfs(new_a, step - 1)
        self.cache.add((a, step))


def solution_2():
    computer = Computer()
    computer.dfs(0, len(computer.program) - 1)
    min_suitable = computer.min_a
    print(f"Min suitable A: {min_suitable}")  # 190384113204239


if __name__ == "__main__":
    solution_2()
