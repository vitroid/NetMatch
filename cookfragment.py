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


fragments = set()
for line in sys.stdin:
    columns = line.split()
    if len(columns) > 2:
        s = frozenset(columns)
        if s not in fragments:
            print(line, end="")
        fragments.add(s)
    else:
        print(line, end="")                  #そのまま出力
