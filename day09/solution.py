from typing import List, Set, Tuple, Dict, Iterator

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day09/input.txt"

FileBlock = Tuple[int, int]  # occupied pages, free pages


class FileSystem:
    def __init__(self, file_path: str):
        self._content: str = self._read_map(file_path)
        self._orig_blocks: List[FileBlock] = list(self._parse_map(self._content))

    def compact_file_map(self) -> List[int]:
        sparse_map = []
        for i, block in enumerate(self._orig_blocks):
            sparse_map += [i] * block[0]
            sparse_map += [None] * block[1]
        # compact map by moving numbers to the left
        left_index, right_index = 0, len(sparse_map) - 1
        while left_index <= right_index:
            if sparse_map[left_index] is not None:
                left_index += 1
                continue
            if sparse_map[right_index] is None:
                right_index -= 1
                continue

            sparse_map[left_index], sparse_map[right_index] = sparse_map[right_index], sparse_map[left_index]
            left_index += 1
            right_index -= 1

        return sparse_map

    @classmethod
    def hash_compact_map(cls, compact_map: List[int]) -> int:
        total = 0
        for i, n in enumerate(compact_map):
            if n is None:
                break
            total += n * i
        return total

    @classmethod
    def _read_map(cls, file_path: str) -> str:
        with open(file_path, 'r') as file:
            return file.read()

    @classmethod
    def _parse_map(cls, content: str) -> Iterator[FileBlock]:
        blocks_count = len(content) // 2
        if len(content) % 2 != 0:
            blocks_count += 1
        for i in range(blocks_count):
            file_size = int(content[i * 2])
            free_pages = int(content[i * 2 + 1]) if i * 2 + 1 < len(content) else 0
            yield file_size, free_pages


def solution_1():
    map = FileSystem(FILE_PATH)
    compact_map = map.compact_file_map()
    print(compact_map)
    compact_map_hash = map.hash_compact_map(compact_map)
    print(compact_map_hash)  # 6471961544878


if __name__ == "__main__":
    solution_1()
