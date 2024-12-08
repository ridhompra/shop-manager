from flask import Blueprint, jsonify
from domain.thirdParties.shopee.services.shop_service import ShopService

router = Blueprint("router", __name__)
shop_service = ShopService()

@router.route("/shop", methods=["GET"])
def get_shop_info():
    try:
        data = shop_service.get_shop_info()
        return jsonify({"data": data, "message": "Success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
