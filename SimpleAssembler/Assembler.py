import sys

input_file=sys.argv[1]
output_file=sys.argv[2]

# input- "/Users/teo/Desktop/CO Project/input.txt"
# output- "/Users/teo/Desktop/CO Project/output.txt"
with open(input_file,"r") as inputstream:
    assembly=inputstream.read().lower()
    assemblyinput=[line.strip() for line in assembly.splitlines() if line.strip()] #there is no need to pop the last line as if it exists it is ignored in splitlines method.


output_file=output_file
wf=open(output_file,"w")
wf.close()

def imm_or_label(given): #Function to check label or imm and return accordingly always returns int
    global counter
    global programcounter
    try:
        return int(given)
    except ValueError:
        try:
            return (labelmap[given]-programcounter)
        except:
            return "error"
    
    

def j_type(instruction):
    '''Instruction- An assembly instruction'''
    '''Return the machine code for it'''

    words=instruction.split()
    ins=words[0]
    codeins="0"
    match ins:
        case "jal":
            codeins="1101111"
        
    args=words[1].split(",")
    rd=args[0]
    try:
        coderd=registerdict[rd]
    except KeyError:
        print(f"Register not found in line {counter}")
        return
    
    imm=imm_or_label(args[1])
    if imm=='error':
        print(f"Illegal Label {args[1]}")
        return
    imm=str(bin_converter(imm,21))
    if imm==-1:
        print(f'Immediate value out of range in line {counter}')
        return 

    imm=imm[::-1]
    codeimm=imm[20]+imm[10:0:-1]+imm[11]+imm[19:12-1:-1]

    codeinstruction=codeimm+coderd+codeins
    print(codeinstruction)

    wf=open(output_file,"a")
    wf.write(codeinstruction+'\n')
    wf.close()

def u_type(instruction):
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

    args=words[1].split(",")
    rd=args[0]
    try:
        coderd=registerdict[rd]
    except KeyError:
        print(f"Register not found in line {counter}")
        return 

    imm=int(args[1])
    imm=str(bin_converter(imm,32))

    if imm==-1:
        print(f'Immediate value out of range in line {counter}')
        return

    imm=imm[::-1]
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
    
    words = string1.split()
    ins = words[0]
    reg=words[1].split(',')

    try: 
        rd=registerdict[reg[0]]
        rs1=registerdict[reg[1]]
        rs2=registerdict[reg[2]]
    except KeyError:
        print(f"Register not found in line {counter}")
        return

    codeop="0110011"
    func7="0000000"

    match ins:
        case 'add':
            func3 = '000'
    
        case 'sub':
            func3 = '000'
            func7='0100000'

        case 'sll':
            func3 = '001'

        case 'slt':
            func3 = '010'

        case 'sltu':
            func3 = '011'

        case 'xor':
            func3 = '100'

        case 'srl':
            func3 = '101'

        case 'or':
            func3 = '110'

        case 'and':
            func3 = '111'

    
    codeinstruction = func7+rs2+rs1+func3+rd+codeop
    print(codeinstruction)

    wf=open(output_file,"a")
    wf.write(codeinstruction+'\n')
    wf.close()

halt_instr="00000000000000000000000001100011"
def b_type(string1):

    words = string1.split() #seperating Opcode and the registers/immediates
    ins = words[0]
    codeins='1100011'
    registers = words[1].split(',') #spliting the registers and immediates
    
    try:
        rs1=registerdict[registers[0]]
        rs2=registerdict[registers[1]]
    except KeyError:
        print(f"Register not found in line {counter}")
        return
    
    immi = imm_or_label(registers[2])
    if immi=="error":
        print(f"Illegal label in {registers[2]}")
        return
    immi=bin_converter(immi,13) #converting immediate to binary

    if immi==-1: #to check if output is -1 which signifies error as mentioned above
        print(f'Immediate value out of range in line {counter}')
        return
    
    immi=immi[::-1]

    match ins:
        case "beq":
            funct3='000'

        case "bne":
            funct3='001'

        case "blt":
            funct3='100'

        case "bge":
            funct3='101'

        case "bltu":
            funct3='110'    
        
        case "bgeu":
            funct3='111'

    codeinstruction=f"{immi[12]}{immi[10:5-1:-1]}{rs2}{rs1}{funct3}{immi[4:0:-1]}{immi[11]}{codeins}"

    if codeinstruction == halt_instr and counter!=last_line:
        print(f"Halt can't be in line {counter} where the last line is line {last_line}.")
        return

    elif codeinstruction!=halt_instr and counter==last_line:
        print("Last instruction not halt instruction.")

    print(codeinstruction)

    wf=open(output_file,'a')
    wf.write(codeinstruction+"\n")
    wf.close()
      
