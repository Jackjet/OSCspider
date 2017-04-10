# -*- coding: UTF-8 -*-

import urllib
import urllib2
import re
import sys
import sqlite3
from db import *

class OSCPspider:

    def __init__(self):
        self.URL = "https://www.oschina.net/project/list"
        self.head = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        self.p_amount = self.amount_of_pages()          #所要爬取网页的总页数

    # 返回开源中国软件列表的总页数
    def amount_of_pages(self):
        request = urllib2.Request(self.URL, None, self.head)
        response = urllib2.urlopen(request)
        pattern = re.compile('<ul class="paging".*?<li.*?<li.*?<li.*?<li.*?<li.*?<li.*?<li>.*?>(.*?)</a>',re.S)
        amount = re.findall(pattern, response.read())
        return int(amount[0])

    # 爬取网页
    def catch_p(self):
        p_db = DB()
        p_db.wipe()
        id = 1

        for i in range(1, self.p_amount + 1):
            request = urllib2.Request(self.URL + '?p=' + str(i), None, self.head)
            response = urllib2.urlopen(request)
            page = response.read()
            pattern = re.compile('<div class="box item">.*?<div class="box-aw">.*?<a  href="(.*?)".*?<div class="title">(.*?)<span class="project-name">(.*?)<.*?<div class="summary">[\s]*(.*?)[\s]{3,}<.*?<footer class="related box">(.*?)</footer>', re.S)
            projects = re.findall(pattern, page)
            for project in projects:
                title = "".join(project[1].split()).replace('"', ' ').replace("'", " ").replace(';', ' ')
                if not title:
                    title = " "
                name = project[2].replace('"', ' ').replace("'", " ").replace(';', ' ')
                if not name:
                    name = " "
                link = project[0]
                summary = project[3].replace('"', ' ').replace("'", " ").replace(';', ' ')
                if not summary:
                    summary = " "
                if len(project[4].split("上次更新: ")) != 1:
                    last_update = project[4].split("上次更新: ")[1].split("<")[0]
                else:
                    last_update = " "
                if len(project[4].split("收藏 ")) != 1:
                    collect = int(project[4].split("收藏 ")[1].split("<")[0])
                else:
                    collect = 0
                if len(project[4].split("评论 ")) != 1:
                    comment = int(project[4].split("评论 ")[1].split("<")[0])
                else:
                    comment = 0
                if len(project[4].split("评分 ")) != 1:
                    score = float(project[4].split("评分 ")[1].split("<")[0])
                else:
                    score = 0.0
                p_db.insert(id, title, name, link, summary, last_update, collect, comment, score)
                id += 1
            sys.stdout.write('\r更新中......' + str(int(round(float(i) / float(self.p_amount), 2) * 100)) + '%')
            sys.stdout.flush()
        print "\n更新完成!"
        return 'ok'

    # 列出本地数据库中的项目
    def list_p(self, op = ''):
        if len(op) >= 3:
            return 'no_op'

        p_db = DB()
        projects = p_db.list(op)
        if projects == None:
            return 'no_op'

        return self.show_p(projects)

        return 'ok'

    # 在本地数据库的项目中查找
    def search_p(self, op):
        if len(op) >= 3:
            return 'no_op'

        p_db = DB()
        projects = p_db.search(op)
        if projects == None:
            return 'no_op'

        return self.show_p(projects)

    # 每次7条地列出项目
    def show_p(self, projects):
        count = 0

        for project in projects:
            if project == []:
                continue
            id = project[0]
            title = project[1]
            name = project[2]
            link = project[3]
            summary = project[4]
            last_update = project[5]
            collect = project[6]
            comment = project[7]
            score = project[8]

            print str(id) + '.' + title + '\n' + name + ' : ' + link + '\n' + summary
            print '最后更新:'.decode('utf8') + last_update + ' 收藏:'.decode('utf8') + str(collect) + ' 评论:'.decode('utf8') + str(comment) + ' 评分:'.decode('utf8') + str(score) + '\n'
            count += 1

            if count >= 7:
                if raw_input("回车继续,输入q退出") == 'q':
                    return 'quit'
                else:
                    count = 0

        return 'ok'