import networkx as nx

def load(file):
    while True:
        line=file.readline()
        if len(line) == 0:
            break
        if len(line)>5 and line[:5] == "@NGPH":
            g = []
            N = int(file.readline())
            while True:
                x,y = [int(x) for x in file.readline().split()]
                if x < 0:
                    break
                g.append([x,y])
            yield g, N


def dumps(gn):
    """グラフをNGPH形式で出力

    Args:
        gn (_type_): tuple of (list of edges, number of nodes)
        nodes (list, optional): ノードのエイリアス. Defaults to None.
    """
    if isinstance(gn, nx.Graph):
        n = len(gn)
        g = [(i,j) for i in gn for j in gn[i] if i<j]
    else:
        g, n = gn
    s = "@NGPH\n"
    s += f"{n}\n"
    for i,j in g:
        s += f"{i} {j}\n"
    s += "-1 -1\n"
    return s
