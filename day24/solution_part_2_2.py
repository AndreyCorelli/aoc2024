from typing import Dict, Optional, Tuple, List

from day07.solution import FILE_PATH
from day24.solution_base import Circuit, binary_to_int, Operation

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day24/input.txt"


circuit = Circuit()
circuit.read_from_file(FILE_PATH)
circuit.sort_operations()
ALL_OP_OUT_NAMES = [op.out_code for op in circuit.operations]


SIZE = 45  # 46 for z


def check_digits():
    carry_sign_name = None
    for i in range(SIZE):
        carry_sign_name = check_digit(i, carry_sign_name)


def bit_sum(x: int, y: int, c: int) -> Tuple[int, int]:
    sp = x ^ y
    s = sp ^ c
    c1 = x and y
    c2 = sp and c
    c_out = c1 or c2
    return s, c_out

"""
Anomaly while searching a candidate for 
z39: x39 AND y39 -> z39-s 'c': wrong operation

(x40 XOR y40) XOR nhk -> z40
C[38] = (jct OR hvf) -> nhk
"""

def check_digit(i: int, carry_sign_name: Optional[str]) -> str:
    z_name = f"z{i:02d}"
    z_oper = [op for op in circuit.operations if op.out_code == z_name][0]
    print(f"Checking z[{i:02d}] ({z_oper}) = f(c[{i:02d}]={carry_sign_name}, x[{i:02d}], y[{i:02d}])")

    # from the very beginning we'll check the next operation
    # one of the candidates should be the (XOR) input for the next digit
    next_z = f"z{(i + 1):02d}"
    next_z_op: Optional[Operation] = None
    for op in circuit.operations:
        if op.out_code == next_z:
            next_z_op = op
            break
    if next_z_op.operation_code != "XOR":
        raise Exception(f"Anomaly while searching a candidate for {next_z}: {next_z_op}-s 'c': wrong operation")
    print(f"... {next_z}: {next_z_op}")

    c_range = [0, 1]
    if i == 0:
        c_range = [0]

    checked_vectors: List[List[int]] = []
    x_bits = [0] * SIZE
    y_bits = [0] * SIZE

    for c in c_range:
        for x in [0, 1]:
            for y in [0, 1]:
                if i > 0:
                    x_bits[i - 1] = c
                    y_bits[i - 1] = c
                x_bits[i] = x
                y_bits[i] = y
                circuit.set_inputs(x_bits, y_bits)
                # I can achieve the carry over = 1 this way (doesn't work??):
                # circuit.input_overrides = {carry_sign_name: bool(c)}
                # or by setting prev digit to 1

                # check correctness: z[i] = f(c[i], x[i], y[i])
                circuit.compute()
                z_val = int(circuit.inputs[z_name])
                s, c_out = bit_sum(x, y, c)
                if s != z_val:
                    raise Exception(f"Anomaly: {z_oper} = f({carry_sign_name}, x[{i:02d}], y[{i:02d}]): "
                                    f"({c}, {x}, {y}) -> {z_val}")
                checked_vectors.append(circuit.get_value_by_out_names(ALL_OP_OUT_NAMES))

    # find carry sign
    if i == SIZE - 1:
        return ""  # don't care about last carry sign

    # a vertical cut of vectors should be 00010111 (only vertical)
    exp_c_values = [0, 0, 0, 1, 0, 1, 1, 1]
    if i == 0:
        exp_c_values = [0, 0, 0, 1]

    candidates: List[str] = []
    for op_index, o in enumerate(ALL_OP_OUT_NAMES):
        is_candidate = True
        for iv, c in enumerate(exp_c_values):
            if checked_vectors[iv][op_index] != c:
                is_candidate = False
                break
        if is_candidate:
            candidates.append(o)

    if len(candidates) == 0:
        raise Exception(f"Anomaly: no candidates found")

    candidate = None

    for c in candidates:
        if c in next_z_op.a or c in next_z_op.b:
            candidate = c
            break

    if not candidates:
        raise Exception(f"None of the potential candidates ({candidates}) "
                        f"found in {next_z_op}")
    return candidate


def solve():
    check_digits()


if __name__ == "__main__":
    solve()
