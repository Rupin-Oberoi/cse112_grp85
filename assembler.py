code_to_be_converted = open('assembly_lang.txt', 'r')
list_of_lines = code_to_be_converted.readlines()
variableNameList = []

outputVar = [000000000000000000000]
numberOfLines = 0

register_data_dict = {}
register_data_dict['R0'] = 0000000000000000
register_data_dict['R1'] = 0000000000000000
register_data_dict['R2'] = 0000000000000000
register_data_dict['R3'] = 0000000000000000
register_data_dict['R4'] = 0000000000000000
register_data_dict['R5'] = 0000000000000000
register_data_dict['R6'] = 0000000000000000
register_data_dict['FLAGS'] = '0000000000000000'


def register_update(outputVar, commandArray):
    if str(outputVar[0:5]) == '00000':
        register_data_dict[commandArray[1]] = register_data_dict[commandArray[2]] + register_data_dict[commandArray[3]]
        if register_data_dict[commandArray[1]] > 255:
            register_data_dict['FLAGS'] = register_data_dict['FLAGS'][0:12] + '1' + register_data_dict['FLAGS'][13:]
            register_data_dict[commandArray[1]] = register_data_dict[commandArray[1]] - 256

    elif str(outputVar[0:5]) == '00001':
        register_data_dict[commandArray[1]] = register_data_dict[commandArray[2]] - register_data_dict[commandArray[3]]
        if register_data_dict[commandArray[1]] < 0:
            register_data_dict['FLAGS'] = register_data_dict['FLAGS'][0:12] + '1' + register_data_dict['FLAGS'][13:]
            register_data_dict[commandArray[1]] = 0

    elif str(outputVar[0:5]) == '00110':
        register_data_dict[commandArray[1]] = register_data_dict[commandArray[2]] * register_data_dict[commandArray[3]]
        if register_data_dict[commandArray[1]] > 255:
            register_data_dict['FLAGS'] = register_data_dict['FLAGS'][0:12] + '1' + register_data_dict['FLAGS'][13:]
    elif str(outputVar[0:5]) == '00111':
        register_data_dict[commandArray[1]] = int(
            register_data_dict[commandArray[2]] / register_data_dict[commandArray[3]])
    elif str(outputVar[0:5]) == '00011':
        register_data_dict[commandArray[1]] = register_data_dict[commandArray[2]]
    elif str(outputVar[0:5]) == '00010':
        register_data_dict[commandArray[1]] = int(commandArray[2])
    elif str(outputVar[0:5]) == '01110':
        if register_data_dict[commandArray[1]] == register_data_dict[commandArray[2]]:
            register_data_dict['FLAGS'] = register_data_dict['FLAGS'][0:15] + '1'
        elif register_data_dict[commandArray[1]] > register_data_dict[commandArray[2]]:
            register_data_dict['FLAGS'] = register_data_dict['FLAGS'][0:14] + '1' + register_data_dict['FLAGS'][15]
        elif register_data_dict[commandArray[1]] < register_data_dict[commandArray[2]]:
            register_data_dict['FLAGS'] = register_data_dict['FLAGS'][0:13] + '1' + register_data_dict['FLAGS'][14:]


s = input("enter command \n")

commandArray = s.split()

R0 = "000"
R1 = "001"
R2 = "010"
R3 = "011"
R4 = "100"
R5 = "101"
R6 = "110"
FLAGS = "111"


def howManyZeros(howMany, starting):
    global outputVar
    zeros = "0" * howMany
    outputVar[starting: starting + howMany] = zeros


def registerCode(register, starting):
    global outputVar
    outputVar[starting: starting + 3] = register


def opCode(commandArray):
    instruction = commandArray[0]
    operationCodes(instruction)


def initCommand(code):
    outputVar[0:5] = code


