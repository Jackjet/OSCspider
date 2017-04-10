# -*- coding: UTF-8 -*-

from spider import *

def main_view():
    print '-------------------------------------------------------'
    print 'l.列出项目\ts.查找项目\tc.更新项目\tq.退出'
    print '|---0.顺序 \t|---0.关键字'
    print '|---1.收藏↑\t|---1.收藏>='
    print '|---2.收藏↓\t|---2.收藏<'
    print '|---3.评论↑\t|---3.评论>='
    print '|---4.评论↓\t|---4.评论<'
    print '|---5.评分↑\t|---5.评分>='
    print '|---6.评分↓\t|---6.评分<'
    print '-------------------------------------------------------'

app = OSCPspider()

while True:
    main_view()
    op = raw_input("请输入:")
    if not op:
        continue
    elif op[0] == 'l':
        flag = app.list_p(op)
    elif op[0] == 's':
        flag = app.search_p(op)
    elif op == 'c':
        flag = app.catch_p()
    elif op == 'q':
        exit()
    else:
        flag = 'no_op'

    if flag == 'no_op':
        print "没有该操作!"