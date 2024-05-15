import os
import pandas as pd

folders = ["pro" + str(x) for x in range(1,12)]
#folders = ["gly1"]
df_out = pd.read_csv("table.csv", sep=';', header=0, names=["name", "RMSD", "Rg", "hbonds", "seq"], index_col=False)

for fold in folders:
    os.chdir(fold)
    os.system('printf "4\n4\n" | /usr/local/gromacs/bin/gmx rms -s em.tpr -f md_0_1_noPBC.xtc -o rmsd.xvg -tu ns -xvg none')
    df_rmsd = pd.read_csv('rmsd.xvg', sep='\s+', header=None, names=['time', 'RMSD'])
    os.system('echo "1" | /usr/local/gromacs/bin/gmx gyrate -s md_0_1.tpr -f md_0_1_noPBC.xtc -o gyrate.xvg -xvg none')
    df_rg = pd.read_csv('gyrate.xvg', sep='\s+', header=None, names=['time', 'Rg'], usecols=[0, 1])
    os.system('printf "splitch 1\nq\n" | /usr/local/gromacs/bin/gmx make_ndx -f nvt.tpr -o')
    os.system('printf "1\n1\n"| /usr/local/gromacs/bin/gmx hbond -f md_0_1_noPBC.xtc -s md_0_1.tpr -n index.ndx -num -xvg none')
    df_hbonds = pd.read_csv('hbnum.xvg', sep='\s+', header=None, names=['time', 'H-bonds'], usecols=[0, 1])

    with open("seq.txt", "r") as f_seq:
        seq = f_seq.read().strip()

    df_out.loc[len(df_out)] = [fold,
                               df_rmsd[df_rmsd.time>0.5].RMSD.mean(),
                               df_rg[df_rg.time>0.5].Rg.mean(),
                               df_hbonds[df_hbonds.time>0.5]["H-bonds"].mean(),
                               seq]
    os.chdir("../")
df_out.to_csv("table.csv", sep=";", na_rep="NA", index=False)
print(df_out)
