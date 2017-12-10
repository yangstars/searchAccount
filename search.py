# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import MySQLdb
import ttk
import datetime


class loginPage(object):
    def __init__(self, root, info='搜素小工具'):
        self.root = root
        self.mainlabel = Label(root, text=info, justify=CENTER)
        self.mainlabel.grid(row=0, columnspan=3)
        self.user = Label(root, text='username', borderwidth=10)
        self.user.grid(row=1, sticky=W)

        self.pwd = Label(root, text='password', borderwidth=10)
        self.pwd.grid(row=2, sticky=W)

        self.userEntry = Entry(root)
        self.userEntry.grid(row=1, column=1, columnspan=3)
        self.userEntry.focus_set()

        self.pwdEntry = Entry(root, show='*')
        self.pwdEntry.grid(row=2, column=1, columnspan=3)

        self.loginButton = Button(root, text='登陆', borderwidth=2, command=self.login)
        self.loginButton.grid(row=3, column=1)

        # self.clearButton = Button(root, text='清除', borderwidth=2, command=self.clear)
        # self.clearButton.grid(row=3, column=2)

        self.clearButton = Button(root, text='注册', borderwidth=2, command=self.register)
        self.clearButton.grid(row=3, column=2)

    #登陆
    def login(self):
        self.username = self.userEntry.get().strip()
        self.password = self.pwdEntry.get().strip()
        self.userid =""
        #对用户名和密码进行验证
        #if len(self.username) == 0 or len(self.password) == 0 or '@' not in self.username:
        if  len(self.username) == 0 or len(self.password) == 0:
            tkMessageBox.showwarning('警告', '用户名或者密码为空或邮件格式不正确')
            self.clear()
            self.userEntry.focus_set()
            return

        # 连接数据库
        db = self.connectdb()
        #判断是否有表，如果有直接插入，如果没有创建表之后插入
        cursor = db.cursor()##  使用cursor()方法获取操作游标
        select_sql = "select * from user WHERE username ='%s'" % (self.username)
        select_data = cursor.execute(select_sql)
        if select_data == 0:
            tkMessageBox.showwarning('提示', '%s该用户未注册' % (self.username))
            return

        User = cursor.fetchall()
        for user in User:
            if self.password == user[2]:
                print "用户登陆成功"
                #隐藏登陆页面
                root.withdraw()
                # 跳转到页面
                self.userid = int(user[0])
                searchPage(self.root, self.username,self.userid)
            else:
                tkMessageBox.showwarning('提示', '密码输入错误，请重新输入')

    #注册
    def register(self):
        self.username = self.userEntry.get().strip()
        self.password = self.pwdEntry.get().strip()
        # 对用户名和密码进行验证
        #if len(self.username) == 0 or len(self.password) == 0 or '@' not in self.username:
        if len(self.username) == 0 or len(self.password) == 0:
            tkMessageBox.showwarning('警告', '用户名或者密码为空或邮件格式不正确')
            self.clear()
            self.userEntry.focus_set()
            return
        # 连接数据库
        db = self.connectdb()
        #判断是否有表，如果有直接插入，如果没有创建表之后插入
        cursor = db.cursor()##  使用cursor()方法获取操作游标

        #cursor.execute("DROP TABLE IF EXISTS `user`")

        # sql = """CREATE TABLE `user` (
        #           `id` int(11) NOT NULL AUTO_INCREMENT,
        #           `username` varchar(64) NOT NULL,
        #           `password` varchar(64) NOT NULL,
        #           PRIMARY KEY (`id`)
        #       ) """

        #cursor.execute(sql)

        #判断用户是否注册
        select_sql = "select * from user WHERE username ='%s'"%(self.username)
        select_data = cursor.execute(select_sql)
        if select_data != 0 :
            tkMessageBox.showwarning('提示','%s该用户已经注册'%(self.username))
        else:
        # results = cursor.fetchall()
        # print select_data
        # print results
        # for row in results:
        #     print row[1]#获取用户id

        #用户插入到数据库
            insert_sql = "INSERT INTO user(username, password) VALUES ('%s','%s')"%(self.username,self.password)
            cursor.execute(insert_sql)
        # 向数据库提交
            try:
                db.commit()
                print "------%s 用户注册成功！-------"%(self.username)
            except:
                db.rollback()

    #数据库连接
    def connectdb(self):
        print('连接到mysql服务器...')
        # 打开数据库连接
        # 用户名:hp, 密码:Hp12345.,用户名和密码需要改成你自己的mysql用户名和密码，并且要创建数据库TESTDB，并在TESTDB数据库中创建好表Student
        db = MySQLdb.connect("127.0.0.1", "root", "root", "py")
        print('连接上了!')
        return db

    def clear(self):
        self.userEntry.delete(0, END)
        self.pwdEntry.delete(0, END)

