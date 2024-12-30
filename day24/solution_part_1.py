from day07.solution import FILE_PATH
from day24.solution_base import Circuit

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day24/input.txt"


def solve():
    circuit = Circuit()
    circuit.read_from_file(FILE_PATH)
    circuit.compute()
    z_values = [(k, v) for k, v in circuit.inputs.items() if k.startswith("z")]
    z_values.sort(reverse=True)

    vector = "".join([str(int(v)) for k, v in z_values])
    dec_value = int(vector, 2)
    print(f"Done: {dec_value} ({vector})")


if __name__ == "__main__":
    solve()
