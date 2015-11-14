#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib as mpl
from matplotlib import pylab as plt
import random
import pandas as pd
import seaborn as sb
import re
from pdb import set_trace
from traceback import print_exc
import yaml
import cPickle

sb.set_context('poster')
font = 'AR PL KaitiM Big5'
mpl.rcParams['font.family'] = font  # 設定中文字體
mpl.rcParams['font.sans-serif'] = font  # 設定中文字體


def PrepData(refresh=False):
    if ('df' in globals()) and (not refresh):
        return
    print 'Refresh'
    fi = 'data.tsv'
    fi = u'資料清單與總表-20150202 - 投稿總表.tsv'
    df = pd.DataFrame.from_csv(fi, sep='\t')
    globals().update(locals())


def save(obj, fi):
    yaml.dump(obj, open(fi, 'wb'))


def load(fi):
    return yaml.load(open(fi, 'rb'))


def clrstr(s, ks, key=''):
    return reduce(lambda x, y: x.replace(y, key), ks, s)


def manfix(x):
    k1 = u'廖秭妤翁嘉駿'.encode('utf8')
    if k1 in x:
        x = x.replace(k1, u'廖秭妤、翁嘉駿'.encode('utf8'))
    return x


def preproc(df):
    col = '作者'
    s = df[col].replace('*', '')
    rgx = re.compile('(\d+\.)')
    rgx1 = re.compile('^l.')
    rgx2 = re.compile('^\d+ ?')
    frgx2 = lambda x: clrstr(x, rgx2.findall(x))
    rgx3 = re.compile('\d+$')
    frgx3 = lambda x: clrstr(x, rgx3.findall(x))
    mainkey = '、'
    # key2 = ','
    fnamedic = makenamedic()

    # 區分作者時
    # 有頓號時以頓號為主， "," 為姓名的一部分
    # 沒有頓號時以 "," 為主， "," 是分隔的一部分
    def split(x):
        keys = ['&', '丶', ' and ']
        if mainkey not in x:
            keys.append(',')
        return clrstr(x, keys, key=mainkey).split(mainkey)

    try:
        s1 = []
        for idx, x in s.iteritems():
            # conds = tuple([(y in x) for y in (mainkey, key2)])
            # if conds == (False, True):
            #     print idx, x
            keys = rgx.findall(x)
            keys.extend(['*', '(沒上標)'])
            x = manfix(clrstr(x, keys))

            qry = rgx1.findall(x)
            if len(qry) > 0:
                x = clrstr(x, qry)

            data = [y.strip() for y in split(x)]
            data = [y for y in map(frgx2, data) if y != '']
            data = map(frgx3, data)
            data = map(fnamedic, data)
            s1.append(data)
    except:
        print_exc()
        set_trace()

    fnamedic(None)
    s1 = pd.Series(s1, index=s.index)
    s1.apply(lambda x: ' | '.join(x)).to_csv('names.txt', index=False)
    return s1


def makenamedic():
    # 英漢名字對照
    dic = {}

    def fix(s):
        # if 'Feng-Yu Wang' in s:
        #     print s
        #     set_trace()

        if s is None:
            fi = 'namedic.yaml'
            save(dic, fi)
            return

        qry = re.search('([-\w ]+)\((.*)\)', s)
        if qry:
            names = qry.groups()
            if len(names) == 2:
                dic[names[0].strip()] = names[1]
                return names[1]
        return s
    return fix


def test():
    cols = [u'公司', u'營收']
    cols = [x.encode('utf8') for x in cols]
    df = pd.DataFrame(np.random.randn(6, 2), columns=cols)
    df.plot()
    plt.show()


if __name__ == '__main__':
    """"""
    refresh = True
    PrepData(refresh)
    s1 = preproc(df)
    df['authors'] = s1.apply(lambda x1: [x.decode('utf8') for x in x1])

