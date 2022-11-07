# !/usr/bin/python
# coding:utf-8

from flask import Flask, request, redirect, render_template, session, url_for
import mysql.connector

app = Flask(__name__,static_folder="static",static_url_path="/")
app.secret_key="any string but secret"

#例外處理 ( try、except )
def db_connection():
    mydb = None
    try:
        mydb = mysql.connector.connect(
        host = "localhost",
        port = 3306,
        user = "root",
        database = "db_1105",
        password = "",
        charset = "utf8"
        )
    except mysql.connector.Error as e:
        print(e)
    return mydb

@app.route("/")
def index():
    return render_template("index.html")

#註冊
@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]
    sql = """
    SELECT * FROM member WHERE username = %s;
    """
    data = (username, )
    mydb = db_connection()
    mycursor = mydb.cursor()
    mycursor.execute(sql, data)
    row = mycursor.fetchone()

    if name == "" or username == "" or password == "":
        return redirect(url_for("error", message = "請重新輸入"))
    elif row:
        return redirect(url_for("error", message = "帳號已經被註冊"))
    else:
        sql = """
        INSERT INTO member (name, username, password) VALUES (%s, %s, %s)
            """
        data = (name, username, password)
        mycursor.execute(sql, data)
        mydb.commit()
        return redirect("/")

#登入
@app.route("/signin", methods=["POST"])
def signin():
    username = request.form["username"]
    password = request.form["password"]
    sql = """
        SELECT * FROM member WHERE username = %s AND password = %s
    """
    data = (username, password)
    mydb = db_connection()
    mycursor = mydb.cursor()
    mycursor.execute(sql, data)
    row = mycursor.fetchone()

    if row:
        session["name"] = row[1]
        session["username"] = username
        session["password"] = password
        return redirect("/member")
    elif username == "" or password == "":
        return redirect(url_for("error", message = "請確認後重新填寫"))
    else:
        return redirect(url_for("error", message = "帳號或密碼輸入錯誤"))

#登入成功會員頁
@app.route("/member")
def member():
    if "username" in session:
        #將名字取出放到變數內
        name = session["name"]
        return render_template("member.html", name = name)
    else:
        return redirect("/")

#登入失敗
@app.route("/error")
def error():
    error=request.args.get("message", "")
    return render_template("error.html", message = error)

#登出
@app.route("/signout")
def signout():
    session.pop("username", None)
    return redirect('/')


@app.route("/api/member", methods = ['GET', 'PATCH'])
def api_member():
    if request.method == 'GET':
        username = request.args.get("username")
        mydb = db_connection()
        mycursor = mydb.cursor()
        sql = """
            SELECT id, name, username FROM member WHERE username = %s;
        """
        val = (username, )
        mycursor.execute(sql, val)
        num = mycursor.fetchone()
        if num:
            return {"data": {
                "id": num[0],
                "name": num[1],
                "username": num[2]
                }
            }
        else:
            return {"data": None}
    
    if request.method == 'PATCH':
        if "username" in session:
            new_name = request.get_json(request.data)
            username = session["username"]
            sql = """
                UPDATE member SET name = %s WHERE username = %s
            """
            val = (new_name["name"], username, )
            mydb = db_connection()
            mycursor = mydb.cursor()
            mycursor.execute(sql, val)
            mydb.commit()
            return {"ok": true }
        else:
            return {"error": true }


if __name__ == "__main__":
    app.run(port = 3000, debug=True)
