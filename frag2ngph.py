#!/usr/bin/env python3
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


def dumps_NGPH(gn):
    """グラフをNGPH形式で出力

    Args:
        gn (_type_): tuple of (list of edges, number of nodes)
        nodes (list, optional): ノードのエイリアス. Defaults to None.
    """
    g, n = gn
    s = "@NGPH\n"
    s += f"{n}\n"
    for i,j in g:
        s += f"{i} {j}\n"
    s += "-1 -1\n"
    return s


def unique(generator):
    "generatorの生成するデータの重複(要素は同じだが順列が異なるもの)を除く。"
    fragments = set()
    for nodeset in generator():
        s = frozenset(nodeset)
        if s not in fragments:
            yield nodeset
        fragments.add(s)


def frag_parser(file):
    "fileから@FRAG形式のデータを読みこみ、データ部分だけをとりだす。"
    for line in file:
        columns = line.split()
        if len(columns) > 2 and line[0] != "-":
            yield columns


def cast_graph(nodes, template):
    "templateのノードのラベルをさしかえる。templateは(グラフ, ノード数)"
    tg, tn = template
    nodes = {i:j for i,j in enumerate(nodes)}
    g = []
    for i,j in tg:
        g.append((nodes[i], nodes[j]))
    return g, tn


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        template = load_NGPH(f)

    for nodes in unique(lambda: frag_parser(sys.stdin)):
        gn = cast_graph(nodes, template)
        print(dumps_NGPH(gn), end="")
