import re
import sys
from io import StringIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import setting_names as nm

file_path = "/home/liuyongfeng/s2client-api-liu/s2client-api/scores/test_scores.txt"
start_comment = "evo higher generations"

def parse_setting(settings, item):
    individuals = settings.split(",")
    for index in range(len(individuals)):
        individuals[index] = individuals[index].replace(" ", '')
        pair = individuals[index].split(':')
        if pair[0] == item:
            return int(pair[1])
    return "no value"


# 准备数据

raw_colomns = [nm.damage_to_enemy, 'dmg_shd', nm.damage_to_mine, 'hurt_shd', 'heal',
               'heal_shd', nm.loops, 'map', 'time', 'settings']

f_in = open(file_path, )
line = f_in.readline()
block = ""
data_name = ""
whole = pd.DataFrame(columns=raw_colomns)

# 读取数据

start = False
while line:  # 读文件
    if (line.find(start_comment) != -1):
        start = True;
    if (start and line.find("//") == -1 and line != ""):  # 写入
        block += line
    line = f_in.readline()

df = pd.read_csv(StringIO(block), sep="\t", header=None)
df.columns = raw_colomns
whole = pd.concat([whole, df])

# 进一步处理

whole.insert(whole.shape[1], nm.is_enemy_pop_evo, 0)
whole.insert(whole.shape[1], nm.sim_length, 0)
whole.insert(whole.shape[1], nm.population_size, 0)

for i in range(0, whole.shape[0]):
    settings_string = whole.loc[i, 'settings']
    whole.loc[i, nm.sim_length] = parse_setting(settings_string, nm.sim_length)
    whole.loc[i, nm.population_size] = parse_setting(
        settings_string, nm.population_size)
    whole.loc[i, nm.is_enemy_pop_evo] = parse_setting(
        settings_string, nm.is_enemy_pop_evo)

# 画图

sns.set_theme(style="ticks", palette="pastel")

# sns.relplot(data=whole, y=nm.damage_to_enemy, x=nm.sim_length, hue=nm.is_enemy_pop_evo)  # 散点图，可以不要

plt.figure()
sns.boxplot(data=whole, y=nm.damage_to_enemy,
            x=nm.sim_length, hue=nm.is_enemy_pop_evo)  # 箱线图
# sns.boxplot(data=whole, y="hurt", x=nm.sim_length, hue=nm.is_enemy_pop_evo) # 箱线图

sns.catplot(data=whole, y=nm.damage_to_enemy, x=nm.sim_length,
            hue=nm.is_enemy_pop_evo, kind="point", capsize=.2)  # 猫图？
# sns.catplot(data=whole, y=nm.loops, x=nm.sim_length, hue=nm.is_enemy_pop_evo, kind="point") # 猫图？

plt.show()
print("end")


# print(whole.iloc[:, 9])
