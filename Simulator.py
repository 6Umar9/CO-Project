class RISC_V_Simulator:
    def __init__(self):
        self.registers = [0] * 32
        self.memory = [0] * 4096  # 4KB memory
        self.pc = 0  # Program Counter
        self.label_map = {}
        self.last_line = 0

    def load_program(self, program):
        self.pc = 0
        for ind, line in enumerate(program):
            if ':' in line:
                label, _ = line.split(':')
                self.label_map[label] = self.pc
                self.last_line = ind
            self.pc += 4

        self.pc = 0  # Reset PC
        self.last_line -= 1  # Adjusting last_line for 0-based index

    def execute(self, program):
        self.load_program(program)
        while self.pc <= len(program) * 4:
            instruction = program[self.pc // 4]
            opcode, *args = instruction.split()
            if opcode in ["add", "sub", "sll", "slt", "sltu", "xor", "srl", "sra", "or", "and"]:
                self.r_type(instruction)
            elif opcode in ["lw", "sw", "jalr", "addi", "slti", "sltiu", "xori", "ori", "andi", "slli", "srli", "srai"]:
                self.i_type(instruction)
            elif opcode in ["beq", "bne", "blt", "bge", "bltu", "bgeu"]:
                self.b_type(instruction)
            elif opcode in ["jal"]:
                self.j_type(instruction)
            elif opcode in ["lui", "auipc"]:
                self.u_type(instruction)
            else:
                print("Unknown instruction:", opcode)
                break

    def imm_or_label(self, given):
        pass  # Implement this function

    def sign_extend(self, value, bits):
        if value >> (bits - 1) & 1:  # Check if the sign bit is set
            return value | ((1 << (32 - bits)) - 1) << bits
        return value


    def twos_compliment(self, no):
        pass  # Implement this function

    def bin_converter(self, no, width=32):
        pass  # Implement this function

    def j_type(self, instruction):
        pass  # Implement this function

    def u_type(self, instruction):
        pass  # Implement this function

    def s_type(self, instruction):
        pass  # Implement this function

    def r_type(self, instruction):
        opcode, rd, rs1, rs2 = instruction.split()
        rd = int(rd[1:])  # Extract destination register number
        rs1 = int(rs1[1:])  # Extract source register 1 number
        rs2 = int(rs2[1:])  # Extract source register 2 number

        def sign_extend(value, bits):
            if value >> (bits - 1) & 1:  # Check if the sign bit is set
                return value | ((1 << (32 - bits)) - 1) << bits
            return value

        if opcode == "slt":
            rs1_value = self.registers[rs1]
            rs2_value = self.registers[rs2]
            rs1_value = sign_extend(rs1_value, 32)
            rs2_value = sign_extend(rs2_value, 32)
            self.registers[rd] = 1 if rs1_value < rs2_value else 0
        elif opcode == "add":
            rs1_value = self.registers[rs1]
            rs2_value = self.registers[rs2]
            rs1_value = sign_extend(rs1_value, 32)
            rs2_value = sign_extend(rs2_value, 32)
            self.registers[rd] = rs1_value + rs2_value
        elif opcode == "sub":
            rs1_value = self.registers[rs1]
            rs2_value = self.registers[rs2]
            rs1_value = sign_extend(rs1_value, 32)
            rs2_value = sign_extend(rs2_value, 32)
            self.registers[rd] = rs1_value - rs2_value
        elif opcode == "sll":
            self.registers[rd] = self.registers[rs1] << (self.registers[rs2] & 0x1F)
        elif opcode == "sltu":
            self.registers[rd] = 1 if self.registers[rs1] < self.registers[rs2] else 0  # Unsigned comparison
        elif opcode == "xor":
            self.registers[rd] = self.registers[rs1] ^ self.registers[rs2]
        elif opcode == "srl":
            self.registers[rd] = self.registers[rs1] >> (self.registers[rs2] & 0x1F)  # Logical right shift
        elif opcode == "or":
            self.registers[rd] = self.registers[rs1] | self.registers[rs2]
        elif opcode == "and":
            self.registers[rd] = self.registers[rs1] & self.registers[rs2]

    def b_type(self, instruction):
        pass  # Implement this function

    def i_type(self, instruction):
        pass  # Implement this function

    


# Example usage:
if __name__ == "__main__":
    simulator = RISC_V_Simulator()
    with open("input.txt", "r") as f:
        program = f.readlines()

    simulator.execute(program)