def i_type(instruction):

    words=instruction.split()
    ins=words[0]
    registers=words[1].split(',')

    if ins in ['lw','sw']:
        r1=registers[0]
        ffs=registers[1].split('(')

        r2=ffs[1][:-1]
        try:
            rd=registerdict[r1]
            rs=registerdict[r2] #removing ')' from register
        except KeyError:
            print(f"Register not found in line {counter}")
            return
        
        immi=bin_converter(int(ffs[0]),12)

        if immi==-1:
            print(f'Immediate value out of range in line {counter}')
            return
        
    
        match ins:
            case "lw":
                codeinstruction=f"{immi}{rs}010{rd}0000011"
                print(codeinstruction)
                wf=open(output_file,'a')
                wf.write(codeinstruction+"\n")
                wf.close()
            case "sw":
                immi=immi[::-1]
                codeinstruction=f"{immi[11:4:-1]}{rd}{rs}010{immi[4::-1]}0100011"
                print(codeinstruction)
                wf=open(output_file,'a')
                wf.write(codeinstruction+"\n")
                wf.close()

    else:
        try:
            rd=registerdict[registers[0]]
            rs=registerdict[registers[1]]
    
        except KeyError:
            print(f"Register not found in line {counter}")
            return

        immi=bin_converter(int(registers[2]),12)

        if immi==-1: #to check if output is -1 which signifies error
            print(f'Immediate value out of range in line {counter}')
            return
        
        
        match ins:
            case "jalr":
                codeins="1100111"
                funct3="000"

            case _:
                codeins="0010011"
                itypes=['addi','slti','sltiu','xori','ori','andi','slli','srli','srai']
                codeitypes=["000","010","011","100","110","111","001","101","101"]
                funct3=codeitypes[itypes.index(ins)]
                # for slli, srli, srai the immediate are fixed as 0000000xxxxx, 0000000xxxxx, 0100000xxxxx because you can shift by only 0-31 positions on a 32 bit number (rs1(b))
        codeinstruction=f"{immi}{rs}{funct3}{rd}{codeins}"
        print(codeinstruction)
        wf=open(output_file,'a')
        wf.write(codeinstruction+"\n")
        wf.close()


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

supported_instructions=["add","sub","sll","slt","sltu","xor","srl","sra","or","and",
                        'addi','slti','sltiu','xori','ori','andi','slli','srli','srai',"lw","jalr",
                        "sw",
                        "beq","bne","blt","bge","bltu","bgeu",
                        "lui","auipc",
                        "jal",
                        "mul","rst","halt","rvrs",
                        ]


counter=1 #counter no used for error lines
last_line=len(assemblyinput)

programcounter=0x00000000 # 32 bit counter for PC

labelmap={} #map which stores label with PC address

for ind,ins in enumerate(assemblyinput): #maps all the labels and removes them too
    if ':' in ins:
        holder=ins.split(':')
        if holder[0] in (supported_instructions+ list(registerdict.keys())):
            print("Misuse of variable as label")
        else:
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

    #some exta instructions that are usually given in RISC V
    
    itypes=['addi','slti','sltiu','xori','ori','andi','slli','srli','srai','lw','jalr','sw']
    rtypes=["add","sub","sll","slt","sltu","xor","srl","or","and"]
    btypes=["beq","bne","blt","bge","bltu","bgeu"]
    
    if counter==last_line:
        if opcode in btypes:
            b_type(i)
            
        else:
            print("Last instrcution not halt instruction.")
    elif opcode in rtypes:
        r_type(i)

    elif opcode in btypes:
        b_type(i)


    elif opcode=="jal":
        j_type(i)

    elif opcode in ["lui","auipc"]:
        u_type(i)

    elif opcode in itypes:
        i_type(i)
#all others are same I am not sure about output order of each line
#keep all code above, above the increment in counters
    
    programcounter+=0x00000004
    counter+=1
    if counter >64:
        print("Extra Instructions above 64 not permitted.")
        break


