from typing import List, Tuple

Operation = Tuple[int, int]

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day17/input.txt"


class Computer:
    def __init__(self):
        self.registers: List[int] = [0, 0, 0]
        self.program: List[Operation] = []
        self.pointer = 0
        self.output: List[int] = []

    def read_program(self, file_path: str) -> None:
        """
        file contains the following:
        Register A: 30878003
        Register B: 0
        Register C: 0

        Program: 2,4,1,2,7,5,0,3,4,7,1,7,5,5,3,0
        """
        self.registers = []
        with open(file_path) as f:
            for line in f:
                if line.startswith("Register"):
                    self.registers.append(int(line.split(": ")[1]))
                elif line.startswith("Program: "):
                    line = line.strip("Program: ")
                    numbers = [int(n) for n in line.split(",")]
                    self.program = [(numbers[i], numbers[i + 1]) for i in range(0, len(numbers), 2)]
                    break
        #self.registers[0] = 190384113204239

    def execute(self) -> None:
        self.output = []
        while 0 <= self.pointer < len(self.program):
            self.pointer = self._perform_operation(self.program[self.pointer])
        print("Done")
        print(f"Output: {','.join([str(n) for n in self.output])}")

    def _perform_operation(self, operation: Operation) -> int:
        cmd, operand = operation
        if cmd == 0:
            # adv instruction: division
            numerator = self.registers[0]
            denominator = 2 ** self._get_combo_operand(operand)
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
            result = numerator // denominator
            self.registers[2] = result
            return self.pointer + 1


        return self.pointer + 1

    def _get_combo_operand(self, operand: int) -> int:
        return operand if operand < 4 else self.registers[operand - 4]

def solution_1():
    computer = Computer()
    computer.read_program(FILE_PATH)
    computer.execute()


if __name__ == "__main__":
    solution_1()
