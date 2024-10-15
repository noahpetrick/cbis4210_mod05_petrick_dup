from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

products = Blueprint('products', __name__)


@products.route('/product', methods=['GET', 'POST'])
def product():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new product
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_price = request.form['product_price']

        # Insert the new product into the database
        cursor.execute('INSERT INTO products (product_name, product_price) VALUES (%s, %s)', (product_name, product_price))
        db.commit()

        flash('New product added successfully!', 'success')
        return redirect(url_for('products.product'))

    # Handle GET request to display all products
    cursor.execute('SELECT * FROM products')
    all_products = cursor.fetchall()
    return render_template('products.html', all_products=all_products)


@products.route('/update_product/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the product's details
        product_name = request.form['product_name']
        product_price = request.form['product_price']

        cursor.execute('UPDATE products SET product_name = %s, product_price = %s WHERE product_id = %s',
                       (product_name, product_price, product_id))
        db.commit()

        flash('Product updated successfully!', 'success')
        return redirect(url_for('products.product'))

    # GET method: fetch product's current data for pre-populating the form
    cursor.execute('SELECT * FROM products WHERE product_id = %s', (product_id,))
    product = cursor.fetchone()
    return render_template('update_product.html', product=product)


@products.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the product
    cursor.execute('DELETE FROM products WHERE product_id = %s', (product_id,))
    db.commit()

    flash('Product deleted successfully!', 'danger')
    return redirect(url_for('products.product'))