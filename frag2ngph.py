#!/usr/bin/env python3
# coding: utf-8
#試しにcookfragment.plをpythonで書きなおしてみた。
# 引数が与えられた場合は、それをテンプレートとみなし、@NGPH形式の個別のグラフを出力する。

import sys
from ngph import load, dumps





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
        template = load(f)

    for nodes in unique(lambda: frag_parser(sys.stdin)):
        gn = cast_graph(nodes, template)
        print(dumps(gn), end="")
