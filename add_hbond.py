import os
import pandas as pd
folders = [name for name in os.listdir(".") if os.path.isdir(name) and name[-3:] == "all"]
df_out = pd.read_csv("table.csv", sep=';', header=1, names=["name", "RMSD", "Rg", "hbonds"])
for fold in folders:
    os.chdir(fold)
    os.system('printf "splitch 1\nq\n" | /usr/local/gromacs/bin/gmx make_ndx -f nvt.tpr -o')
    os.system('printf "1\n1\n"| /usr/local/gromacs/bin/gmx hbond -f md_0_1_noPBC.xtc -s md_0_1.tpr -n index.ndx -num -xvg none')
    df_in = pd.read_csv('hbnum.xvg', sep='\s+', header=None, names=['time', 'H-bonds'], usecols=[0, 1])
    df_out.loc[df_out["name"]==fold, "hbonds"] = df_in[df_in.time>0.5]["H-bonds"].mean()
    os.chdir("../")
df_out.to_csv("table.csv", sep=";", na_rep="NA", index=False)
print(df_out)
