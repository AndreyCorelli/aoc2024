from typing import List, Tuple, Dict

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
        self.start_keyboard_index = len(self.pipeline) - 1
        self.keyboard_last_pos: List[Tuple[Coords]] = []

    def get_possible_paths_count(self, seq: str) -> int:
        return self._get_possible_paths_count(seq, self.start_keyboard_index)

    def _get_possible_paths_count(self, seq: str, keyboard_index: int) -> int:
        cache_key = (seq, keyboard_index)
        if cache_key in self.cache:
            return self.cache[cache_key]
        result = self._get_possible_paths_count_impl(seq, keyboard_index)
        self.cache[cache_key] = result
        return result

    def _get_possible_paths_count_impl(self, seq: str, keyboard_index: int) -> int:
        layout = self.pipeline[keyboard_index]
        if keyboard_index == 0:
            # this is the keyboard I'm pressing
            total_options = 0

            start_smb = "A"  # for both layouts the pointer is over A first
            for smb in seq:
                options = layout.path_to_symbol[(start_smb, smb)]
                total_options += len(options[0])
                start_smb = smb
            return total_options

        length = 0
        start_smb = "A"  # for both layouts the pointer is over A first
        for smb in seq:
            paths = layout.path_to_symbol[(start_smb, smb)]
            start_smb = smb

            min_path_length = float("inf")
            for path in paths:
                path_len = self._get_possible_paths_count(path, keyboard_index - 1)
                min_path_length = min(min_path_length, path_len)
            length += min_path_length
        return length


def solution():
    outputs = OUTPUTS_REAL.split(" ")
    outputs = [o.strip() for o in outputs if o.strip()]

    for layout in (KEYBOARD_LAYOUT_DIR, KEYBOARD_LAYOUT_DIGITAL):
        layout.populate_all_paths_to_symbols()

    total = 0
    # cool thing I don't have to clean the cache - the further, the faster
    solver = DfsSolver(25)
    for i, output in enumerate(outputs):
        print(f"[{i + 1}] ({output})")
        ln = solver.get_possible_paths_count(output)
        num = int(output[:-1])
        total += ln * num

    print(f"Done {total}")


if __name__ == "__main__":
    solution()
