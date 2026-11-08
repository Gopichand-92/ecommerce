
from flask import jsonify

from services.cart_service import (
    add_to_cart as add_to_cart_service,
    get_cart as get_cart_service,
    update_cart_item as update_cart_item_service,
    remove_cart_item as remove_cart_item_service
)


# ==========================================
# ADD PRODUCT TO CART
# ==========================================

def add_to_cart(user_id, product_id, quantity):

    try:
        result = add_to_cart_service(
            user_id,
            product_id,
            quantity
        )

        return jsonify({
            "message": "Product added to cart successfully",
            "cart": result
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400

    except Exception as error:

        return jsonify({
            "error": "Unable to add product to cart",
            "details": str(error)
        }), 500


# ==========================================
# GET CART ITEMS
# ==========================================

def get_cart(user_id):

    result = get_cart_service(user_id)

    return jsonify(result), 200


# ==========================================
# UPDATE CART ITEM QUANTITY
# ==========================================

def update_cart_item(user_id, cart_item_id, quantity):

    try:

        result = update_cart_item_service(
            user_id,
            cart_item_id,
            quantity
        )

        return jsonify(result), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400

    except Exception as error:

        return jsonify({
            "error": "Unable to update cart quantity",
            "details": str(error)
        }), 500


# ==========================================
# REMOVE PRODUCT FROM CART
# ==========================================

def remove_cart_item(user_id, cart_item_id):

    try:

        result = remove_cart_item_service(
            user_id,
            cart_item_id
        )

        return jsonify(result), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400

    except Exception as error:

        return jsonify({
            "error": "Unable to remove cart item",
            "details": str(error)
        }), 500
