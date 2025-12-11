import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO products (name, image, price, description) VALUES (?, ?, ?, ?)",
            ('Product 1', 'images/product1.jpg', 10.00, 'This is a short description for product 1.')
            )

cur.execute("INSERT INTO products (name, image, price, description) VALUES (?, ?, ?, ?)",
            ('Product 2', 'images/product2.jpg', 20.00, 'This is a short description for product 2.')
            )

cur.execute("INSERT INTO products (name, image, price, description) VALUES (?, ?, ?, ?)",
            ('Product 3', 'images/product3.jpg', 30.00, 'This is a short description for product 3.')
            )

connection.commit()
connection.close()
