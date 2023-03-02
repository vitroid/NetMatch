#!/usr/bin/env python
# coding: utf-8
#試しにcookfragment.plをpythonで書きなおしてみた。
# 引数が与えられた場合は、それをテンプレートとみなし、@NGPH形式の個別のグラフを出力する。

import sys


def load_NGPH(file):
    g = []
    while True:
        line=file.readline()
        if len(line) == 0:
            break
        if len(line)>5 and line[:5] == "@NGPH":
            N = int(file.readline())
            while True:
                x,y = [int(x) for x in file.readline().split()]
                if x < 0:
                    break
                g.append([x,y])
    return g, N


def dumps_NGPH(gn, nodes=None):
    """グラフをNGPH形式で出力

    Args:
        gn (_type_): tuple of (list of edges, number of nodes)
        nodes (list, optional): ノードのエイリアス. Defaults to None.
    """
    g, n = gn
    if nodes is not None:
        nodes = {i:j for i,j in enumerate(nodes)}
    else:
        nodes = {i:i for i in range(n)}
    s = "@NGPH\n"
    s += f"{n}\n"
    for i,j in g:
        s += f"{nodes[i]} {nodes[j]}\n"
    s += "-1 -1\n"
    return s


if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
        template = load_NGPH(f)
else:
    template = None


fragments = set()
for line in sys.stdin:
    columns = line.split()
    if len(columns) > 2:
        s = frozenset(columns)
        if s not in fragments:
            if template is None:
                print(line, end="")
            else:
                if line[0] != "-":
                    print(dumps_NGPH(template, nodes=[int(i) for i in columns]), end="")
        fragments.add(s)
    else:
        if template is None:
            print(line, end="")                  #そのまま出力
