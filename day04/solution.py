from typing import Tuple


def read_file(file_path: str) -> Tuple[str, ...]:
    with open(file_path, "r") as file:
        return tuple([l.strip() for l in file.readlines()])


def calculate_word_count(file_path: str) -> int:
    lines = read_file(file_path)
#     lines = """
# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX""".strip().split("\n")

    word, reverse = "XMAS", "SAMX"
    w, h = len(lines[0]), len(lines)
    word_len = len(word)
    count = 0

    # calculate horizontal entries
    for i, line in enumerate(lines):
        for j in range(len(line) - word_len + 1):
            if line[j:j + len(word)] == word:
                count += 1
            if line[j:j + len(reverse)] == reverse:
                count += 1

    # calculate vertical entries
    for i in range(w):
        for j in range(h - word_len + 1):
            if "".join([lines[j + k][i] for k in range(word_len)]) == word:
                count += 1
            if "".join([lines[j + k][i] for k in range(word_len)]) == reverse:
                count += 1

    # calculate diagonal entries - top left to bottom right
    for i in range(w - word_len + 1):
        for j in range(h - word_len + 1):
            if "".join([lines[j + k][i + k] for k in range(word_len)]) == word:
                count += 1
            if "".join([lines[j + k][i + k] for k in range(word_len)]) == reverse:
                count += 1

    # calculate diagonal entries - top right to bottom left
    for i in range(w - word_len + 1):
        for j in range(h - word_len + 1):
            if "".join([lines[j + k][i + word_len - k - 1] for k in range(word_len)]) == word:
                count += 1
            if "".join([lines[j + k][i + word_len - k - 1] for k in range(word_len)]) == reverse:
                count += 1

    return count

def calculate_cross_word_count(file_path: str) -> int:
    lines = read_file(file_path)
#     lines = """
# .M.S......
# ..A..MSMS.
# .M.S.MAA..
# ..A.ASMSM.
# .M.S.M....
# ..........
# S.S.S.S.S.
# .A.A.A.A..
# M.M.M.M.M.
# ..........""".strip().split("\n")
    w, h = len(lines[0]), len(lines)
    count_crosses = 0

    for i in range(h - 2):
        for j in range(w - 2):
            if lines[i][j] == "M" and lines[i][j + 2] == "M":
                if lines[i + 1][j + 1] == "A":
                    if lines[i + 2][j] == "S" and lines[i + 2][j + 2] == "S":
                        count_crosses += 1
            if lines[i][j] == "S" and lines[i][j + 2] == "S":
                if lines[i + 1][j + 1] == "A":
                    if lines[i + 2][j] == "M" and lines[i + 2][j + 2] == "M":
                        count_crosses += 1
            if lines[i][j] == "M" and lines[i][j + 2] == "S":
                if lines[i + 1][j + 1] == "A":
                    if lines[i + 2][j] == "M" and lines[i + 2][j + 2] == "S":
                        count_crosses += 1
            if lines[i][j] == "S" and lines[i][j + 2] == "M":
                if lines[i + 1][j + 1] == "A":
                    if lines[i + 2][j] == "S" and lines[i + 2][j + 2] == "M":
                        count_crosses += 1

    return count_crosses

if __name__ == "__main__":
    file_path = "/Users/andreisitaev/sources/sennder/aoc2024/day04/input.txt"
    print(calculate_cross_word_count(file_path))
