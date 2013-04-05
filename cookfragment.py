#!/usr/bin/env python
# coding: utf-8
#試しにcookfragment.plをpythonで書きなおしてみた。

import sys
fragments = set()
for line in sys.stdin:                      #stdinから1行読みこむ
    columns = line.split()                  #分割
    if len(columns) > 2:                    #3つ以上要素がある行なら
        if columns[0][0] == "-":                  #もし最初の要素が"-"からはじまるなら
            for fragment in fragments:      #すべての記録済みフラグメントについて
                print " ".join(fragment)    #メンバーを1行に出力
            print line,
        else:
            fragments.add(frozenset(columns)) #メンバーを固定集合とし、fragments集合に追加
    else:
        print line,                         #そのまま出力

