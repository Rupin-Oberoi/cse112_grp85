from sys import stdin
list_of_lines = []
for line in stdin:
    list_of_lines.append(line)


output_line = '0000000000000000'
error_flag = -1

def dec_8_bin(a):
    bin_ = '{0:08b}'.format(a)
    if a>255:
        return bin_[-8:]
    elif a<0:
        bin_ = dec_8_bin(0)
    return bin_

variable_dict = {}
label_dict = {}

memory_list = []
for line in list_of_lines:
    if line[0:3]!='var':
        memory_list.append(line)

len = len(memory_list)
i = len
while i<256:
    memory_list.append('00000000')
    i+=1

halt_flag = 0

reg2bin = ['000','001','010','011','100','101','110','111']
reg2bin_dict = {'R0':'000', 'R1':'001', 'R2':'010', 'R3':'011', 'R4':'100', 'R5':'101', 'R6':'110', 'FLAGS':'111'}

def check_var(line):
    global len
    global variable_dict
    obj = line.split()
    if obj[0]== 'var':
        return True
    else:
        return False
        
def allot_var(line):
    global len
    global variable_dict
    obj = line.split()
    if check_var(line)== True:
        variable_dict[obj[1]] = len
        len+=1

def check_label(line):
    if line.find(':')!=-1:
        return True
    else:
        return False

def allot_label(line):
    global len
    global label_dict
    obj = line.split()
    if check_label(line)==True:
        a = memory_list.index(line)
        label_dict[obj[0][0:-1]] = a
        len+=1


    
def instr2opc(line):
    global output_line
    global error_flag
    global halt_flag
    obj = line.split()
    opc = '00000'
    if check_label(line)==False:
        instr = obj[0]
    elif check_label(line) ==True:
        instr = obj[1]
    if instr == 'add':
        opc = '00000'
    if instr == 'sub':
        opc = '00001'
    if instr == 'mov' and obj[2][0]=='$':
        opc = '00010'
    if instr == 'mov' and obj[2][0]!='$':
        opc = '00011'
    if instr == 'ld':
        opc = '00100'
    if instr == 'st':
        opc = '00101'
    if instr == 'mul':
        opc = '00110'
    if instr == 'div':
        opc = '00111'
    if instr == 'rs':
        opc = '01000'
    if instr == 'ls':
        opc = '01001'
    if instr == 'xor':
        opc = '01010'
    if instr == 'or':
        opc = '01011'
    if instr == 'and':
        opc = '01100'
    if instr == 'not':
        opc = '01101'
    if instr == 'cmp':
        opc = '01110'
    if instr == 'jmp':
        opc = '01111'
    if instr == 'jlt':
        opc = '10000'
    if instr == 'jgt':
        opc = '10001'
    if instr == 'je':
        opc = '10010'
    if instr == 'hlt':
        opc = '10011'
        halt_flag = 1
    else:
        error_flag = 1
    output_line = opc + output_line[5:]

def read_operands(line):
    global output_line
    global memory_list
    obj = line.split()
    opr1 = ''
    opr2 = ''
    opr3 = ''
    imm = ''
    mem = ''
    if check_label(line) == False:
        if obj[0] in ['add', 'sub', 'mul', 'or', 'xor', 'and']:
            opr1 = obj[1]
            opr2 = obj[2]
            opr3 = obj[3]
            output_line = output_line[0:7] + reg2bin_dict[opr1] + reg2bin_dict[opr2] + reg2bin_dict[opr3]
        elif obj[0] in ['rs', 'ls'] or (obj[0] == 'mov' and obj[2][0] == '$'):
            opr1 = obj[1]
            imm = obj[2]
            output_line = output_line[0:5] + reg2bin_dict[opr1] + dec_8_bin(int((imm[1:])))
        elif obj[0] in ['div', 'not', 'cmp'] or (obj[0] == 'mov' and obj[2][0]!='$'):
            opr1 = obj[1]
            opr2 = obj[2] 
            output_line = output_line[0:5] +'00000'+ reg2bin_dict[opr1] + reg2bin_dict[opr2]
        elif obj[0] in ['ld', 'st']:
            opr1 = obj[1]
            mem = obj[2]
            output_line = output_line[0:5] + reg2bin_dict[opr1] + dec_8_bin(variable_dict[mem])
        elif obj[0] in ['jmp', 'jlt', 'jgt', 'je']:
            mem = obj[1]
            output_line = output_line[0:8] + dec_8_bin(label_dict[mem])
        elif obj[0]=='hlt':
            output_line = output_line[0:5] + '00000000000'
        
        return [opr1, opr2, opr3, imm, mem]
    
    elif check_label(line) == True:
        if obj[1] in ['add', 'sub', 'mul', 'or', 'xor', 'and']:
            opr1 = obj[2]
            opr2 = obj[3]
            opr3 = obj[4]
            output_line = output_line[0:7] + reg2bin_dict[opr1] + reg2bin_dict[opr2] + reg2bin_dict[opr3]
        elif obj[1] in ['rs', 'ls'] or (obj[1] == 'mov' and obj[3][0] == '$'):
            opr1 = obj[2]
            imm = obj[3]
            output_line = output_line[0:5] + reg2bin_dict[opr1] + dec_8_bin(int((imm[1:])))
        elif obj[1] in ['div', 'not', 'cmp'] or (obj[1] == 'mov' and obj[3][0]!='$'):
            opr1 = obj[2]
            opr2 = obj[3] 
            output_line = output_line[0:10] + reg2bin_dict[opr1] + reg2bin_dict[opr2]
        elif obj[1] in ['ld', 'st']:
            opr1 = obj[2]
            mem = obj[3]
            output_line = output_line[0:5] + reg2bin_dict[opr1] + dec_8_bin(variable_dict[mem])
        elif obj[1] in ['jmp', 'jlt', 'jgt', 'je']:
            mem = obj[2]
            output_line = output_line[0:8] + dec_8_bin(label_dict[mem])
        elif obj[1]=='hlt':
            output_line = output_line[0:5] + '00000000000'
        
hlt_error =0
imm_error = 0
instr_error = 0
def pass1(line):
    global list_of_lines
    allot_var(line)
    allot_label(line)
line_number = 0
def pass0(line):
    global list_of_lines
    global hlt_error
    global imm_error
    global instr_error
    obj = line.split()
    global line_number 
    line_number+=1
    if list_of_lines[-1].strip()[-3:] !='hlt':
        print('last instruction is not halt')
        hlt_error = 1
    if line!='\n':    
        if check_label(line) == False:
            if obj[0] == 'mov' and obj[2][0]=='$':
                if int(obj[2][1:])>255 or int(obj[2][1:])<0:
                    print('Error on line '+str(line_number)+': Illegal immediate value used')
                    imm_error = 1
    if line!='\n':
        if check_label(line)==False:
            if obj[0] not in ['add','sub','mov','jmp','jlt','je','jgt','div','mul','ld','st','rs','ls','xor','or','and','not','cmp','hlt', 'var']:
                instr_error =1
                print('Error on line ' + str(line_number)+ ': Typo in instruction name')
    

def pass2(line):
    instr2opc(line)
    read_operands(line)
    if check_var(line) == False:
        print(output_line)

for line in list_of_lines:
    pass0(line)
    if hlt_error==1:
        break
    if imm_error ==1:
        break
    if instr_error==1:
        break

for line in list_of_lines:
    if hlt_error + imm_error + instr_error ==0:
        if line!='\n':
            pass1(line)

for line in list_of_lines:
    if hlt_error + imm_error + instr_error ==0:
        if line!='\n':
            pass2(line)
