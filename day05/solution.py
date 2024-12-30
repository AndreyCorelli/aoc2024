from typing import Tuple, List, Dict, Set


def parse_file(file_path: str) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
    with open(file_path, 'r') as file:
        content = file.read().strip()
        sections = content.split("\n\n")

        if len(sections) != 2:
            raise ValueError("File content format is incorrect.")

        section_1 = sections[0].splitlines()
        tuples_list = [tuple(map(int, line.split('|'))) for line in section_1]

        section_2 = sections[1].splitlines()
        lists_of_integers = [list(map(int, line.split(','))) for line in section_2]

    return tuples_list, lists_of_integers


def solve_part_1(file_path: str):
    orders, plans = parse_file(file_path)
    precedencs = {a: set() for a, _ in orders}
    for a, b in orders:
        precedencs[a].add(b)

    result = 0
    for plan in plans:
        if _is_plan_correct(plan, precedencs):
            result += plan[int(len(plan) / 2)]

    return result

def _is_plan_correct(plan: List[int], precedencs: Dict[int, Set[int]]) -> bool:
    for i in range(1, len(plan)):
        current_prerequisites = precedencs.get(plan[i])
        if current_prerequisites:
            for j in range(i):
                if plan[j] in current_prerequisites:
                    return False
    return True


def solve_part_2(file_path: str):
    orders, plans = parse_file(file_path)
    precedencs = {a: set() for a, _ in orders}
    for a, b in orders:
        precedencs[a].add(b)

    result = 0
    for plan in plans:
        if _is_plan_correct(plan, precedencs):
            continue
        plan = _fix_plan(plan, precedencs)
        result += plan[int(len(plan) / 2)]

    return result


def _fix_plan(plan: List[int], precedencs: Dict[int, Set[int]]) -> List[int]:
    while True:
        in_order = True
        for i in range(1, len(plan)):
            current_prerequisites = precedencs.get(plan[i])
            if not current_prerequisites:
                continue
            for j in range(i):
                if plan[j] in current_prerequisites:
                    in_order = False
                    plan[i], plan[j] = plan[j], plan[i]
                    break
        if in_order:
            break
    return plan


if __name__ == "__main__":
    file_path = "/Users/andreisitaev/sources/sennder/aoc2024/day05/input.txt"
    print(solve_part_2(file_path))  # expected: 123
