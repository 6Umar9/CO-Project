import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
wf=open(output_file,"w")
wf.close()
def jtype(instruction):
    '''Instruction- An assembly instruction'''
    '''Return the machine code for it'''
    words=instruction.split()
    ins=words[0]
    codeins="0"
    match ins:
        case "jal":
            codeins="1101111"
        case _:
            print("Not a valid jtype instruction.")
    args=words[1].split(",")
    rd=args[0]
    try:
        coderd=registerdict[rd]
    except KeyError:
        print(f"Register not found in line {counter}")
        return -1
    imm=int(args[1])
    imm=str(bin_converter(imm,21))
    imm=imm[::-1]
    if imm=="-1":
        print(f'Immediate value out of range in line {counter}')
    else:
        codeimm=imm[20]+imm[10:0:-1]+imm[11]+imm[19:12-1:-1]

        codeinstruction=codeimm+coderd+codeins
        print(codeinstruction)
        wf=open(output_file,"a")
        wf.write(codeinstruction+'\n')
        wf.close()

def utype(instruction):
    '''Instruction- An assembly instruction'''
    '''Return the machine code for it'''
    global counter
    words=instruction.split()
    ins=words[0]
    codeins="0"
    match ins:
        case "lui":
            codeins="0110111"
        case "auipc":
            codeins="0010111"
        case _:
            print("Not a valid utype instruction.")
    args=words[1].split(",")
    rd=args[0]
    try:
        coderd=registerdict[rd]
    except KeyError:
        print(f"Register not found in line {counter}")
        return -1

    imm=int(args[1])
    imm=str(bin_converter(imm,32))
    imm=imm[::-1]
    if imm=="-1":
        print(f'Immediate value out of range in line {counter}')
    else:
        codeimm=imm[31:11:-1]

        codeinstruction=codeimm+coderd+codeins
        print(codeinstruction)
        wf=open(output_file,"a")
        wf.write(codeinstruction+'\n')
        wf.close()
def bonus(instruction):
    '''Instruction- An assembly instruction'''
    '''Return the machine code for it'''
    
    words=instruction.split()
    ins=words[0]
    codeins="0"
    match ins:
        case "mul":
            codeins="0110011"
        case "rst":
            codeins="0010111"
        case "halt":
            print("Not a valid utype instruction.")
        case "rvrs":
            pass

def r_type(string1):
    
    list1 = string1.split()
    opcode = list1[0]
    reg=list1[1].split(',')

    try: 
        rd=registerdict[reg[0]]
        rs1=registerdict[reg[1]]
        rs2=registerdict[reg[2]]
    except KeyError:
        print(f"Register not found in line {counter}")
        return -1

    codeop="0110011"
    func7="0000000"
    if opcode == 'add':
        func3 = '000'
    
    elif opcode == 'sub':
        func3 = '000'
        func7='0100000'

    elif opcode == 'sll':
        func3 = '001'

    elif opcode == 'slt':
        func3 = '010'

    elif opcode == 'sltu':
        func3 = '011'

    elif opcode == 'xor':
        func3 = '100'

    elif opcode == 'srl':
        func3 = '101'

    elif opcode == 'or':
        func3 = '110'

    elif opcode == 'and':
        func3 = '111'

    else:
        raise ValueError(f"Invalid opcode for R-type instruction") #I don't know either to raise or print error
    
    bin_str = func7+rs2+rs1+func3+rd+"0110011"
    return bin_str
        


