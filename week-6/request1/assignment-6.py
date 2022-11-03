
# 載入 Flask 所有相關的工具
from flask import Flask # 載入 Flask
from flask import request # 載入 Request 物件
from flask import render_template # 載入 render_template 函式
from flask import redirect
from flask import url_for
from flask import session # 載入 session 工具
import mysql.connector
import mysql.connector
memberdb=mysql.connector.connect(user='root', 
                                password='',
                                host='127.0.0.1',
                                database='website')
cursor=memberdb.cursor()

# 建立 Application 物件
app=Flask(__name__,static_folder="assignment-6", static_url_path="/")
# 設定 session 的密鑰
app.secret_key=" any string but secret "  

# 使用 GET 方法(沒有特別寫method)，處理路徑 / 的對應函式
@app.route("/")
def home():
        return  render_template("home.html")

@app.route("/signin",methods=["POST"])
def signin():
    # 接收 POST 方法的 Query String
    count=request.form["count"]
    key=request.form["key"]
    # query 會以 tuple 形式呈現
    query=("SELECT name, username, password FROM member WHERE username=%s")
    cursor.execute(query, (count,))
    result = cursor.fetchone()

    if count=="" or key=="":
        return redirect("/error?message=請輸入帳號、密碼")
    elif count==result[1] and key==result[2]:
        session["username"]=count
        session["name"]=result[0]
        return redirect("/member")
    else:   
        return redirect("/error?message=帳號或密碼輸入錯誤")

@app.route("/member")
def member():
    if "username" not in session:
           return redirect("/")
    name=session["name"]
    return render_template("member.html",nametext=name)

@app.route("/error")
def error():
    text=request.args.get("message","")
    return render_template("error.html",message=text)

@app.route("/signout")
def signout():
    # 移除session中的username(count)
    session.pop("username", None)
    return redirect(url_for("home"))

# 啟動網站伺服器，可透過 port 參數指定埠號
app.run(port=3000)

cursor.close()
memberdb.close()