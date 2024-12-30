import heapq
from typing import List, Tuple, Set, Dict, Optional

from day21.keyboard import KEYBOARD_LAYOUT_DIR, KEYBOARD_LAYOUT_DIGITAL, Coords, KeyboardLayout

OUTPUTS_TEST = "029A 980A 179A 456A 379A"
OUTPUTS_REAL = "964A 140A 413A 670A 593A"


class Keyboard:
    def __init__(self, index: int, layout: KeyboardLayout):
        self.index = index
        self.layout = layout

    def get_possible_paths_count(self, s: str, e: str) -> int:
        return len(self.layout.path_to_symbol.get((s, e), []))


class DfsSolver:
    def __init__(self, dir_keyboards_count: int):
        self.cache: Dict[Tuple[str, int], int] = {}
        self.pipeline = [KEYBOARD_LAYOUT_DIR] * dir_keyboards_count + [KEYBOARD_LAYOUT_DIGITAL]
        self.keyboard_last_pos: List[Tuple[Coords]] = []

    def get_possible_paths_count(self, seq: str, keyboard_index: Optional[int] = None) -> int:
        keyboard_index = keyboard_index if keyboard_index is not None else len(self.pipeline) - 1
        # TODO: cache it
        layout = self.pipeline[keyboard_index]
        if keyboard_index == 0:
            # this is the keyboard I'm pressing
            total_options = 0

            start_smb = "A"  # for both layouts the pointer is over A first
            # from start pos to the following pos to the following pos ...
            for smb in seq:
                start_pos, end_pos = layout.coords_by_key[start_smb], layout.coords_by_key[smb]
                options = layout.path_to_symbol[(start_pos, end_pos)]
                # no matter which path to choose - all of them have the same length
                total_options += len(options[0])
                start_smb = smb
            return total_options

        length = 0
        start_smb = "A"  # for both layouts the pointer is over A first
        for smb in seq:
            start_pos, end_pos = layout.coords_by_key[start_smb], layout.coords_by_key[smb]
            paths = layout.path_to_symbol[(start_pos, end_pos)]
            start_smb = smb

            min_path_length = float("inf")
            for path in paths:
                path_len = self.get_possible_paths_count(path, keyboard_index - 1)
                min_path_length = min(min_path_length, path_len)
            if min_path_length == float("inf"):
                raise Exception(f"Path from {start_pos}({start_smb}) to {end_pos}({smb}) not found")
            length += min_path_length
        return length


def solution():
    outputs = OUTPUTS_REAL.split(" ")
    outputs = [o.strip() for o in outputs if o.strip()]

    for layout in (KEYBOARD_LAYOUT_DIR, KEYBOARD_LAYOUT_DIGITAL):
        layout.populate_all_paths_to_symbols()

    total = 0
    solver = DfsSolver(25)
    for i, output in enumerate(outputs):
        print(f"[{i + 1}] ({output})")
        ln = solver.get_possible_paths_count(output)
        num = int(output[:-1])
        total += ln * num

    print(f"Done {total}")


if __name__ == "__main__":
    solution()
