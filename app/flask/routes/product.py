from flask import request, jsonify, Blueprint
from service.product import ProductService

product_router = Blueprint("product_router", __name__)

product_service = ProductService()

@product_router.route("/products", methods=["POST"])
def create_products():
    products_data = request.json
    products = product_service.create_products(products_data)
    return jsonify([product.__dict__ for product in products]), 201

@product_router.route("/products", methods=["GET"])
def get_all_products():
    page = int(request.args.get('page', 1))  
    limit = int(request.args.get('limit', 10))  
    name = request.args.get('name', None)
    price = request.args.get('price', None)

    products = product_service.get_all_products(page=page, limit=limit, name=name, price=price)
    
    return jsonify(products), products["status_code"]

@product_router.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = product_service.get_product_by_id(product_id)
    return jsonify(product), product["status_code"]

@product_router.route("/products", methods=["PUT"])
def update_products():
    product_data = request.json
    product_ids = request.json.get("ids", [])
    updated = product_service.update_products(product_ids, product_data)
    if updated:
        return jsonify([product.__dict__ for product in updated])
    return jsonify({"message": "Products not found"}), 404

@product_router.route("/products", methods=["DELETE"])
def delete_products():
    product_ids = request.json.get("ids", [])
    deleted = product_service.delete_products(product_ids)
    if deleted:
        return jsonify({"message": "Products deleted"})
    return jsonify({"message": "Products not found"}), 404


