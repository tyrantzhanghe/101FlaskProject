# 引入模块
import os
import hashlib
import datetime
import functools
from main import app
from models import User
from flask import request,jsonify
from models import *
from flask import render_template, redirect, session
from form import Task
from main import csrf
from settings import STATICFILES_DIR

from main import api
from flask_restful import Resource

# 定义MD5加密函数
def SetPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


# 定义cookie装饰器，获取cookie
def loginValid(fun):
    @functools.wraps(fun)
    def inner(*args, **kwargs):
        username = request.cookies.get("username")
        id = request.cookies.get("id", 0)
        user = User.query.get(int(id))
        session_username = session.get("username")
        if user and user.user_name == username and username == session_username:
            return fun(*args, **kwargs)
        else:
            return redirect("/login/")

    return inner



#分页器
# class Page:
#     def __init__(self,data,page_size):
#         self.data=data
#         self.page_size=page_size
#         self.is_start=False
#         self.is_end=False
#         self.page_count=len(data)
#         self.next_page=0
#         self.previons_page=0
#         # self.page_number=self.page_count/page_size
#         self.page_number=(data+page_size-1)//page_size
#         self.page_range=range(1,self.page_number+1)
#
#     def page_data(self,page):
#         self.next_page=int(page)+1
#         self.previons_page=int(page)-1
#         if page<=self.page_range[-1]:
#             pass


# class Calendar:
#     """
#     当前类实现日历功能
#     1、返回列表嵌套列表的日历
#     2、安装日历格式打印日历
#         # 如果一号周周一那么第一行1-7号   0
#         # 如果一号周周二那么第一行empty*1+1-6号  1
#         # 如果一号周周三那么第一行empty*2+1-5号  2
#         # 如果一号周周四那么第一行empty*3+1-4号  3
#         # 如果一号周周五那么第一行empyt*4+1-3号  4
#         # 如果一号周周六那么第一行empty*5+1-2号  5
#         # 如果一号周日那么第一行empty*6+1号   6
#         # 输入 1月
#         # 得到1月1号是周几
#         # [] 填充7个元素 索引0对应周一
#         # 返回列表
#         # day_range 1-30
#     """
#     def __init__(self,month = "now"):
#         self.result = []
#
#         big_month = [1, 3, 5, 7, 8, 10, 12]
#         small_month = [4, 6, 9, 11]
#
#         #获取当前月
#         now = datetime.datetime.now()
#         if month == "now":
#             month = now.month
#             first_date = datetime.datetime(now.year, now.month, 1, 0, 0)
#             # 年 月 日 时 分
#         else:
#             #assert int(month) in range(1,13)
#             first_date = datetime.datetime(now.year, month, 1, 0, 0)
#
#         if month in big_month:
#             day_range = range(1, 32)  # 指定月份的总天数
#         elif month in small_month:
#             day_range = range(1, 31)
#         else:
#             day_range = range(1, 29)
#
#         # 获取指定月天数
#         self.day_range = list(day_range)
#         first_week = first_date.weekday()  # 获取指定月1号是周几 6
#
#         line1 = []  # 第一行数据
#         for e in range(first_week):
#             line1.append("empty")
#         for d in range(7 - first_week):
#             line1.append(
#                 str(self.day_range.pop(0))+"—django开发"
#                          )
#         self.result.append(line1)
#         while self.day_range:  # 如果总天数列表有值，就接着循环
#             line = []  # 每个子列表
#             for i in range(7):
#                 if len(line) < 7 and self.day_range:
#                     line.append(str(self.day_range.pop(0))+"—django开发")
#                 else:
#                     line.append("empty")
#             self.result.append(line)
#     def return_month(self):
#         """
#         返回列表嵌套列表的日历
#         """
#         return self.result

class Calendar:
    """
    当前类实现日历功能
    1、返回列表嵌套列表的日历
    2、安装日历格式打印日历
        # 如果一号周周一那么第一行1-7号   0
        # 如果一号周周二那么第一行empty*1+1-6号  1
        # 如果一号周周三那么第一行empty*2+1-5号  2
        # 如果一号周周四那么第一行empty*3+1-4号  3
        # 如果一号周周五那么第一行empyt*4+1-3号  4
        # 如果一号周周六那么第一行empty*5+1-2号  5
        # 如果一号周日那么第一行empty*6+1号   6
        # 输入 1月
        # 得到1月1号是周几
        # [] 填充7个元素 索引0对应周一
        # 返回列表
        # day_range 1-30
    """

    def __init__(self, month="now"):
        self.result = []

        big_month = [1, 3, 5, 7, 8, 10, 12]
        small_month = [4, 6, 9, 11]

        # 获取当前月
        now = datetime.datetime.now()
        if month == "now":
            month = now.month
            first_date = datetime.datetime(now.year, now.month, 1, 0, 0)
            # 年 月 日 时 分
        else:
            # assert int(month) in range(1,13)
            first_date = datetime.datetime(now.year, month, 1, 0, 0)

        if month in big_month:
            day_range = range(1, 32)  # 指定月份的总天数
        elif month in small_month:
            day_range = range(1, 31)
        else:
            day_range = range(1, 29)

        # 获取指定月天数
        self.day_range = list(day_range)
        first_week = first_date.weekday()  # 获取指定月1号是周几 6

        line1 = []  # 第一行数据
        for e in range(first_week):
            line1.append({"day": '', 'project': ''})
        for d in range(7 - first_week):
            dir1 = {}
            dir1['day'] = str(self.day_range.pop(0))
            dir1['project'] = 'django开发'
            line1.append(dir1)  # [{day:n,pro:d},{}]
        self.result.append(line1)
        while self.day_range:  # 如果总天数列表有值，就接着循环
            line = []  # 每个子列表
            for i in range(7):
                if len(line) < 7 and self.day_range:
                    dir2 = {}
                    dir2['day'] = str(self.day_range.pop(0))
                    dir2['project'] = 'django开发'
                    line.append(dir2)
                else:
                    line.append({"day": '', 'project': ''})
            self.result.append(line)

    def return_month(self):
        """
        返回列表嵌套列表的日历
        """
        return self.result


