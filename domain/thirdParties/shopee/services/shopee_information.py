from config.shopee_client import ShopeeClientConfig
from utils.utils import json_response, setup_logger
import logging
from domain.redis.configuration import RedisClient
from config.shopee_client import ShopeeClientConfig
from config.database import RedisKey
from domain.thirdParties.shopee.services.shop_service import ShopService


class ShopInformation(ShopService):
    def get_shop_info(self):
        timestamp = ShopeeClientConfig.get_timestamp()
        retries = 0  
        # access_token = "your_access_token"  
        
        while retries < self.retry_limit:
            params = {
                "partner_id": ShopeeClientConfig.PARTNER_ID,
                "timestamp": timestamp,
                "access_token": ShopeeClientConfig.get_access_token(),
                "shop_id": ShopeeClientConfig.SHOP_ID,
                "partner_key": ShopeeClientConfig.PARTNER_KEY,
                "signature": ShopeeClientConfig.generate_signature("/shop/get", timestamp, params),
            }

            try:
                response = self.client.make_request("/shop/get", method="GET", params=params)
                if response.status_code == 200:
                    return json_response(200, "Shop information retrieved successfully", response.json())
                elif response.status_code == 401:
                    retries += 1
                    # access_token = self.login_to_shopee()  #login shopee
                    RedisClient.redis_client.setex(RedisKey.SHOPEE_ACCESS_TOKEN_KEY, 3600, access_token)  
                    continue  
                else:
                    return json_response(response.status_code, f"Failed to fetch shop info. Status code: {response.status_code}", {})
            except Exception as e:
                logger = logging.getLogger("ShopeeIntegration")
                logger.error(f"Error fetching shop info: {str(e)}")
                return json_response(500, f"An error occurred: {str(e)}", {})
        
        return json_response(401, "Failed to authenticate with third-party service after multiple attempts", {})