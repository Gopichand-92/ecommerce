from dao.product_colors_dao import get_colors as get_product_colors


def get_colors(product_id):
    colors = get_product_colors(product_id)
    items = [color["color_name"] for color in colors]

    return {
        "count": len(items),
        "items": items
    }