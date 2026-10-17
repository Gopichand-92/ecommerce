from dao import product_dao


def get_products_with_offers(search_text, category_name, max_price):

    rows = product_dao.get_products_with_offers(
        search_text,
        category_name,
        max_price
    )

    products = {}

    for row in rows:

        product_id = row[0]

        if product_id not in products:

            products[product_id] = {
                "id": row[0],
                "name": row[1],
                "price": row[2],
                "description": row[3],
                "image": row[4],
                "offers": []
            }

        if row[5] is not None:

            discount_amount = (
                float(row[2]) * float(row[6])
            ) / 100

            products[product_id]["offers"].append({
                "offer_type": row[5],
                "discount_amount": discount_amount
            })

    return list(products.values())