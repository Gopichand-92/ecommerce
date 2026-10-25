from flask import jsonify
from service.cart_service import add_to_cart as add_to_cart_service


def add_to_cart(product_id, quantity):
    result = add_to_cart_service(product_id, quantity)

    return jsonify({
        "message": "Product added to cart successfully",
        "cart": result
    }), 200
