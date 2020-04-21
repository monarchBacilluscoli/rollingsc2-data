import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

result = {}
is_show_each = True
is_subfigure = True
# prob_type = 0 # 0:3objs, 1: 2objs
obj_show = 2  # 0: dmg aver, 1: dmg best, 2: hurt aver, 3: hurt best
sub_figure_wid = 3
sub_figure_height = 2

title2 = {1: "aver damage to enemy",
          2: "best damage to enemy",
          3: "aver damage to mine",
          4: "best damage to mine",
          5: "aver win loop",
          6: "best win loop"}


# fmri = sns.load_dataset("fmri")
# sns.relplot(x="timepoint", y="signal", kind="line", data=fmri);

# f, axes = plt.subplots(2, 2, figsize=(7, 7), sharex=True)

if(is_subfigure):
    f, axes = plt.subplots(sub_figure_height, sub_figure_wid, sharex=True)

sub_count = 0
for i in np.hstack((range(3, 6), 9, 10)):
    a = np.loadtxt("./"+str(i)+"_start.txt")

    one = a[0:101, obj_show]

    for j in range(1, int(np.shape(a)[0]/101)):
        b = a[j*101:j*101+101, obj_show]
        one = np.vstack((one, b))

    data_name = open("./"+str(i)+"_clear.txt").readline().replace("_",
                                                                  "").replace("//", "").replace("\n", "")
    data_counts = np.shape(one)[0]
    if(is_show_each):
        one = pd.DataFrame(one)
        print(one.shape)
        if (is_subfigure):
            # plt.figure()
            # pt = sns.pointplot(np.transpose(one))
            sub_axe = axes[sub_count//sub_figure_wid,
                           sub_count % sub_figure_wid]
            pt = sns.pointplot(data=one, ax=sub_axe)
            sub_axe.set_title(data_name + " data counts: " + str(data_counts))
            sub_axe.set_ylabel(title2[obj_show])
            sub_count += 1
        else:
            plt.figure()
            pt = sns.pointplot(one)
            plt.title(label=data_name + " data counts: " + str(data_counts))
            plt.ylabel(ylabel=title2[obj_show])
    result[data_name] = np.mean(one, axis=0)


result = pd.DataFrame(result)
# one = one.transpose()
print(result)

plt.figure()
pt = sns.lineplot(data=result)
plt.xlabel("generations")
plt.ylabel("damage")
plt.title("Schemes in 3 objs: "+title2[obj_show])
plt.show()
pass
