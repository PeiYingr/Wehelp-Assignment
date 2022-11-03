# 載入 Flask 所有相關的工具
from flask import Flask # 載入 Flask
from flask import request # 載入 Request 物件
from flask import render_template # 載入 render_template 函式

# 建立 Application 物件
app=Flask(__name__,static_folder="assignment-4", static_url_path="/")

# 使用 GET 方法(沒有特別寫method)，處理路徑 / 的對應函式
@app.route("/")
def home():
    return  render_template("home.html")

# 啟動網站伺服器，可透過 port 參數指定埠號
app.run(port=3000)