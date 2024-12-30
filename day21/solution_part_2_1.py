import heapq
from typing import List, Tuple, Set

from day21.keyboard import BaseKeyboard, KeyboardDir, KeyboardDigital, ACTIONS, OPPOSITE_MOVES, Coords, \
    KEYBOARD_LAYOUT_DIGITAL, KEYBOARD_LAYOUT_DIR

OUTPUTS_TEST = "029A 980A 179A 456A 379A"
OUTPUTS_REAL = "964A 140A 413A 670A 593A"



class Pipeline:
    def __init__(self):
        self.keyboards: List[BaseKeyboard] = [
            KeyboardDir() for _ in range(26)
        ]
        self.keyboards += [KeyboardDigital()]
        self.keyboards.reverse()


class KeyboardRouter:
    def __init__(self):
        self.pipeline = Pipeline()

    def solve_output(self, output: str) -> int:
        overall_input = ""

        for o_char in output:
            cur_pattern = o_char
            print(f"Processing {cur_pattern}")
            for i, kb in enumerate(self.pipeline.keyboards):
                print(f"Keyboard {i} ...")
                success, cur_pattern = self._find_shortest_input(kb, cur_pattern)
                assert success, f"Failed to find input for {cur_pattern}"
            overall_input += cur_pattern

        a = int(output[:-1])
        b = len(overall_input)
        return a * b

    def _find_shortest_input(self, kb: BaseKeyboard, desired_output: str) -> Tuple[bool, str]:
        # kb is in the current state (pos)
        # we're searching for the shortest sequence to get the desired_output
        visited: Set[str] = set()

        # score - input - current output - kb pos
        stack: List[Tuple[int, str, str, Coords]] = [(0, "", "", kb.pos)]
        while stack:
            score, inp, out, pos = heapq.heappop(stack)
            kb.pos = pos
            if out == desired_output:
                return True, inp

            last_action = inp[-1] if inp else ""
            for action in ACTIONS:
                opposite_move = OPPOSITE_MOVES.get(last_action)
                if opposite_move == action:
                    continue

                new_input = inp + action
                if new_input in visited:
                    continue
                visited.add(new_input)

                success, cur_out = kb.process_action(action)
                if not success:
                    continue

                score = len(new_input) - len(cur_out) * 100
                heapq.heappush(stack, (score, new_input, cur_out, kb.pos))

        return False, ""


def solution():
    KEYBOARD_LAYOUT_DIGITAL.populate_all_paths_to_symbols()
    KEYBOARD_LAYOUT_DIR.populate_all_paths_to_symbols()
    print("All layouts' paths populated")

    outputs = OUTPUTS_TEST.split(" ")
    outputs = [o.strip() for o in outputs if o.strip()]

    total = 0
    for i, output in enumerate(outputs):
        print(f"[{i + 1}] ({output})")
        router = KeyboardRouter()
        result = router.solve_output(output)
        print(result)
        total += result
    print(f"Done {total}")


if __name__ == "__main__":
    solution()
