# -*- coding: UTF-8 -*-

import sqlite3

class DB:
    def __init__(self):
        try:
            self.cur = sqlite3.connect('projects.db')
            self.cur.text_factory = sqlite3.OptimizedUnicode
            self.cur.execute('CREATE TABLE IF NOT EXISTS project(id INT, title TEXT, name TEXT, link TEXT, summary TEXT, last_update TEXT, collect INT, comment INT, score REAL);')
        except sqlite3.Error, msg:
            print 'Error %s:' % msg.args[0]

    def __del__(self):
        if self.cur:
            self.cur.close()

    def wipe(self):
        self.cur.execute("DROP TABLE IF EXISTS project")
        self.cur.execute('CREATE TABLE project(id INT, title TEXT, name TEXT, link TEXT, summary TEXT, last_update TEXT, collect INT, comment INT, score REAL);')

    def insert(self, id, title, name, link, summary, last_update, collect, comment, score):
        self.cur.execute('INSERT INTO project(id) VALUES(' + str(id) + ');')
        self.cur.execute('UPDATE project set title=' + '"' + title + '"' + ' WHERE id=' + str(id) + ';')
        self.cur.execute('UPDATE project set name=' + '"' + name + '"' + ' WHERE id=' + str(id) + ';')
        self.cur.execute('UPDATE project set link=' + '"' + link + '"' + ' WHERE id=' + str(id) + ';')
        self.cur.execute('UPDATE project set summary=' + '"' + summary + '"' + ' WHERE id=' + str(id) + ';')
        self.cur.execute('UPDATE project set last_update=' + '"' + last_update + '"' + ' WHERE id=' + str(id) + ';')
        self.cur.execute('UPDATE project set collect=' + str(collect) + ' WHERE id=' + str(id) + ';')
        self.cur.execute('UPDATE project set comment=' + str(comment) + ' WHERE id=' + str(id) + ';')
        self.cur.execute('UPDATE project set score=' + str(score) + ' WHERE id=' + str(id) + ';')
        self.cur.commit()

    def list(self, op):
        if op == 'l0' or op == 'l':
            return self.cur.execute("SELECT * FROM project")
        elif op == 'l1':
            return self.cur.execute("SELECT * FROM project ORDER BY collect")
        elif op == 'l2':
            return self.cur.execute("SELECT * FROM project ORDER BY collect DESC")
        elif op == 'l3':
            return self.cur.execute("SELECT * FROM project ORDER BY comment")
        elif op == 'l4':
            return self.cur.execute("SELECT * FROM project ORDER BY comment DESC")
        elif op == 'l5':
            return self.cur.execute("SELECT * FROM project ORDER BY score")
        elif op == 'l6':
            return self.cur.execute("SELECT * FROM project ORDER BY score DESC")
        else:
            return None

    def search(self, op):
        if op == 's0' or op == 's':
            keyword = raw_input("请输入关键字: ")
            cursor = self.cur.cursor()
            cursor.execute("SELECT * FROM project WHERE title LIKE" + "'%" + keyword + "%';")
            projects = cursor.fetchall()
            cursor.execute("SELECT * FROM project WHERE name LIKE" + "'%" + keyword + "%';")
            projects += cursor.fetchall()
            cursor.execute("SELECT * FROM project WHERE summary LIKE" + "'%" + keyword + "%';")
            projects += cursor.fetchall()
            return projects
        elif op == 's1':
            number = raw_input("请输入数值: ")
            return self.cur.execute("SELECT * FROM project WHERE collect >= " + number + ";")
        elif op == 's2':
            number = raw_input("请输入数值: ")
            return self.cur.execute("SELECT * FROM project WHERE collect < " + number + ";")
        elif op == 's3':
            number = raw_input("请输入数值: ")
            return self.cur.execute("SELECT * FROM project WHERE comment >= " + number + ";")
        elif op == 's4':
            number = raw_input("请输入数值: ")
            return self.cur.execute("SELECT * FROM project WHERE comment < " + number + ";")
        elif op == 's5':
            number = raw_input("请输入数值: ")
            return self.cur.execute("SELECT * FROM project WHERE score >= " + number + ";")
        elif op == 's6':
            number = raw_input("请输入数值: ")
            return self.cur.execute("SELECT * FROM project WHERE score < " + number + ";")
        else:
            return None