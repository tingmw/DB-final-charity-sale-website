import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

des1 = '''
## 產品描述
以天然植物油為基底，手工冷製而成的植萃香皂。
不添加人工色素與刺激性成分，泡沫細緻溫和，適合日常清潔使用。
每一塊香皂皆為手工製作，外觀與色澤略有不同，正是手作獨一無二的證明。

---

## 產品特色
手工冷製，保留天然油脂滋潤感
植物油基底，洗後不乾澀
無添加人工色素
適合一般膚質使用
義賣商品，收益將用於公益用途

---

## 規格資訊
重量：約 90g ± 10g
保存期限：約 12 個月
產地：台灣手工製作
'''

des2 = '''
## 產品描述
以厚實耐用的帆布材質製作，適合日常外出、購物或上課使用。
簡約設計搭配實用容量，可輕鬆收納書籍、文件或隨身物品。
重複使用的帆布袋，為生活帶來便利，也為環境減少負擔。

---

## 產品特色
- 厚磅帆布材質，耐用不易變形
- 可重複使用，環保友善
- 大容量設計，適合日常攜帶
- 簡約風格，男女皆適合
- 義賣商品，收益將用於公益用途

---

## 規格資訊
尺寸：約 35 x 40 cm  
材質：棉質帆布  
產地：台灣設計製作
'''

des3 = '''
## 產品描述
選用簡單天然的原料，低糖配方製作的手工烘焙餅乾。
口感酥脆不膩，適合作為下午茶或日常小點心。
每一份餅乾皆為少量製作，保留手工烘焙的溫度與風味。

---

## 產品特色
- 手工烘焙，非大量生產
- 原料單純，低糖配方
- 無添加人工香料與色素
- 適合搭配茶飲或咖啡
- 義賣商品，收益將用於公益用途

---

## 規格資訊
內容量：約 120g  
保存期限：約 30 天  
產地：台灣手工製作
'''


cur.execute("INSERT INTO products (name, image, price, description) VALUES (?, ?, ?, ?)",
            ('手工香皂', 'images/product1.jpg', 180, des1)
            )

cur.execute("INSERT INTO products (name, image, price, description) VALUES (?, ?, ?, ?)",
            ('環保帆布袋', 'images/product2.jpg', 220.00, des2)
            )

cur.execute("INSERT INTO products (name, image, price, description) VALUES (?, ?, ?, ?)",
            ('手工烘焙餅乾', 'images/product3.jpg', 130.00, des3)
            )

connection.commit()
connection.close()
