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

supported_instructions=["add","sub","sll","slt","sltu","xor","srl","sra","or","and",
                        'addi','slti','sltiu','xori','ori','andi','slli','srli','srai',"lw","jalr",
                        "sw",
                        "beq","bne","blt","bge","bltu","bgeu",
                        "lui","auipc",
                        "jal",
                        "mul","rst","halt","rvrs",
                        ]

def process_1(registers):
    try:
        rd=registerdict[registers[0]]
        rs=registerdict[registers[1]]
    
    except KeyError:
        print(f"Register not found in line {counter}")
        return None

    except:
        print("Unknown Error")
        return None

    immi=binconverter(int(registers[2]),12)

    if immi=='-1': #to check if output is -1 which signifies error
        print(f'Immediate value out of range in line {counter}')
        return None
    
    return rd, rs, immi
                
def process_2(registers):
    r1=registers[0]
    ffs=registers[1].split('(')
    r2=ffs[1][-1]
    try:
        rd=registerdict[r1]
        rs=registerdict[r2] #removing ')' from register
    except KeyError:
        print(f"Register not found in line {counter}")
        return
    imm=binconverter(int(ffs[0]),12)

    if imm=='-1':
        print(f'Immediate value out of range in line {counter}')
        return

    return rd, rs, imm
with open("input.txt","r") as inputstream:
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

    ins=instructionsplit[0]

    try:
        registers=instructionsplit[1].split(",")
    except:
        pass #case for bonus instructions when nothing follows rst or halt

    #some exta instructions that are usually given in RISC V

    if ins in supported_instructions:
        match ins:
            case "addi":
                result=process_1(registers)
                if result:
                    rd,rs,immi=result
                print(f"{immi}{rs}000{rd}0010011") 

            case "slti":
                result=process_1(registers)
                if result:
                    rd,rs,immi=result
                    
                print(f"{immi}{rs}010{rd}0010011") 
            case "sltiu":
                result=process_1(registers)
                if result:
                    rd,rs,immi=result

                print(f"{immi}{rs}011{rd}0010011") 
            case "xori":
                result=process_1(registers)
                if result:
                    rd,rs,immi=result

                print(f"{immi}{rs}100{rd}0010011") 
            case "ori":
                result=process_1(registers)
                if result:
                    rd,rs,immi=result

                print(f"{immi}{rs}110{rd}0010011") 
            case "andi":
                result=process_1(registers)
                if result:
                    rd,rs,immi=result

                print(f"{immi}{rs}111{rd}0010011")
            
            # case "slli":
            #     result=process_1(registers)
            #     if result:
            #         rd,rs,immi=result

            #     print(f"{immi}{rs}001{rd}0010011") 
                
            # case "srli":
            #     result=process_1(registers)
            #     if result:
            #         rd,rs,immi=result

            #     print(f"{immi}{rs}101{rd}0010011") 
                
            # case "srai":
            #     result=process_1(registers)
            #     if result:
            #         rd,rs,immi=result

            #     print(f"{immi}{rs}101{rd}0010011")
            # for slli, srli, srai the immediate are fixed as 0000000xxxxx, 0000000xxxxx, 0100000xxxxx because you can shift by only 0-31 positions on a 32 bit number (rs1(b))
            
            case "lw":
                result=process_2(registers)
                if result:
                    rd,rs,immi=result

                print(f"{immi}{rs}010{rd}0000011")

            case "jalr":
                result=process_1(registers)
                if result:
                    rd,rs,immi=result

                print(f"{immi}{rs}000{rd}1100111")
            case "sw":
                result=process_2(registers)
                if result:
                    rs2,rs1,immi=result

                immmi=immi[::-1]
                print(f"{immi[11:4:-1]}{rs2}{rs1}010{c[4::-1]}0100011")


        programcounter+=0x00000004
        counter+=1

    else:
        print(f"Instruction '{ins}' in line {counter} Not supported by this architecture.")
