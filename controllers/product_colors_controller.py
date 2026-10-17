from flask import jsonify
from service.product_colors_service import get_colors as get_product_colors


def get_colors(product_id):
    return jsonify(get_product_colors(product_id))