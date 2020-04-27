import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import re
import sys
from io import StringIO

f_in = open("./dis_test.txt")
line = f_in.readline()
block = ""
data_name = ""
whole = pd.DataFrame(
    columns=['dmg', 'hurt', 'win_loop', 'hp_m', 'hp_e', 'rank', 'settings'])
while line:
    if(line.find("//") != -1):
        # todo 写入上一组数据
        if(block != ""):
            df = pd.read_csv(StringIO(block), sep="\t", header=None)
            df.columns = ['dmg', 'hurt', 'win_loop', 'hp_m', 'hp_e', 'rank']
            df['settings'] = data_name
            whole = pd.concat([whole, df])

        # todo 开始下一组数据
        data_name = line.replace("//", "").replace(" ", "").replace("\n", "")
        block = ""
    else:
        block += line
    line = f_in.readline()
# todo 写入最后一组数据
df = pd.read_csv(StringIO(block), sep="\t", header=None)
df.columns = ['dmg', 'hurt', 'win_loop', 'hp_m', 'hp_e', 'rank']
df['settings'] = data_name
whole = pd.concat([whole, df])

print(whole.iloc[1, :])

sns.set(style="darkgrid")
f, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect("equal")
whole["dmg"] = -whole['dmg']
ax = sns.relplot(x='dmg', y='hurt', hue='settings',
                style="settings", data=whole[whole['rank'] == 0],alpha=0.5)
# ax = sns.jointplot(x='dmg', y='hurt', data=whole).plot_joint(sns.relplot, zorder=0)
# sns.kdeplot(whole[whole['settings']=='3010\t300']["dmg"], whole[whole['settings']=='3010\t300']['hurt'], cmap='Reds', shade=True, shade_lowest=False)
# sns.kdeplot(whole[whole['settings']=='3111\t300']["dmg"], whole[whole['settings']=='3111\t300']['hurt'], cmap='Blues', shade=True, shade_lowest=False)
# sns.kdeplot(whole[whole['settings']=='3000\t300']["dmg"], whole[whole['settings']=='3000\t300']['hurt'], cmap='Greens', shade=True, shade_lowest=False)
sns.pairplot(whole[(['hurt', 'dmg', 'settings'])], hue="settings")
print(whole[whole['settings'] == '3010\t300']["dmg"])
plt.show()

# todo 同样配置的数据用字典怼一起去.
# todo 把其中同一类目的数据横向怼一起
