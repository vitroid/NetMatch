#!/usr/bin/env python3
import sys

import numpy as np
from pairlist import pairs_iter


def load_lammps(file):
    natom = 0
    while True:
        line = file.readline()
        cols = line.split()
        if cols[0] == "ITEM:":
            if cols[1] == "NUMBER":
                natom = int(file.readline())
            elif cols[1] == "BOX":
                cell = []
                for i in range(3):
                    line = file.readline()
                    cols = line.split()
                    assert float(cols[0]) == 0
                    cell.append(float(cols[1]))
            elif cols[1] == "ATOMS":
                atoms = []
                for i in range(natom):
                    cols = file.readline().split()
                    atoms.append([float(x) for x in cols[2:]])
                break
            else:
                pass
                # print(line)
    return cell, atoms


cell, atoms = load_lammps(sys.stdin)
cell = np.diag(np.array(cell))
celli = np.linalg.inv(cell)
atoms = np.array(atoms)

print("@NGPH")
print(len(atoms))
for i,j,d in pairs_iter(atoms, 3.0, cell):
    print(i,j)
print(-1,-1)
