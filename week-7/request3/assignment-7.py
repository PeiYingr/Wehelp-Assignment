# 載入 Flask 所有相關的工具
from flask import Flask, request, render_template,redirect, session, jsonify, make_response 
import json
import mysql.connector
# websitedb=mysql.connector.connect(user='root', 
#                                 password='',
#                                 host='127.0.0.1',
#                                 database='website')
# cursor=websitedb.cursor()

websitedb = {
    "user":"root",
    "password":"",
    "host":"127.0.0.1",
    "database":"website",
}
# create connection pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name = "wehelp_pool",
    pool_size = 5,
    pool_reset_session = True,
    **websitedb
)

# 建立 Application 物件
app=Flask(__name__,static_folder="assignment-7", static_url_path="/")
# 設定 session 的密鑰
app.secret_key=" any string but secret "  
# app.config["JSON_AS_ASCII"] = False  # json格式的中文資料會以 ASCII 編碼顯示的解決辦法


# 使用 GET 方法(沒有特別寫method)，處理路徑 / 的對應函式
@app.route("/")
def home():
        return  render_template("home.html")

@app.route("/signup",methods=["POST"])
def signup():
    # 接收 POST 方法的 Query String
    name=request.form["name"]
    count=request.form["count"]
    key=request.form["key"]
    try:
        connection_object = connection_pool.get_connection()
        cursor =  connection_object.cursor()
        query=("SELECT username FROM member WHERE username=%s")
        cursor.execute(query, (count,))
        result = cursor.fetchone()
        if result!=None: # 其實跟寫 if result一樣(都是True)
            return redirect("/error?message=帳號已經被註冊")
        else:
            add_member="INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
            newdata=(name, count, key)
            cursor.execute(add_member, newdata)
            connection_object.commit()
            return  render_template("home.html")
    finally:
        cursor.close()
        connection_object.close()

@app.route("/signin",methods=["POST"])
def signin():
    # 接收 POST 方法的 Query String
    count=request.form["count"]
    key=request.form["key"]
    try:
        connection_object = connection_pool.get_connection()
        cursor =  connection_object.cursor()
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
    finally:
        cursor.close()
        connection_object.close()

@app.route("/member")
def member():
    if "username" not in session:
           return redirect("/")
    else:
        try:
            connection_object = connection_pool.get_connection()
            cursor =  connection_object.cursor()
            query=("SELECT member.name, message.content FROM member INNER JOIN message ON member.id=message.member_id ORDER BY message.time;")
            cursor.execute(query)
            result = cursor.fetchall()
            name=session["name"]
            return render_template("member.html",nametext=name,result=result)
        finally:
            cursor.close()
            connection_object.close()

@app.route("/message",methods=["POST"])
def message():
    message=request.form["messagecontent"]    
    id=session["id"]
    try:
        connection_object = connection_pool.get_connection()
        cursor =  connection_object.cursor()
        add_message="INSERT INTO message(member_id, content) VALUES (%s, %s)"
        newmessage=(id, message) 
        cursor.execute(add_message, newmessage)
        connection_object.commit()
        return  redirect("/member")
    except:
        print("Unexpected Error")
    finally:
        cursor.close()
        connection_object.close()


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

# 要求⼀：後端建立查詢會員資料的 API
@app.route("/api/member")
def api_member():
    username=request.args.get("username", "")
    try:
        connection_object = connection_pool.get_connection()
        cursor =  connection_object.cursor()
        query=("SELECT id, name, username FROM member where username=%s")
        cursor.execute(query,(username,))
        result_api = cursor.fetchone()
        if "username" in session and result_api!=None:       
            response_json={
                "data":{
                    "id" :result_api[0], 
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
    except:
        response_null={"data": None}
        response=jsonify(response_null)
        return response
    finally:
        cursor.close()
        connection_object.close()

# 要求三：完成修改姓名的功能
@app.route("/api/member",methods=["PATCH"])
def api_member_update():
    try:
        connection_object = connection_pool.get_connection()
        cursor =  connection_object.cursor()
        if "username" in session:
            front_request=request.get_json()
            username=session["username"]
            update_name="UPDATE member SET name=%s WHERE username=%s"
            update=(front_request["name"], username) 
            cursor.execute(update_name, update)
            connection_object.commit()
            response_ok={"ok":True}
            response=make_response(jsonify(response_ok), 200)
            return response
        else:
            response_error={"error":True}
            response=make_response(jsonify(response_error), 400)
            return response
    except:
        response_error={"error":True}
        response=make_response(jsonify(response_error), 400)
        return response
    finally:
        cursor.close()
        connection_object.close()
        
# 啟動網站伺服器，可透過 port 參數指定埠號
app.run(port=3000)
