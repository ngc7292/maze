#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/3/15'
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
import time
import random
from flask import Flask,session,redirect,url_for,request,render_template_string

app = Flask(__name__)

# 直接调用init_rolls即可返回一个列表
def rm_rord(x, y, cols, rows, M):
    '''
    :param x: 矩阵行数
    :param y: 矩阵列数
    :param cols: 总列数
    :param rows: 总行数
    :param M[rows][cols]: 准备删除的矩阵
    :return bools:需要从列表中删除的该点
    '''
    rm_top_l = 0 if x < 1 or y < 1 else 1
    rm_top_r = 0 if x < 1 or y > cols - 2 else 1
    rm_bot_l = 0 if x > rows - 2 or y < 1 else 1
    rm_bot_r = 0 if x > rows - 2 or y > cols - 2 else 1
    
    if rm_top_l == 1:
        if M[x - 1][y - 1] == 1 and M[x - 1][y] == 1 and M[x][y - 1] == 1:
            return True
    if rm_top_r == 1:
        if M[x - 1][y] == 1 and M[x - 1][y + 1] == 1 and M[x][y + 1] == 1:
            return True
    if rm_bot_l == 1:
        if M[x][y - 1] == 1 and M[x + 1][y - 1] == 1 and M[x + 1][y] == 1:
            return True
    if rm_bot_r == 1:
        if M[x][y + 1] == 1 and M[x + 1][y] == 1 and M[x + 1][y + 1] == 1:
            return True
    return False


def check_num(r, c, cols, rows, M, h_list):
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
        if x < 0 or y < 0 or x >= cols or y >= rows:
            f_del.append(f)
            continue
        if M[x][y] == 1 and (x, y) not in h_list:
            f_del.append(f)
            f_sum = check_num(x, y, cols, rows, M, h_list)
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


def init_rolls(cols, rows):
    '''
    :param cols: 总列数
    :param rows: 总行数
    :return M: 生成的迷宫矩阵
    '''
    
    M = []
    
    for i in range(rows):
        r = []
        for j in range(cols):
            z = 1 if i % 2 == 1 and j % 2 == 1 else 0
            r.append(z)
        M.append(r)
    
    r, c = 0, 0
    
    M[r][c] = 1
    
    m_list = [(0, 1), (1, 0)]
    
    h_list = [(0, 0)]
    
    while m_list:
        r, c = random.choice(m_list)
        
        if rm_rord(r, c, cols, rows, M) == True:
            m_list.remove((r, c))
            continue
        
        M[r][c] = 1
        
        if r == rows - 1:
            for i in range(c, cols):
                M[r][i] = 1
            break
        elif c == cols - 1:
            for i in range(r, rows):
                M[i][c] = 1
            break
        
        m_list.remove((r, c))
        
        h_list.append((r, c))
        
        m_add = check_num(r, c, cols, rows, M, h_list)
        
        for i in m_add:
            if i not in M:
                m_list.append(i)
    
    return M


# 检查脚本，返回True & False
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

@app.route('/')
@app.route('/index')
def index():
    return redirect("/login")
    
@app.route("/login",methods=['GET'])
def login():
    if request.method == "GET":
        username = request.args.get('username')
        if username != None:
            session['username'] = username
            return redirect("/level1")
        else:
            return "please give your username"
    else:
        return "please use get method"
    
