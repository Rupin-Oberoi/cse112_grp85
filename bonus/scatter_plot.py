from sys import stdin
import sys
import os
import matplotlib.pyplot as plt

file = open(r'source_bin.txt', 'r')
list_of_lines = file.readlines()

memory = []
for line in list_of_lines:
    memory.append(line[0:-1])
memory[-1] = list_of_lines[-1]
number_of_lines = len(memory)
i = number_of_lines
while i < 256:
    memory.append('0000000000000000')
    i = i + 1
k = 0
register_file = []
pc = 0
while k < 8:
    register_file.append('0000000000000000')
    k = k + 1


def dec_16_bin(a):
    bin_ = '{0:016b}'.format(a)
    if a > 65535:
        return bin_[-16:]
    elif a < 0:
        bin_ = dec_16_bin(0)
    return bin_


def dec_8_bin(a):
    bin_ = '{0:08b}'.format(a)
    if a > 255:
        return bin_[-8:]
    elif a < 0:
        bin_ = dec_8_bin(0)
    return bin_


def bin2dec(a):
    bin_ = int(a, 2)
    return bin_


halt_flag = False


def read_opcode(line, register_file, memory):
    global halt_flag
    global pc
    if line[0:5] == '00000':  # add
        pc += 1
        register_file[-1] = '0000000000000000'
        register_file[bin2dec(line[7:10])] = dec_16_bin(bin2dec(register_file[bin2dec(line[10:13])]) + bin2dec(register_file[bin2dec(line[13:])]))
        if bin2dec(register_file[bin2dec(line[10:13])]) + bin2dec(register_file[bin2dec(line[13:16])]) > 65535:
            register_file[-1] = register_file[-1][0:12] + '1' + register_file[-1][13:]
    elif line[0:5] == '00001':  # sub
        pc += 1
        register_file[-1] = '0000000000000000'
        register_file[bin2dec(line[7:10])] = dec_16_bin(bin2dec(register_file[bin2dec(line[10:13])]) - bin2dec(register_file[bin2dec(line[13:])]))
        if bin2dec(register_file[bin2dec(line[10:13])]) + bin2dec(register_file[bin2dec(line[13:16])]) < 0:
            register_file[-1] = register_file[-1][0:12] + '1' + register_file[-1][13:]
    elif line[0:5] == '00110':  # mul
        pc += 1
        register_file[-1] = '0000000000000000'
        register_file[bin2dec(line[7:10])] = dec_16_bin(bin2dec(register_file[bin2dec(line[10:13])]) * bin2dec(register_file[bin2dec(line[13:])]))
        if bin2dec(register_file[bin2dec(line[10:13])]) + bin2dec(register_file[bin2dec(line[13:16])]) > 65535:
            register_file[-1] = register_file[-1][0:12] + '1' + register_file[-1][13:]
    elif line[0:5] == '00010':  # mov immediate
        pc += 1
        register_file[-1] = '0000000000000000'
        register_file[bin2dec(line[5:8])] = dec_16_bin(bin2dec(line[8:]))
    elif line[0:5] == '01000':  # right shift
        pc += 1
        register_file[-1] = '0000000000000000'
        if bin2dec(line[8:]) < 16:
            register_file[bin2dec(line[5:8])] = '0' * bin2dec(line[8:]) + register_file[bin2dec(line[5:8])][0:(16 - bin2dec(line[8:]))]
        elif bin2dec(line[8:]) >= 16:
            register_file[bin2dec(line[5:8])] = '0' * 16
    elif line[0:5] == '01001':  # left shift
        pc += 1
        register_file[-1] = '0000000000000000'
        register_file[bin2dec(line[5:8])] = dec_16_bin(register_file[bin2dec(line[5:8])] * bin2dec(line[8:]))
    elif line[0:5] == '01010':  # bitwise xor
        pc += 1
        register_file[-1] = '0000000000000000'
        for i in range[0:16]:
            register_file[bin2dec(line[7:10])][i] = str(int(register_file[bin2dec(line[10:13])][i]) ^ int(register_file[bin2dec(line[13:])][i]))
    elif line[0:5] == '01011':  # bitwise or
        pc += 1
        register_file[-1] = '0000000000000000'
        for i in range[0:16]:
            register_file[bin2dec(line[7:10])][i] = str(int(register_file[bin2dec(line[10:13])][i]) | int(register_file[bin2dec(line[13:])][i]))
    elif line[0:5] == '01100':  # bitwise and
        pc += 1
        register_file[-1] = '0000000000000000'
        for i in range[0:16]:
            register_file[bin2dec(line[7:10])][i] = str(int(register_file[bin2dec(line[10:13])][i]) & int(register_file[bin2dec(line[13:])][i]))
    elif line[0:5] == '00011':  # mov register
        pc += 1
        register_file[bin2dec(line[10:13])] = register_file[bin2dec(line[13:])]
        register_file[-1] = '0000000000000000'
    elif line[0:5] == '00111':  # div
        pc += 1
        register_file[-1] = '0000000000000000'
        register_file[0] = dec_16_bin(bin2dec(register_file[bin2dec(line[10:13])]) // bin2dec(register_file[bin2dec(line[13:])]))
        register_file[1] = dec_16_bin(bin2dec(register_file[bin2dec(line[10:13])]) % bin2dec(register_file[bin2dec(line[13:])]))
    elif line[0:5] == '01101':  # invert
        pc += 1
        register_file[-1] = '0000000000000000'
        for i in range[0:16]:
            register_file[bin2dec(line[10:13])][i] = str(~int((register_file[bin2dec(line[13:])][i])))
    elif line[0:5] == '01110':  # compare
        pc += 1
        register_file[-1] = '0000000000000000'
        if register_file[bin2dec(line[10:13])] == register_file[bin2dec(line[13:])]:
            register_file[-1] = '0000000000000001'
        elif bin2dec(register_file[bin2dec(line[10:13])]) > bin2dec(register_file[bin2dec(line[13:])]):
            register_file[-1] = '0000000000000010'
        elif bin2dec(register_file[bin2dec(line[10:13])]) < bin2dec(register_file[bin2dec(line[13:])]):
            register_file[-1] = '0000000000000100'
    elif line[0:5] == '00100':  # load
        pc += 1
        register_file[-1] = '0000000000000000'
        register_file[bin2dec(line[5:8])] = memory[bin2dec(line[8:])]
    elif line[0:5] == '00101':  # store
        pc += 1
        register_file[-1] = '0000000000000000'
        memory[bin2dec(line[8:])] = register_file[bin2dec(line[5:8])]
    elif line[0:5] == '01111':  # jmp
        pc = bin2dec(line[8:])
        register_file[-1] = '0000000000000000'

    elif line[0:5] == '10000':  # jlt
        if register_file[-1][-3] == '1':
            pc =bin2dec(line[8:])
            register_file[-1] = '0000000000000000'
        else:
            pc += 1
            register_file[-1] = '0000000000000000'
    elif line[0:5] == '10001':  # jgt
        if register_file[-1][-2] == '1':
            pc = bin2dec(line[8:])
            register_file[-1] = '0000000000000000'
        else:
            pc += 1
            register_file[-1] = '0000000000000000'
    elif line[0:5] == '10010':  # je
        if register_file[-1][-1] == '1':
            pc = bin2dec(line[8:])
            register_file[-1] = '0000000000000000'
        else:
            pc += 1
            register_file[-1] = '0000000000000000'
    elif line[0:5] == '10011':  # hlt
        pc += 1
        halt_flag = True

cycle_list = []
pc_list = []
cycle = 0

def run(line):
    global cycle
    global pc_list
    global cycle_list
    read_opcode(list_of_lines[pc][0:-1], register_file, memory)
    cycle+=1
    pc_list.append(pc)
    cycle_list.append(cycle)
    if line[0:5] in ['00100', '00101']:
        cycle_list.append(cycle)
        pc_list.append((bin2dec(line[8:]))+1)



while halt_flag == False:
    run(list_of_lines[pc][0:-1])

plt.scatter(cycle_list, pc_list)
plt.xlabel('cycle number')
plt.ylabel('memory address accessed')
plt.title('SCATTER GRAPH')
plt.show()



file.close()
