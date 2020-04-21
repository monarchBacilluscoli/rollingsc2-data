#!/usr/bin/python3
import numpy as np

print("Hello, World!")

in_this_block = False
current_block_count = 0
block = ""

for current_block_count in range(1, 100, 1):
    f_in = open("./" + str(current_block_count) + "_clear.txt", mode='r')
    f_out = open("./" + str(current_block_count) + "_start.txt", mode='w')
    line = f_in.readline()

    while line:
        if(line.find("start:") != -1):
            # current_block_count += 1
            # f_out = open("./" + str(current_block_count) + "_clear.txt", mode='w')
            # # print(type(block))
            # block = replace_field_name(block)
            # f_out.write(block)
            # block = ""
            # f_out.close()
            in_this_block = True
        if in_this_block:
            block += line
        if(line == "\n"):
            # todo output
            f_out.write(block.replace("start:\n",""))
            # f_out.write("\n")
            block = ""
            in_this_block = False
        line = f_in.readline()
    f_in.close()
    f_out.close()
# print(block)
