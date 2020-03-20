#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime, re, os, random, json, urllib.parse, urllib.request
from flask import Flask, render_template, request, jsonify, session, abort, redirect, url_for, Response
import pymysql
import flask
import json
import requests

app = Flask(__name__)
app.secret_key = b'\xa3P\x05\x1a\xf8\xc6\xff\xa4!\xd2\xb5\n\x96\x05\xed\xc3\xc90=\x07\x8d>\x8e\xeb'

conn = pymysql.connect(host="127.0.0.1", user="speed", password="itazhe123", database="speed", charset="utf8")


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
            abort(Response("请输入相关信息！"))

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

            print(session["user_info"]["priv"])

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
    
    if user_info.get("priv") == "2":
        print(user_info.get("priv"))
        return render_template("index2.html", uname=user_info.get("uname"))

    if user_info:
        return render_template("index4.html", uname=user_info.get("uname"))
    else:
        # return redirect(url_for("login_handle"))
        abort(Response("登录失败！"))


@app.route("/menu", methods=["GET", "POST"])
def menu_handle():
    if request.method == "GET":
        cur = conn.cursor()
        cur.execute("SELECT * from menu")
        rows = cur.fetchall()   

        cur2 = conn.cursor()
        cur2.execute("SELECT * from menu2")
        rows2 = cur2.fetchall()

        cur3 = conn.cursor()
        cur3.execute("SELECT * from menu3")
        rows3 = cur3.fetchall()

        cur4 = conn.cursor()
        cur4.execute("SELECT * from menu4")
        rows4 = cur4.fetchall()

        cur5 = conn.cursor()
        cur5.execute("SELECT * from menu5")
        rows5 = cur5.fetchall()
        # cur.close()   
        # cur2.close()

        # 进店必买
        rows = list(rows)
        # 替换
        m = 0 
        while m < len(rows):
            rows[m] = list(rows[m])
            m += 1
        print(rows)
        for i in rows:
            n = i[-1].replace("\\", "/")
            i[-1] = n
        print(rows)

        # 特色小吃
        rows2 = list(rows2)
        # 替换
        m = 0 
        while m < len(rows2):
            rows2[m] = list(rows2[m])
            m += 1
        print(rows2)
        for i in rows2:
            n = i[-1].replace("\\", "/")
            i[-1] = n
        print(rows2)

        # 零食
        rows3 = list(rows3)
        # 替换
        m = 0 
        while m < len(rows3):
            rows3[m] = list(rows3[m])
            m += 1
        print(rows3)
        for i in rows3:
            n = i[-1].replace("\\", "/")
            i[-1] = n
        print(rows3)

        # 酒水饮料
        rows4 = list(rows4)
        # 替换
        m = 0 
        while m < len(rows4):
            rows4[m] = list(rows4[m])
            m += 1
        print(rows4)
        for i in rows4:
            n = i[-1].replace("\\", "/")
            i[-1] = n
        print(rows4)

        # 其他服务
        rows5 = list(rows5)
        # 替换
        m = 0 
        while m < len(rows5):
            rows5[m] = list(rows5[m])
            m += 1
        print(rows5)
        for i in rows5:
            n = i[-1].replace("\\", "/")
            i[-1] = n
        print(rows5)

        return render_template("goods.html", menus=rows, menus2=rows2, menus3=rows3, menus4=rows4, menus5=rows5)



app.config["UPLOAD_FOLDER"] = r"static\img\image"

# basedir = os.path.abspath(os.path.dirname(__file__))


