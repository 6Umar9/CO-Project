import sys

input_file=sys.argv[1]
output_file=sys.argv[2]
a=open(output_file,"w")
a.close()
class RISC_V_Simulator:
    def __init__(self):
        self.registers = [0] * 32
        self.memory= [0] * 32
        self.pc= 0

    def int_to_bin(self,num,width): #returns with 0b remove if needed using slicing
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
        if signed==1:
            if bin[0]=='1':
                width=len(bin)-1
                num=(2**width)-int(bin[1:],2)
                return -num
            return int(bin[1:],2)
        elif signed==0:
            return int(bin,2)

    def register_output(self):
        output=self.int_to_bin(self.pc,32)
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

    def stype(self,ins):
        imm=ins[::-1][25:32][::-1]+ins[::-1][7:12][::-1]
        immval=self.bin_to_int(imm,1)
        reg=ins[::-1][15:20][::-1]
        memadr=immval+self.registers[self.bin_to_int(reg,0)]
        self.memory[memadr//4]=self.registers[self.bin_to_int(ins[::-1][20:25][::-1],0)]
    
    def utype(self,ins):
        rd=ins[::-1][7:12][::-1]
        rdint=self.bin_to_int(rd,0)
        imm=ins[::-1][12:32][::-1]
        if ins[::-1][0:7][::-1] == "0110111": #lui
            self.registers[rdint]=self.bin_to_int(imm+"0"*12,1)
        if ins[::-1][0:7][::-1] == "0010111": #auipc
            self.registers[rdint]=self.bin_to_int(imm+"0"*12,1)+4*self.pc

    def execute(self,input_file):
        read=open(input_file,'r')
        program=read.read().split()
        while self.pc<len(program):
            opcode=program[self.pc][-7:]
            #use match case to match opcodes and run your functions 
            match opcode:
                case '0100011': #s_type
                    self.stype(program[self.pc])
                case '0110111':
                    self.utype(program[self.pc])
                case '0010111':
                    self.utype(program[self.pc])
#incase of btype or any change in pc then reduce the changed pc to pc -1 since it increases by one
            sim.register_output()
            self.pc+=1
sim = RISC_V_Simulator()
sim.execute(input_file)
sim.memory_output()
