
from flask import jsonify

from service.order_service import (
    get_checkout as get_checkout_service,
    place_order as place_order_service,
    get_user_orders as get_user_orders_service,
    get_order_details as get_order_details_service,
    cancel_order as cancel_order_service
)


# ==========================================
# SECTION 1: GET CHECKOUT DETAILS
# ==========================================

def get_checkout(user_id):

    # Call service to fetch checkout information
    result = get_checkout_service(user_id)

    # Return checkout details as JSON
    return jsonify(result), 200


# ==========================================
# SECTION 2: PLACE ORDER
# ==========================================

def place_order(data):

    try:

        # Extract request values
        user_id = data.get("user_id")
        delivery_address = data.get("delivery_address")
        payment_method = data.get("payment_method")

        # Call service to place the order
        result = place_order_service(
            user_id,
            delivery_address,
            payment_method
        )

        # Return successful order response
        return jsonify(result), 201

    except ValueError as error:

        # Return validation errors
        return jsonify({
            "message": str(error)
        }), 400

    except Exception as error:

        # Return unexpected errors
        return jsonify({
            "message": "Unable to place order",
            "error": str(error)
        }), 500


# ==========================================
# SECTION 3: GET USER ORDERS
# ==========================================

def get_user_orders(user_id):

    # Call service to fetch user's order history
    result = get_user_orders_service(user_id)

    # Return order history as JSON
    return jsonify(result), 200


# ==========================================
# SECTION 4: GET ORDER DETAILS
# ==========================================

def get_order_details(order_id, user_id):

    # Call service to fetch selected order details
    result = get_order_details_service(
        order_id,
        user_id
    )

    # Return 200 if order exists, otherwise 404
    status_code = 200 if result["order_items"] else 404

    return jsonify(result), status_code


# ==========================================
# SECTION 5: CANCEL ORDER
# ==========================================

def cancel_order(order_id, user_id):

    try:

        # Call service to cancel the selected order
        result = cancel_order_service(
            order_id,
            user_id
        )

        # Return successful cancellation response
        return jsonify(result), 200

    except ValueError as error:

        # Return validation or cancellation errors
        return jsonify({
            "message": str(error)
        }), 400

    except Exception as error:

        # Return unexpected errors
        return jsonify({
            "message": "Unable to cancel order",
            "error": str(error)
        }), 500
