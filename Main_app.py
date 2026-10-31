
from flask import Flask, jsonify, request, render_template

from controllers.product_colors_controller import get_colors
from dao import product_dao
from service import product_service
from service.product_details_service import get_product_details
from controllers.cart_controller import (add_to_cart,get_cart,update_cart_item,remove_cart_item)
from controllers.order_controller import (
    get_checkout as get_checkout_controller,
    place_order as place_order_controller,
    get_user_orders as get_user_orders_controller,
    get_order_details as get_order_details_controller,
    cancel_order as cancel_order_controller
)

import validate_login
import get_username
import create_user
import put_username
import delete_username
import get_all_users
import search_products
import search_users
import re


# ==========================================
# FLASK APPLICATION
# ==========================================

app = Flask(__name__)


# ==========================================
# LOGIN PAGE
# ==========================================

@app.route('/', methods=['GET'])
def login_page():
    return render_template('login.html', username="")


# ==========================================
# LOGIN API
# ==========================================

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


# ==========================================
# FORGOT USERNAME PAGE
# ==========================================

@app.route('/forgot_username', methods=['GET'])
def forgot_username_page():

    return render_template(
        'forgot_username.html',
        email="",
        username=""
    )


# ==========================================
# FIND USERNAME BY EMAIL
# ==========================================

@app.route('/forgot_username/check', methods=['GET'])
def forgot_username():

    email = request.args.get('Email')

    if not email:
        return jsonify({
            "error": "Email is required"
        }), 400

    result = get_username.check_email_existance(email)

    return render_template(
        'forgot_username.html',
        email=email,
        username=result
    )


# ==========================================
# CREATE USER PAGE
# ==========================================

@app.route('/create_user', methods=['GET'])
def create_user_page():

    return render_template('create_user.html')


# ==========================================
# CREATE USER API
# ==========================================

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


# ==========================================
# UPDATE USERNAME
# ==========================================

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


# ==========================================
# DELETE USERNAME
# ==========================================

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


# ==========================================
# GET ALL USERS API
# ==========================================

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


# ==========================================
# GET ALL USERS PAGE
# ==========================================

@app.route('/users', methods=['GET'])
def users():

    return render_template('get_all_users.html')


# ==========================================
# SEARCH USERS API
# ==========================================

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


# ==========================================
# SEARCH USERS PAGE
# ==========================================

@app.route('/search', methods=['GET'])
def search_page():

    return render_template('search_users.html')


# ==========================================
# SEARCH PRODUCTS API
# ==========================================

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


# ==========================================
# SEARCH PRODUCTS PAGE
# ==========================================

@app.route('/search_products_page', methods=['GET'])
def search_products_page():

    return render_template('search_products.html')


# ==========================================
# PRODUCTS WITH OFFERS API
# ==========================================

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


# ==========================================
# PRODUCT COLORS API
# ==========================================

@app.route('/colors', methods=['GET'])
def colors():

    product_id = request.args.get('product_id', type=int)

    if not product_id or product_id < 1:

        return jsonify({
            "error": "Valid product_id is required"
        }), 400

    return get_colors(product_id)


# ==========================================
# PRODUCTS PAGE
# ==========================================

@app.route('/products', methods=['GET'])
def products_page():

    return render_template('products.html')


# ==========================================
# PRODUCT DETAILS PAGE
# ==========================================

@app.route('/product-details', methods=['GET'])
def product_details_page():

    return render_template('product_details.html')


# ==========================================
# PRODUCT DETAILS API
# ==========================================

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

# ==========================================
# ADD TO CART API
# ==========================================

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart_route():

    data = request.get_json(silent=True) or {}

    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if user_id is None or product_id is None:

        return jsonify({
            "error": "User ID and Product ID are required"
        }), 400

    # Pass all three values to the controller
    return add_to_cart(
        user_id,
        product_id,
        quantity
    )


# ==========================================
# GET CART API
# ==========================================

@app.route('/get_cart/<int:user_id>', methods=['GET'])
def get_cart_route(user_id):

    return get_cart(user_id)

# ==========================================
# CHECKOUT PAGE
# ==========================================

@app.route('/checkout/<int:user_id>', methods=['GET'])
def checkout_page(user_id):

    return render_template(
        'checkout.html',
        user_id=user_id
    )


# ==========================================
# GET CHECKOUT DETAILS API
# ==========================================

@app.route('/api/checkout/<int:user_id>', methods=['GET'])
def checkout_api(user_id):

    return get_checkout_controller(user_id)


# ==========================================
# PLACE ORDER API
# ==========================================

@app.route('/place_order', methods=['POST'])
def place_order_route():

    data = request.get_json(silent=True) or {}

    return place_order_controller(data)


# ==========================================
# ORDERS PAGE
# ==========================================

@app.route('/orders/<int:user_id>', methods=['GET'])
def orders_page(user_id):

    return render_template(
        'orders.html',
        user_id=user_id
    )


# ==========================================
# GET USER ORDERS API
# ==========================================

@app.route('/get_orders/<int:user_id>', methods=['GET'])
def get_orders_route(user_id):

    return get_user_orders_controller(user_id)


# ==========================================
# GET ORDER DETAILS API
# ==========================================

@app.route(
    '/get_order_details/<int:order_id>/<int:user_id>',
    methods=['GET']
)
def get_order_details_route(order_id, user_id):

    return get_order_details_controller(
        order_id,
        user_id
    )
#==========================================
#cart_page
#=========================================

@app.route('/cart')
def cart_page():
    return render_template('cart.html')

# ==========================================
# UPDATE CART ITEM QUANTITY API
# ==========================================

@app.route(
    '/update_cart/<int:user_id>/<int:cart_item_id>',
    methods=['PUT']
)
def update_cart_route(user_id, cart_item_id):

    data = request.get_json(silent=True) or {}

    quantity = data.get('quantity')

    if quantity is None:

        return jsonify({
            "error": "Quantity is required"
        }), 400

    return update_cart_item(
        user_id,
        cart_item_id,
        quantity
    )


# ==========================================
# REMOVE CART ITEM API
# ==========================================

@app.route(
    '/remove_cart/<int:user_id>/<int:cart_item_id>',
    methods=['DELETE']
)
def remove_cart_route(user_id, cart_item_id):

    return remove_cart_item(
        user_id,
        cart_item_id

    )


# ==========================================
# CANCEL ORDER API
# ==========================================

@app.route(
    '/cancel_order/<int:user_id>/<int:order_id>',
    methods=['PUT']
)
def cancel_order_route(user_id, order_id):

    # Call controller to cancel the selected order
    return cancel_order_controller(
        order_id,
        user_id
    )
# ==========================================
# RUN FLASK APPLICATION
# ==========================================

if __name__ == '__main__':

    app.run(debug=True)
