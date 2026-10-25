from dao.cart_dao import (get_cart_id,get_cart_item,insert_cart_item,update_cart_quantity)

def add_to_cart(product_id, quantity):
    user_id = 2

    cart_id = get_cart_id(user_id)

    result = get_cart_item(cart_id, product_id)

    if result:
        cart_item_id = result[0]
        new_quantity = result[1] + quantity
        update_cart_quantity(cart_item_id, new_quantity)
        final_quantity = new_quantity
    else:
        insert_cart_item(cart_id, product_id, quantity)
        final_quantity = quantity

    return {
        "cart_id": cart_id,
        "product_id": product_id,
        "quantity": final_quantity
    }