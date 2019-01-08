#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
import os
import os.path

class Node(object):
    """定义类来描述指针"""
    def __init__(self, name, changeTime='', size='', data='', p=None):
        self.name = name               # 文件名
        self.changeTime = changeTime   # 修改时间
        self.size = size               # 文件大小
        self.data = data               # 文件内容
        self.next = p


class LinkList(object):
    """单链表"""

    def __init__(self):
        self.head = None

    # 初始化单链表
    def create(self, data):
        self.head = Node(data[0])
        p = self.head
        for i in data[1:]:
            p.next = Node(i)
            p = p.next

    # 获取单链表的长度
    def len(self):
        p = self.head
        length = 0
        while p != None:
            length += 1
            p = p.next
        return length

    # 判断单链表是否为空
    def is_empty(self):
        return self.len() == 0

    def add(self, name, changeTime, size, data):
        temp = Node(name, changeTime, size, data)
        if self.is_empty():
            self.head = temp
        else:
            temp.next = self.head
            self.head = temp

    # 获取单链表指定位置的数据
    def getItem(self, index):
        if self.is_empty():
            print("单链表为空")
            return
        if index >= self.len() or index < 0:
            print("索引超过单链表长度")
            return
        p = self.head
        count = 0
        while count != index:
            p = p.next
            count += 1
        return p.data

    # 获取单链表指定元素的索引
    def find(self, item):
        p = self.head
        index = 0
        while p != None:
            if p.name == item:
                return index
            p = p.next
            index += 1

    # 删除单链表指定位置的元素
    def delete(self, index):
        if self.is_empty():
            #print("单链表为空")
            return
        if index >= self.len() or index < 0:
            #print("索引超过单链表长度")
            return
        if index == 0:
            self.head = self.head.next
        else:
            p = self.head
            count = 0
            while count < index-1:
                p = p.next
                count += 1
            p.next = p.next.next

    # 打印单链表, 也就是在文件系统中的文件内容
    def print(self):
        p = self.head
        while p != None:
            print(p.name + '\t' + str(int(p.size/1024)+1) + 'KB\t' + p.changeTime)
            p = p.next

    # 指定文件系统的文件保存到本地
    def getFile(self, index):
        p = self.head
        count = 0
        while count < index-1:
            p = p.next
            count += 1
        with open(p.name, 'w+') as f:
            f.write(p.data)

    # 退出文件系统并保存系统中的所有文件内容到open打开的文件中
    def saveFile(self, filename):
        with open(filename, 'w+') as f:
            p = self.head
            while p != None:
                data = p.name + '\n' + str(p.size) + '\n' + p.changeTime + '\n' + p.data
                f.write(data)
                p = p.next

# 打开指定的本地文件
def readFile(fileName):
    global filename
    filename = fileName
    with open(fileName, 'w+') as f:
        pass

# 保存文件系统中所有的文件到本地
def saveFile(filename):
    L.saveFile(filename)

# 检查本地是否有该文件, 有则读取到文件系统中
def PUT(fileName):
    if (os.path.exists(fileName)):
        fsize = os.path.getsize(fileName)
    else:
        print('open file error.\n')
        return

    with open(fileName, 'r') as f:
        data = f.read()
        changeTime = time.strftime('%a %b %H:%M:%S %Y',time.localtime(time.time()))
        L.add(fileName, changeTime, fsize, data)

# 检查文件系统中是否有该文件, 有则保存到本地
def GET(fileName):
    index = L.find(fileName)
    if index is None:
        print('file not exist.\n')
        return
    L.getFile(index)

# 指定删除文件系统的文件
def RM(fileName):
    index = L.find(fileName)
    L.delete(index)

# 指定删除本地的文件
def KILL(fileName):
    if (os.path.exists(fileName)):
        fsize = os.path.getsize(fileName)
        os.remove(fileName)
    else:
        print('kill file error.\n')
        
    return

L = LinkList()

filename = ''

while True:
    arg = input('PFS>').strip()
    # 将获取到的命令行输入拆分
    arg = arg.split(' ', 1)
    arg1 = arg[0]
    flag = 0    # 用于有没有传入命令参数   0:没有 1:有
    if len(arg) >= 2:
        arg2 = arg[1].strip()
        flag = 1

    if arg1 == 'open':
        readFile(arg2)
        fileName = arg2
    elif arg1 == 'put':
        PUT(arg2)
    elif arg1 == 'get':
        if (flag == 0):
            print('file not exist.\n')
        else:
            GET(arg2)
    elif arg1 == 'rm':
        if (flag == 0):
            print('file not exist.\n')
        else:
            RM(arg2)
    elif arg1 == 'dir':
        L.print()
    elif arg1 == 'kill':
        if (flag == 0):
            print('kill file error.\n')
        else:
            KILL(arg2)
    elif arg1 == 'quit':
        break
    else:
        print('command input error.\n');

# 退出文件系统并保存系统中的所有文件内容到open打开的文件中
if filename != '':
    saveFile(filename)
