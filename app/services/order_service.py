
import repositories.order_repository as order_repository


# ==========================================
# SECTION 1: GET CHECKOUT DETAILS
# ==========================================

def get_checkout(user_id):

    # Fetch products from the user's cart using DAO
    cart_items = order_repository.get_checkout_items(user_id)

    # Check whether the cart contains products
    if not cart_items:

        return {
            "message": "Your Cart is Empty",
            "cart": [],
            "total_amount": 0
        }

    # Calculate total amount of all products
    total_amount = sum(
        float(item["product_price"]) * item["quantity"]
        for item in cart_items
    )

    # Return cart products and total amount
    return {
        "message": "Checkout details fetched successfully",
        "cart": cart_items,
        "total_amount": round(total_amount, 2)
    }


# ==========================================
# SECTION 2: PLACE ORDER
# ==========================================

def place_order(user_id, delivery_address, payment_method):

    # Validate delivery address
    if not delivery_address:
        raise ValueError("Delivery address is required")

    # Convert payment method to uppercase
    payment_method = payment_method.upper()

    # Currently, only COD is implemented
    if payment_method != "COD":
        raise ValueError("Online payment is not integrated yet")

    # COD payment is collected during delivery
    payment_status = "Pending"

    # Get database connection from DAO
    conn = order_repository.get_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # Start database transaction
        conn.start_transaction()

        # Fetch products from the user's cart
        cart_items = order_repository.get_checkout_items(user_id)

        # Check whether cart is empty
        if not cart_items:
            raise ValueError("Your Cart is Empty")

        # Calculate total price of cart products
        total_amount = sum(
            float(item["product_price"]) * item["quantity"]
            for item in cart_items
        )

        # Insert order information into orders table
        order_id = order_repository.insert_order(
            cursor,
            user_id,
            round(total_amount, 2),
            delivery_address,
            payment_method,
            payment_status
        )

        # Insert each purchased product into order_items table
        for item in cart_items:

            order_repository.insert_order_item(
                cursor,
                order_id,
                item
            )

        # Remove purchased products from cart_item table
        order_repository.delete_cart_items(cursor, user_id)

        # Save all database changes
        conn.commit()

        # Return order confirmation details
        return {
            "order_id": order_id,
            "user_id": user_id,
            "total_amount": round(total_amount, 2),
            "payment_method": payment_method,
            "payment_status": payment_status,
            "order_status": "Placed",
            "message": "Order placed successfully"
        }

    except Exception:

        # Undo all database changes if an error occurs
        conn.rollback()
        raise

    finally:

        # Close database cursor and connection
        cursor.close()
        conn.close()


# ==========================================
# SECTION 3: GET USER ORDERS
# ==========================================

def get_user_orders(user_id):

    # Fetch all orders belonging to the user
    orders = order_repository.get_user_orders(user_id)

    # Check whether the user has any orders
    if not orders:

        return {
            "message": "No orders found",
            "orders": []
        }

    # Return order history
    return {
        "message": "Orders fetched successfully",
        "orders": orders
    }


# ==========================================
# SECTION 4: GET ORDER DETAILS
# ==========================================

def get_order_details(order_id, user_id):

    # Fetch products belonging to the selected order
    order_items = order_repository.get_order_details(
        order_id,
        user_id
    )

    # Check whether the order exists
    if not order_items:

        return {
            "message": "Order not found",
            "order_items": []
        }

    # Return purchased product details
    return {
        "message": "Order details fetched successfully",
        "order_items": order_items
    }


# ==========================================
# SECTION 5: CANCEL ORDER
# ==========================================

def cancel_order(order_id, user_id):

    # Convert IDs into integers
    try:
        order_id = int(order_id)
        user_id = int(user_id)

    except (ValueError, TypeError):
        raise ValueError("Invalid Order ID or User ID")

    # Validate IDs
    if order_id <= 0 or user_id <= 0:
        raise ValueError("Order ID and User ID must be positive")

    # Cancel the order using DAO
    result = order_repository.cancel_order(order_id, user_id)

    # Check whether an order was updated
    if result == 0:
        raise ValueError(
            "Order cannot be cancelled. It may not exist, "
            "may not belong to this user, or may no longer be in Placed status."
        )

    # Return cancellation confirmation
    return {
        "order_id": order_id,
        "user_id": user_id,
        "order_status": "Cancelled",
        "message": "Order cancelled successfully"
    }
