import re
import sys
from io import StringIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import setting_names as nm


def parse_setting(settings, item):
    individuals = settings.split(",")
    for index in range(len(individuals)):
        individuals[index] = individuals[index].replace(" ", '')
        pair = individuals[index].split(':')
        if pair[0] == item:
            return int(pair[1])
    return "no value"


# todo 先要处理成长类型数据，（再处理成宽类型数据？），然后绘图。

print(nm.sim_length)

raw_colomns = ['dmg', 'dmg_shd', 'hurt', 'hurt_shd', 'heal',
               'heal_shd', 'win_loop', 'map', 'time', 'settings']

f_in = open("test_scores.txt")
line = f_in.readline()
block = ""
data_name = ""
whole = pd.DataFrame(columns=raw_colomns)

while line:  # 读文件
    if (line.find("//") == -1 and line != ""):  # 写入
        block += line
    line = f_in.readline()

df = pd.read_csv(StringIO(block), sep="\t", header=None)
df.columns = raw_colomns
whole = pd.concat([whole, df])

whole.insert(whole.shape[1], nm.is_enemy_pop_evo, 0)
whole.insert(whole.shape[1], "sim_length", 0)
whole.insert(whole.shape[1], nm.population_size, 0)

for i in range(0, whole.shape[0]):
    settings_string = whole.loc[i, 'settings']
    whole.loc[i, nm.sim_length] = parse_setting(settings_string, nm.sim_length)
    whole.loc[i, nm.population_size] = parse_setting(settings_string, nm.population_size)
    whole.loc[i, nm.is_enemy_pop_evo] = parse_setting(settings_string, nm.is_enemy_pop_evo)

sns.set_theme()
sns.relplot(data=whole, y="dmg", x=nm.sim_length, hue=nm.is_enemy_pop_evo)

plt.show()
print("end")
# print(whole.iloc[:, 9])
