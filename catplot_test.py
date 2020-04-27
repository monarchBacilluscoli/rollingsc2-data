import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import re
import sys
from io import StringIO

obj_num = 6 # dmg dmg hurt hurt heal heal loop 
map_name = 'PCANP_EnemyZealotsModMoreVSMarines'


#! only for test

all_data = {}

# print(data)

# catplot 一次只能对比同一个目标, 也就是三个目标想要一起比较z的话最好是子图
f_in = open("./test_scores.txt")
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
    # plt.figure()
    # sns.catplot(data=kv[1])
    # plt.title(kv[0])
    # print(kv[1].iloc[:, 2])
    # print(type(kv[1].iloc[:, 2]))
    if(obj_num == 6):  # 仅计算胜利
        series = kv[1].drop(kv[1][kv[1]['loop'] < 800].index)
        final_sheet[kv[0]] = series.iloc[:, obj_num]
    final_sheet[kv[0]] = kv[1].iloc[:, obj_num]
# plt.show()
print(final_sheet)
sns.catplot(kind='box',data=final_sheet)
# sns.pointplot(data=final_sheet)

plt.show()

# todo 同样配置的数据用字典怼一起去.
# todo 把其中同一类目的数据横向怼一起