def b_type(string1):

    linesplit = string1.split() #seperating Opcode and the registers/immediates
    opcode = linesplit[0] #opcode assigned
    registers = linesplit[1].split(',') #spliting the registers and immediates
    wf=open(output_file,"a")
    match opcode:

        case "beq":
            try: #test for register to fit for B-Type instructions
                a=registerdict[registers[0]]
                b=registerdict[registers[1]]
            except KeyError:
                print(f"Register not found in line {counter}")
                return
            
            c=binconverter(int(registers[2]),12) #converting immediate to binary

            if c=='-1': #to check if output is -1 which signifies error as mentioned above
                print(f'Immediate value out of range in line {counter}')
                return
            
            c=c[::-1]
            print(f"{c[11]}{c[10:5-1:-1]}{b}{a}000{c[4:0:-1]}{c[11]}1100011")
            wf.write(f"{c[11]}{c[10:5-1:-1]}{b}{a}000{c[4:0:-1]}{c[11]}1100011"+"\n")

        case "bne":
            try: #test for register to fit for B-Type instructions
                a=registerdict[registers[0]]
                b=registerdict[registers[1]]
            except KeyError:
                print(f"Register not found in line {counter}")
                return
            
            c=binconverter(int(registers[2]),12) #converting immediate to binary

            if c=='-1': #to check if output is -1 which signifies error as mentioned above
                print(f'Immediate value out of range in line {counter}')
                return
            
            c=c[::-1]
            print(f"{c[11]}{c[10:5-1:-1]}{b}{a}001{c[4:0:-1]}{c[11]}1100011")
            wf.write(f"{c[11]}{c[10:5-1:-1]}{b}{a}001{c[4:0:-1]}{c[11]}1100011"+"\n")
        case "blt":
            try: #test for register to fit for B-Type instructions
                a=registerdict[registers[0]]
                b=registerdict[registers[1]]
            except KeyError:
                print(f"Register not found in line {counter}")
                return
            
            c=binconverter(int(registers[2]),12) #converting immediate to binary

            if c=='-1': #to check if output is -1 which signifies error as mentioned above
                print(f'Immediate value out of range in line {counter}')
                return
            
            c=c[::-1]
            
            print(f"{c[11]}{c[10:5-1:-1]}{b}{a}100{c[4:0:-1]}{c[11]}1100011")
            wf.write(f"{c[11]}{c[10:5-1:-1]}{b}{a}100{c[4:0:-1]}{c[11]}1100011"+"\n")

        case "bge":
            try: #test for register to fit for B-Type instructions
                a=registerdict[registers[0]]
                b=registerdict[registers[1]]
            except KeyError:
                print(f"Register not found in line {counter}")
                return
            
            c=binconverter(int(registers[2]),12) #converting immediate to binary

            if c=='-1': #to check if output is -1 which signifies error as mentioned above
                print(f'Immediate value out of range in line {counter}')
                return
            
            c=c[::-1]
            
            print(f"{c[11]}{c[10:5-1:-1]}{b}{a}101{c[4:0:-1]}{c[11]}1100011")
            wf.write(f"{c[11]}{c[10:5-1:-1]}{b}{a}101{c[4:0:-1]}{c[11]}1100011"+"\n")

        case "bltu":
            try: #test for register to fit for B-Type instructions
                a=registerdict[registers[0]]
                b=registerdict[registers[1]]
            except KeyError:
                print(f"Register not found in line {counter}")
                return
            
            c=binconverter(int(registers[2]),12) #converting immediate to binary

            if c=='-1': #to check if output is -1 which signifies error as mentioned above
                print(f'Immediate value out of range in line {counter}')
                return
            
            c=c[::-1]
            
            print(f"{c[11]}{c[10:5-1:-1]}{b}{a}110{c[4:0:-1]}{c[11]}1100011")
            wf.write(f"{c[11]}{c[10:5-1:-1]}{b}{a}110{c[4:0:-1]}{c[11]}1100011"+"\n")
        
        case "bgeu":
            try: #test for register to fit for B-Type instructions
                a=registerdict[registers[0]]
                b=registerdict[registers[1]]
            except KeyError:
                print(f"Register not found in line {counter}")
                return
            
            c=binconverter(int(registers[2]),12) #converting immediate to binary

            if c=='-1': #to check if output is -1 which signifies error as mentioned above
                print(f'Immediate value out of range in line {counter}')
                return
            
            c=c[::-1]
            
            print(f"{c[11]}{c[10:5-1:-1]}{b}{a}111{c[4:0:-1]}{c[11]}1100011")
            wf.write(f"{c[11]}{c[10:5-1:-1]}{b}{a}111{c[4:0:-1]}{c[11]}1100011"+"\n")
    #programcounter+= int(registers[]) #figuring this out still
    wf.close()        


