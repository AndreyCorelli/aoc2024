import heapq
from typing import List, Tuple, Set

from day21.keyboard import BaseKeyboard, KeyboardDir, KeyboardDigital, ACTIONS, OPPOSITE_MOVES


OUTPUTS_TEST = "029A 980A 179A 456A 379A"
OUTPUTS_REAL = "964A 140A 413A 670A 593A"



class Pipeline:
    def __init__(self):
        self.keyboards: List[BaseKeyboard] = [
            KeyboardDir(), KeyboardDir(), KeyboardDigital(),
        ]

    def stringify_state(self) -> str:
        return "_".join(f"{k.pos[0],k.pos[1]}" for k in self.keyboards)

    def restore_state_from_string(self, s: str):
        for i, k in enumerate(self.keyboards):
            k.pos = tuple(map(int, s.split("_")[i].strip("()").split(",")))

    def process_action(self, a: str) -> Tuple[bool, str]:
        for k in self.keyboards:
            success, a = k.process_action(a)
            if not success:
                return False, ""
            if not a:
                return True, ""
        return True, a


def solve_output(output: str) -> int:
    # try random actions, until the last keyboard outputs the correct output
    visited: Set[str] = set()
    pipeline = Pipeline()

    # stack: input len - output len, input, output, state
    stack: List[Tuple[int, str, str, str]] = [(0, "", "", pipeline.stringify_state())]

    while stack:
        input_len, inp, out, state = heapq.heappop(stack)
        if out == output:
            return len(inp)

        last_action = inp[-1] if inp else ""
        for action in ACTIONS:
            opposite_move = OPPOSITE_MOVES.get(last_action)
            if opposite_move == action:
                continue

            new_input = inp + action
            if new_input in visited:
                continue
            visited.add(new_input)

            pipeline.restore_state_from_string(state)
            allowed, cur_out = pipeline.process_action(action)
            if not allowed:
                continue

            new_output = out + cur_out
            if new_output and not output.startswith(new_output):
                continue

            # if len(new_output) > 2:
            #     print(new_output)

            heapq.heappush(stack, (input_len + 1 - len(cur_out) * 99999999,
                                   new_input, new_output, pipeline.stringify_state()))

    return -1


def input_test():
    inp = "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"
    out = ""
    pipeline = Pipeline()
    for i in inp:
        _, cur_out = pipeline.process_action(i)
        out += cur_out
    print(f"Test output: {out}")


def solution():
    outputs = OUTPUTS_TEST.split(" ")
    outputs = [o.strip() for o in outputs if o.strip()]

    total = 0
    for i, output in enumerate(outputs):
        print(f"[{i + 1}] ({output})")
        a = int(output[:-1])
        b = solve_output(output)
        print(f"{a*b}")
        total += a * b

    print(f"Done {total}")


if __name__ == "__main__":
    solution()
