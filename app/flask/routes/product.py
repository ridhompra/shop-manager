from flask import request, jsonify, Blueprint
from service.product import ProductService

router = Blueprint("router", __name__)

product_service = ProductService()

@router.route("/products", methods=["POST"])
def create_products():
    products_data = request.json
    products = product_service.create_products(products_data)
    return jsonify([product.__dict__ for product in products]), 201

@router.route("/products", methods=["GET"])
def get_all_products():
    products = product_service.get_all_products()
    return jsonify([product.__dict__ for product in products])

@router.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = product_service.get_product_by_id(product_id)
    if product:
        return jsonify(product.__dict__)
    return jsonify({"message": "Product not found"}), 404

@router.route("/products", methods=["PUT"])
def update_products():
    product_data = request.json
    product_ids = request.json.get("ids", [])
    updated = product_service.update_products(product_ids, product_data)
    if updated:
        return jsonify([product.__dict__ for product in updated])
    return jsonify({"message": "Products not found"}), 404

@router.route("/products", methods=["DELETE"])
def delete_products():
    product_ids = request.json.get("ids", [])
    deleted = product_service.delete_products(product_ids)
    if deleted:
        return jsonify({"message": "Products deleted"})
    return jsonify({"message": "Products not found"}), 404


