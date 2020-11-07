import setting_names as nm
from io import StringIO
import sys
import re
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']


data_scolumns = [nm.aver+nm.damage_to_enemy, nm.best+nm.damage_to_enemy, nm.aver+nm.damage_to_mine,
                 nm.best+nm.damage_to_mine, nm.aver+nm.loops, nm.best+nm.loops]
aver_test_results = {}
test_count = {}

f_in = open("./conver_data.txt")
line = f_in.readline()
block = ""
data_name = ""
while line:
    if(line.find("//") != -1):
        # todo 写入上一组数据
        if(block != ""):
            df = pd.read_csv(StringIO(block), sep="\t", header=None)
            df.columns = data_scolumns
            # df['settings'] = data_name
            if(data_name in aver_test_results.keys()):
                aver_test_results[data_name] += df
                test_count[data_name] += 1
            else:
                aver_test_results[data_name] = df
                test_count[data_name] = 1
            # print(df)
            # sns.lineplot(data=df)
            # plt.show()

        # todo 开始下一组数据
        data_name = line.replace("//", "").replace(" ", "").replace("\n", "")
        block = ""
    else:
        block += line
    line = f_in.readline()
# todo 写入最后一组数据
df = pd.read_csv(StringIO(block), sep="\t", header=None)
df.columns = data_scolumns
# df['settings'] = data_name
if(data_name in aver_test_results.keys()):
    aver_test_results[data_name] += df
    test_count[data_name] += 1
else:
    aver_test_results[data_name] = df
    test_count[data_name] = 1


# sns.set(style="darkgrid")
# 对于每一类数据, 除以这个数据的个数并展示
for kv in aver_test_results.items():
    aver_test_results[kv[0]] = aver_test_results[kv[0]]/test_count[kv[0]]
    plt.figure(figsize=(5, 3.5))
    sns.lineplot(data=aver_test_results[kv[0]][[
                 nm.aver+nm.damage_to_enemy, nm.best+nm.damage_to_enemy, nm.aver+nm.damage_to_mine, nm.best+nm.damage_to_mine]])
    # plt.title("2 Objs Convergence Curve 2000")
    plt.xlabel("Generations")
    plt.ylabel("Health points")
    plt.savefig("2_obj_conver.svg")
    plt.show()
plt.show()

print(aver_test_results)


pass
