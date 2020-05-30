import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import re
import sys
from io import StringIO

data_scolumns = ['dmg', 'max_dmg', 'hurt',
                 'max_hurt', 'winloop', 'max_winloop']
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

# 对于每一类数据, 除以这个数据的个数并展示
for kv in aver_test_results.items():
    aver_test_results[kv[0]] = aver_test_results[kv[0]]/test_count[kv[0]]
    plt.figure()
    sns.lineplot(data=aver_test_results[kv[0]][['dmg', 'max_dmg', 'hurt', 'max_hurt']])
    plt.title("2 Objs Convergence Curve 2000")
plt.show()

print(aver_test_results)


pass
