#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pdb import set_trace
from matplotlib import pylab as plt
import seaborn as sb
import matplotlib as mpl
import numpy as np
import networkx as nx

sb.set_context('poster')
font = 'AR PL KaitiM Big5'
mpl.rcParams['font.family'] = font  # 設定中文字體
mpl.rcParams['font.sans-serif'] = font  # 設定中文字體


def show(func):
    def fun(*args, **kwargs):
        ret = func(*args, **kwargs)
        fi = kwargs.get('fi')
        if fi:
            plt.savefig(fi)
        else:
            plt.show()
        plt.close()
        return ret
    return fun


