from domain.sqlAlchemy.configuration import SessionLocal
from domain.sqlAlchemy.model.product_model import Product
from domain.sqlAlchemy.repository.base_repository import BaseRepository
from typing import List, Dict, Any
from utils import utils
import logging

class ProductService:
    def __init__(self):
        self.db = SessionLocal()
        self.model = Product
        self.product_repo = BaseRepository(self.model, self.db)

    def create_products(self, products_in: List[Dict[str, Any]]):
        return self.product_repo.create(products_in)

    def get_all_products(self, page: int = 1, limit: int = 10, name:str = None, price: float = None):
        try:
            filters = {}
            if name:
                filters['name'] = f"%{name}%"
            if price:
                filters['price'] = {"min": price, "max": 220}
            # if price:
            #     filters['price'] = ">",price # "price == 100"
            products = self.product_repo.get_all(page=page, limit=limit, filters= filters, columns=["name", "price"])
            products_dict = [self.model.to_dict(product) for product in products]
            total_products = self.product_repo.count()
            total_pages = total_products // limit + (1 if total_products % limit != 0 else 0)
            next_page = page + 1 if page < total_pages else None
            prev_page = page - 1 if page > 1 else None

            pagination = {
                "page": page,
                "limit": limit,
                "total": total_products,
                "total_page": total_pages,
                "next": next_page,
                "prev": prev_page,
            }

            return utils.json_response(200, "Get Products Successfully!", products_dict, pagination=pagination)
        
        except Exception as e:
            logging.error(f"Unexpected error occurred: {str(e)}")
            return utils.json_response(500, "Internal Server Error", log_level="error")


    def get_product_by_id(self, product_id: int):
        return self.product_repo.get_by_id(product_id)

    def get_products_by_ids(self, product_ids: List[int]):
        return self.product_repo.get_by_ids(product_ids)

    def update_products(self, product_ids: List[int], products_in: List[Dict[str, Any]]):
        return self.product_repo.update(product_ids, products_in)

    def delete_products(self, product_ids: List[int]):
        return self.product_repo.delete(product_ids)

