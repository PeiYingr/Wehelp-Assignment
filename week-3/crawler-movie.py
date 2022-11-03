#　要求二：Python 網頁爬取資料並儲存到檔案中 (Optional)
#抓取 PTT 電影版的網頁原始碼(HTML)
# 利用內建的模組套件request建立網路連線
import urllib.request as req
movie=[]
def getData(url):
    # url="https://www.ptt.cc/bbs/movie/index.html"
    # 建立一個 request 物件, 附加 Request Headers 的資訊(User-Agent!)
    request=req.Request(url, headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    })
    # 利用 request 物件打開網址，取得網站的原始碼(HTML、CSS、JS)放置變數data中
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    #print(data)    

    # 解析原始碼, 取得每篇文章的標題
    # 載入BeautifulSoup4套件，做解析
    import bs4
    # 讓 BeautifulSoup 協助我們解析 HTML 格式文件
    moviepage=bs4.BeautifulSoup(data, "html.parser")
    # BeautifulSoup中的工具find_all ，可以從網頁中尋找所有符合篩選條件的標籤【find_all ("要找的標籤名稱", 篩選條件)】
    movietitles=moviepage.find_all("div", class_="title")
    # 用for迴圈把標題一個一個從列表抓出來
    for title in movietitles:
        if title.a != None:
        #「!=」 是「不等於」的意思! ( 如果a標籤不等於none的話，印出來)
            comment=title.a.string[0:4]
            if comment=="[好雷]":
                movie.append(title.a.string)
            if comment=="[普雷]":
                movie.append(title.a.string)
            if comment=="[負雷]":
                movie.append(title.a.string)
    # 抓取上一頁(接下來的頁面)的連結
    netLink=moviepage.find("a",string="‹ 上頁") # 找到內文是 ‹ 上頁 的 a標籤
    return netLink["href"]        
# 主程式: 抓取多個頁面的標題
pageurl="https://www.ptt.cc/bbs/movie/index.html"
page=0
while page<10:
    pageurl="https://www.ptt.cc"+getData(pageurl)
    page+=1
print(movie)

with open("movie.txt", mode="w", encoding="utf-8") as file:
    for one in movie:
        if one[0:4]=="[好雷]":
            file.write(one+"\n")
    for one in movie:
        if one[0:4]=="[普雷]":
            file.write(one+"\n") 
    for one in movie: 
        if one[0:4]=="[負雷]":
            file.write(one+"\n")

    #另一寫法
    # arr=["[好雷]","[普雷]","[負雷]"]
    # for x in arr:
    #    for one in movie:
    #     if one[0:4]==x:
    #         file.write(one+"\n")
