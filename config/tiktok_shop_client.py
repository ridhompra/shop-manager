import os
import hmac
import hashlib
import time
from urllib.parse import urlencode


class TikTokClientConfig:
    BASE_URL = os.getenv("TIKTOK_BASE_URL", "https://open-api.tiktokglobalshop.com")
    APP_KEY = os.getenv("TIKTOK_APP_KEY", "12345")
    APP_SECRET = os.getenv("TIKTOK_APP_SECRET", "777")

    @staticmethod
    def get_timestamp():
        """
        Get the current timestamp in seconds.
        
        Returns:
            int: Current timestamp in seconds.
        """
        return int(time.time())

    @staticmethod
    def generate_signature(path: str, query_params: dict) -> str:
        """
        Generate an HMAC-SHA256 signature for TikTok Shop API authentication.

        Args:
            path (str): The API endpoint path (e.g., "/api/orders").
            query_params (dict): Dictionary of query parameters excluding 'sign' 
                                 and 'access_token'.

        Returns:
            str: The generated signature (HMAC-SHA256 hash).
        """
        # Step 1: Reorder query parameters alphabetically by key, excluding 'sign' and 'access_token'
        query_params = {k: v for k, v in query_params.items() if k not in {"sign", "access_token"}}
        sorted_keys = sorted(query_params.keys())

        # Step 2: Concatenate all parameters in the format {key}{value} and append the request path to the beginning
        concatenated_params = ''.join(f"{key}{query_params[key]}" for key in sorted_keys)
        base_string = f"{path}{concatenated_params}"

        # Step 3: Wrap the base string with app secret
        final_string = f"{TikTokClientConfig.APP_SECRET}{base_string}{TikTokClientConfig.APP_SECRET}"

        # Step 4: Generate the HMAC-SHA256 signature
        hmac_hash = hmac.new(TikTokClientConfig.APP_SECRET.encode(), final_string.encode(), hashlib.sha256)
        signature = hmac_hash.hexdigest()

        return signature

    @classmethod
    def generate_signed_url(cls, path: str, query_params: dict) -> str:
        """
        Generate a full URL with the HMAC-SHA256 signature for TikTok Shop API requests.

        Args:
            path (str): The API endpoint path (e.g., "/api/orders").
            query_params (dict): Query parameters (excluding 'sign' and 'access_token').

        Returns:
            str: The complete URL with the generated signature included.
        """
        timestamp = cls.get_timestamp()
        query_params["timestamp"] = timestamp
        query_params["app_key"] = cls.APP_KEY

        # Generate the signature
        signature = cls.generate_signature(path, query_params)
        query_params["sign"] = signature

        # Build the full URL
        encoded_params = urlencode(query_params)
        full_url = f"{cls.BASE_URL}{path}?{encoded_params}"

        return full_url