class searchPage(object):
    def __init__(self, root, username, userid):
        self.userid = userid
        self.root = root
        self.username = username
        self.searchPage = Toplevel(self.root)
        self.searchPage.geometry('800x550+400+140')
        self.searchPage.title('账号搜索')
        self.searchButton = Button(self.searchPage, text='增加', command=self.add)
        self.searchButton.grid(row=0, column=1)

        self.searchlabel = Label(self.searchPage, text='搜索条件：')
        self.searchlabel.grid(row=1, column=0)

        self.appNameLabel = Label(self.searchPage, text='应用名:')
        self.appNameLabel.grid(row=2, column=0)
        self.appNameEntry = Entry(self.searchPage)
        self.appNameEntry.grid(row=2, column=1)

        self.appAccountLabel = Label(self.searchPage, text='账号:')
        self.appAccountLabel.grid(row=3, column=0)
        self.appAccountEntry = Entry(self.searchPage)
        self.appAccountEntry.grid(row=3, column=1)

        self.searchButton = Button(self.searchPage, text='搜索', command=self.get_tree)
        self.searchButton.grid(row=4, column=1)

        # self.resultLabel = Label(self.searchPage, text='搜素内容:')
        # self.resultLabel.grid(row=4, column=0)
        # self.sendText = Text(self.searchPage)
        # self.sendText.grid(row=5, column=1)
        # win = Tkinter.Tk()
        # 定义中心列表区域
        self.tree = ttk.Treeview(self.searchPage, show="headings", height=18, columns=("a", "b", "c", "d", "e","f"))
        self.vbar = ttk.Scrollbar(self.searchPage, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.tree.column("a", width=80, anchor="center")
        self.tree.column("b", width=100, anchor="center")
        self.tree.column("c", width=120, anchor="center")
        self.tree.column("d", width=120, anchor="center")
        self.tree.column("e", width=120, anchor="center")
        self.tree.column("f", width=150, anchor="center")
        self.tree.heading("a", text="app")
        self.tree.heading("b", text="账号")
        self.tree.heading("c", text="密码")
        self.tree.heading("d", text="注册邮箱")
        self.tree.heading("e", text="手机号")
        self.tree.heading("f", text="创建时间")
        # 调用方法获取表格内容插入
        # self.get_tree()
        self.tree.grid(row=5, column=1, sticky=NSEW)
        self.vbar.grid(row=5, column=2, sticky=NS)

        # 整体区域定位
        # self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        # self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        # self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        # self.frame_bottom.grid(row=2, column=0, columnspan=2)
        #
        # self.frame_left_top.grid_propagate(0)
        # self.frame_right_top.grid_propagate(0)
        # self.frame_center.grid_propagate(0)
        # self.frame_bottom.grid_propagate(0)

        self.root.mainloop()
        # self.newButton = Button(self.sendPage, text='new mail', command=self.newMail)
        # self.newButton.grid(row=4, column=1)

    #数据库连接
    def connectdb(self):
        print('连接到mysql服务器...')
        # 打开数据库连接
        # 用户名:hp, 密码:Hp12345.,用户名和密码需要改成你自己的mysql用户名和密码，并且要创建数据库TESTDB，并在TESTDB数据库中创建好表Student
        db = MySQLdb.connect("127.0.0.1", "root", "root", "py",charset="utf8")
        print('连接上了!')
        return db

    def get_tree(self):
        # 删除原来的数据
        for _ in map(self.tree.delete, self.tree.get_children("")):
            pass
        appName = self.appNameEntry.get().strip()
        appAccount = self.appAccountEntry.get().strip()

        # 根据条件模糊模糊搜索
        # 连接数据库
        db1 = self.connectdb()
        # 判断是否有表，如果有直接插入，如果没有创建表之后插入
        cursor = db1.cursor()  # 使用cursor()方法获取操作游标
        if len(appName) == 0 and len(appAccount) != 0:
            select_sql = "SELECT * from app_account WHERE user_id='%d'and app_account LIKE '%s'" % (self.userid, appAccount)
        elif len(appName) != 0 and len(appAccount) == 0:
            select_sql = "SELECT * from app_account WHERE user_id='%d'and app_name LIKE '%s'" % (self.userid, appName)
        elif len(appName) == 0 and len(appAccount) == 0:
            select_sql = "SELECT * from app_account WHERE user_id='%d'" % (self.userid)
        else:
            select_sql = "SELECT * from app_account WHERE user_id='%d'and app_account LIKE '%s' AND app_account LIKE '%s'" % (self.userid, appName, appAccount)

        select_data = cursor.execute(select_sql)
        if select_data == 0:
            tkMessageBox.showwarning('提示', '没有历史信息')
            return
        cursor.fetchall
        result = cursor.fetchall()
        for account in result:
            a = account[2]
            self.tree.insert("", "end", values=(account[2],account[3],account[4],account[5],account[6],account[7]))

    def add(self):
        addPage(self.root,self.userid)


class addPage(object):
    def __init__(self, root, userid):
        self.userid = userid
        self.root = root
        self.addPage = Toplevel(root)
        self.addPage.geometry('240x180+630+200')
        self.addPage.title('账号添加')

        self.appNamelabel = Label(self.addPage, text='aap名称：')
        self.appNamelabel.grid(row=1, column=0)
        self.appNameEntry = Entry(self.addPage)
        self.appNameEntry.grid(row=1, column=1)

        self.loginAccountLabel = Label(self.addPage, text='登陆账号:')
        self.loginAccountLabel.grid(row=2, column=0)
        self.loginAccountEntry = Entry(self.addPage)
        self.loginAccountEntry.grid(row=2, column=1)

        self.pwdLabel = Label(self.addPage, text='登陆密码:')
        self.pwdLabel.grid(row=3, column=0)
        self.pwdEntry = Entry(self.addPage)
        self.pwdEntry.grid(row=3, column=1)

        self.mailLabel = Label(self.addPage, text='绑定邮箱:')
        self.mailLabel.grid(row=4, column=0)
        self.mailEntry = Entry(self.addPage)
        self.mailEntry.grid(row=4, column=1)

        self.phoneLabel = Label(self.addPage, text='手机号:')
        self.phoneLabel.grid(row=5, column=0)
        self.phoneEntry = Entry(self.addPage)
        self.phoneEntry.grid(row=5, column=1)

        self.searchButton = Button(self.addPage, text='添加', command=self.addAccount)
        self.searchButton.grid(row=6, column=1)

        self.root.mainloop()

    def addAccount(self):
        user_id=self.userid
        app_name=self.appNameEntry.get().strip()
        app_account=self.loginAccountEntry.get().strip()
        app_pwd=self.pwdEntry.get().strip()
        app_mail=self.mailEntry.get().strip()
        app_phone=self.phoneEntry.get().strip()
        create_time =datetime.datetime.now()
        # 连接数据库
        db = self.connectdb()
        #判断是否有表，如果有直接插入，如果没有创建表之后插入
        cursor = db.cursor() #使用cursor()方法获取操作游标
        # SQL 插入语句
        sql = "INSERT INTO app_account(user_id,app_name,app_account,app_pwd,app_mail,app_phone,create_time)VALUES ('%s', '%s', '%s', '%s', '%s','%s','%s')"%(user_id,app_name,app_account,app_pwd,app_mail,app_phone,create_time)
        print  sql
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            # 隐藏登陆页面
            self.addPage.withdraw()
            tkMessageBox.showwarning('提示', '添加成功！')
        except:
            db.rollback()
        # 关闭数据库连接
        db.close()

    #数据库连接
    def connectdb(self):
        print('连接到mysql服务器...')
        # 打开数据库连接
        # 用户名:hp, 密码:Hp12345.,用户名和密码需要改成你自己的mysql用户名和密码，并且要创建数据库TESTDB，并在TESTDB数据库中创建好表Student
        db = MySQLdb.connect("127.0.0.1", "root", "root", "py",charset="utf8")
        print('连接上了!')
        return db




if __name__ == '__main__':
    root = Tk()
    root.title('登陆注册')
    root.geometry('250x150+600+300')
    myLogin = loginPage(root)
    # root.wait_window(myLogin.mySendMail.sendPage)
    mainloop()
