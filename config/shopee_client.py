import os
import hmac
import hashlib
import time
from domain.redis.configuration import RedisClient
from config.database import RedisKey


class ShopeeClientConfig:
    BASE_URL = os.getenv("SHOPEE_BASE_URL", "https://partner.test-stable.shopeemobile.com")
    PARTNER_ID = os.getenv("SHOPEE_PARTNER_ID", "1")
    PARTNER_KEY = os.getenv("SHOPEE_PARTNER_KEY", "test....")
    SHOP_ID = os.getenv("SHOPEE_SHOP_ID", "129772")

    @staticmethod
    def get_timestamp():
        """
        Get current timestamp in milliseconds.
        :return: Current timestamp in milliseconds
        """
        return int(time.time())

    def get_access_token():
        return RedisClient.redis_client.get(RedisKey.SHOPEE_ACCESS_TOKEN_KEY)

    @staticmethod
    def generate_signature(path: str, timestamp: int, access_token: str):
        """
        Generate an HMAC-SHA256 signature for Shopee API authentication.

        This method generates a signature required for authenticating requests 
        to the Shopee API. The signature is generated using the combination of 
        partner ID, API path, timestamp, access token, and shop ID, along with 
        the partner key.

        Args:
            path (str): The API endpoint path (e.g., "/api/v2/shop/auth_partner").
            timestamp (int): The Unix timestamp (in seconds) for the request.
            access_token (str): The access token associated with the shop.

        Returns:
            - str: The generated signature (HMAC-SHA256 hash).
        """
        timestamp = int(time.time())

        base_string = f"{ShopeeClientConfig.PARTNER_ID}{path}{timestamp}{access_token}{ShopeeClientConfig.SHOP_ID}".encode()
        sign = hmac.new(ShopeeClientConfig.PARTNER_KEY.encode(), base_string, hashlib.sha256).hexdigest()

        return sign
