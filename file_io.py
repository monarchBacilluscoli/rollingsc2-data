#!/usr/bin/python3
import numpy as np


def replace_field_name(block):
    block = block.replace("Enemy Loss average: ", "")
    block = block.replace("Enemy Loss best: ", "")
    block = block.replace("My Team Loss average: ", "")
    block = block.replace("My Team Loss best: ", "")
    block = block.replace("average: ", "")
    block = block.replace("best: ", "")
    block = block.replace(" ", "")
    block = block.replace("\t\t", "\t")
    return block


print("Hello, World!")

f = open("./obj_record.txt")

in_this_block = True
block_count = 10
current_block_count = 0
block = ""
line = f.readline()
while line:
    if(line.find("//") != -1): # 又碰上下一个
        current_block_count += 1
        f_out = open("./" + str(current_block_count) + "_clear.txt", mode='w')
        # print(type(block))
        block = replace_field_name(block)
        f_out.write(block)
        block = ""
        f_out.close()
    block += line
    line = f.readline()

current_block_count += 1
f_out = open("./" + str(current_block_count) + "_clear.txt", mode='w')
block = replace_field_name(block)
f_out.write(block)
block = ""
f_out.close()

# print(block)


f.close()
