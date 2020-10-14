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
file_path = "/home/liuyongfeng/s2client-api-liu/s2client-api/scores/test_scores.txt"
# this is used to mark the start of the useable data
start_comment = "evo higher generations"
map_name = "PCANP_EnemyZealotsModMoreVSMarines"


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

whole.insert(whole.shape[1], nm.is_enemy_pop_evo, 0)
whole.insert(whole.shape[1], nm.sim_length, 0)
whole.insert(whole.shape[1], nm.population_size, 0)
whole.insert(whole.shape[1], nm.max_generations, 0)
whole = whole[whole[nm.map_name] == map_name]  # filter
whole = whole.reset_index()

for i in range(0, whole.shape[0]):
    settings_string = whole.loc[i, 'settings']
    whole.loc[i, nm.sim_length] = parse_setting(settings_string, nm.sim_length)
    whole.loc[i, nm.population_size] = parse_setting(
        settings_string, nm.population_size)
    whole.loc[i, nm.is_enemy_pop_evo] = parse_setting(
        settings_string, nm.is_enemy_pop_evo)
    whole.loc[i, nm.max_generations] = parse_setting(
        settings_string, nm.max_generations)

# 画图

sns.set_theme(style="ticks", palette="pastel")

# 对比不同sim_length的设置
max_generations_filter = 20
sim_length_com = whole[whole[nm.max_generations] ==
                       max_generations_filter]  # 仅筛出max_generations为20的数据
sim_length_com = whole


sns.relplot(data=sim_length_com, y=nm.damage_to_enemy, x=nm.sim_length,
            hue=nm.is_enemy_pop_evo)  # 散点图，可以不要

sns.boxplot(data=sim_length_com, y=nm.damage_to_enemy,
            x=nm.sim_length, hue=nm.is_enemy_pop_evo)

fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(10, 10))
sns.pointplot(data=sim_length_com, y=nm.damage_to_enemy, x=nm.sim_length,
              hue=nm.is_enemy_pop_evo, kind="point", capsize=.2, ax=axs[0, 0])
sns.pointplot(data=sim_length_com, y=nm.loops, x=nm.sim_length,
              hue=nm.is_enemy_pop_evo, kind="point", capsize=.2, ax=axs[0, 1])
sns.swarmplot(data=sim_length_com, y=nm.damage_to_enemy, x=nm.sim_length,
              hue=nm.is_enemy_pop_evo, ax=axs[1, 0])
sns.swarmplot(data=sim_length_com, y=nm.loops, x=nm.sim_length,
              hue=nm.is_enemy_pop_evo, ax=axs[1, 1])
plt.suptitle(nm.max_generations + ": " + str(max_generations_filter) + ", ")


sns.catplot(data=sim_length_com, y=nm.damage_to_enemy, x=nm.sim_length,
            hue=nm.is_enemy_pop_evo, kind="swarm")

# 显著性检验
sls = sim_length_com[nm.sim_length].unique()
sls.sort(axis=0)
for i in sls:  # 提取所有的sim_length
    gc1 = sim_length_com[(sim_length_com[nm.sim_length] == i)
                         & (sim_length_com[nm.is_enemy_pop_evo] == 1)][nm.damage_to_enemy]
    gc2 = sim_length_com[(sim_length_com[nm.sim_length] == i)
                         & (sim_length_com[nm.is_enemy_pop_evo] == 0)][nm.damage_to_enemy]
    stat = stats.ttest_ind(gc1, gc2)
    if(stat.pvalue == None):
        print("pvalue has no value")
    print(str(nm.sim_length), ":\t", i,
          ",\tpvalue:\t", stat.pvalue, ",\t", end="")
    if (stat.pvalue < 0.05):
        print("具有显著性差异")
    else:
        print("不具有显著性差异")


# 对比不同max_generations的设置
sim_length_filter = 75
population_size_filter = 10
generation_com = whole[(whole[nm.sim_length] == sim_length_filter) & (
    whole[nm.population_size] == population_size_filter)]

fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(10, 10))
sns.pointplot(data=generation_com, y=nm.damage_to_enemy,
              x=nm.max_generations, hue=nm.is_enemy_pop_evo, capsize=.2, ax=axs[0, 0])
sns.pointplot(data=generation_com, y=nm.loops,
              x=nm.max_generations, hue=nm.is_enemy_pop_evo, capsize=.2, ax=axs[0, 1])  # 猫图形式
sns.swarmplot(data=generation_com, y=nm.damage_to_enemy,
              x=nm.max_generations, hue=nm.is_enemy_pop_evo, ax=axs[1, 0])
sns.swarmplot(data=generation_com, y=nm.loops,
              x=nm.max_generations, hue=nm.is_enemy_pop_evo, ax=axs[1, 1])  # 虫子图形式
plt.suptitle(nm.sim_length+": "+str(sim_length_filter))


# plt.figure()
# sns.boxplot(data=generation_com, y=nm.damage_to_enemy,
#             x=nm.max_generations, hue=nm.is_enemy_pop_evo)

# 对比不同population_size的设置
sim_length_filter = 75
max_generation_filter = 40
population_com = whole[(whole[nm.sim_length] ==
                        sim_length_filter) & (whole[nm.max_generations] == max_generation_filter)]

fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(10, 10))
sns.boxplot(data=population_com, y=nm.damage_to_enemy,
            x=nm.population_size, hue=nm.is_enemy_pop_evo, ax=axs[0, 0])
sns.boxplot(data=population_com, y=nm.loops,
            x=nm.population_size, hue=nm.is_enemy_pop_evo, ax=axs[0, 1])  # 猫图形式
sns.swarmplot(data=population_com, y=nm.damage_to_enemy,
              x=nm.population_size, hue=nm.is_enemy_pop_evo, ax=axs[1, 0])
sns.swarmplot(data=population_com, y=nm.loops,
              x=nm.population_size, hue=nm.is_enemy_pop_evo, ax=axs[1, 1])  # 虫子图形式
plt.suptitle(nm.sim_length+": "+str(sim_length_filter))

# 对不同population_size相同设置的个体进行显著性差异检验
sls = population_com[nm.is_enemy_pop_evo].unique()
sls.sort(axis=0)
for i in sls:  # 提取所有的sim_length
    gc1 = population_com[(population_com[nm.is_enemy_pop_evo] == i)
                         & (population_com[nm.population_size] == 10)][nm.loops]
    gc2 = population_com[(population_com[nm.is_enemy_pop_evo] == i)
                         & (population_com[nm.population_size] == 20)][nm.loops]
    stat = stats.ttest_ind(gc1, gc2)
    if(stat.pvalue == None):
        print("pvalue has no value")
    print('population_size是否产生显著性差异\t', 'enemy_evo:', i,
          ",\tpvalue:\t", stat.pvalue, ",\t", end="")
    if (stat.pvalue < 0.05):
        print("具有显著性差异")
    else:
        print("不具有显著性差异")

plt.show()
print("end")
# print(whole.iloc[:, 9])