@app.route("/admin", methods=["GET", "POST"])
def admin_handle():
    if request.method == "GET":
        return render_template("admin.html")    
    elif request.method == "POST":
        # 进店必买
        try:
            menu_item_title = request.form.get("menu_item_title")
            menu_item_title_price = request.form.get("menu_item_title_price")  
            menu_item_description = request.form.get("menu_item_description")

            # print(menu_item_title, menu_item_title_price, menu_item_description)
            # 获取照片
            uploaded_file = flask.request.files["azhe"]
            file_name = uploaded_file.filename
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)

            s = ""
            for i in file_path:
                n = i.replace("\\", "/")
                s += n
            # print(s)
            file_path = s
            print(file_path)

            uploaded_file.save(file_path)

            if menu_item_title:
                try:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO menu VALUES (default, %s, %s, %s, %s)", (menu_item_title, menu_item_title_price, menu_item_description, file_path))
                    cur.close()
                    conn.commit()
                except:
                    abort(Response("菜品信息失败！"))
        except Exception as e:
            print(e)

        # 特色小吃
        try:
            menu_item_title = request.form.get("uname")
            menu_item_title_price = request.form.get("uprice")  
            menu_item_description = request.form.get("uinfor")

            # print(menu_item_title, menu_item_title_price, menu_item_description)
            # 获取照片
            uploaded_file = flask.request.files["yrz"]
            file_name = uploaded_file.filename
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
            s = ""
            for i in file_path:
                n = i.replace("\\", "/")
                s += n
            # print(s)
            file_path = s
            print(file_path)
            # print(file_path)
            uploaded_file.save(file_path)
            
            if menu_item_title:
                try:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO menu2 VALUES (default, %s, %s, %s, %s)", (menu_item_title, menu_item_title_price, menu_item_description, file_path))
                    cur.close()
                    conn.commit()
                except:
                    abort(Response("菜品信息失败！"))
        except Exception as e:
            print(e)

        # 零食
        try:
            menu_item_title = request.form.get("uname2")
            menu_item_title_price = request.form.get("uprice2")  
            menu_item_description = request.form.get("uinfor2")

            # print(menu_item_title, menu_item_title_price, menu_item_description)
            # 获取照片
            uploaded_file = flask.request.files["qwe"]
            file_name = uploaded_file.filename
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
            s = ""
            for i in file_path:
                n = i.replace("\\", "/")
                s += n
            # print(s)
            file_path = s
            print(file_path)
            # print(file_path)
            uploaded_file.save(file_path)

            if menu_item_title:
                try:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO menu3 VALUES (default, %s, %s, %s, %s)", (menu_item_title, menu_item_title_price, menu_item_description, file_path))
                    cur.close()
                    conn.commit()
                except:
                    abort(Response("菜品信息失败！"))
        except Exception as e:
            print(e)

        # 酒水饮料
        try:
            menu_item_title = request.form.get("uname3")
            menu_item_title_price = request.form.get("uprice3")  
            menu_item_description = request.form.get("uinfor3")

            # print(menu_item_title, menu_item_title_price, menu_item_description)
            # 获取照片
            uploaded_file = flask.request.files["asd"]
            file_name = uploaded_file.filename
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
            s = ""
            for i in file_path:
                n = i.replace("\\", "/")
                s += n
            # print(s)
            file_path = s
            print(file_path)
            # print(file_path)
            uploaded_file.save(file_path)

            if menu_item_title:
                try:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO menu4 VALUES (default, %s, %s, %s, %s)", (menu_item_title, menu_item_title_price, menu_item_description, file_path))
                    cur.close()
                    conn.commit()
                except:
                    abort(Response("菜品信息失败！"))
        except Exception as e:
            print(e)

        # 其他服务
        try:
            menu_item_title = request.form.get("uname4")
            menu_item_title_price = request.form.get("uprice4")  
            menu_item_description = request.form.get("uinfor4")

            # print(menu_item_title, menu_item_title_price, menu_item_description)
            # 获取照片
            uploaded_file = flask.request.files["zxc"]
            file_name = uploaded_file.filename
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
            s = ""
            for i in file_path:
                n = i.replace("\\", "/")
                s += n
            # print(s)
            file_path = s
            print(file_path)
            # print(file_path)
            uploaded_file.save(file_path)

            if menu_item_title:
                try:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO menu5 VALUES (default, %s, %s, %s, %s)", (menu_item_title, menu_item_title_price, menu_item_description, file_path))
                    cur.close()
                    conn.commit()
                except:
                    abort(Response("菜品信息失败！"))
        except Exception as e:
            print(e)

        # 下架
        try:
            menu_item_title = request.form.get("uname5")
            menu_item_title_price = request.form.get("uprice5")  

            print(menu_item_title, menu_item_title_price)
            if menu_item_title == '进店必买':
                menu_item_title = "menu"
                print(menu_item_title)
            elif menu_item_title == "特色小吃":
                menu_item_title = "menu2"
                print(menu_item_title)
            elif menu_item_title == "零食":
                menu_item_title = "menu3"
            elif menu_item_title == "酒水饮料":
                menu_item_title = "menu4"
            elif menu_item_title == "其他服务":
                menu_item_title = "menu5"
            else:
                abort(Response("请输入正确的种类！！！"))


            try:
                cur = conn.cursor()
                cur.execute("delete from %s where fname='%s'" %  (menu_item_title, menu_item_title_price))
                cur.close()
                conn.commit()
            except:
                abort(Response("菜品下架失败！"))
        except Exception as e:
            print(e)
               
        return render_template("admin.html")


@app.route("/cart", methods=["GET", "POST"])
def cart_handle():
    if request.method == "GET":
        return render_template("cart.html")


@app.route("/about")
def about_handle():
    return render_template("about.html")


@app.route("/garbage", methods=["GET", "POST"])
def garbage_handle():
    if request.method == "GET":
        return render_template("garbage.html")
    elif request.method == "POST":
        uinput = request.form.get("input")
        print(uinput)

        # laji = input("\n请输入垃圾：")
        url = "http://apis.juhe.cn/rubbish/search?q=%s&key=3113b4933f324070f50905bbf0670d77" % uinput
        rsp = requests.get(url).text
        print(rsp)

        rsp = json.loads(rsp)
        garbage = rsp["result"]

        return render_template("garbage.html", garbages=garbage)

        
@app.route("/cart2")
def cart2_handle():
    return render_template("cart_2.html")

@app.route("/cart3")
def cart3_handle():
    return render_template("cart_3.html")


@app.route("/message_board", methods=["GET", "POST"])
def message_board_handle():
    if request.method == "GET":
        cur = conn.cursor()
        cur.execute("SELECT uname, pub_time, content, cid FROM user, message WHERE user.uid = message.uid")
        res = cur.fetchall()
        cur = conn.cursor()
        cur.execute("SELECT * from message")
        num = cur.rowcount
        cur.close()        
        
        return render_template("detail_page_2.html", messages=res, number=num)
    elif request.method == "POST":
        user_info = session.get("user_info")
        if not user_info:
            abort(Response("未登录！"))

        content = request.form.get("content")
        if content:
            content = content.strip()
            if 0 < len(content) <= 200:
                # 将留言保存到数据库
                uid = user_info.get("uid")
                pub_time = datetime.datetime.now()
                from_ip = request.remote_addr

                try:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO message (uid, content, pub_time, from_ip) VALUES (%s, %s, %s, %s)", (uid, content, pub_time, from_ip))
                    cur.close()
                    conn.commit()
                    return redirect(url_for("message_board_handle"))
                except Exception as e:
                    print(e)
                    
        abort(Response("留言失败！"))


if __name__ == "__main__":
    app.run(host= "0.0.0.0", port=3333, debug=True)


# blueprint