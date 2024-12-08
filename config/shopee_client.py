import os
import hmac
import hashlib
import time
from domain.redis.configuration import RedisClient
from config.database import RedisKey


class ShopeeClientConfig:
    BASE_URL = "https://partner.shopeemobile.com/api/v2"
    PARTNER_ID = os.getenv("SHOPEE_PARTNER_ID", "your_partner_id")
    PARTNER_KEY = os.getenv("SHOPEE_PARTNER_KEY", "your_partner_key")
    SHOP_ID = os.getenv("SHOPEE_SHOP_ID", "your_shop_id")

    @staticmethod
    def get_timestamp():
        """
        Get current timestamp in milliseconds.
        :return: Current timestamp in milliseconds
        """
        return int(time.time())

    @staticmethod
    def generate_signature(api_path, timestamp, params, custom_message=""):
        """
        Generate HMAC-SHA256 signature for Shopee API request.

        :param api_path: The API endpoint path
        :param params: Dictionary of parameters to be included in the request
        :param custom_message: Optional custom message to use in signature generation
        :return: HMAC-SHA256 signature
        """
        message = f"{ShopeeClientConfig.PARTNER_ID}{api_path}{params}{timestamp}{ShopeeClientConfig.get_access_token()}{ShopeeClientConfig.SHOP_ID}{ShopeeClientConfig.PARTNER_KEY}"

        if custom_message:
            message = custom_message

        signature = hmac.new(ShopeeClientConfig.PARTNER_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()

        return signature
    
    def get_access_token():
        return RedisClient.redis_client.get(RedisKey.SHOPEE_ACCESS_TOKEN_KEY)
  