def binconverter( number, width): #takes input as int and width which is number of bits the binary shouldbe 
        if -1*(2**(width-1))<=number<(2**(width-1)):
            ret=f'{number:032b}'
            ret=ret[32-width:]
            if number>=0:
                return ret
            else:
                ret2=''
                ind=ret.rfind('1')

                for i in ret[:ind]:
                    if i=='0':
                        ret2+="1"
                    else:
                        ret2+="0"
                ret2=ret2+ret[ind:]
                return ret2
        else:
            return '-1'

def sign_extension(no,bits):
    no=str(no)
    l=len(no)
    if bits>l:
        no=no[0]*(bits-l)+no
    elif bits==l:
        pass
    else:
        pass
        #not enough bits
        # no=no[l-bits:]
    
    return no

def twos_compliment(no):
    no=str(no)
    l=len(no)
    if no[0]=='1':
        no='0'+no
        l+=1
    compli=2**(l)-1-int(no,base=2)+1
    compli_bin=bin(compli)[2:]
    return compli_bin

# print(twos_compliment(110))

def bin_converter(no,width=32):
    if -1*(2**(width-1))<=no<2**(width-1):
        if no>=0:
            ret="0"+bin(no)[2:]
            return sign_extension(ret,width)
        else:
            no*=-1
            compli=twos_compliment(bin(no)[2:])
            return sign_extension(compli,width)
            
    else:
        return -1

registerdict={ #dictionary with all register address
    "zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011",
    "tp": "00100", "t0": "00101", "t1": "00110", "t2": "00111",
    "s0": "01000", "fp": "01000", #different names for same register
    "s1": "01001", "a0": "01010", "a1": "01011", "a2": "01100",
    "a3": "01101", "a4": "01110", "a5": "01111", "a6": "10000",
    "a7": "10001", "s2": "10010", "s3": "10011", "s4": "10100",
    "s5": "10101", "s6": "10110", "s7": "10111", "s8": "11000",
    "s9": "11001", "s10": "11010", "s11": "11011", "t3": "11100",
    "t4": "11101", "t5": "11110", "t6": "11111"
}

with open(input_file,"r") as inputstream:
        assembly=inputstream.read().lower()
        assemblyinput=assembly.splitlines() #there is no need to pop the last line as if it exists it is ignored in splitlines method.


counter=1 #counter no used for error lines
programcounter=0x00000000 # 32 bit counter for PC

labelmap={} #map which stores label with PC address

for ind,ins in enumerate(assemblyinput): #maps all the labels and removes them too
    if ':' in ins:
        holder=ins.split(':')
        labelmap[holder[0]]=programcounter
        assemblyinput[ind]=holder[1]
    programcounter+=0x00000004
            
programcounter=0x00000000 #resetting the program counter again

