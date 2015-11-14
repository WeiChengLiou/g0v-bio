#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import itertools as it
from explr import save, load
from graph import *
from collections import defaultdict
from pdb import set_trace


def saveGraph(G):
    # node
    df = {}
    for k, v in G.node.iteritems():
        df[k] = v
    df = pd.DataFrame(df).T
    df.index.name = 'name'
    df = df.sort(columns='size', ascending=False)
    df.to_csv('node.csv', sep='\t', encoding='utf8')

    df1 = []
    for key in G.edges_iter():
        k1, k2 = key
        data = G.get_edge_data(*key).copy()
        data['src'] = k1
        data['dst'] = k2
        df1.append(data)
    df1 = pd.DataFrame(df1)
    df1 = df1[['src', 'dst', 'cnt']]
    df1.to_csv('link.csv', sep='\t', encoding='utf8', index=False)

    return df, df1


def makeGraph(df, cnt):
    G = nx.Graph()
    col = 'authors'
    authors = set()
    df[col].apply(authors.update)
    print len(authors)

    for k, v in cnt.iteritems():
        G.add_node(k, size=v)

    dic = defaultdict(int)
    for i, x in df.iterrows():
        for x1, x2 in it.combinations(x[col], 2):
            key = tuple(sorted([x1, x2]))
            dic[key] += 1
    for key in dic:
        G.add_edge(*key, cnt=dic[key])
    return G


def papercnt(df):
    dic = defaultdict(int)
    for k, xs in df['authors'].iteritems():
        for x in xs:
            dic[x] += 1
    return pd.Series(dic)


def show(df, pos):
    nx.draw_networkx_nodes(G, pos, node_size=10, alpha=0.5)
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    xlim, ylim = [0, 0], [0, 0]
    for v in pos.values():
        xlim[0] = min(xlim[0], v[0])
        xlim[1] = max(xlim[1], v[0])
        ylim[0] = min(ylim[0], v[1])
        ylim[1] = max(ylim[1], v[1])
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.show()


if __name__ == '__main__':
    """"""
    # s = papercnt(df)
    # G = makeGraph(df, s)
    # pos = nx.graphviz_layout(G)

    #test(df, pos)
    df1, df2 = saveGraph(G)

