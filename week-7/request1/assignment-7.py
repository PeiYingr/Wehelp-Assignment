
# 載入 Flask 所有相關的工具
from flask import Flask, request, render_template,redirect, session, jsonify
import json
import mysql.connector
websitedb=mysql.connector.connect(user='root', 
                                password='',
                                host='127.0.0.1',
                                database='website')
cursor=websitedb.cursor()
  
# 建立 Application 物件
app=Flask(__name__,static_folder="assignment-7", static_url_path="/")
# 設定 session 的密鑰
app.secret_key=" any string but secret "  
# app.config["JSON_AS_ASCII"] = False  # json格式的中文資料會以 ASCII 編碼顯示的解決辦法


# 使用 GET 方法(沒有特別寫method)，處理路徑 / 的對應函式
@app.route("/")
def home():
        return render_template("home.html")

@app.route("/signup",methods=["POST"])
def signup():
    # 接收 POST 方法的 Query String
    name=request.form["name"]
    count=request.form["count"]
    key=request.form["key"]

    query=("SELECT username FROM member WHERE username=%s")
    cursor.execute(query, (count,))
    result = cursor.fetchone()
    if result!=None: # 其實跟寫 if result一樣(都是True)
        return redirect("/error?message=帳號已經被註冊")
    else:
        add_member="INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
        newdata=(name, count, key)
        cursor.execute(add_member, newdata)
        websitedb.commit()
        return  render_template("home.html")

@app.route("/signin",methods=["POST"])
def signin():
    # 接收 POST 方法的 Query String
    count=request.form["count"]
    key=request.form["key"]
    # query 會以 tuple 形式呈現
    query=("SELECT name, username, password, id FROM member WHERE username=%s")
    cursor.execute(query, (count,))
    result = cursor.fetchone()
    if count=="" or key=="":
        return redirect("/error?message=請輸入帳號、密碼")
    elif count==result[1] and key==result[2]:
        session["username"]=result[1]
        session["name"]=result[0]
        session["id"]=result[3]
        return redirect("/member")
    else:   
        return redirect("/error?message=帳號或密碼輸入錯誤")

@app.route("/member")
def member():
    if "username" not in session:
           return redirect("/")
    else:
        query=("SELECT member.name, message.content FROM member INNER JOIN message ON member.id=message.member_id ORDER BY message.time;")
        cursor.execute(query)
        result = cursor.fetchall()
        name=session["name"]
        return render_template("member.html",nametext=name,result=result)

@app.route("/message",methods=["POST"])
def message():
    message=request.form["messagecontent"]    
    id=session["id"]
    add_message="INSERT INTO message(member_id, content) VALUES (%s, %s)"
    newmessage=(id, message) 
    cursor.execute(add_message, newmessage)
    websitedb.commit()
    return  redirect("/member")

@app.route("/error")
def error():
    text=request.args.get("message","")
    return render_template("error.html",message=text)

@app.route("/signout")
def signout():
    # 移除session中的username(count)
    session.pop("username")
    session.pop("name")
    session.pop("id")
    return redirect("/")

@app.route("/api/member")
def api_member():
    username=request.args.get("username", "")
    query=("SELECT id, name, username FROM member where username=%s")
    cursor.execute(query,(username,))
    result_api = cursor.fetchone()
    if "username" in session:   
        if result_api!=None:    
            response_json={
                "data":{
                    "id" : result_api[0], 
                    "name" : result_api[1],
                    "username" : result_api[2]
                }
            }
            # 把py的字典轉換為json格式
            # json.dumps僅是協助將字典或列表轉換為JSON的字串形式，Request Header的content-type會是text/html
            # response=json.dumps(response_json, ensure_ascii=False)
            # 使用 jsonify() 來處理回應的資訊，會把原本的數據序列化為 JSON ，並添加content-type為application/json標頭
            response=jsonify(response_json)
            return response 
        else:
            response_null={"data": result_api}
            response=jsonify(response_null)
            return response
    else:
        response_null={"data": result_api}
        response=jsonify(response_null)
        return response

# 啟動網站伺服器，可透過 port 參數指定埠號
app.run(port=3000)

cursor.close()
websitedb.close()