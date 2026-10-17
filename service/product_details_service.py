
import dao.product_details_dao as product_dao


def get_product_details(product_id):

    product = product_dao.get_product_details(product_id)

    if product is None:
        print("Product not found")
        return None

    offers = product_dao.get_offers(product_id)
    product["offers"] = offers
    product["offer_count"] = len(offers)

    colors = product_dao.get_colors(product_id)
    product["colors"] = colors
    product["color_count"] = len(colors)

    return product


def get_colors(product_id):
    return product_dao.get_colors(product_id)


def get_offers(product_id):
    return product_dao.get_offers(product_id)
