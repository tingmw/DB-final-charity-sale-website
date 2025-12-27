import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, session
import json
from werkzeug.utils import secure_filename
import markdown
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        file = request.files.get('image')
        price = request.form['price']
        description = request.form['description']
        
        image_filename = None

        if not name:
            flash('Name is required!')
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filename = 'images/' + filename
        else:
            flash('Image file is required or file type is not allowed!')
            return render_template('add.html')

        if name and image_filename:
            conn = get_db_connection()
            conn.execute('INSERT INTO products (name, image, price, description) VALUES (?, ?, ?, ?)',
                         (name, image_filename, price, description))
            conn.commit()
            conn.close()
            return redirect(url_for('products'))

    return render_template('add.html')

@app.route('/edit/<int:product_id>', methods=('GET', 'POST'))
def edit(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    
    all_products = conn.execute('SELECT id, name FROM products ORDER BY name').fetchall()
    
    conn.close()

    if request.method == 'POST':
        name = request.form['name']
        new_file = request.files.get('image')
        price = request.form['price']
        description = request.form['description']
        
        image_filename = product['image'] 
        
        if new_file and new_file.filename != '' and allowed_file(new_file.filename):
            filename = secure_filename(new_file.filename)
            new_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filename = 'images/' + filename     

        if not name:
            flash('Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE products SET name = ?, image = ?, price = ?, description = ?'
                         ' WHERE id = ?',
                         (name, image_filename, price, description, product_id))
            conn.commit()
            conn.close()
            return redirect(url_for('products'))

    return render_template('edit.html', product=product, all_products=all_products)

@app.route('/delete/<int:product_id>', methods=('POST',))
def delete(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('products'))

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    p_id = str(product_id)
    if p_id in cart:
        cart[p_id] += quantity
    else:
        cart[p_id] = quantity
    
    session['cart'] = cart
    flash('商品已加入購物車！')
    return redirect(url_for('products'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'cart' not in session or not session['cart']:
        flash('購物車是空的，快去逛逛吧！')
        return redirect(url_for('products'))

    conn = get_db_connection()
    cart_items = []
    grand_total = 0
    
    for p_id, qty in session['cart'].items():
        product = conn.execute('SELECT * FROM products WHERE id = ?', (int(p_id),)).fetchone()
        if product:
            item_total = product['price'] * qty
            grand_total += item_total
            cart_items.append({'info': product, 'quantity': qty, 'total': item_total})

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        order_details = json.dumps([{'name': i['info']['name'], 'qty': i['quantity']} for i in cart_items])
        
        conn.execute('INSERT INTO orders (customer_name, customer_phone, customer_email, customer_address, order_items, total_price) VALUES (?, ?, ?, ?, ?, ?)',
                     (name, phone, email, address, order_details, grand_total))
        conn.commit()
        conn.close()
        
        session.pop('cart', None)
        return redirect(url_for('payment'))

    conn.close()
    return render_template('checkout.html', items=cart_items, total=grand_total)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template('payment.html')

if __name__ == '__main__':
    app.run(debug=True)
