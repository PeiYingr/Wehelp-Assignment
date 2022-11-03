
# 載入 Flask 所有相關的工具
from flask import * # * 代表載入全部的物件、函式、工具

from mysql.connector import pooling
connection_pool = pooling.MySQLConnectionPool(pool_name="member_pool",
                                      pool_size=10,
                                      pool_reset_session=True,
                                      host='127.0.0.1',
                                      database='website',
                                      user='root',
                                      password='')
  
websitedb = connection_pool.get_connection() # 從連接池中獲取 Connection 對象
# websitedb=mysql.connector.connect(user='root', 
#                                 password='',
#                                 host='127.0.0.1',
#                                 database='website')

#! 老師建議 cursor 不要共用，應該要在每個route去抓一次，因為如果共用，同時有兩個route取抓資料跑的話會出現錯誤
# cursor=websitedb.cursor()

# 建立 Application 物件
app=Flask(__name__,static_folder="assignment-6", static_url_path="/")
# 設定 session 的密鑰
app.secret_key=" any string but secret "  

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

    cursor=websitedb.cursor()
    query=("SELECT username FROM member WHERE username=%s")
    cursor.execute(query, (count,))
    result = cursor.fetchone()
    if result!=None:
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

    cursor=websitedb.cursor()
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
        cursor=websitedb.cursor()
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
    cursor=websitedb.cursor()
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

# 啟動網站伺服器，可透過 port 參數指定埠號
app.run(port=3000)
cursor=websitedb.cursor()
cursor.close()
websitedb.close()