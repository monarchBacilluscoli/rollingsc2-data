import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import setting_names as nm
from io import StringIO

file_path = "./3_obj_one_run"

raw_colomns = [nm.aver+nm.damage_to_enemy, nm.best+nm.damage_to_enemy, nm.aver +
               nm.damage_to_mine, nm.best+nm.damage_to_mine, nm.aver+nm.loops, nm.best+nm.loops]
f_in = open(file_path)
data = f_in.read()
block = pd.read_csv(StringIO(data), sep="\t", header=None)
block = block.dropna(axis=1)
block.columns = raw_colomns

plt.figure(figsize=(5, 3.5))
sns.lineplot(data=block.drop(
    columns=[nm.aver+nm.loops, nm.best+nm.loops]))
plt.xlabel("Generations")
plt.ylabel("Health points")
plt.savefig("3_obj_conver.svg")
plt.show()
pass
