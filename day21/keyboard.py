import heapq
from typing import Tuple, Dict, Optional, List, Set

Coords = Tuple[int, int]

LAYOUT_DIGITAL_S = "7:0,0; 8:1,0; 9:2,0; 4:0,1; 5:1,1; 6:2,1; 1:0,2; 2:1,2; 3:2,2; G:0,3; 0:1,3; A:2,3"
LAYOUT_DIR_S = "G:0,0; ^:1,0; A:2,0; <:0,1; v:1,1; >:2,1"
MOVE_BY_DIR = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}

ACTIONS = ["v", ">", "^", "<", "A"]
OPPOSITE_MOVES = {
    "^": "v",
    "v": "^",
    "<": ">",
    ">": "<",
}


class KeyboardLayout:
    def __init__(self, s: str):
        # s = "A:0,0\nB:0,1\nC:0,2\nD:1,0\nE:1,1\nF:1,2\nG:2,0\nH:2,1\nI:2,2"
        key_strings = s.replace("\n", ";").replace(" ", "").split(";")
        self.coords_by_key: Dict[str, Coords] = {
            key: tuple(map(int, coords.split(",")))
            for key, coords in [pair.split(":") for pair in key_strings]
        }
        self.key_by_coords: Dict[Coords, str] = {
            coords: key
            for key, coords in self.coords_by_key.items()
        }
        self.w = max(x for x, y in self.coords_by_key.values()) + 1
        self.h = max(y for x, y in self.coords_by_key.values()) + 1
        self.g_pos = self.coords_by_key["G"]
        self.initial_pos = self.coords_by_key["A"]
        # we never need to reach G
        self.symbols = set([v for v in self.key_by_coords.values() if v != "G"])

        # path_to_symbol: (symbol, pos): [input_str, ...]
        # (start_smb, end_smb): [path_1, path_2, ...]}
        self.path_to_symbol: Dict[Tuple[str, str], List[str]] = {}

    def populate_all_paths_to_symbols(self) -> None:
        for s in self.symbols:
            for e in self.symbols:
                self._populate_path_to_symbol(s, e)

    def _populate_path_to_symbol(self, s: str, e: str) -> None:
        # how to reach symbol e from s
        self.path_to_symbol[(s, e)] = []
        visited: Set[str] = set()

        shortest_path = 999999
        end_coords = self.coords_by_key[e]

        # path len - cur pos - cur input
        stack: List[Tuple[int, Coords, str]] = [(0, self.coords_by_key[s], "")]
        while stack:
            path_len, cur_pos, cur_path = heapq.heappop(stack)
            if path_len > shortest_path:
                continue
            if cur_pos == end_coords:
                shortest_path = path_len
                self.path_to_symbol[(s, e)].append(cur_path + "A")
                continue

            for action in ACTIONS[:-1]:
                dx, dy = MOVE_BY_DIR[action]
                new_pos = cur_pos[0] + dx, cur_pos[1] + dy
                if not self.is_valid_coords(new_pos):
                    continue

                new_path = cur_path + action
                if new_path in visited:
                    continue
                visited.add(new_path)
                heapq.heappush(stack, (path_len + 1, new_pos, new_path))

    def is_valid_coords(self, coords: Coords) -> bool:
        x, y = coords
        return (0 <= x < self.w and 0 <= y < self.h) and (x, y) != self.g_pos

KEYBOARD_LAYOUT_DIGITAL = KeyboardLayout(LAYOUT_DIGITAL_S)
KEYBOARD_LAYOUT_DIR = KeyboardLayout(LAYOUT_DIR_S)


class BaseKeyboard:
    def __init__(self, layout: KeyboardLayout):
        self.layout = layout
        self.pos = layout.initial_pos
        self.output = ""

    def process_action(self, a: str) -> Tuple[bool, str]:
        # a could be <. >, ^, v, or A (action)
        # return None if action is deprecated (hover over G)
        if a == "A":
            btn = self.layout.key_by_coords[self.pos]
            self.output += btn
            return True, btn

        dx, dy = MOVE_BY_DIR[a]
        nx, ny = self.pos[0] + dx, self.pos[1] + dy
        if not self.layout.is_valid_coords((nx, ny)):
            return False, ""
        self.pos = (nx, ny)
        return True, ""


class KeyboardDigital(BaseKeyboard):
    def __init__(self):
        super().__init__(KEYBOARD_LAYOUT_DIGITAL)


class KeyboardDir(BaseKeyboard):
    def __init__(self):
        super().__init__(KEYBOARD_LAYOUT_DIR)
