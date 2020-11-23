import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import re
import sys
from io import StringIO

file_name = "./test_scores_3.txt"
obj_num = 6  # dmg dmg hurt hurt heal heal loop
map_name = 'PCANP_EnemyZealotsModMoreVSMarines'
title2 = {0: "Damage (to enemy)",
          1: "SHD damage to enemy",
          2: "Damage (to my team)",
          3: "SHD damage to mine",
          4: "Healed to enemy",
          5: "SHD healed to mine",
          6: "Loop used"}

#! only for test

all_data = {}

# print(data)

# catplot 一次只能对比同一个目标, 也就是三个目标想要一起比较z的话最好是子图
f_in = open(file_name)
line = f_in.readline()
block = ""
data_name = ""
while line:
    if(line.find("//") != -1):
        # todo 写入上一组数据
        if(block != ""):
            block = re.sub(r'\t'+map_name+r'.*', "", block)
            df = pd.read_csv(StringIO(block), sep="\t", header=None)
            df.columns = ['dmg_hp', 'dmg_shd', 'hurt_hp',
                          'hurt_shd', 'heal_hp', 'heal_shield', 'loop']
            all_data[data_name] = df

        data_name = line.replace("//", "").replace(" ", "")
        # todo 开始下一组数据
        block = ""
    else:
        if(line.find(map_name) != -1):
            # block += re.sub(r'[a-z]', '', re.sub(r'[A-Z]', '', line)).replace("_","")
            block += line
    line = f_in.readline()
# todo 写入最后一组数据
block = re.sub(r'\t'+map_name+r'.*', "", block)
if(block != ""):
    df = pd.read_csv(StringIO(block), sep="\t", header=None)
    df.columns = ['dmg_hp', 'dmg_shd', 'hurt_hp',
                  'hurt_shd', 'heal_hp', 'heal_shield', 'loop']
    all_data[data_name] = df

# df = pd.read_csv(StringIO(all_data[data_name]), sep="\t")
# df.columns=['dmg_hp','dmg_shd','hurt_hp','hurt_shd','heal_hp','heal_shield','loop']
# print(df)

print(len(all_data))

final_sheet = pd.DataFrame()
for kv in all_data.items():
    if(obj_num == 6):  # 仅计算胜利
        series = pd.DataFrame(kv[1].drop(
            kv[1][kv[1]['loop'] < 800].index).iloc[:, obj_num])
        series.columns = [kv[0]]
        final_sheet = pd.concat([final_sheet, series], axis=1)
    else:

        # final_sheet[kv[0]] = kv[1].iloc[:, obj_num]
        series = pd.DataFrame(kv[1].iloc[:, obj_num])
        series.columns = [kv[0]]
        final_sheet = pd.concat([final_sheet, series], axis=1)
        # print(final_sheet)
# plt.show()
print(final_sheet)
# sns.set(style="ticks", palette="husl")
# sns.set(style="darkgrid", palette="husl")
sns.catplot(kind='box', data=final_sheet, height=3, aspect=1)
# sns.pointplot(data=final_sheet)
plt.xlabel("Settings")
plt.ylabel(title2[obj_num])
# plt.title("Schemes in 3 objs: " + title2[obj_num])
plt.show()

# todo 同样配置的数据用字典怼一起去.
# todo 把其中同一类目的数据横向怼一起
