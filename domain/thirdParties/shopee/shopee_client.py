import requests
from config.shopee_client import ShopeeClientConfig

class ShopeeClient:
    def __init__(self):
        self.base_url = ShopeeClientConfig.BASE_URL
        self.partner_id = ShopeeClientConfig.PARTNER_ID
        self.partner_key = ShopeeClientConfig.PARTNER_KEY   

    def make_request(self, endpoint, method="GET", params=None, data=None):
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.request(method, url, headers=headers, params=params, json=data)
        response.raise_for_status()
        return response.json()
