from typing import List, Set, Tuple, Dict, Iterator, Optional

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day09/input.txt"

AddedBlock = Tuple[int, int]  # occupied pages, free pages


class FileBlock:
    def __init__(self, index: int, occupied_pages: int, free_pages: int):
        self.index = 0
        self.occupied_pages = occupied_pages
        self.free_pages = free_pages
        # [[index, pages], ...]
        self.added_blocks: List[AddedBlock] = []

    def __str__(self) -> str:
        s = f"{self.index}) [{self.occupied_pages}, {self.free_pages}]"
        if self.added_blocks:
            s += f" + {self.added_blocks}"
        return s

    def __repr__(self):
        return self.__str__()


class PageBlock:
    def __init__(self, file_index: Optional[int], start: int, count: int):
        self.file_index = file_index
        self.start = start
        self.count = count

    def __str__(self) -> str:
        return f"{self.file_index} -> [{self.start}) [{self.count}]"

    def __repr__(self):
        return self.__str__()


class FileSystem:
    def __init__(self, file_path: str):
        self._content: str = self._read_map(file_path)
        self._orig_blocks: List[FileBlock] = list(self._parse_map(self._content))
        for i, b in enumerate(self._orig_blocks):
            b.index = i

    def compact_file_map(self) -> List[int]:
        # build PageBlock-s
        blocks: List[PageBlock] = []
        cur_len = 0
        for i, file in enumerate(self._orig_blocks):
            blocks.append(PageBlock(i, cur_len, file.occupied_pages))
            cur_len += file.occupied_pages
            blocks.append(PageBlock(None, cur_len, file.free_pages))
            cur_len += file.free_pages

        # squeeze PageBlock-s
        right_index = len(blocks) - 1
        first_free_index = 0
        while right_index > 0:
            last_block = blocks[right_index]
            if last_block.file_index is None:
                right_index -= 1
                continue

            # find an empty block big enough to fit the last_block
            for j in range(first_free_index, right_index):
                if blocks[j].file_index is not None:
                    continue
                if blocks[j].count < last_block.count:
                    continue
                # move the last_block to the empty block
                if blocks[j].count == last_block.count:
                    # replace empty block with the last_block
                    blocks[j].file_index = last_block.file_index
                    last_block.file_index = None
                    # update the first free block index
                    for k in range(first_free_index, j + 1):
                        if blocks[k].file_index is None:
                            first_free_index = k
                            break
                else:
                    # split the empty block
                    blocks[j].count -= last_block.count
                    blocks.insert(j, PageBlock(last_block.file_index, blocks[j].start, last_block.count))
                    blocks[j].start += last_block.count
                    last_block.file_index = None
                break
            right_index -= 1

        # build a compacted map out of blocks
        sparse_map: List[int] = []
        for block in blocks:
            for i in range(block.count):
                sparse_map.append(block.file_index)
        return sparse_map



    @classmethod
    def hash_compact_map(cls, compact_map: List[int]) -> int:
        total = 0
        for i, n in enumerate(compact_map):
            if n is None:
                continue
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
            yield FileBlock(0, file_size, free_pages)


def solution_1():
    map = FileSystem(FILE_PATH)
    compact_map = map.compact_file_map()
    print(compact_map)
    compact_map_hash = map.hash_compact_map(compact_map)
    print(compact_map_hash)  # 6471961544878


if __name__ == "__main__":
    solution_1()
