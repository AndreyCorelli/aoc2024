from typing import List, Tuple, Optional

Operation = Tuple[int, int]

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day17/input.txt"


class Computer:
    def __init__(self):
        self.registers: List[int] = [0, 0, 0]
        self.program: List[Operation] = []
        self.program_string = ""
        self.pointer = 0
        self.output: List[int] = []
        self.verbose_log = False

    def read_program(self, file_path: str) -> None:
        self.registers = []
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("Register"):
                    self.registers.append(int(line.split(": ")[1]))
                elif line.startswith("Program: "):
                    line = line.strip("Program: ")
                    self.program_string = line
                    numbers = [int(n) for n in line.split(",")]
                    self.program = [(numbers[i], numbers[i + 1]) for i in range(0, len(numbers), 2)]
                    break

    def find_starting_value(self, start_value: int, stop_at: Optional[int] = None) -> None:
        msg_till_log, count_between_log = 0, 500000

        for i in range(start_value, stop_at or start_value + 2000000):
            msg_till_log -= 1
            if self.verbose_log and msg_till_log <= 0:
                print(f"Checking value: {i}")
                msg_till_log = count_between_log - 1

            self.registers = [0, 0, 0]
            self.registers[0] = i
            if self.execute_until_output_matches_program():
                print(f"Found starting value: {i}")
                return
        print(f"Nothing found between [{start_value}, {stop_at}]")

    def execute_until_output_matches_program(self) -> bool:
        self.pointer = 0
        self.output = []
        start_a_value = self.registers[0]

        output_str = ""
        last_output_length = 0
        while 0 <= self.pointer < len(self.program):
            self.pointer = self._perform_operation(self.program[self.pointer])
            if self.pointer < 0:
                return False
            # check the output
            if last_output_length < len(self.output):
                if output_str:
                    output_str += ","
                output_str += str(self.output[-1])
                if not self.program_string.startswith(output_str):
                    return False
                if len(self.output) > 6:
                    if self.verbose_log:
                        print(f"{output_str}..] -> for A={start_a_value}")
                    else:
                        print(start_a_value)
                last_output_length = len(self.output)
        return output_str == self.program_string

    def _perform_operation(self, operation: Operation) -> int:
        cmd, operand = operation
        if cmd == 0:
            # adv instruction: division
            numerator = self.registers[0]
            denominator = 2 ** self._get_combo_operand(operand)
            if denominator < 0:
                return -1
            result = numerator // denominator
            self.registers[0] = result
            return self.pointer + 1

        if cmd == 1:
            # bitwise xor
            a = self.registers[1]
            b = operand
            result = a ^ b
            self.registers[1] = result
            return self.pointer + 1

        if cmd == 2:
            # value of its combo operand modulo 8, then writes that value to the B register.
            a = self._get_combo_operand(operand)
            self.registers[1] = a % 8
            return self.pointer + 1

        if cmd == 3:
            """
            The jnz instruction (opcode 3) does nothing if the A register is 0. 
            However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; 
            if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
            """
            if self.registers[0] != 0:
                return operand
            return self.pointer + 1

        if cmd == 4:
            """
            The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, 
            then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
            """
            a = self.registers[1]
            b = self.registers[2]
            result = a ^ b
            self.registers[1] = result
            return self.pointer + 1

        if cmd == 5:
            """
            The out instruction (opcode 5) calculates the value of its combo operand modulo 8,
            then outputs that value. (If a program outputs multiple values, they are separated by commas.)
            """
            a = self._get_combo_operand(operand)
            a = a % 8
            self.output += [a]
            return self.pointer + 1

        if cmd == 6:
            """
            The bdv instruction (opcode 6) works exactly like the adv instruction except
            that the result is stored in the B register. (The numerator is still read from the A register.)
            """
            numerator = self.registers[0]
            denominator = 2 ** self._get_combo_operand(operand)
            if denominator < 0:
                return -1
            result = numerator // denominator
            self.registers[1] = result
            return self.pointer + 1

        if cmd == 7:
            """
            The cdv instruction (opcode 7) works exactly like the adv instruction except that
            the result is stored in the C register. (The numerator is still read from the A register.)
            """
            numerator = self.registers[0]
            denominator = 2 ** self._get_combo_operand(operand)
            if denominator < 0:
                return -1
            result = numerator // denominator
            self.registers[2] = result
            return self.pointer + 1


        return -1

    def _get_combo_operand(self, operand: int) -> int:
        return operand if operand < 4 else self.registers[operand - 4]

def solution_2():
    computer = Computer()
    computer.read_program(FILE_PATH)
    start = 0
    end = 8**10
    computer.find_starting_value(start, end)


if __name__ == "__main__":
    solution_2()
