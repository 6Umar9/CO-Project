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

###df registermap(s):
    #registerdict={
    #"zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011",
    #"tp": "00100", "t0": "00101", "t1": "00110", "t2": "00111",
    #"s0": "01000", "fp": "01000",
    #"s1": "01001", "a0": "01010", "a1": "01011", "a2": "01100",
    #"a3": "01101", "a4": "01110", "a5": "01111", "a6": "10000",
    #"a7": "10001", "s2": "10010", "s3": "10011", "s4": "10100",
    #"s5": "10101", "s6": "10110", "s7": "10111", "s8": "11000",
    #"s9": "11001", "s10": "11010", "s11": "11011", "t3": "11100",
    #"t4": "11101", "t5": "11110", "t6": "11111"}
    #try:
    #    return registerdict[s]
    #except KeyError:
    #    return -1

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

with open("input.txt","r") as inputstream:
        assembly=inputstream.read()
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
            print(f"0010011{a}000{b}{c}")
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
            print(f"0010011{a}011{b}{c}")
        case "lw":
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
            print(f"0000011{a}010{b}{c}")
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
            print(f"1110011{a}000{b}{c}")
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
            print(f"0100011{c[:5]}010{b}{a}{c[5:]}")
                
#all others are same i am not sure about output order of each line
#keep all code for one line above increment in counters
        
    programcounter+=0x00000004
    counter+=1



#R-type instructions
def r_type(string1):
    
    list1 = string1.split()
    opcode = list1[0]
    reg=list1[1].split(',')
    rd=registerdict.get(reg[0])
    rs1=registerdict.get(reg[1])
    rs2=registerdict.get(reg[2])    
        
        

    op_code = {

        'add' : '0110011',
        'sub' : '0110011',
        'sll' : '0110011',
        'slt' : '0110011',
        'sltu' : '0110011',
        'xor' : '0110011',
        'srl' : '0110011',
        'or' : '0110011',
        'and' : '0110011'
    }

    if opcode == 'add':
        func3 = '000'
        func7='0000000'
    
    elif opcode == 'sub':
        func3 = '000'
        func7='0100000'

    elif opcode == 'sll':
        func3 = '001'
        func7='0000000'

    elif opcode == 'slt':
        func3 = '010'
        func7='0000000'

    elif opcode == 'sltu':
        func3 = '011'
        func7='0000000'

    elif opcode == 'xor':
        func3 = '100'
        func7='0000000'

    elif opcode == 'srl':
        func3 = '101'
        func7='0000000'

    elif opcode == 'or':
        func3 = '110'
        func7='0000000'

    elif opcode == 'and':
        func3 = '111'
        func7='0000000'

    else:
        raise ValueError(f"Invalid opcode for R-type instruction")
    
    bin_str = func7+rs2+rs1+func3+rd+op_code[opcode]
    return bin_str
        
#B-type Instructions
def b_type(string1):
    
    linesplit = string1.split() #seperating Opcode and the registers/immediates
    opcode = linesplit[0] #opcode assigned
    registers = linesplit[1].split(',') #spliting the registers and immediates

    registerdict={ #dictionary with all register address
    "zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011",
    "tp": "00100", "t0": "00101", "t1": "00110", "t2": "00111",
    "s0": "01000", "fp": "01000",
    "s1": "01001", "a0": "01010", "a1": "01011", "a2": "01100",
    "a3": "01101", "a4": "01110", "a5": "01111", "a6": "10000",
    "a7": "10001", "s2": "10010", "s3": "10011", "s4": "10100",
    "s5": "10101", "s6": "10110", "s7": "10111", "s8": "11000",
    "s9": "11001", "s10": "11010", "s11": "11011", "t3": "11100",
    "t4": "11101", "t5": "11110", "t6": "11111"}

    match opcode:

        case "beq":
            try: #test for register to fit for B-Type instructions
                a=registerdict[registers[1]]
                b=registerdict[registers[2]]
            except KeyError:
                print(f"Register not found in line {counter}")
                #break #implement it in the for loop later on
            c=binconverter(int(registers[0]),5) #converting immediate to binary
            d = binconverter(int(registers[3]),8)
            if c=='-1' or d == '-1': #to check if output is -1 which signifies error as mentioned above
                print(f'Immediate value out of range in line {counter}')
                #break
            print(f"1100011{c}000{a}{b}{d}")

        case "bne":
            try:
                a = registerdict[registers[1]]
                b = registerdict[registers[2]]
            except KeyError:
                print(f"Register not found in line {counter}")
                #break
            c = binconverter(int(registers[0]),5)
            d = binconverter(int(registers[3]),8)
            if c == '-1' or d == '-1':
                print(f"Immediate value out of range in line{counter}")
                #break
            print(f"1100011{c}001{a}{b}{d}")

        case "blt":
            try:
                a = registerdict[registers[1]]
                b = registerdict[registers[2]]
            except KeyError:
                print(f"Register not found in line {counter}")
                #break
            c = binconverter(int(registers[0]),5)
            d = binconverter(int(registers[3]),8)
            if c == '-1' or d == '-1':
                print(f"Immediate value out of range in line{counter}")
                #break
            print(f"1100011{c}100{a}{b}{d}")

        case "bge":
            try:
                a = registerdict[registers[1]]
                b = registerdict[registers[2]]
            except KeyError:
                print(f"Register not found in line {counter}")
                #break
            c = binconverter(int(registers[0]),5)
            d = binconverter(int(registers[3]),8)
            if c == '-1' or d == '-1':
                print(f"Immediate value out of range in line{counter}")
                #break
            print(f"1100011{c}101{a}{b}{d}")

        case "bltu":
            try:
                a = registerdict[registers[1]]
                b = registerdict[registers[2]]
            except KeyError:
                print(f"Register not found in line {counter}")
                #break
            c = binconverter(int(registers[0]),5)
            d = binconverter(int(registers[3]),8)
            if c == '-1' or d == '-1':
                print(f"Immediate value out of range in line{counter}")
                #break
            print(f"1100011{c}110{a}{b}{d}")
        
        case "bgeu":
            try:
                a = registerdict[registers[1]]
                b = registerdict[registers[2]]
            except KeyError:
                print(f"Register not found in line {counter}")
                #break
            c = binconverter(int(registers[0]),5)
            d = binconverter(int(registers[3]),8)
            if c == '-1' or d == '-1':
                print(f"Immediate value out of range in line{counter}")
                #break
            print(f"1100011{c}111{a}{b}{d}")
    #programcounter+= int(registers[]) #figuring this out still
        
    counter += 1;
