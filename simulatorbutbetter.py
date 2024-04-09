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

    def int_to_bin(self,num,width):
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

    def bin_to_int(self,bin):
        if bin[0]=='1':
            width=len(bin)-1
            num=(2**width)-int(bin[1:],2)
            return -num
        return int(bin[1:],2)

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
            output=output+"0x"+format(4*i+65536,"08x")+":"+"0b"+format(j,"032b")+"\n"
        with open(output_file,"a") as file:
            file.write(output)
    
    def execute(self,input_file):
        read=open(input_file,'r')
        program=read.read().split()
        while self.pc<len(program):
            sim.register_output()
            print(program[self.pc])
            self.pc+=1
sim = RISC_V_Simulator()
sim.execute(input_file)
sim.memory_output()
