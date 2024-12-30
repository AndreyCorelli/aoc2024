from typing import Dict

from day07.solution import FILE_PATH
from day24.solution_base import Circuit, binary_to_int, Operation

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day24/input.txt"

# new operation name -> orig operation name
new_to_orig: Dict[str, str] = {}

circuit = Circuit()
circuit.read_from_file(FILE_PATH)


def rename_inputs():
    for op in circuit.operations:
        a, b = op.a[0], op.b[0]
        if a == "y" and b == "x":
            op.a, op.b = op.b, op.a

        # case 1: x ^ y -> w[i]
        if op.operation_code == "XOR":
            if op.a.startswith("x") and op.b.startswith("y"):
                x_index, y_index = int(op.a[1:]), int(op.b[1:])
                if x_index != y_index:
                    raise Exception(f"Anomaly: {op} - mixed indices")
                new_op_out = f"w{x_index:02d}"
                new_to_orig[new_op_out] = op.out_code
                op.out_code = new_op_out

        # case 2: x & y -> v[i]
        if op.operation_code == "AND":
            if op.a.startswith("x") and op.b.startswith("y"):
                x_index, y_index = int(op.a[1:]), int(op.b[1:])
                if x_index != y_index:
                    raise Exception(f"Anomaly: {op} - mixed indices")
                new_op_out = f"v{x_index:02d}"
                new_to_orig[new_op_out] = op.out_code
                op.out_code = new_op_out


def check_carry_out():
    # carry out to the next digit is  OR(v[i], AND[w[i], c[i-1]])
    for op in circuit.operations:
        a, b = op.a[0], op.b[0]
        if b == "v" and a != "v":
            op.a, op.b = op.b, op.a

        # that's also the only OR operation
        if op.operation_code != "OR":
            continue

        if a != "v":
            raise Exception(f"Anomaly: {op} - OR should be (v, AND(w, cin))")


def solve():
    rename_inputs()
    check_carry_out()




if __name__ == "__main__":
    solve()
