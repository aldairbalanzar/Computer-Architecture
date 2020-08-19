"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

    def load(self, filename):
        """Load a program into memory."""
        filename = sys.argv[1]
        try:
            address = 0
            with open(filename) as file:
                for line in file:
                    split_line = line.split('#')[0]
                    command = split_line.strip()
                    if command:
                        instruction = int(command, 2)
                        # print(f'{instruction:8b} is {instruction}')
                        self.ram[address] = instruction
                        address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file not found.')
            sys.exit()

    if len(sys.argv) < 2:
        print(f'please provide a second file to load with this program as such: python cpu.py [insert second file here]')
        sys.exit()

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()


    # should accept the address to read and return the value stored there.
    def ram_read(self, MAR):
        return self.ram[MAR]

    # should accept a value to write, and the address to write it to.
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
    
    def run(self):
        """Run the CPU."""
        HLT = 0b00000001 
        LDI = 0b10000010 
        PRN = 0b01000111

        is_running = True

        print(f'\n ({is_running}) Now running...\n')

        while is_running:
            IR = self.ram[self.pc]

            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]

            if IR == HLT:
                print(f'\n Goodbye...')
                is_running = False
            elif IR == LDI:
                self.ram_write(operand_a, operand_b)
            elif IR == PRN:
                print(self.ram_read(self.ram[self.pc+1]))
                self.pc += 2
            else:
                self.pc += 1 
                