# 載入 Flask 所有相關的工具
from email import message
from flask import Flask # 載入 Flask
from flask import request # 載入 Request 物件
from flask import render_template # 載入 render_template 函式
from flask import redirect
from flask import url_for
# 建立 Application 物件
app=Flask(__name__,static_folder="assignment-4", static_url_path="/")

# 使用 GET 方法(沒有特別寫method)，處理路徑 / 的對應函式
@app.route("/")
def home():
    return  render_template("home.html")

@app.route("/signin",methods=["POST"])
def signin():
    # 接收 POST 方法的 Query String
    count=request.form["count"]
    key=request.form["key"]
    if count=="" or key=="":
        return redirect("/error?message=請輸入帳號、密碼")
    elif count=="test" and key=="test":
        return redirect("/member")
    else:   
        return redirect("/error?message=帳號或密碼輸入錯誤")

@app.route("/member")
def member():
    return  render_template("member.html")

@app.route("/error")
def error():
    text=request.args.get("message","")
    return  render_template("error.html",message=text)

# 啟動網站伺服器，可透過 port 參數指定埠號
app.run(port=3000)