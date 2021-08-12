import sys
input_file = sys.stdin.readlines()


'''the below functions are used to determine the type of statement a line is'''
var_table  = []

def check_variable(s):
    trimmed = s.trim()
    obj = trimmed.split()
    if obj[0]=="var":
        return True
    else:
        return False

def ret_variable(s):
    trimmed = s.trim()
    obj = trimmed.split()
    if check_variable(s) == True:
        var_table.append(obj[1])
        return obj[1]
    else:
        return False

label_list = []

def check_label(s):
    if s.find(":")!=-1:
        return True
    else:
        return False

def ret_label(s):
    if check_label(s)==True:
        l_string = s.lstrip()
        position = s.find(":")
        label_name = l_string[0:position:1]
        label_list.append(label_name)
        return label_name
    else:
        return False

store_rgstr_list = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6']

instr_list = ["add", "sub", "mov", "mov", "ld", "st", "mul", "div", "rs", "ls", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt", "je", "hlt"]
opc_list = ['00000', '00001', '00010', '00011', '00100', '00101', '00110', '00111', '01000', '01001', '01010', '01011', '01100', '01101', '01110', '01111', '10000', '10001', '10010', '10011']
opc_type_list = ['A','A','B','C','D','D','A', 'C','B','B','A','A','A','C','C','E','E','E','E','F']

def int2bin(n):
    mid_bin = format(n,"b")
    str_mid_bin = str(mid_bin)
    while (len(str_mid_bin)<8):
        str_mid_bin = "0" + str_mid_bin
    return int(str_mid_bin)

memory_table = []
for i in range(0, 255):
    memory_table.append(int2bin(i))


opc_dict = {}
opc_dict["add"] = ['00000','A']
opc_dict["sub"] = ['00001','A']
opc_dict["mov"] = ['00010','B']
opc_dict["mov"] = ['00011','C']
opc_dict["ld"]  = ['00100','D']
opc_dict["st"]  = ['00101','D']
opc_dict["mul"] = ['00110','A']
opc_dict["div"] = ['00111','C']
opc_dict["rs"]  = ['01000','B']
opc_dict["ls"]  = ['01001','B']
opc_dict["xor"] = ['01010','A']
opc_dict["or"]  = ['01011','A']
opc_dict["and"] = ['01100','A']
opc_dict["not"] = ['01101','C']
opc_dict["cmp"] = ['01110','C']
opc_dict["jmp"] = ['01111','E']
opc_dict["jlt"] = ['10000','E']
opc_dict["jgt"] = ['10001','E']
opc_dict["je"]  = ['10010','E']
opc_dict["hlt"] = ['10011','F']

type_dict = {}
type_dict['00000'] = 'A'
type_dict['00001'] = 'A'
type_dict['00010'] = 'B'
type_dict['00011'] = 'C'
type_dict['00100'] = 'D'
type_dict['00101'] = 'D'
type_dict['00110'] = 'A'
type_dict['00111'] = 'C'
type_dict['01000'] = 'B'
type_dict['01001'] = 'B'
type_dict['01010'] = 'A'
type_dict['01011'] = 'A'
type_dict['01100'] = 'A'
type_dict['01101'] = 'C'
type_dict['01110'] = 'C'
type_dict['01111'] = 'E'
type_dict['10000'] = 'E'
type_dict['10001'] = 'E'
type_dict['10010'] = 'E'
type_dict['10011'] = 'F'

def instr2opc(s):
    instr = ''
    trimmed = s.trim()
    obj = trimmed.split()
    if check_valid_instr(s):
        obj[0] = instr
        opc = opc_dict[instr][1]
        return opc


def check_valid_instr(s):
    trimmed = s.trim()
    obj = trimmed.split()
    if check_label(trimmed) == False and check_variable(trimmed)==False:
        if obj[0] in instr_list:
            return True
        else:
            print('ERROR: typo in instruction name')
    elif check_label(trimmed) == True and check_variable(trimmed) == False:
        if obj[1] in instr_list:
            return True
        else:
            print ('ERROR: Typo in instruction name')
    else:
        return False

def read_operands(s):
    trimmed = s.trim()
    obj = trimmed.split()
    if type_dict[instr2opc(s)] == 'A':
        opr1 = ''
        opr2 = ''
        opr3 = ''
        if len(obj) != 4:
            print('SYNTAX ERROR')
        elif len(obj) == 4:
            opr1 = obj[1]
            opr2 = obj[2]
            opr3 = obj[3]
    
    if type_dict[instr2opc(s)] == 'B':
        opr1 = ''
        opr2 = 0
        if len(obj) !=3:
            print('SYNTAX ERROR: wrong instruction type')
        elif len(obj) == 3:
            if int(obj[2])>=0 and int(obj[2])<=255:
                opr1 = obj[1]
                opr2 = int(obj[2])
            else:
                print('ERROR: Illegal immediate value')
    
    if type_dict[instr2opc(s)] == 'C':
        opr1 = ''
        opr2 = 0
        if len(obj) !=3:
            print('SYNTAX ERROR: wrong instruction type')
        elif len(obj) == 3:
            if obj[1] in store_rgstr_list:
                opr1 = obj[1]
            else: 
                print('SYNTAX ERROR: wrong instruction type')
            opr2 = obj[2]
        
    if type_dict[instr2opc(s)] == 'D':
        opr1 = ''
        opr2 = 0
        if len(obj) !=3:
            print("SYNTAX ERROR: wrong instruction type")
        elif len(obj) ==3:
            if obj[1] in store_rgstr_list and obj[2] in var_table:
                opr1 = obj[1]
                opr2 = obj[2]
            elif obj[1] in store_rgstr_list and obj[2] not in var_table:
                print('ERROR: Variable not defined')
            else:
                print ('SYNTAX ERROR: wrong instruction type')

    if type_dict[instr2opc(s)] == 'E':
        opr1 = 0
        if len(obj) != 2:
            print("SYNTAX ERROR: wrong instruction type")
        elif len(obj) == 2:
            if  obj[1] in label_list:
                obj[1] = opr1
            else:
                print('Undefined label used')
    