@app.route("/level1",methods=['GET'])
def level1():
    level1_num = 5
    if request.method == "GET":
        solve = request.args.get("solve")
        if 'username' in session:
            if solve :
                m_list = session['m_list1']
                now_time = int(time.time())
                s_time = session['time1']
                if now_time-s_time >=30:
                    session['level'] = 1
                    return redirect("/level1")
                try:
                    solve_list = solve.split("|")
                    solve_n_list = []
                    for i in solve_list:
                        solve_coordinate = i.split(",")
                        ii = (int(solve_coordinate[0]), int(solve_coordinate[1]))
                        solve_n_list.append(ii)
                except:
                    return redirect("/level1")
                
                if check_right(solve_n_list,m_list) == True:
                    session['level'] = 2
                    return redirect("/level2")
                else:
                    session['level'] = 1
                    return redirect('/level1')
            else:
                M = init_rolls(level1_num,level1_num)
                session['m_list1'] = M
                session['time1'] = time.time()
                tem = """
<!doctype html>
<head>
<title>welcome to ngc's misc</title>
<style>
li{list-style-type:none;height:20px}
</style>
</head>
<body>
<h1>welcome to ngc's maze</h1>
<p>here have some Challenge for you , you must solve them to get the flag</p>
<p>if you have some solution to this challenge please get solve=0,1|1,2|... to solve this chanllage</p>
<p>every challage you have 30 sec to solve</p>
<p>here is your frist maze:</p>
<ul>
{% for i in m_list %}
    <li>{{ i }}</li>
{% endfor %}
</ul></body>"""
                return render_template_string(tem,m_list=M)
        else:
            return redirect("/login")
    else:
        return redirect("/login")


@app.route("/level2", methods=['GET'])
def level2():
    level2_num = 7
    if request.method == "GET":
        solve = request.args.get("solve")
        if 'level' in session:
            if session['level'] <= 1:
                level = session['level']
                url = "/level%s"%level
                return redirect(url)
        if 'username' in session:
            if solve:
                m_list = session['m_list2']
                now_time = int(time.time())
                s_time = session['time2']
                if now_time - s_time >= 30:
                    session['level'] = 2
                    return redirect("/level2")
                try:
                    solve_list = solve.split("|")
                    solve_n_list = []
                    for i in solve_list:
                        solve_coordinate = i.split(",")
                        ii = (int(solve_coordinate[0]), int(solve_coordinate[1]))
                        solve_n_list.append(ii)
                except:
                    return redirect("/level2")
                
                if check_right(solve_n_list, m_list) == True:
                    session['level'] = 3
                    return redirect("/level3")
                else:
                    session['level'] = 2
                    return redirect('/level2')
            else:
                M = init_rolls(level2_num, level2_num)
                session['m_list2'] = M
                session['time2'] = time.time()
                tem = """
<!doctype html>
<head>
<title>welcome to ngc's misc</title>
<style>
li{list-style-type:none;height:20px}
</style>
</head>
<body>
<h1>welcome to ngc's maze</h1>
<p>here have some Challenge for you , you must solve them to get the flag</p>
<p>if you have some solution to this challenge please get solve=0,1|1,2|... to solve this chanllage</p>
<p>every challage you have 30 sec to solve</p>
<p>here is your 2nd maze:</p>
<ul>
{% for i in m_list %}
    <li>{{ i }}</li>
{% endfor %}
</ul></body>"""
                return render_template_string(tem, m_list=M)
        else:
            return redirect("/login")
    else:
        return redirect("/login")


@app.route("/level3", methods=['GET'])
def level3():
    level3_num = 15
    if request.method == "GET":
        solve = request.args.get("solve")
        if 'level' in session:
            if session['level'] <= 2:
                level = session['level']
                url = "/level%s"%level
                return redirect(url)
        if 'username' in session:
            if solve:
                m_list = session['m_list3']
                now_time = int(time.time())
                s_time = session['time3']
                if now_time - s_time >= 30:
                    session['level'] = 3
                    return redirect("/level3")
                try:
                    solve_list = solve.split("|")
                    solve_n_list = []
                    for i in solve_list:
                        solve_coordinate = i.split(",")
                        ii = (int(solve_coordinate[0]), int(solve_coordinate[1]))
                        solve_n_list.append(ii)
                except:
                    return redirect("/level3")
                
                if check_right(solve_n_list, m_list) == True:
                    session['level'] = 4
                    return redirect("/level4")
                else:
                    session['level'] = 3
                    return redirect('/level3')
            else:
                M = init_rolls(level3_num, level3_num)
                session['m_list3'] = M
                session['time3'] = time.time()
                tem = """
<!doctype html>
<head>
<title>welcome to ngc's misc</title>
<style>
li{list-style-type:none;height:20px}
</style>
</head>
<body>
<h1>welcome to ngc's maze</h1>
<p>here have some Challenge for you , you must solve them to get the flag</p>
<p>if you have some solution to this challenge please get solve=0,1|1,2|... to solve this chanllage</p>
<p>every challage you have 30 sec to solve</p>
<p>here is your 3rd maze:</p>
<ul>
{% for i in m_list %}
    <li>{{ i }}</li>
{% endfor %}
</ul></body>"""
                return render_template_string(tem, m_list=M)
        else:
            return redirect("/login")
    else:
        return redirect("/login")


