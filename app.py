#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime, re, os, random, json, urllib.parse, urllib.request
from flask import Flask, render_template, request, jsonify, session, abort, redirect, url_for, Response
import pymysql

app = Flask(__name__)
app.secret_key = os.urandom(24)

conn = pymysql.connect(host="127.0.0.1", user="chun", password="602661651nizhan$", database="speed", charset="utf8")


@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/login")
#     return redirect(url_for("login_handle"))


@app.route("/reg", methods=["GET", "POST"])
def reg_handle():
    if request.method == "GET":
        return render_template("reg.html")
    elif request.method == "POST":
        uname = request.form.get("uname")
        upass = request.form.get("upass")
        upass2 = request.form.get("upass2")
        phone = request.form.get("phone")
        email = request.form.get("email")

        if not (uname and uname.strip() and upass and upass2 and phone and email):
            abort(500)

        # if re.search(r"[\u4E00-\u9FFF]", uname):
        #     abort(Response("用户名含有中文汉字！"))

        if not re.fullmatch("[a-zA-Z0-9_]{4,20}", uname):
            abort(Response("用户名不合法！"))
        
        cur = conn.cursor()
        cur.execute("SELECT uid FROM user WHERE uname=%s", (uname,))
        res = cur.rowcount
        cur.close()      
        if res != 0:
            abort(Response("用户名已被注册！"))

        # 密码长度介于6-15
        if not (len(upass) >= 6 and len(upass) <= 15 and upass == upass2):
            abort(Response("密码错误！"))

        if not re.fullmatch(r"[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+", email):
            abort(Response("邮箱格式错误！"))

        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO user VALUES (default, %s, md5(%s), %s, %s, sysdate(), sysdate(), '1', '1')", (uname, uname + upass, phone, email))
            cur.close()
            conn.commit()
        except:
            abort(Response("用户注册失败！"))

        # session.pop(phone)
        # 注册成功就跳转到登录页面
        return redirect(url_for("login_handle"))


@app.route("/logout")
def logout_handle():
    res = {"err": 1, "desc": "未登录！"}
    if session.get("user_info"):
        session.pop("user_info")
        res["err"] = 0
        res["desc"] = "注销成功！"
    
    return jsonify(res)


@app.route("/login", methods=["GET", "POST"])
def login_handle():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        uname = request.form.get("uname")
        upass = request.form.get("upass")

        print(uname, upass)

        if not (uname and uname.strip() and upass and upass.strip()):
            abort(Response("登录失败！"))

        if not re.fullmatch("[a-zA-Z0-9_]{4,20}", uname):
            abort(Response("用户名不合法！"))

        # 密码长度介于6-15
        if not (len(upass) >= 6 and len(upass) <= 15):
            abort(Response("密码不合法！"))    
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE uname=%s and upass=md5(%s)", (uname, uname + upass))
        res = cur.fetchone()
        cur.close()
              
        if res:
            # 登录成功就跳转到用户个人中心
            cur_login_time = datetime.datetime.now()

            session["user_info"] = {
                "uid": res[0],
                "uname": res[1],
                "upass": res[2],
                "phone": res[3],
                "email": res[4],
                "reg_time": res[5],
                "last_login_time": res[6],
                "priv": res[7],
                "state": res[8],
                "cur_login_time": cur_login_time
            }

            try:
                cur = conn.cursor()
                cur.execute("UPDATE user SET last_login_time=%s WHERE uid=%s", (cur_login_time, res[0]))
                cur.close()
                conn.commit()
            except Exception as e:
                print(e)

            return redirect(url_for("user_center"))
        else:
            # 登录失败
            return render_template("index.html", login_fail=1)


@app.route("/check_uname")
def check_uname():
    uname = request.args.get("uname")
    if not uname:
        abort(500)

    res = {"err": 1, "desc": "用户名已被注册！"}

    cur = conn.cursor()
    cur.execute("SELECT uid FROM user WHERE uname=%s", (uname,))
    if cur.rowcount == 0:
        # 用户名没有被注册
        res["err"] = 0
        res["desc"] = "用户名没有被注册！"
    cur.close()

    return jsonify(res)


@app.route("/login_success", methods=["GET", "POST"])
def login_success():
    # if request.method == "GET":
    return render_template("index2.html")
    # elif request.method == "POST":


@app.route("/user_center")
def user_center():
    user_info = session.get("user_info")

    if user_info:
        return render_template("index2.html", uname=user_info.get("uname"))
    else:
        return redirect(url_for("login_handle"))


@app.route("/menu", methods=["GET", "POST"])
def menu_handle():
    if request.method == "GET":
        cur = conn.cursor()
        cur.execute("SELECT * from menu")
        rows = cur.fetchall()
        cur.close()        
        rows = list(rows)
        # 替换
        m = 0 
        while m < len(rows):
            rows[m] = list(rows[m])
            m += 1
        print(rows)
        for i in rows:
            n = i[-1].replace("/", "\\")
            i[-1] = n
        print(rows)
        return render_template("goods.html", menus=rows)

# 有问题
@app.route("/admin", methods=["GET", "POST"])
def admin_handle():
    if request.method == "GET":
        return render_template("admin.html")    


@app.route("/list")
def list_page():
    return render_template("map_listing.html")


if __name__ == "__main__":
    app.run(port=80, debug=True)


# blueprint