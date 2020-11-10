import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import re
import sys
from io import StringIO

data_file_name = "./dis_test_comp_2.txt"

f_in = open(data_file_name)
line = f_in.readline()
block = ""
data_name = ""
whole = pd.DataFrame(
    columns=['Damage (to enemy)', 'Damage (to my team)', 'win_loop', 'hp_m', 'hp_e', 'rank', 'Settings'])
while line:
    if(line.find("//") != -1):
        # todo 写入上一组数据
        if(block != ""):
            df = pd.read_csv(StringIO(block), sep="\t", header=None)
            df.columns = ['Damage (to enemy)', 'Damage (to my team)', 'win_loop', 'hp_m', 'hp_e', 'rank']
            df['Settings'] = data_name
            whole = pd.concat([whole, df])

        # todo 开始下一组数据
        data_name = line.replace(
            "//", "").replace(" ", "").replace("\n", "").replace('\t', '+').replace('300', '')
        block = ""
    else:
        block += line
    line = f_in.readline()
# todo 写入最后一组数据
df = pd.read_csv(StringIO(block), sep="\t", header=None)
df.columns = ['Damage (to enemy)', 'Damage (to my team)', 'win_loop', 'hp_m', 'hp_e', 'rank']
df['Settings'] = data_name
whole = pd.concat([whole, df])

whole = whole.reset_index()
print(whole.iloc[1, :])

sns.set(style="darkgrid")
whole["Damage (to enemy)"] = -whole['Damage (to enemy)']
# sns.relplot(x='Damage (to enemy)', y='Damage (to my team)', hue='Settings',
#             style="Settings", data=whole[whole['rank'] == 0], alpha=0.9, height=4, aspect=1.2)
# sns.jointplot(x='Damage (to enemy)', y='Damage (to my team)', data = whole[whole['rank'] == 0])
plt.title("Final Pop Distribution")
print(whole.dtypes)
whole[("Damage (to enemy)")] = whole["Damage (to enemy)"].astype(np.float)
whole[("Damage (to my team)")] = whole["Damage (to my team)"].astype(np.float)
# ax = sns.jointplot(x='dmg', y='Damage (to my team)', data=whole).plot_joint(sns.relplot, zorder=0)
# sns.kdeplot(whole[whole['settings']=='3010\t300']["dmg"], whole[whole['settings']=='3010\t300']['Damage (to my team)'], cmap='Reds', shade=True, shade_lowest=False)
# sns.kdeplot(whole[whole['settings']=='3111\t300']["dmg"], whole[whole['settings']=='3111\t300']['Damage (to my team)'], cmap='Blues', shade=True, shade_lowest=False)
# sns.kdeplot(whole[whole['settings']=='3000\t300']["dmg"], whole[whole['settings']=='3000\t300']['Damage (to my team)'], cmap='Greens', shade=True, shade_lowest=False)
# sns.pairplot(data=whole[(['Damage (to my team)', 'Damage (to enemy)', 'Settings'])],hue="Settings", height=2, aspect=1.2)
# sns.pointplot(data=whole, x="Damage (to my team)", y="Damage (to enemy)",
#   hue="Settings", height=2, aspect=1.2)
sns.jointplot(data=whole, x="Damage (to my team)", y="Damage (to enemy)",
              hue="Settings", height=4)
plt.savefig(data_file_name.replace(".txt", ".svg"))
plt.show()
# todo 同样配置的数据用字典怼一起去.
# todo 把其中同一类目的数据横向怼一起