@app.route("/level4", methods=['GET'])
def level4():
    level4_num = 35
    if request.method == "GET":
        solve = request.args.get("solve")
        if 'level' in session:
            if session['level'] <= 3:
                level = session['level']
                url = "/level%s"%level
                return redirect(url)
        if 'username' in session:
            if solve:
                m_list = session['m_list4']
                now_time = int(time.time())
                s_time = session['time4']
                if now_time - s_time >= 30:
                    session['level'] = 4
                    return redirect("/level4")
                try:
                    solve_list = solve.split("|")
                    solve_n_list = []
                    for i in solve_list:
                        solve_coordinate = i.split(",")
                        ii = (int(solve_coordinate[0]), int(solve_coordinate[1]))
                        solve_n_list.append(ii)
                except:
                    return redirect("/level4")
                
                if check_right(solve_n_list, m_list) == True:
                    session['level'] = 5
                    return redirect("/level5")
                else:
                    session['level'] = 4
                    return redirect('/level4')
            else:
                M = init_rolls(level4_num, level4_num)
                session['m_list4'] = M
                session['time4'] = time.time()
                tem = """
<!doctype html>
<head>
<title>welcome to ngc's misc</title>
<style>
li{list-style-type:none;height:20px}
</style>
</head>
<body>
<h1>welcome to ngc's maze</h1>
<p>here have some Challenge for you , you must solve them to get the flag</p>
<p>if you have some solution to this challenge please get solve=0,1|1,2|... to solve this chanllage</p>
<p>every challage you have 30 sec to solve</p>
<p>here is your 4th maze:</p>
<ul>
{% for i in m_list %}
    <li>{{ i }}</li>
{% endfor %}
</ul></body>"""
                return render_template_string(tem, m_list=M)
        else:
            return redirect("/login")
    else:
        return redirect("/login")


@app.route("/level5", methods=['GET'])
def level5():
    level5_num = 55
    if request.method == "GET":
        solve = request.args.get("solve")
        if 'level' in session:
            if session['level'] <= 4:
                level = session['level']
                url = "/level%s"%level
                return redirect(url)
        if 'username' in session:
            if solve:
                m_list = session['m_list5']
                now_time = int(time.time())
                s_time = session['time5']
                if now_time - s_time >= 30:
                    session['level'] = 5
                    return redirect("/level5")
                try:
                    solve_list = solve.split("|")
                    solve_n_list = []
                    for i in solve_list:
                        solve_coordinate = i.split(",")
                        ii = (int(solve_coordinate[0]), int(solve_coordinate[1]))
                        solve_n_list.append(ii)
                except:
                    return redirect("/level5")
                
                if check_right(solve_n_list, m_list) == True:
                    flag = "hgame{797ead6a7aeeb1ae228e0caff7d09306}"
                    return flag
                else:
                    session['level'] = 5
                    return redirect('/level5')
            else:
                M = init_rolls(level5_num, level5_num)
                session['m_list5'] = M
                session['time5'] = time.time()
                tem = """
<!doctype html>
<head>
<title>welcome to ngc's misc</title>
<style>
li{list-style-type:none;height:20px}
</style>
</head>
<body>
<h1>welcome to ngc's maze</h1>
<p>here have some Challenge for you , you must solve them to get the flag</p>
<p>if you have some solution to this challenge please get solve=0,1|1,2|... to solve this chanllage</p>
<p>every challage you have 30 sec to solve</p>
<p>here is your frist maze:</p>
<ul>
{% for i in m_list %}
    <li>{{ i }}</li>
{% endfor %}
</ul></body>"""
                return render_template_string(tem, m_list=M)
        else:
            return redirect("/login")
    else:
        return redirect("/login")
    

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(host="0.0.0.0")

