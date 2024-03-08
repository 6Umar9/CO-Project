 

def registermap(s):
    registerdict={
    "zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011",
    "tp": "00100", "t0": "00101", "t1": "00110", "t2": "00111",
    "s0": "01000", "fp": "01000",  # Note the duplicate key "fp"
    "s1": "01001", "a0": "01010", "a1": "01011", "a2": "01100",
    "a3": "01101", "a4": "01110", "a5": "01111", "a6": "10000",
    "a7": "10001", "s2": "10010", "s3": "10011", "s4": "10100",
    "s5": "10101", "s6": "10110", "s7": "10111", "s8": "11000",
    "s9": "11001", "s10": "11010", "s11": "11011", "t3": "11100",
    "t4": "11101", "t5": "11110", "t6": "11111"}
    try:
        return registerdict[s]
    except KeyError:
        return -1

inputstream=open("input.txt","r")
assembly=inputstream.read()
assemblyinput=assembly.split('\n')

counter=0
programcounter=0x00000000

labelmap={}

assemblyinput.pop()
for i in assemblyinput:
    labelsplit=i.split(":")
    if len(labelsplit)>1:
        labelmap[labelsplit[0]]=programcounter
        instructionsplit=labelsplit[1].split()
    else:
        instructionsplit=labelsplit[0].split()
    opcode=instructionsplit[0]
    print(opcode)
    arguementsplit=instructionsplit[1].split(",")
    programcounter+=0x00000004
    counter+=1

print(labelmap)