@app.route("/")
@loginValid
def index1():
    return render_template("index.html")


@app.route("/index/")
@loginValid
def index():
    return render_template("index.html")


@app.route("/user_info/")
def user_info():
    calendar = Calendar().return_month()
    now = datetime.datetime.now()
    return render_template("user_info.html", **locals())


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        print(username)
        password = request.form.get("password")
        encode_password = SetPassword(password)
        print(password)
        email = request.form.get("email")
        print(email)
        user = User()
        user.user_name = username
        user.password = encode_password
        user.email = email
        user.save()
    return render_template("register.html")


@app.route("/login/", methods=["GET", "POST"])
@csrf.exempt
def login():
    error_msg = ""
    if request.method == "POST":
        user_email = request.form.get("email")
        user_password = SetPassword(request.form.get("password"))
        user = User.query.filter_by(email=user_email).first()
        if user:
            if user_password == user.password:
                response = redirect("/index/")
                response.set_cookie("username", user.user_name)
                response.set_cookie("email", user.email)
                response.set_cookie("id", str(user.id))
                session["username"] = user.user_name
                return response
            else:
                error_msg = "密码错误"
        else:
            error_msg = "用户不存在，请重新输入或注册"
    return render_template("login.html", error=error_msg)


@app.route("/logout/")
def logout():
    response = redirect("/login/")
    response.delete_cookie("username")
    response.delete_cookie("id")
    response.delete_cookie("id")
    del session["username"]
    return response


@app.route("/forgot_password/")
def forgt_password():
    return render_template("forgot-password.html")


@app.route("/leave/", methods=["GET", "POST"])
@loginValid
def leave():
    if request.method == "POST":
        request_name = request.form.get("request_name")
        request_type = request.form.get("request_type")
        request_start_time = request.form.get("start_tiame")
        request_end_time = request.form.get("end_tiame")
        request__phone = request.form.get("phone")
        request_description = request.form.get("request_description")

        leaves = Leave()
        leaves.request_name = request_name
        leaves.request_type = request_type
        leaves.request_start_time = request_start_time
        leaves.request_end_time = request_end_time
        leaves.request__phone = request__phone
        leaves.request_description = request_description
        leaves.request_id = request.cookies.get("id")
        leaves.request_static = "0"
        leaves.save()
        return redirect("/leaves_list/1/")
    return render_template("leave.html")



@app.route("/leaves_list/<int:page>/")
@loginValid
def leaves_list(page,):
    page-=1
    page_num=5
    user_id=int(request.cookies.get("id"))#获取登录者的id
    # leaves=Leave.query.filter_by(request_id=user_id)#根据id查找找该用户的所有请假数据
    all_data=len(Leave.query.all())
    b=(all_data+page_num-1)//page_num
    lis=[]
    for i in range(1,b+1):
        lis.append(i)
    leave_page=Leave.query.filter_by(request_id=user_id).offset(page*page_num).limit(page_num)
    return render_template("leaves_list.html",**locals())


@app.route("/add_task/",methods=["GET","POST"])
def add_task():
    task=Task()
    if task.validate_on_submit():
        formData=task.data
    else:
        errors_list=list(task.errors.keys())
        errors=task.errors
        print(errors)
    return render_template("add_task.html",**locals())

@app.route("/cancel/",methods=["GET","POST"])
@csrf.exempt
def cancel():
    # data1 = request.args
    # data2 = request.data
    # data3 = request.form
    id = request.form.get("id") #通过args接受get请求数据
    leave = Leave.query.get(int(id))
    leave.delete()
    return jsonify({"data":"删除成功"}) #返回json数据

@app.route("/picture/",methods=["GET","POST"])
def picture():
    if request.method=="POST":
        file=request.files.get("photo")
        file_name=file.filename
        file_path="img/%s"%file_name
        save_path=os.path.join(STATICFILES_DIR,file_path)
        file.save(save_path)

        p=Picture()
        p.picture=file_path
        p.save()
    return render_template("picture.html",**locals())

#定义API
@api.resource("/Api/leave/")
class LeaveApp(Resource):
    def __init__(self):
        """
        定义返回格式
        """
        super(LeaveApp, self).__init__()
        self.result={
            "version":"1.0",
            "data":""
        }
    def set_data(self,leave):
        """
        定义返回数据
        """
        result_data={
            "resquest_name":leave.request_name,
            "request_type":leave.request_type,
            "request_start_time":leave.request_start_time,
            "request_end_time":leave.request_end_time,
            "request_description":leave.request_description,
            "request_phone":leave.request__phone,
        }
        return result_data

    def get(self):
        """
        处理get请求
        """
        data=request.args
        id=data.get("id")
        if id:
            leave=Leave.query.get(int(id))
            result_data=self.set_data(leave)
        else:
            leaves=Leave.request.all()
            result_data=[]
            for leave in leaves:
                result_data.append(self.set_data(leave))
        self.result["data"]=result_data
        return self.result