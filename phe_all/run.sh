printf "1\n" | gmx editconf -f helix.pdb -princ -o helix_turned.pdb
gmx pdb2gmx -f helix_turned.pdb -o helix_processed.gro -water spce -ff "charmm27" -ignh
gmx editconf -f helix_processed.gro -o helix_newbox.gro -c -d 1.0 -bt dodecahedron
gmx solvate -cp helix_newbox.gro -cs spc216.gro -o helix_solv.gro -p topol.top
gmx grompp -f ions.mdp -c helix_solv.gro -p topol.top -o ions.tpr
printf "SOL" | gmx genion -s ions.tpr -o helix_solv_ions.gro -p topol.top -pname NA -nname CL -neutral
gmx grompp -f minim.mdp -c helix_solv_ions.gro -p topol.top -o em.tpr
gmx mdrun -deffnm em
gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -v -deffnm nvt
gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
gmx mdrun -v -deffnm npt
gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md_0_1.tpr
gmx mdrun -v -deffnm md_0_1
printf "1\n0\n" | gmx trjconv -s md_0_1.tpr -f md_0_1.xtc -o md_0_1_noPBC.xtc -pbc mol -center
