#!/usr/bin/env python3

"""
@NGPHを読みこみ、cycleをさがし、json形式で出力する。
"""

from ngph import load
import networkx as nx
from cycless.cycles import cycles_iter
import sys
from logging import getLogger, basicConfig, INFO
import json

# set up logger
basicConfig(level=INFO)
logger = getLogger(__name__)

for g, N in load(sys.stdin):
    graph = nx.Graph(g)
    cycles = [cycle for cycle in cycles_iter(graph, 8)]
    print(json.dumps(cycles, indent=2))
