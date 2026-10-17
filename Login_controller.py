from flask import Flask, jsonify, request, render_template
from controllers.product_colors_controller import get_colors
from dao import product_dao
from service import product_service
from service.product_details_service import get_product_details
import validate_login
import get_username
import create_user
import put_username
import delete_username
import get_all_users
import search_products
import search_users
import search_users
import re 



# Initialize the Flask application
app = Flask(__name__)

# First open the login page
@app.route('/')
def login_page():

    return render_template(
        'login.html',
        username=""
    )


# Define a GET API endpoint
@app.route('/Login', methods=['GET'])
def hello_world():

    # request.args.get() syntax: ('parameter_name', 'default_value')
    Username = request.args.get('Username')
    Password = request.args.get('Password')

    pattern = r"^[a-zA-Z0-9_-]{3,16}$"

    # Check username pattern
    if re.fullmatch(pattern, Username):

        result = validate_login.check_user_existance(
            Username,
            Password
        )

        return result, 200

    else:

        return "Invalid Username (must contain only letters, numbers)", 400


# --------------------------------------------------
# Forgot Username Page
# --------------------------------------------------

@app.route('/forgot_username', methods=['GET'])
def forgot_username_page():

    return render_template(
        'forgot_username.html',
        email="",
        username=""
    )


# --------------------------------------------------
# Find username by email
# --------------------------------------------------

@app.route('/forgot_username/check', methods=['GET'])
def forgot_username():

    Email = request.args.get('Email')

    result = get_username.check_email_existance(Email)

    return render_template(
        'forgot_username.html',
        email=Email,
        username=result
    )


# --------------------------------------------------
# Create User Page
# --------------------------------------------------

@app.route('/create_user', methods=['GET'])
def create_user_page():

    return render_template(
        'create_user.html'
    )


# --------------------------------------------------
# Create user 
# --------------------------------------------------

@app.route('/create_user', methods=['POST'])
def create_user_data():
    data = request.get_json()

    Username = data.get('username')
    Password = data.get('password')
    Email = data.get('email')
    # print("Username:", Username)
    # print("Password:", Password)
    # print("Email:", Email)

    result = create_user.check_user_creation(
        Username,
        Password,
        Email
    )

    if result:
        return "User created successfully", 201
    else:
        return "User creation failed", 400


# --------------------------------------------------
# update username
# --------------------------------------------------
@app.route('/update_username', methods=['PUT'])
def update_username_data():

    # Get JSON data from client
    client_data = request.get_json()

    user_name = client_data.get('user_name')
    new_username = client_data.get('new_username')

    result = put_username.check_user_update(user_name, new_username)

    if result:
        return "Username updated successfully", 200
    else:
        return "Failed to update username", 400

# --------------------------------------------------
# update username
# --------------------------------------------------

@app.route('/delete_username', methods=['DELETE'])
def delete_username_data():

    # Get JSON data from client
    client_data = request.get_json()

    deletion_user_name = client_data.get('user_name')

    result = delete_username.check_user_deletion(
        deletion_user_name
    )

    if result:
        return "Username deletion successfully", 200
    else:
        return "Failed to delete username", 400


# # --------------------------------------------------
# # Get all users
# # --------------------------------------------------
# @app.route('/users', methods=['GET'])
# def users_page():

#     users = get_all_users.get_all_users()

#     return render_template(
#         'users.html',
#         users=users
#     )


# --------------------------------------------------
# Get all users
# --------------------------------------------------
@app.route('/all_users', methods=['GET'])
def all_users():
    users = get_all_users.get_all_users()

    users_json = [{"id": user[0], "name": user[1], "email": user[2]} for user in users]
    return jsonify(users_json), 200


@app.route('/users', methods=['GET'])
def users():
    return render_template('get_all_users.html')


# --------------------------------------------------
# Search users
# --------------------------------------------------
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

# --------------------------------------------------
# Search users page
# --------------------------------------------------
@app.route('/search')
def search_page():

    return render_template('search_users.html')



# --------------------------------------------------
# Search products 
# --------------------------------------------------

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


# --------------------------------------------------
# Search products page
# --------------------------------------------------

@app.route('/search_products_page', methods=['GET'])
def search_products_page():

    return render_template(
        'search_products.html'
    )
#--------------------------------------------------
# search products offers
#--------------------------------------------------
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


#--------------------------------------------------
# search products colors
#--------------------------------------------------
@app.route("/colors", methods=["GET"])
def colors():
    product_id = request.args.get("product_id")
    if not product_id:
        return jsonify({"error": "product_id is required"}), 400
 
    return get_colors(product_id)
 
@app.route("/products", methods=["GET"])
def products_page():
    return render_template("products.html")



#--------------------------------------------------
# product details page
#--------------------------------------------------



@app.route("/api/product-details", methods=["GET"])
def product_details_api():
    product_id = request.args.get("product_id", type=int)

    if not product_id:
        return jsonify({"error": "product_id is required"}), 400

    product = get_product_details(product_id)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product)

 
@app.route("/product-details", methods=["GET"])
def product_details_page():
    return render_template("product_details.html")
 
 

# Run the local development server
if __name__ == '__main__':
    app.run(debug=True)