#!/usr/bin/env python3

"""
@NGPHを読みこみ、quasipolyhedraを探す。
"""

from ngph import dumps
import networkx as nx
from debug.polyhed import polyhedra_iter
import sys
from graphstat.graphstat_sqlite3 import GraphStat
from collections import defaultdict
import json
from logging import getLogger, basicConfig, INFO, DEBUG


# set up logger
basicConfig(level=INFO)
logger = getLogger(__name__)

def main():
    gdb = GraphStat("graph.sqlite3", create_if_nonexist=False)
    # count = defaultdict(int)

    cycles = json.load(sys.stdin)
    logger.info(f"Number of cycles: {len(cycles)}")
    for cycleset in polyhedra_iter(cycles, maxnfaces=14):
        vitrite = nx.Graph()
        for cycle in cycleset:
            nx.add_cycle(vitrite, cycles[cycle])
        id = gdb.query_id(vitrite)
        if id < 0:
            logger.info([len(cycles[cycle]) for cycle in cycleset])
            # assert False
            id = gdb.register()
        logger.info(f"Found id {id}")
        print(f"#id {id}")
        print(dumps(vitrite), end="")


import cProfile
if __name__ == '__main__':
   cProfile.run('main()', filename='polyhed.prof')
