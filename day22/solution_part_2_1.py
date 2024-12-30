from typing import List, Tuple, Dict

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day22/input.txt"


class HashSequence:
    def __init__(self, line: str):
        self.deltas: Dict[Tuple[int, ...], int] = {}
        self._read_from_line(line)

    def _read_from_line(self, line: str) -> None:
        nums = [int(x) for x in line.strip()]
        # list of diff nums[i] - nums[i-1]
        diff_seq = [b - a for a, b in zip(nums, nums[1:])]
        #diff_seq = [nums[0]] + diff_seq  # should I?
        for i in range(len(diff_seq) - 3):
            value = nums[i + 3 + 1]
            key = tuple(diff_seq[i:i + 4])
            if key not in self.deltas:
                self.deltas[key] = value

    @classmethod
    def read_from_multiline_file(cls, file_path: str) -> List["HashSequence"]:
        with open(file_path, "r") as file:
            return [cls(line) for line in file.readlines() if line.strip()]

    def filter_sequences(self, min_value: int) -> None:
        # leave only those with value >= min_value
        self.deltas = {k: v for k, v in self.deltas.items() if v >= min_value}

    @classmethod
    def maximize_bananas(cls, sequences: List["HashSequence"]) -> int:
        max_bananas = 0
        best_delta = None

        # get all unique deltas where the value is at least 1
        all_deltas: Dict[Tuple[int, ...], int] = {}

        for s in sequences:
            for key, val in s.deltas.items():
                stored = all_deltas.get(key, 0)
                all_deltas[key] = stored + val

        # find the best delta
        for key, val in all_deltas.items():
            if val > max_bananas:
                max_bananas = val
                best_delta = key

        print(f"Max bananas: {max_bananas} at delta {best_delta}")
        return max_bananas

def solution():
    sequences = HashSequence.read_from_multiline_file(FILE_PATH + ".pre")
    for seq in sequences:
        seq.filter_sequences(1)

    HashSequence.maximize_bananas(sequences)


if __name__ == "__main__":
    solution()  # 2211 - too low, 2218 - too low, 2232 - too high, 2227, 2219 - wrong
    # 2232 - too low, 2242 - too high, 2237 - low
    # Frame is: (2238..[-2239]..2241)
