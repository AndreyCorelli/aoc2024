def get_lists_distance(a, b):
    a.sort()
    b.sort()
    distance = 0
    for i in range(len(a)):
        distance += abs(a[i] - b[i])
    return distance

def get_lists_hash(a, b):
    b_hash = {}
    for i in b:
        count = b_hash.get(i, 0)
        b_hash[i] = count + 1

    hsh = 0
    for i in a:
        hsh += b_hash.get(i, 0) * i
    return hsh


def read_lists_from_file(file_path):
    a_list, b_list = [], []
    with open(file_path, "r") as file:
        for line in file.readlines():
            line = line.strip()
            if not line:
                continue
            a, b = line.split()
            a_list.append(int(a))
            b_list.append(int(b))
    return a_list, b_list

def test_lists():
    path = "/Users/andreisitaev/sources/sennder/aoc2024/day01/input.txt"
    a_list, b_list = read_lists_from_file(path)
    print(get_lists_hash(a_list, b_list))


if __name__ == "__main__":
    test_lists()
