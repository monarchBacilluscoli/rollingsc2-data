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
file_path = "no_evo_mix_map.txt"
# this is used to mark the start of the useable data
start_comment = "evo higher generations"
map_name = "2P_EnemyMarinesZsVSMainesZs"


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
block = f_in.read()

whole = pd.read_csv(StringIO(block), sep="\t", header=None)
whole.columns = raw_colomns

# 解析settings并设置条目
whole.insert(whole.shape[1], nm.is_enemy_pop_evo, 0)
whole.insert(whole.shape[1], nm.sim_length, 0)
whole.insert(whole.shape[1], nm.population_size, 0)
whole.insert(whole.shape[1], nm.max_generations, 0)
whole = whole[whole[nm.map_name] == map_name]  # filter
whole.reset_index()

for i in range(0, whole.shape[0]):
    settings_string = whole.loc[i, 'settings']
    whole.loc[i, nm.sim_length] = parse_setting(settings_string, nm.sim_length)
    whole.loc[i, nm.population_size] = parse_setting(
        settings_string, nm.population_size)
    whole.loc[i, nm.is_enemy_pop_evo] = parse_setting(
        settings_string, nm.is_enemy_pop_evo)
    whole.loc[i, nm.max_generations] = parse_setting(
        settings_string, nm.max_generations)

print(whole)

# 显著性检验
epe = whole[nm.is_enemy_pop_evo].unique()
dg1 = whole[whole[nm.is_enemy_pop_evo] == 1][nm.damage_to_enemy]
dg0 = whole[whole[nm.is_enemy_pop_evo] == 0][nm.damage_to_enemy]
lp1 = whole[whole[nm.is_enemy_pop_evo] == 1][nm.loops]
lp0 = whole[whole[nm.is_enemy_pop_evo] == 0][nm.loops]
stat_dg = stats.ttest_ind(dg0, dg1)
stat_lp = stats.ttest_ind(lp0, lp1)

if(stat_dg.pvalue == None):
    print("pvalue has no value")
print(str(nm.damage_to_enemy), ":\t",
      ",\tpvalue:\t", stat_dg.pvalue, ",\t", end="")
if (stat_dg.pvalue < 0.05):
    print("具有显著性差异")
else:
    print("不具有显著性差异")

if(stat_lp.pvalue == None):
    print("pvalue has no value")
print(str(nm.loops), ":\t",
      ",\tpvalue:\t", stat_lp.pvalue, ",\t", end="")
if (stat_lp.pvalue < 0.05):
    print("具有显著性差异")
else:
    print("不具有显著性差异")


# 画图

sns.set_theme(style="ticks", palette="pastel")
plt.figure(figsize=(2.5,3))
sns.boxplot(data=whole, y=nm.loops,
            x=nm.is_enemy_pop_evo)
plt.savefig("evo_mix_map_loops.svg")
plt.figure(figsize=(2.5,3))
sns.boxplot(data=whole, y=nm.damage_to_enemy,
            x=nm.is_enemy_pop_evo)
plt.savefig("evo_mix_map_dmg.svg")
plt.show()
pass
