
from repositories.cart_repository import (
    get_cart_item,
    insert_cart_item,
    update_cart_quantity,
    remove_cart_item as remove_cart_item_dao,
    get_user_cart
)


# ==========================================
# ADD PRODUCT TO CART
# ==========================================

def add_to_cart(user_id, product_id, quantity):

    # Convert values into integers
    user_id = int(user_id)
    product_id = int(product_id)
    quantity = int(quantity)

    # Validate values
    if user_id <= 0 or product_id <= 0 or quantity <= 0:
        raise ValueError("User ID, Product ID and Quantity must be positive")

    # Check whether the product already exists in the user's cart
    result = get_cart_item(user_id, product_id)

    if result:

        cart_item_id = result[0]
        new_quantity = result[1] + quantity

        # Update existing product quantity
        update_cart_quantity(cart_item_id, new_quantity)

    else:

        # Insert new product into cart
        insert_cart_item(user_id, product_id, quantity)

        new_quantity = quantity

    return {
        "user_id": user_id,
        "product_id": product_id,
        "quantity": new_quantity
    }


# ==========================================
# GET ALL CART ITEMS
# ==========================================

def get_cart(user_id):

    result = get_user_cart(user_id)

    if not result:
        return {
            "message": "Your Cart is Empty",
            "cart": []
        }

    return {
        "message": "Cart items fetched successfully",
        "cart": result
    }


# ==========================================
# UPDATE CART ITEM QUANTITY
# ==========================================

def update_cart_item(user_id, cart_item_id, quantity):

    user_id = int(user_id)
    cart_item_id = int(cart_item_id)
    quantity = int(quantity)

    if user_id <= 0 or cart_item_id <= 0 or quantity <= 0:
        raise ValueError("Invalid cart item or quantity")

    # Check whether the cart item belongs to this user
    cart_items = get_user_cart(user_id)

    cart_item = next(
        (item for item in cart_items
         if item["cart_item_id"] == cart_item_id),
        None
    )

    if not cart_item:
        raise ValueError("Cart item not found")

    # Update quantity
    update_cart_quantity(cart_item_id, quantity)

    return {
        "message": "Cart quantity updated successfully",
        "cart_item_id": cart_item_id,
        "quantity": quantity
    }


# ==========================================
# REMOVE PRODUCT FROM CART
# ==========================================

def remove_cart_item(user_id, cart_item_id):

    user_id = int(user_id)
    cart_item_id = int(cart_item_id)

    if user_id <= 0 or cart_item_id <= 0:
        raise ValueError("Invalid user ID or cart item ID")

    result = remove_cart_item_dao(cart_item_id, user_id)

    if result == 0:
        raise ValueError("Cart item not found")

    return {
        "message": "Product removed from cart successfully",
        "cart_item_id": cart_item_id
    }