for i in assemblyinput: #main processing of assembly lines
    instructionsplit=i.split()
    #if len(labelsplit)>1:
    #    labelmap[labelsplit[0]]=programcounter
    #    instructionsplit=labelsplit[1].split()
    #else:
    #    instructionsplit=labelsplit[0].split()
    opcode=instructionsplit[0]
    
    registers=instructionsplit[1].split(",")

    #some exta instructions that are usually given in RISC V
    itypes=['addi','slti','sltiu','xori','ori','andi','slli','srli','srai']
    rtypes=["add","sub","sll","slt","sltu","xor","srl","or","and"]
    btypes=["beq","bne","blt","bge","bltu","bgeu"]
    codeitypes=["000","010","011","100","110","111","001","101","101"]
    if opcode in rtypes:
        ret=r_type(i)
        print(ret)
        wf=open(output_file,"a")
        wf.write(ret+"\n")
        wf.close()
    if opcode in btypes:
        b_type(i)
    if opcode=="jal":
        ret=jtype(i)
        if ret==-1:
            break
    if opcode in ["lui","auipc"]:
        ret=utype(i)
        if ret==-1:
            break

    '''if opcode in itypes:
        funct3=codeitypes[itypes.index(opcode)]
        try: #test for register to fit
            a=registerdict[registers[0]]
            b=registerdict[registers[1]]
        except KeyError:
            print(f"Register not found in line {counter}")
            break

        c=binconverter(int(registers[2]),12)
        if c=='-1': #to check if output is -1 which signifies error
            print(f'Immediate value out of range in line {counter}')
            break


        print(f"{c}{b}{funct3}{a}0010011") 
        # for slli, srli, srai the immediate are fixed as 0000000xxxxx, 0000000xxxxx, 0100000xxxxx because you can shift by only 0-31 positions on a 32 bit number (rs1(b))
        break'''

    # remaning cases
    match opcode: #match for the opcodes
       
        case "addi":
            try: #test for register to fit
                a=registerdict[registers[0]]
                b=registerdict[registers[1]]
            except KeyError:
                print(f"Register not found in line {counter}")
                break
            c=binconverter(int(registers[2]),12)
            if c=='-1': #to check if output is -1 which signifies error
                print(f'Immediate value out of range in line {counter}')
                break
            print(f"{c}{b}000{a}0010011")
            wf=open(output_file,"a")
            wf.write(f"{c}{b}000{a}0010011"+"\n")
            wf.close()
        case "sltiu":
            try:
                a=registerdict[registers[0]]
                b=registerdict[registers[1]]
            except KeyError:
                print(f"Register not found in line {counter}")
                break
            c=binconverter(int(registers[2]),12)
            if c=='-1':
                print(f'Immediate value out of range in line {counter}')
                break
            print(f"{c}{b}011{a}0010011")
            wf=open(output_file,"a")
            wf.write(f"{c}{b}011{a}0010011"+"\n")
            wf.close()
        case "lw":
            ffs=registers[1].split('(')
            try:
                a=registerdict[registers[0]]
                b=registerdict[ffs[1][:-1]] #removing ')' from register
            except KeyError:
                print(f"Register not found in line {counter}")
                break
            c=binconverter(int(ffs[0]),12)
            if c=='-1':
                print(f'Immediate value out of range in line {counter}')
                break
            print(f"{c}{b}010{a}0000011")
            wf=open(output_file,"a")
            wf.write(f"{c}{b}010{a}0000011"+"\n")
            wf.close()
        case "jalr":
            try:
                a=registerdict[registers[0]]
                b=registerdict[registers[1]]
            except KeyError:
                print(f"Register not found in line {counter}")
                break
            
            c=binconverter(int(registers[2]),12)
            if c=='-1':
                print(f'Immediate value out of range in line {counter}')
                break

            print(f"{c}{b}000{a}1100111")
            wf=open(output_file,"a")
            wf.write(f"{c}{b}000{a}1100111"+"\n")
            wf.close()
        case "sw":

            ffs=registers[1].split('(')
            try:
                a=registerdict[registers[0]]
                b=registerdict[ffs[1][:-1]]
            except KeyError:
                print(f"Register not found in line {counter}")
                break

            c=binconverter(int(ffs[0]),12)
        
            if c=='-1':
                print(f'Immediate value out of range in line {counter}')
                break 
            c=c[::-1]
            print(f"{c[11:4:-1]}{a}{b}010{c[4::-1]}0100011")
            wf=open(output_file,"a")
            wf.write(f"{c[11:4:-1]}{a}{b}010{c[4::-1]}0100011"+"\n")
            wf.close()
#all others are same I am not sure about output order of each line
#keep all code above, above the increment in counters
    
    programcounter+=0x00000004
    counter+=1



#R-type instructions
def r_type(string1):
    
    list1 = string1.split()
    opcode = list1[0]
    reg=list1[1].split(',')

    try: 
        rd=registerdict[reg[0]]
        rs1=registerdict[reg[1]]
        rs2=registerdict[reg[2]]
    except KeyError:
        print(f"Register not found in line {counter}")
        return

    codeop="0110011"
    func7="0000000"
    if opcode == 'add':
        func3 = '000'
    
    elif opcode == 'sub':
        func3 = '000'
        func7='0100000'

    elif opcode == 'sll':
        func3 = '001'

    elif opcode == 'slt':
        func3 = '010'

    elif opcode == 'sltu':
        func3 = '011'

    elif opcode == 'xor':
        func3 = '100'

    elif opcode == 'srl':
        func3 = '101'

    elif opcode == 'or':
        func3 = '110'

    elif opcode == 'and':
        func3 = '111'

    else:
        raise ValueError(f"Invalid opcode for R-type instruction") #I don't know either to raise or print error
    
    bin_str = func7+rs2+rs1+func3+rd+opcode
    return bin_str
        
