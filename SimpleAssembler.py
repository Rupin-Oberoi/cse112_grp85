outputVar = [000000000000000000000]
variableNameList = []
numberOfLines = 0

s = input("enter command \n")

commandArray = s.split()

reg0 = "000"
reg1 = "001"
reg2 = "010"
reg3 = "011"
reg4 = "100"
reg5 = "101"
reg6 = "110"
flag = "111"

Type = ""


def howManyZeros(howMany, starting):
    zeros = "0" * howMany
    outputVar[starting: starting + howMany] = zeros


def registerCode(register, starting):
    outputVar[starting: starting + 3] = register


def opCode():
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
        howManyZeros(8-jb, 8)
        outputVar[16-jb:16] = binaryConverter(value)


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
    print("finish this")


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


def functionVar():
    variableNameList.append(commandArray[1])

variableDictionary{}

opCode()
numberOfLines += 1

print(outputVar)
