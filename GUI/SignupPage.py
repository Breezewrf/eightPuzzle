# -*- coding: utf-8 -*-
# @Time    : 2020/10/13 16:20
# @Author  : Breeze
# @Email   : 578450426@qq.com
import json
from tkinter import *
from tkinter.messagebox import showinfo

infoPath = './info.json'


class SignupPage(object):
    def __init__(self, master=None):
        self.root = master
        self.root.geometry('%dx%d' % (300, 200))
        self.SIGNusername = StringVar()
        self.SIGNpassword = StringVar()
        self.SIGNrepassword = StringVar()
        self.SignUp()

    def SignUp(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Label(self.page, text='注册账号: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.SIGNusername).grid(row=1, column=1, stick=E)
        Label(self.page, text='密码: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.SIGNpassword, show='*').grid(row=2, column=1, stick=E)
        Label(self.page, text='确认密码: ').grid(row=3, stick=W, pady=10)
        Entry(self.page, textvariable=self.SIGNrepassword, show='*').grid(row=3, column=1, stick=E)
        Button(self.page, text='注册', command=self.SignUpCheck).grid(row=4, stick=W, pady=10)
        Button(self.page, text='退出', command=self.page.quit).grid(row=4, column=1, stick=E)

    def SignUpCheck(self):
        uid = self.SIGNusername.get()
        pw = self.SIGNpassword.get()
        print("show:", len(uid), pw)
        repw = self.SIGNrepassword.get()
        if pw != repw:
            showinfo(title="错误", message="两次输入的密码不一致,请重新输入")
        else:
            with open(infoPath, 'w') as f:
                info = {"uid": str(uid), "pw": str(pw)}

                print("!!!")
                json.dump(info, f)
            f.close()
            showinfo(title="ok", message="注册成功")