def operationCodes(instruction):
    if instruction == "add":
        initCommand("00000")
        functionA()

    elif instruction == "sub":
        initCommand("00001")
        functionA()

    elif instruction == "mul":
        initCommand("00110")
        functionA()

    elif instruction == "xor":
        initCommand("01010")
        functionA()

    elif instruction == "sub":
        initCommand("01011")
        functionA()

    elif instruction == "and":
        initCommand("01100")
        functionA()

    elif instruction == "mov" and commandArray[2][0] == "$":
        initCommand("00010")
        functionB()

    elif instruction == "mov" and commandArray[2][0] == "r":
        initCommand("00011")
        functionC()

    elif instruction == "ld":
        initCommand("00100")
        functionD()

    elif instruction == "st":
        initCommand("00101")
        functionD()

    elif instruction == "div":
        initCommand("00111")
        functionC()

    elif instruction == "rs":
        initCommand("01000")
        functionB()

    elif instruction == "ls":
        initCommand("01001")
        functionB()

    elif instruction == "not":
        initCommand("01101")
        functionC()

    elif instruction == "cmp":
        initCommand("01110")
        functionC()

    elif instruction == "jmp":
        initCommand("01111")
        functionE()

    elif instruction == "jlt":
        initCommand("10000")
        functionE()

    elif instruction == "jgt":
        initCommand("10001")
        functionE()

    elif instruction == "je":
        initCommand("10010")
        functionE()

    elif instruction == "halt":
        initCommand("10011")
        functionF()

    elif instruction == "var":
        functionVar()


def immediateValue(value):
    jb = len(binaryConverter(value))

    if jb > 8:
        print("FLAG")
    else:
        howManyZeros(8 - jb, 8)
        outputVar[16 - jb:16] = binaryConverter(value)


def binaryConverter(value):
    binaryNumber = bin(int(value))
    finalBinary = binaryNumber[2:len(binaryNumber)]
    return finalBinary


def registerCall(register, start):
    binaryNumber = binaryConverter(register)
    if len(binaryNumber) == 3:
        outputVar[start:start + 3] = binaryNumber

    elif len(binaryNumber) == 2:
        outputVar[start:start + 3] = "0" + binaryNumber

    elif len(binaryNumber) == 1:
        outputVar[start:start + 3] = "00" + binaryNumber


def memoryAddress(value):
    index = numberOfLines.text("value")
    


def functionA():
    howManyZeros(2, 5)
    registerCall(commandArray[1][1], 7)
    registerCall(commandArray[2][1], 10)
    registerCall(commandArray[3][1], 13)


def functionB():
    registerCall(commandArray[1][1], 5)
    immediateValue(commandArray[2][1:len(commandArray[2])])


def functionC():
    howManyZeros(5, 5)
    registerCall(commandArray[1][1], 11)
    registerCall(commandArray[2][1], 14)


def functionD():
    registerCall(commandArray[1][1], 5)
    memoryAddress(commandArray[2])


def functionE():
    howManyZeros(3, 5)
    memoryAddress(commandArray[1])


def functionF():
    howManyZeros(11, 5)


def functionVar(variableNameList):
    if commandArray[1] not in variableNameList:
        variableNameList.append(commandArray[1])


def pass1(list_of_lines):
    variableNameList = []
    variable_address_list = []
    non_var_flag = 0
    line_number = 0
    last_line = list_of_lines[-1]
    last_line_trim = last_line.strip()
    if last_line_trim != 'hlt':
        print('ERROR: LAST STATEMENT IS NOT HLT')
    else:
        for s in list_of_lines:
            outputVar = [000000000000000000000]
            line_number += 1
            trimmed = s.strip()
            commandArray = trimmed.split()
            opCode(commandArray)
            register_update(outputVar, commandArray)
            print(*outputVar, sep='')
            if trimmed == 'hlt':
                break

def printvaraibles():
    for i in variableNameList:
        print (commandArray)
    binaryConverter(variableNameList[i])
    
        
pass1()
opCode(commandArray)

code_to_be_converted.close()
