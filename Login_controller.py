from flask import Flask, jsonify, request, render_template
from controllers.product_colors_controller import get_colors
from dao import product_dao
from service import product_service
from service.product_details_service import get_product_details
from controllers.cart_controller import add_to_cart
import validate_login
import get_username
import create_user
import put_username
import delete_username
import get_all_users
import search_products
import search_users
import re


app = Flask(__name__)
#---------------------------------------------------------
# Login Page
#---------------------------------------------------------
@app.route('/')
def login_page():
    return render_template('login.html', username="")

#---------------------------------------------------------
# Login API
#--------------------------------------------------------
@app.route('/Login', methods=['GET'])
def hello_world():
    username = request.args.get('Username')
    password = request.args.get('Password')

    pattern = r"^[a-zA-Z0-9_-]{3,16}$"

    if username and re.fullmatch(pattern, username) and password:
        result = validate_login.check_user_existance(
            username,
            password
        )
        return result, 200

    return jsonify({
        "error": "Invalid username or password"
    }), 400

#---------------------------------------------------------
# Forgot Username Page
#---------------------------------------------------------
@app.route('/forgot_username', methods=['GET'])
def forgot_username_page():
    return render_template(
        'forgot_username.html',
        email="",
        username=""
    )

#---------------------------------------------------------
# Find Username by Email
#---------------------------------------------------------
@app.route('/forgot_username/check', methods=['GET'])
def forgot_username():
    email = request.args.get('Email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    result = get_username.check_email_existance(email)

    return render_template(
        'forgot_username.html',
        email=email,
        username=result
    )

#---------------------------------------------------------
# Create User Page
#---------------------------------------------------------
@app.route('/create_user', methods=['GET'])
def create_user_page():
    return render_template('create_user.html')

#---------------------------------------------------------
# Create User API
#---------------------------------------------------------
@app.route('/create_user', methods=['POST'])
def create_user_data():
    data = request.get_json(silent=True) or {}

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({
            "error": "Username, password and email are required"
        }), 400

    result = create_user.check_user_creation(
        username,
        password,
        email
    )

    if result:
        return jsonify({
            "message": "User created successfully"
        }), 201

    return jsonify({
        "error": "User creation failed"
    }), 400

#---------------------------------------------------------
# Update Username
#---------------------------------------------------------
@app.route('/update_username', methods=['PUT'])
def update_username_data():
    data = request.get_json(silent=True) or {}

    user_name = data.get('user_name')
    new_username = data.get('new_username')

    if not user_name or not new_username:
        return jsonify({
            "error": "Both usernames are required"
        }), 400

    result = put_username.check_user_update(
        user_name,
        new_username
    )

    if result:
        return jsonify({
            "message": "Username updated successfully"
        }), 200

    return jsonify({
        "error": "Failed to update username"
    }), 400

#---------------------------------------------------------
# Delete Username
#---------------------------------------------------------
@app.route('/delete_username', methods=['DELETE'])
def delete_username_data():
    data = request.get_json(silent=True) or {}
    username = data.get('user_name')

    if not username:
        return jsonify({
            "error": "Username is required"
        }), 400

    result = delete_username.check_user_deletion(username)

    if result:
        return jsonify({
            "message": "Username deleted successfully"
        }), 200

    return jsonify({
        "error": "Failed to delete username"
    }), 400

#---------------------------------------------------------
# Get All Users API
#---------------------------------------------------------
@app.route('/all_users', methods=['GET'])
def all_users():
    users = get_all_users.get_all_users()

    users_json = [
        {
            "id": user[0],
            "name": user[1],
            "email": user[2]
        }
        for user in users
    ]

    return jsonify(users_json), 200

#---------------------------------------------------------
# Get All Users Page
#---------------------------------------------------------
@app.route('/users', methods=['GET'])
def users():
    return render_template('get_all_users.html')

#---------------------------------------------------------
# Search Users API
#---------------------------------------------------------
@app.route('/search_users', methods=['GET'])
def search_users_data():
    username = request.args.get('username')

    users = search_users.search_users(username)

    users_json = [
        {
            "id": user[0],
            "name": user[1],
            "email": user[2]
        }
        for user in users
    ]

    return jsonify(users_json), 200

#---------------------------------------------------------
# Search Users Page
#---------------------------------------------------------
@app.route('/search')
def search_page():
    return render_template('search_users.html')

#---------------------------------------------------------
# Search Products API
#---------------------------------------------------------
@app.route('/search_products', methods=['GET'])
def search_products_data():
    category = request.args.get('category')
    max_price = request.args.get('max_price')

    products = search_products.search_products(
        category,
        max_price
    )

    products_json = [
        {
            "id": product[0],
            "name": product[1],
            "price": product[2],
            "description": product[3],
            "image": product[4]
        }
        for product in products
    ]

    return jsonify(products_json), 200

#---------------------------------------------------------
# Search Products Page
#---------------------------------------------------------
@app.route('/search_products_page', methods=['GET'])
def search_products_page():
    return render_template('search_products.html')

#---------------------------------------------------------
# Products with Offers API
#---------------------------------------------------------
@app.route('/products_with_offers', methods=['GET'])
def products_with_offers():
    category = request.args.get('category')
    max_price = request.args.get('max_price')
    search = request.args.get('search')

    products = product_service.get_products_with_offers(
        search,
        category,
        max_price
    )

    return jsonify(products), 200

#---------------------------------------------------------
# Product Colors API
#---------------------------------------------------------
@app.route('/colors', methods=['GET'])
def colors():
    product_id = request.args.get('product_id', type=int)

    if not product_id or product_id < 1:
        return jsonify({
            "error": "Valid product_id is required"
        }), 400

    return get_colors(product_id)


# Products Page
@app.route('/products', methods=['GET'])
def products_page():
    return render_template('products.html')

#---------------------------------------------------------
# Product Details API
#---------------------------------------------------------
@app.route('/api/product-details', methods=['GET'])
def product_details_api():
    product_id = request.args.get('product_id', type=int)

    if not product_id or product_id < 1:
        return jsonify({
            "error": "Valid product_id is required"
        }), 400

    product = get_product_details(product_id)

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product), 200

#---------------------------------------------------------
# Product Details Page and Add to Cart
#---------------------------------------------------------
@app.route('/product-details', methods=['GET', 'POST'])
def product_details_page():

    # GET: Open the product details page
    if request.method == 'GET':
        return render_template('product_details.html')

    # POST: Receive product ID and quantity
    data = request.get_json()

    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    # Check product ID and quantity
    if not isinstance(product_id, int) or product_id < 1:
        return jsonify({"error": "Invalid product ID"}), 400

    if not isinstance(quantity, int) or quantity < 1:
        return jsonify({"error": "Invalid quantity"}), 400

    # Add product to cart
    return add_to_cart(product_id, quantity)



if __name__ == '__main__':
    app.run(debug=True)
