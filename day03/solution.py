import re


def process_file(file_path: str):
    with open(file_path, 'r') as file:
        content = file.read()
    # content = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, content)

    total_sum = 0
    for match in matches:
        num1, num2 = map(int, match)
        product = num1 * num2
        total_sum += product

    print(f"Total: {total_sum}")  # 157621318


def process_file_2(file_path: str):
    with open(file_path, 'r') as file:
        content = file.read()
    #content = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

    entries_by_index = []

    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.finditer(pattern, content)
    for match in matches:
        num1, num2 = map(int, match.groups())
        start_index = match.start()
        product = num1 * num2
        entries_by_index.append((start_index, product,))

    pattern = r"do()"
    matches = re.finditer(pattern, content)
    for match in matches:
        start_index = match.start()
        entries_by_index.append((start_index, True,))

    pattern = r"don\'t\(\)"
    matches = re.finditer(pattern, content)
    for match in matches:
        start_index = match.start()
        entries_by_index.append((start_index, False,))

    entries_by_index.sort(key=lambda entry: entry[0])
    op_allowed, total = True, 0
    for index, entry in entries_by_index:
        if entry is True:
            op_allowed = True
            continue
        if entry is False:
            op_allowed = False
            continue
        if op_allowed:
            total += entry

    print(f"Total: {total}")  # 157621318



if __name__ == "__main__":
    path = "/Users/andreisitaev/sources/sennder/aoc2024/day03/input.txt"
    process_file_2(path)
