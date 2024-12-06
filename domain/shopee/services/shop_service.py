from domain.shopee.shopee_client import ShopeeClient

class ShopService:
    def __init__(self):
        self.client = ShopeeClient()
        self.retry_limit = 3  # Set a retry limit to prevent infinite retries



