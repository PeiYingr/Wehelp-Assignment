# 要求一：Python 取得網路上的資料並儲存到檔案中
# 網路連線
from gc import collect
import urllib.request as request
import json
src="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json"
with request.urlopen(src) as response:
    data=json.load(response)    # 利用json模組處理json資料格式 
# 記得!!py把json資料讀取進來之後會是一個「字典」型態, data 是一個字典資料   
collection=data["result"]["results"] # 擷取results下一層的列表(值)

import csv
# 開啟輸出的CSV檔案
with open("data.csv", mode="w",newline="",encoding="utf-8") as csvfile:
#建立CSV檔寫入器
    write=csv.writer(csvfile)  # 設定write為寫入 data.csv檔案中(的動作?)
    for x in collection:       # 把景點一行一行寫入
        if x["xpostDate"][0:4]>="2015":
            photo=x["file"].split("https")
            all=(x["stitle"],x["address"][5:8],x["longitude"],x["latitude"],"https"+photo[1])
            write.writerow(all)