#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/3/13'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
             ┏┓   ┏┓
            ┏┛┻━━━┛┻┓
            ┃       ┃
            ┃ ┳┛ ┗┳ ┃
            ┃   ┻   ┃
            ┗━┓   ┏━┛
              ┃   ┗━━━┓
              ┃神兽保佑┣┓
              ┃永无BUG  ┏┛
              ┗┓┓┏━┳┓┏━┛
               ┃┫┫ ┃┫┫
               ┗┻┛ ┗┻┛
"""

import random
import numpy as np
from flask import Flask,request,redirect, url_for,session

app = Flask(__name__)


def rm_rord(x,y,cols,rows,M):
    '''
    :param x: 矩阵行数
    :param y: 矩阵列数
    :param cols: 总列数
    :param rows: 总行数
    :param M[rows][cols]: 准备删除的矩阵
    :return bools:需要从列表中删除的该点
    '''
    rm_top_l = 0 if x<1 or y<1 else 1
    rm_top_r = 0 if x<1 or y>cols-2 else 1
    rm_bot_l = 0 if x>rows-2 or y<1 else 1
    rm_bot_r = 0 if x>rows-2 or y>cols-2 else 1
    
    if rm_top_l == 1:
        if M[x-1][y-1] == 1 and M[x-1][y] == 1 and M[x][y-1] == 1:
            return True
    if rm_top_r == 1:
        if M[x-1][y] == 1 and M[x-1][y+1] == 1 and M[x][y+1] == 1:
            return True
    if rm_bot_l == 1:
        if M[x][y-1] == 1 and M[x+1][y-1] == 1 and M[x+1][y] == 1:
            return True
    if rm_bot_r == 1:
        if M[x][y+1] == 1 and M[x+1][y] == 1 and M[x+1][y+1] == 1:
            return True
    return False

def check_num(r,c,cols,rows,M,h_list):
    '''
    :param r:
    :param c:
    :param cols:
    :param rows:
    :param M:
    :return:
    '''
    f_list = [(r - 1, c), (r + 1, c), (r, c + 1), (r, c - 1)]

    f_del = []
    f_sum = []

    for f in f_list:
        x, y = f
        if x<0 or y<0 or x>=cols or y>=rows:
            f_del.append(f)
            continue
        if M[x][y] == 1 and (x,y) not in h_list:
            f_del.append(f)
            f_sum = check_num(x,y,cols,rows,M,h_list)
        elif M[x][y] == 1:
            f_del.append(f)
        elif rm_rord(x, y, cols, rows, M) == True:
            f_del.append(f)
        else:
            continue

    for f in f_del:
        f_list.remove(f)
        
    for f in f_sum:
        f_list.append(f)
        
    return f_list

def init_rolls(cols,rows):
    '''
    :param cols: 总列数
    :param rows: 总行数
    :return M: 生成的迷宫矩阵
    '''
    
    M = []
    
    for i in range(rows):
        r = []
        for j in range(cols):
            z = 1 if i%2 == 1 and j%2 == 1 else 0
            r.append(z)
        M.append(r)
    
    r,c = 0,0
    
    M[r][c] = 1
    
    m_list = [(0,1),(1,0)]
    
    h_list = [(0,0)]

    while m_list:
        r,c = random.choice(m_list)
        
        if rm_rord(r,c,cols,rows,M) == True:
            m_list.remove((r,c))
            continue
        
        M[r][c] = 1
        
        if r == rows-1 :
            for i in range(c,cols):
                M[r][i] = 1
            break
        elif c == cols-1:
            for i in range(r,rows):
                M[i][c] = 1
            break
        
        m_list.remove((r,c))
        
        h_list.append((r,c))
        
        m_add = check_num(r,c,cols,rows,M,h_list)
        
        for i in m_add:
            if i not in M:
                m_list.append(i)
    
    return M


def check_right(n_list,M_list):
    if type(n_list) != list and type(M_list) != list:
        return False
    l_m = len(M_list)-1
    l = len(n_list)
    for i in range(0,l):
        if i == l-1:
            if n_list[i] == (l_m,l_m):
                return True
            else:
                return False
        a = n_list[i]
        x,y = a
        a_next = n_list[i+1]
        if a[0] == a_next[0]-1 or a[0] == a_next[0]+1 or a[1] == a_next[1]+1 or a[1] == a_next[1]-1:
            if M_list[x][y] == 1:
                continue
            else:
                return False
        else:
            return False
        
    
M_test = [
    [1, 0, 1, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1],
]

n_list = [(0,0),(1,0),(1,1),(2,1),(3,1),(4,1),(4,2),(4,3),(4,4)]

a = check_right(n_list,M_test)

print(a)
        
level1 = 5
level2 = 9
level3 = 15
level4 = 35
level5 = 55

a = init_rolls(55,55)

for zz in a:
    print(zz)