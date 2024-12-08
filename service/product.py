from sqlalchemy.orm import Session
from domain.sqlAlchemy.configuration import SessionLocal
from domain.sqlAlchemy.model.product_model import Product
from domain.sqlAlchemy.repository.base_repository import BaseRepository
from typing import List, Dict, Any

class ProductService:
    def __init__(self):
        self.db = SessionLocal()
        self.product_repo = BaseRepository(Product, self.db)

    def create_products(self, products_in: List[Dict[str, Any]]):
        return self.product_repo.create(products_in)

    def get_all_products(self):
        return self.product_repo.get_all()

    def get_product_by_id(self, product_id: int):
        return self.product_repo.get_by_id(product_id)

    def get_products_by_ids(self, product_ids: List[int]):
        return self.product_repo.get_by_ids(product_ids)

    def update_products(self, product_ids: List[int], products_in: List[Dict[str, Any]]):
        return self.product_repo.update(product_ids, products_in)

    def delete_products(self, product_ids: List[int]):
        return self.product_repo.delete(product_ids)

