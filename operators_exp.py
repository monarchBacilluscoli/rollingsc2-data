import re
import sys
from io import StringIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

import setting_names as nm

# 一些设置

# data file path
file_path = "./old_experiment.txt"
# this is used to mark the start of the useable data
start_comment = "evo higher generations"
map_name = "PCANP_EnemyZealotsModMoreVSMarines"

data_filters = {
    nm.map_name: "PCANP_EnemyZealotsModMoreVSMarines",
}


def parse_setting(settings, item):  # 解析设置字符串
    individuals = settings.split(",")
    for index in range(len(individuals)):
        individuals[index] = individuals[index].replace(" ", '')
        pair = individuals[index].split(':')
        if pair[0] == item:
            return int(pair[1])
    return "no value"


# 准备一些通用设置

raw_colomns = [nm.damage_to_enemy, 'dmg_shd', nm.damage_to_mine, 'hurt_shd', 'heal',
               'heal_shd', nm.loops, nm.map_name, 'time', 'settings']

f_in = open(file_path, )
line = f_in.readline()
block = ""
data_name = ""
whole = pd.DataFrame(columns=raw_colomns)

# 读取数据

start = False
while line:  # 读文件
    if (line.find(start_comment) != -1):
        start = True
    if (start and line.find("//") == -1 and line != ""):  # 写入
        block += line
    line = f_in.readline()

df = pd.read_csv(StringIO(block), sep="\t", header=None)
df.columns = raw_colomns
whole = pd.concat([whole, df])

# 进一步处理

whole.insert(whole.shape[1], nm.is_enemy_pop_evo, 0)  # 插入对应的数据列
whole.insert(whole.shape[1], nm.sim_length, 0)
whole.insert(whole.shape[1], nm.population_size, 0)
whole.insert(whole.shape[1], nm.max_generations, 0)
whole.insert(whole.shape[1], nm.objective_size, 0)
whole.insert(whole.shape[1], )

whole = whole[whole[nm.map_name] == map_name]  # filter
whole = whole.reset_index()

for i in range(0, whole.shape[0]):  # 解析每一个数据列
    settings_string = whole.loc[i, 'settings']
    whole.loc[i, nm.sim_length] = parse_setting(settings_string, nm.sim_length)
    whole.loc[i, nm.population_size] = parse_setting(
        settings_string, nm.population_size)
    whole.loc[i, nm.is_enemy_pop_evo] = parse_setting(
        settings_string, nm.is_enemy_pop_evo)
    whole.loc[i, nm.max_generations] = parse_setting(
        settings_string, nm.max_generations)
    whole.loc[i, nm.objective_size] = parse_setting(
        settings_string, nm.objective_size)

# 画图

sns.set_theme(style="ticks", palette="pastel")

sns.catplot(data = whole, )

plt.show()
print("end")
# print(whole.iloc[:, 9])
