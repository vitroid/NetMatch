#!/usr/bin/env python3
import sys

import numpy as np
import yaplotlib as yap
from ngph import load
from graphstat.graphstat_sqlite3 import GraphStat
import networkx as nx
from cycless.cycles import cycles_iter
from logging import getLogger, basicConfig, INFO

# set up logger
basicConfig(level=INFO)
logger = getLogger(__name__)

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
# celli = np.linalg.inv(cell)
atoms = np.array(atoms)


gdb = GraphStat("graph.sqlite3", create_if_nonexist=True)

s = yap.RandomPalettes(100, offset=3)
with open(sys.argv[1]) as file:
    for g, N in load(file):
        graph = nx.Graph()
        for i,j in g:
            graph.add_edge(i,j)
        id = gdb.query_id(graph)
        if id < 0:
            id = gdb.register()
        s += yap.Layer(id)
        s += yap.Color(id+2)

        # 可視化
        # ノードの表を作る
        nodes = list(graph)
        # 重心
        d = atoms[nodes] - atoms[nodes[0]]
        d -= np.floor(d+0.5)
        com = atoms[nodes[0]] + np.mean(d, axis=0)
        for cycle in cycles_iter(graph, maxsize=8):
            d = atoms[cycle,:] - com
            d -= np.floor(d+0.5)
            s += yap.Polygon((com+d)@cell)
print(s)
