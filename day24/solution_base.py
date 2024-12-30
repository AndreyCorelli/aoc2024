from typing import Dict, List, Optional

OPERATIONS = {
    "AND": lambda a, b: a and b,
    "OR": lambda a, b: a or b,
    "XOR": lambda a, b: a ^ b
}


def binary_to_int(x: List[int]) -> int:
    return int("".join([str(i) for i in x]), 2)


class Operation:
    def __init__(self, a: str, b: str, out_code: str, operation_code: str):
        self.a = a
        self.b = b
        self.out_code = out_code
        self.operation_code = operation_code
        self.operation = OPERATIONS[operation_code]

    def __str__(self):
        return f"{self.a} {self.operation_code} {self.b} -> {self.out_code}"

    def __repr__(self):
        return str(self)

    def compute(self, a_value: bool, b_value: bool) -> bool:
        return self.operation(a_value, b_value)


class Circuit:
    def __init__(self):
        self.wires: Dict[str, bool] = {}
        self.operations: List[Operation] = []
        # mix of wires and operations' inputs
        self.inputs: Dict[str, Optional[bool]] = {}
        self.operations_ordered: List[List[Operation]] = []
        self.input_overrides: Dict[str, Optional[bool]] = {}

    def read_from_file(self, file_path: str):
        with open(file_path) as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if " -> " in line:
                    operation, out_code = line.split(" -> ")
                    a, operation_code, b = operation.split(" ")
                    self.operations.append(Operation(a, b, out_code, operation_code))
                else:
                    wire_code, wire_value = line.split(": ")
                    self.wires[wire_code] = True if wire_value == "1" else False
        # define inputs
        self.inputs = {**self.wires}

    def sort_operations(self) -> None:
        unsorted_ops = self.operations.copy()
        clusters: List[List[Operation]] = []
        allowed_inputs = set(self.inputs.keys())

        while unsorted_ops:
            cluster = []
            for op in unsorted_ops:
                if op.a in allowed_inputs and op.b in allowed_inputs:
                    cluster.append(op)
            if not cluster:
                break
            clusters.append(cluster)
            for op in cluster:
                unsorted_ops.remove(op)
                allowed_inputs.add(op.out_code)

        self.operations_ordered = clusters

    def compute(self) -> None:
        self.sort_operations()
        for cluster in self.operations_ordered:
            for operation in cluster:
                a_value = self.input_overrides.get(operation.a,
                    self.inputs[operation.a])
                b_value = self.input_overrides.get(operation.b,
                                         self.inputs[operation.b])
                self.inputs[operation.out_code] = operation.compute(a_value, b_value)

    def get_binary_value(self, prefix: str, reverse: bool = False) -> List[int]:
        key_val = [(k, v) for k, v in self.inputs.items() if k.startswith(prefix)]
        key_val.sort(reverse=reverse)
        return [int(v) for k, v in key_val]

    def set_inputs(self, x_bits: List[int], y_bits: List[int]) -> None:
        # cleanup inputs before setting new values
        self.inputs = {}
        for i, bit in enumerate(x_bits):
            self.inputs[f"x{i:02d}"] = bool(bit)
        for i, bit in enumerate(y_bits):
            self.inputs[f"y{i:02d}"] = bool(bit)

    def get_value_by_out_names(self, out_names: List[str]) -> List[int]:
        return [int(self.inputs[name]) for name in out_names]