from domain.sqlAlchemy.configuration import SessionLocal
from domain.sqlAlchemy.model.product_model import Product
from domain.sqlAlchemy.repository.base_repository import BaseRepository
from typing import List, Dict, Any
from utils import utils
from datetime import datetime
import logging

class ProductService:
    def __init__(self):
        self.db = SessionLocal()
        self.model = Product
        self.product_repo = BaseRepository(self.model, self.db)

    def create_products(self, products_in: List[Dict[str, Any]]):
        """
        Create multiple products in the database.
        :param products_in: List of dictionaries containing product details.
        :return: Response indicating success or failure.
        """
        try:
            self.model.validation(products_in)
            try:
                trx = self.product_repo.begin()
                created_products = self.product_repo.create(products_in)
                response = [self.model.to_dict(product) for product in created_products]
                self.product_repo.commit(trx=trx)
            except Exception as e:
                self.product_repo.rollback(trx=trx)
                logging.error(f"Validation error while creating products: {str(ve)}")
                return utils.json_response(500, f"Validation Error: {str(ve)}", log_level="error")
            return utils.json_response(
                201,
                "Products created successfully!",
                response
            )
        except ValueError as ve:
            self.product_repo.rollback(trx=trx)
            logging.error(f"Validation error while creating products: {str(ve)}")
            return utils.json_response(400, f"Validation Error: {str(ve)}", log_level="error")
        except Exception as e:
            logging.error(f"Unexpected error while creating products: {str(e)}")
            return utils.json_response(500, "Internal Server Error", log_level="error")


    def get_all_products(self, page: int = 1, limit: int = 10, name:str = None, price: float = None):
        try:
            filters = {"deteled_at" : None}
            if name:
                filters['name'] = f"%{name}%"
            if price:
                filters['price'] = {"min": price, "max": 220}
            # if price:
            #     filters['price'] = ">",price # "price == 100"
            products = self.product_repo.get_all(page=page, limit=limit, filters= filters, columns=["id","name", "price", "updated_at"], order_by=[("updated_at", "DESC")])
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
        try:
            product = self.product_repo.get_by_id(product_id)
            if product:
                product_dict = self.model.to_dict(product)
                return utils.json_response(200, "Get Detail Product Successfully!", [product_dict]) 
            return utils.json_response(404, "Data Not Found", log_level="error")
        except Exception as e:
            logging.error(f"Error occurred while fetching product by id {product_id}: {str(e)}")
            return utils.json_response(500, "Internal Server Error", log_level="error")

    def update_products(self, products_in: List[Dict[str, Any]]):
        """
        Update multiple products in the database.
        :param product_ids: List of product IDs to be updated.
        :param products_in: List of dictionaries containing updated product details.
        :return: Response indicating success or failure.
        """
        try:
            product_ids = [
                product.update({"updated_at": datetime.now()}) or product["id"]
                for product in products_in
            ]

            if not product_ids or not products_in:
                return utils.json_response(400, "Product IDs and product details must be provided.", log_level="error")
            
            products = self.product_repo.get_by_ids(product_ids)
            if len(products) != len(product_ids):
                return utils.json_response(404, "Some product IDs are invalid or not found.", log_level="error")
            
            self.product_repo.close()

            try:
                trx = self.product_repo.begin()
                updated_products = self.product_repo.update(products_in)
                response = [self.model.to_dict(product) for product in updated_products]
                self.product_repo.commit(trx=trx)
            except Exception as e:
                self.product_repo.rollback(trx=trx)
                logging.error(f"Validation error while updating products: {str(ve)}")
                return utils.json_response(500, "Internal Server Error", log_level="error")

            return utils.json_response(
                200,
                "Products updated successfully!",
                response
            )
        except ValueError as ve:
            logging.error(f"Validation error while updating products: {str(ve)}")
            return utils.json_response(400, f"Validation Error: {str(ve)}", log_level="error")
        except Exception as e:
            logging.error(f"Unexpected error while updating products: {str(e)}")
            return utils.json_response(500, str(e), log_level="error")

    def delete_products(self, product_ids: List[int]):
        """
        Soft delete multiple products by updating the deleted_at field.
        :param product_ids: List of product IDs to be soft deleted.
        :return: Response indicating success or failure.
        """
        try:
            if not product_ids:
                return utils.json_response(400, "Product IDs must be provided.", log_level="error")
            
            products = self.product_repo.get_by_ids(product_ids)
            if len(products) != len(product_ids):
                return utils.json_response(404, "Some product IDs are invalid or not found.", log_level="error")
            
            try:
                trx = self.product_repo.begin()

                now = datetime.now()
                updated_products = []
                for product in products:
                    product["deleted_at"] = now  
                    updated_product = self.product_repo.update(product)
                    updated_products.append(updated_product)

                self.product_repo.commit(trx=trx)

                response = [self.model.to_dict(product) for product in updated_products]
                return utils.json_response(200, "Products soft deleted successfully!", response)

            except Exception as e:
                self.product_repo.rollback(trx=trx)
                logging.error(f"Error while soft deleting products: {str(e)}")
                return utils.json_response(500, "Internal Server Error", log_level="error")
        
        except Exception as e:
            logging.error(f"Unexpected error while soft deleting products: {str(e)}")
            return utils.json_response(500, str(e), log_level="error")


