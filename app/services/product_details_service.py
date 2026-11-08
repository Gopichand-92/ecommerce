
import repositories.product_details_repository as product_repository


def get_product_details(product_id):

    product = product_repository.get_product_details(product_id)

    if product is None:
        print("Product not found")
        return None

    offers = product_repository.get_offers(product_id)
    product["offers"] = offers
    product["offer_count"] = len(offers)

    colors = product_repository.get_colors(product_id)
    product["colors"] = colors
    product["color_count"] = len(colors)

    return product


def get_colors(product_id):
    return product_repository.get_colors(product_id)


def get_offers(product_id):
    return product_repository.get_offers(product_id)