#B-type Instructions
def b_type(string1):

    linesplit = string1.split() #seperating Opcode and the registers/immediates
    opcode = linesplit[0] #opcode assigned
    registers = linesplit[1].split(',') #spliting the registers and immediates

    match opcode:

        case "beq":
            try: #test for register to fit for B-Type instructions
                a=registerdict[registers[0]]
                b=registerdict[registers[1]]
            except KeyError:
                print(f"Register not found in line {counter}")
                return
            
            c=binconverter(int(registers[2]),12) #converting immediate to binary

            if c=='-1': #to check if output is -1 which signifies error as mentioned above
                print(f'Immediate value out of range in line {counter}')
                return
            
            c=c[::-1]
            print(f"{c[12]}{c[10:5-1:-1]}{b}{a}000{c[4::-1]}1100011")

        case "bne":
            try: #test for register to fit for B-Type instructions
                a=registerdict[registers[0]]
                b=registerdict[registers[1]]
            except KeyError:
                print(f"Register not found in line {counter}")
                return
            
            c=binconverter(int(registers[2]),12) #converting immediate to binary

            if c=='-1': #to check if output is -1 which signifies error as mentioned above
                print(f'Immediate value out of range in line {counter}')
                return
            
            c=c[::-1]
            print(f"{c[12]}{c[10:5-1:-1]}{b}{a}001{c[4::-1]}1100011")

        case "blt":
            try: #test for register to fit for B-Type instructions
                a=registerdict[registers[0]]
                b=registerdict[registers[1]]
            except KeyError:
                print(f"Register not found in line {counter}")
                return
            
            c=binconverter(int(registers[2]),12) #converting immediate to binary

            if c=='-1': #to check if output is -1 which signifies error as mentioned above
                print(f'Immediate value out of range in line {counter}')
                return
            
            c=c[::-1]
            print(f"{c[12]}{c[10:5-1:-1]}{b}{a}100{c[4::-1]}1100011")


        case "bge":
            try: #test for register to fit for B-Type instructions
                a=registerdict[registers[0]]
                b=registerdict[registers[1]]
            except KeyError:
                print(f"Register not found in line {counter}")
                return
            
            c=binconverter(int(registers[2]),12) #converting immediate to binary

            if c=='-1': #to check if output is -1 which signifies error as mentioned above
                print(f'Immediate value out of range in line {counter}')
                return
            
            c=c[::-1]
            print(f"{c[12]}{c[10:5-1:-1]}{b}{a}101{c[4::-1]}1100011")


        case "bltu":
            try: #test for register to fit for B-Type instructions
                a=registerdict[registers[0]]
                b=registerdict[registers[1]]
            except KeyError:
                print(f"Register not found in line {counter}")
                return
            
            c=binconverter(int(registers[2]),12) #converting immediate to binary

            if c=='-1': #to check if output is -1 which signifies error as mentioned above
                print(f'Immediate value out of range in line {counter}')
                return
            
            c=c[::-1]
            print(f"{c[12]}{c[10:5-1:-1]}{b}{a}110{c[4::-1]}1100011")

        
        case "bgeu":
            try: #test for register to fit for B-Type instructions
                a=registerdict[registers[0]]
                b=registerdict[registers[1]]
            except KeyError:
                print(f"Register not found in line {counter}")
                return
            
            c=binconverter(int(registers[2]),12) #converting immediate to binary

            if c=='-1': #to check if output is -1 which signifies error as mentioned above
                print(f'Immediate value out of range in line {counter}')
                return
            
            c=c[::-1]
            print(f"{c[12]}{c[10:5-1:-1]}{b}{a}111{c[4::-1]}1100011")

    #programcounter+= int(registers[]) #figuring this out still
        
    counter += 1


