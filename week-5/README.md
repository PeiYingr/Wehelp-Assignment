# Week-5 Assignment
## (一) 要求三：SQL CRUD
### 利⽤要求⼆建立的資料庫和資料表，寫出能夠滿⾜以下要求的 SQL 指令：
#### 參考教學文件：W3Schools SQL Tutorial

* 使⽤ INSERT 指令新增⼀筆資料到 member 資料表中，這筆資料的 username 和 password 欄位必須是 test。接著繼續新增⾄少 4 筆隨意的資料。
```SQL
INSERT INTO member(name, username, password, follower_count) VALUES('彭彭老師', 'test', 'test', 114);
INSERT INTO member(name, username, password, follower_count) VALUES('丁滿', 'test2', 'test2', 10);
INSERT INTO member(name, username, password, follower_count) VALUES('辛巴', 'test3', 'test3', 15);
INSERT INTO member(name, username, password, follower_count) VALUES('娜娜', 'test4', 'test4', 20);
INSERT INTO member(name, username, password, follower_count) VALUES('刀疤', 'test5', 'test5', 25);
```
![要求三-1](https://user-images.githubusercontent.com/111441731/196763727-6fd2e1fc-fc5c-42d7-aee7-f86b6d97ffa7.JPG)

* 使⽤ SELECT 指令取得所有在 member 資料表中的會員資料。
```SQL
SELECT * FROM member;
```
![要求三-2](https://user-images.githubusercontent.com/111441731/196764696-60f80e37-f01f-4bfa-adbe-805ab13237e1.JPG)

* 使⽤ SELECT 指令取得所有在 member 資料表中的會員資料，並按照 time 欄位，由近到遠排序。
```SQL
SELECT * FROM member ORDER BY time DESC;
```
![要求三-3](https://user-images.githubusercontent.com/111441731/196765143-8022ed50-f1e6-4410-838c-72e2b3b0c484.JPG)

* 使⽤ SELECT 指令取得 member 資料表中第 2 ~ 4 共三筆資料，並按照 time 欄位，由近到遠排序。( 並非編號 2、3、4 的資料，⽽是排序後的第 2 ~ 4 筆資料 )
```SQL
SELECT * FROM member ORDER BY time DESC LIMIT 1, 3;
```
![要求三-4](https://user-images.githubusercontent.com/111441731/196765343-16b35a05-dd34-466c-95b4-4f750ac2cdad.JPG)

* 使⽤ SELECT 指令取得欄位 username 是 test 的會員資料。
```SQL
SELECT * FROM member WHERE username='test';
```
![要求三-5](https://user-images.githubusercontent.com/111441731/196765494-6353136a-6869-4efe-b1aa-c05eded4b785.JPG)

* 使⽤ SELECT 指令取得欄位 username 是 test、且欄位 password 也是 test 的資料。
```SQL
SELECT * FROM member WHERE username='test'and password='test';
```
![要求三-6](https://user-images.githubusercontent.com/111441731/196765657-c7c6db74-0869-4605-95fc-ce056bc68258.JPG)

* 使⽤ UPDATE 指令更新欄位 username 是 test 的會員資料，將資料中的 name 欄位改成 test2。
```SQL
UPDATE member SET name='test2' WHERE username='test';
```
![要求三-7](https://user-images.githubusercontent.com/111441731/196765866-9662ff58-d2d5-4254-828f-b443e1c30620.JPG)

---
## (二) 要求四：SQL Aggregate Functions
### 利⽤要求⼆建立的資料庫和資料表，寫出能夠滿⾜以下要求的 SQL 指令：

* 取得 member 資料表中，總共有幾筆資料 ( 幾位會員 )。
```SQL
SELECT COUNT(*) FROM member;
```
![要求四-1](https://user-images.githubusercontent.com/111441731/196766101-f2040701-2b4f-4a22-9746-25bbf6b7ad21.JPG)

* 取得 member 資料表中，所有會員 follower_count 欄位的總和。
```SQL
SELECT SUM(follower_count) FROM member;
```
![要求四-2](https://user-images.githubusercontent.com/111441731/196766176-017374dd-39c5-4de0-a38f-fe17a7ea2893.JPG)

* 取得 member 資料表中，所有會員 follower_count 欄位的平均數。
```SQL
SELECT AVG(follower_count) FROM member;
```
![要求四-3](https://user-images.githubusercontent.com/111441731/196766268-aea479d9-ac20-4d1b-bcc1-a47573a157a9.JPG)

---
## (三) 要求五：SQL JOIN
* 在資料庫中，建立新資料表紀錄留⾔資訊，取名字為 message。資料表中必須包含以下欄位設定：
![image](https://user-images.githubusercontent.com/111441731/196766442-c54105c5-9bd7-4872-b3fe-4fc97ee0f7d2.png)
```SQL
CREATE TABLE message(
id BIGINT PRIMARY KEY AUTO_INCREMENT,
member_id  BIGINT NOT NULL,
content VARCHAR(255) NOT NULL,
like_count INT UNSIGNED NOT NULL DEFAULT 0,
time DATETIME NOT NULL DEFAULT NOW(),
FOREIGN KEY(member_id) REFERENCES member(id)
);
```
![要求五-0](https://user-images.githubusercontent.com/111441731/196766754-0b53dfb0-84ee-40f9-9ac7-f09b5fa07096.JPG)

* 新增資料到 message 資料表中
```SQL
INSERT INTO message(member_id, content, like_count) VALUES('1', '作業這樣就可以了', 100);
INSERT INTO message(member_id, content, like_count) VALUES('1', '看起來沒什麼問題哦，很不錯呀', 150);
INSERT INTO message(member_id, content, like_count) VALUES('1', '基本的部份沒問題，這樣就可以了', 120);
INSERT INTO message(member_id, content, like_count) VALUES('1', '做得很好呀，我沒有其他問題', 150);
INSERT INTO message(member_id, content, like_count) VALUES('2', '騙妳的~', 200);
INSERT INTO message(member_id, content, like_count) VALUES('2', '納欸阿捏', 180);
INSERT INTO message(member_id, content, like_count) VALUES('3', '熊出沒，小心！', 180);
INSERT INTO message(member_id, content, like_count) VALUES('4', '最近有些村民養的雞被狐狸吃了', 300);
INSERT INTO message(member_id, content, like_count) VALUES('5', '請協助清除城鎮周圍的史萊姆', 165);
```
![要求五-0 1](https://user-images.githubusercontent.com/111441731/196766780-55abd910-6d8b-4547-99e0-0ddab43433b8.JPG)

* 取得所有在 message 資料表中的資料。
```SQL
SELECT * FROM message;
```
![要求五-0 2](https://user-images.githubusercontent.com/111441731/196766799-222e7670-dc92-4b92-adb9-d334c731086f.JPG)

* 使⽤ SELECT 搭配 JOIN 語法，取得所有留⾔，結果須包含留⾔者會員的姓名。
```SQL
SELECT member.name, message.content FROM member INNER JOIN message ON member.id=message.member_id;
```
![要求五-1](https://user-images.githubusercontent.com/111441731/196767700-7c0e7904-3076-422d-a93c-be3dfaee017e.JPG)

* 使⽤ SELECT 搭配 JOIN 語法，取得 member 資料表中欄位 username 是 test 的所有留⾔，資料中須包含留⾔者會員的姓名。
```SQL
SELECT member.name, message.content FROM member INNER JOIN message ON member.id=message.member_id WHERE username='test';
```
![要求五-2](https://user-images.githubusercontent.com/111441731/196767925-53c1bef5-b3a1-4678-88d9-60980008f355.JPG)

* 使⽤ SELECT、SQL Aggregate Functions 搭配 JOIN 語法，取得 member 資料表中欄位 username 是 test 的所有留⾔平均按讚數。
```SQL
SELECT AVG(like_count) FROM member INNER JOIN message ON member.id=message.member_id WHERE username='test';
```
![要求五-3](https://user-images.githubusercontent.com/111441731/196768142-e583ee0c-e341-4b1a-b748-a76408915f28.JPG)
