import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
import markdown

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products LIMIT 3').fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/products')
def products():
    search = request.args.get('search')
    conn = get_db_connection()
    if search:
        products = conn.execute('SELECT * FROM products WHERE name LIKE ?', ('%' + search + '%',)).fetchall()
    else:
        products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()

    description_html = markdown.markdown(product['description'])   # markdown

    return render_template('product.html', product=product, description_html=description_html)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        image = request.form['image']
        price = request.form['price']
        description = request.form['description']

        if not name:
            flash('Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO products (name, image, price, description) VALUES (?, ?, ?, ?)',
                         (name, image, price, description))
            conn.commit()
            conn.close()
            return redirect(url_for('products'))

    return render_template('add.html')

@app.route('/edit/<int:product_id>', methods=('GET', 'POST'))
def edit(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()

    if request.method == 'POST':
        name = request.form['name']
        image = request.form['image']
        price = request.form['price']
        description = request.form['description']

        if not name:
            flash('Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE products SET name = ?, image = ?, price = ?, description = ?'
                         ' WHERE id = ?',
                         (name, image, price, description, product_id))
            conn.commit()
            conn.close()
            return redirect(url_for('products'))

    return render_template('edit.html', product=product)

@app.route('/delete/<int:product_id>', methods=('POST',))
def delete(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    flash('Product was successfully deleted!')
    return redirect(url_for('products'))

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template('payment.html')

if __name__ == '__main__':
    app.run(debug=True)
