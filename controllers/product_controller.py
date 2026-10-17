from flask import jsonify, request
from service import product_service


def get_products_with_offers():

    category = request.args.get('category')
    max_price = request.args.get('max_price')

    products = product_service.get_products_with_offers(
        category,
        max_price
    )

    return jsonify(products), 200