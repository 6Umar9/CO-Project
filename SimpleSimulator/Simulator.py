import sys

input_file= sys.argv[1]
output_file=sys.argv[2]
a=open(output_file,"w")
a.close()
class RISC_V_Simulator:
    def __init__(self):
        self.registers = [0] * 32
        self.registers[2]=256
        self.memory= [0] * 32
        self.pc= 0

    def int_to_bin(self,num,width=32): #returns with 0b remove if needed using slicing
        num=int(num)
        width=width-1
        if num<0:
            num=(2**(width))+num
            output="0b1"+format(num,f'0{width}b')
            return output
        output="0b0"+format(num,f'0{width}b')
        return output
  
    
    def sext(self,bin,width):
        nw=width-len(bin)
        return (bin[0]*nw)+bin

    def bin_to_int(self,bin,signed):
        bin=str(bin)
        if signed==1:
            if bin[0]=='1':
                width=len(bin)-1
                num=(2**width)-int(bin[1:],2)
                return -num
            return int(bin[1:],2)
        elif signed==0:

            return int(bin,2)

    def register_output(self):
        output=self.int_to_bin(4*(self.pc),32)
        for i in self.registers:
            output=output+ " " + self.int_to_bin(i,32)
        output=output+"\n"
        with open(output_file,"a") as file:
            file.write(output)

    def memory_output(self):
        output=""
        for i,j in enumerate(self.memory):
            output=output+"0x"+format(4*i+65536,"08x")+":"+self.int_to_bin(j,32)+"\n"
        with open(output_file,"a") as file:
            file.write(output)

    def rtype(self, ins, ):
        rd = ins[::-1][7:12][::-1]
        rs1 = ins[::-1][15:20][::-1]
        rs2 = ins[::-1][20:25][::-1]
        funct3 = ins[::-1][12:15][::-1]
        funct7 = ins[::-1][25:32][::-1]

        if funct3 == '000' and funct7 == '0000000':  # ADD
            self.registers[self.bin_to_int(rd, 0)] = self.registers[self.bin_to_int(rs1, 0)] + self.registers[self.bin_to_int(rs2, 0)]
        elif funct3 == '000' and funct7 == '0100000':  # SUB
            self.registers[self.bin_to_int(rd, 0)] = self.registers[self.bin_to_int(rs1, 0)] - self.registers[self.bin_to_int(rs2, 0)]
        elif funct3 == '111' and funct7 == '0000000':  # AND
            self.registers[self.bin_to_int(rd, 0)] = self.registers[self.bin_to_int(rs1, 0)] & self.registers[self.bin_to_int(rs2, 0)]
        elif funct3 == '110' and funct7 == '0000000':  # OR
            self.registers[self.bin_to_int(rd, 0)] = self.registers[self.bin_to_int(rs1, 0)] | self.registers[self.bin_to_int(rs2, 0)]
        elif funct3 == '100' and funct7 == '0000000':  # XOR
            self.registers[self.bin_to_int(rd, 0)] = self.registers[self.bin_to_int(rs1, 0)] ^ self.registers[self.bin_to_int(rs2, 0)]
        elif funct3 == '001'and funct7== '0000000': #SLL
            self.registers[self.bin_to_int(rd, 0)] = self.registers[self.bin_to_int(rs1, 0)] << self.bin_to_int(self.int_to_bin( self.registers[self.bin_to_int(rs2, 0)] )[2:][-5:],0)
        elif funct3 == '010' and funct7=='0000000':  # SLT
            self.registers[self.bin_to_int(rd, 0)] = 1 if self.registers[self.bin_to_int(rs1, 0)] < self.registers[self.bin_to_int(rs2, 0)] else 0
        elif funct3 == '011' and funct7=='0000000':  # SLTU
            self.registers[self.bin_to_int(rd, 0)] = 1 if self.bin_to_int(self.int_to_bin(self.registers[self.bin_to_int(rs1, 0)])[2:], 0) < self.bin_to_int(self.int_to_bin(self.registers[self.bin_to_int(rs2, 0)])[2:], 0) else 0
        elif funct3 == '101' and funct7 == '0000000':  # SRL
            self.registers[self.bin_to_int(rd, 0)] = self.registers[self.bin_to_int(rs1, 0)] >> self.bin_to_int(self.int_to_bin( self.registers[self.bin_to_int(rs2, 0)] )[2:][-5:],0)

        self.pc+=1

    def i_type(self, instruction):
        opcode = instruction[-7:]
        imm = instruction[::-1][20:32][::-1]
        imm_value = self.bin_to_int(imm, 1)
        rd = instruction[::-1][7:12][::-1]
        rs1 = instruction[::-1][15:20][::-1]
        funct3=instruction[::-1][12:15][::-1]

        match opcode:
            case '1100111':  # jalr
                self.registers[self.bin_to_int(rd,0)] = 4*self.pc + 4
                self.pc = (int(rs1)+imm_value)//4
            case '0010011' : #sltiu
                if funct3 == '011':
                    if self.bin_to_int(self.int_to_bin(self.registers[self.bin_to_int(rs1, 0)])[2:], 0) < self.bin_to_int(imm,0): 
                        self.registers[self.bin_to_int(rd, 0)] = 1 
                    else:
                        self.registers[self.bin_to_int(rd,0)] = 0
                if funct3 == '000':
                    self.registers[self.bin_to_int(rd, 0)] = self.registers[self.bin_to_int(rs1, 0)] + imm_value
                self.pc+=1
            case "0000011":
                if funct3 =='010':
                    self.registers[self.bin_to_int(rd, 0)] = self.memory[(self.registers[self.bin_to_int(rs1, 0)] + imm_value - 16**4)//4] 
                self.pc+=1

    def stype(self,ins):
        imm=ins[::-1][25:32][::-1]+ins[::-1][7:12][::-1]
        immval=self.bin_to_int(imm,1)
        rs1=ins[::-1][15:20][::-1]
        rs2=ins[::-1][20:25][::-1]
        funct3=ins[::-1][12:15][::-1]
        memadr=immval+self.registers[self.bin_to_int(rs1,0)] -16**4
        self.memory[memadr//4]=self.registers[self.bin_to_int(rs2,0)]
        self.pc+=1

    def btype(self, instruction):
        opcode = instruction[-7:]
        imm = instruction[-32]+instruction[-8]+instruction[-31:-25] + instruction[-12:-7] + '0'
        rs1 = self.bin_to_int(instruction[::-1][15:20][::-1], 0)
        rs2 = self.bin_to_int(instruction[::-1][20:25][::-1], 0)
        funct3=instruction[::-1][12:15][::-1]

        imm_value = self.bin_to_int(imm, 1)
        rs1_value = self.registers[rs1]
        rs2_value = self.registers[rs2]
    
        # def sign_extend(value, bits):
        #     if value >> (bits - 1) & 1:  # Check if the sign bit is set
        #         return value | ((1 << (32 - bits)) - 1) << bits
        #     return value

        def signed_to_unsigned(value):
            return self.bin_to_int(self.int_to_bin(value)[2:],0)

        done=False

        match funct3:
            case '000':  # beq
                if rs1_value == rs2_value:
                    self.pc = self.pc + imm_value//4
                    done=True
            case '001':  # bne
                if rs1_value != rs2_value:
                    self.pc = self.pc + imm_value//4
                    done=True
            case '101':  # bge
                if rs1_value >= rs2_value:
                    self.pc = self.pc + imm_value//4
                    done=True
            case '111':  # bgeu
                if signed_to_unsigned(rs1_value) >= signed_to_unsigned(rs2_value):
                    self.pc = self.pc + imm_value//4
                    done=True
            case '110':  # bltu
                if signed_to_unsigned(rs1_value) < signed_to_unsigned(rs2_value):
                    self.pc = self.pc + imm_value//4
                    done=True
            case '100':  # blt
                if rs1_value < rs2_value:
                    self.pc = self.pc + imm_value//4
                    done=True
        
        if not done:
            self.pc+=1

 

    def utype(self,ins):
        opcode=ins[-7:]
        rd=ins[::-1][7:12][::-1]
        rdint=self.bin_to_int(rd,0)
        imm=ins[::-1][12:32][::-1]
        if opcode == "0110111": #lui
            self.registers[rdint]=self.bin_to_int(imm+"0"*12,1)
        if opcode == "0010111": #auipc
            self.registers[rdint]=self.bin_to_int(imm+"0"*12,1)+4*self.pc
        
        self.pc+=1

    def j_type(self, instruction):
        # opcode=instruction[-7:]
        rd=instruction[-12:-7]
        imm=instruction[-32]+instruction[-20:-12]+instruction[-21]+instruction[-31:-21]+'0'
        # imm[-21]=instruction[-32]
        # imm[-11:-1]=instruction[-31:-21]
        # imm[-12]=instruction[-21]
        # imm[-20:-12]=instruction[-20:-12]

        self.registers[self.bin_to_int(rd,0)]=4*self.pc+4
        self.pc+=self.bin_to_int(self.sext(imm, 32), 1)//4 #imm 0 bit is 0

    def execute(self,input_file):
        read=open(input_file,'r')
        program=[line.strip() for line in read.read().splitlines() if line]
        while self.pc<len(program): 
            if program[self.pc]=='00000000000000000000000001100011':
                self.register_output()
                break
            opcode=program[self.pc][-7:]
            #use match case to match opcodes and run your functions 
            match opcode:
                case '0110011': #r_type
                    self.rtype(program[self.pc])
                case '0000011'|'0010011'|'1100111': #i_type
                    self.i_type(program[self.pc])
                case '0100011': #s_type
                    self.stype(program[self.pc])
                case '1100011': #b_type
                    self.btype(program[self.pc])
                case '0110111'|'0010111':
                    self.utype(program[self.pc])
                case '1101111':
                    self.j_type(program[self.pc])

            self.register_output()
        self.memory_output()

sim = RISC_V_Simulator()
sim.execute(input_file)





# with open(output_file, 'r') as f:
#     print(f.read())
