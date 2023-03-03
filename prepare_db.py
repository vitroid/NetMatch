#!/usr/bin/env python3

"""
graph.sqlite3の初期化。
重要な構造4つは最初にIDを与えておく。
"""
from ngph import load
from graphstat.graphstat_sqlite3 import GraphStat
import networkx as nx

gdb = GraphStat("graph.sqlite3", create_if_nonexist=True)
for fragment in ("ice1c.ngph", "ice1h2.ngph", "barrelan.ngph", "dodeca.ngph"):
    with open(fragment) as file:
        for g, N in load(file):
            graph = nx.Graph()
            for i,j in g:
                graph.add_edge(i,j)
            id = gdb.query_id(graph)
            if id < 0:
                id = gdb.register()
