from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Dict, Any
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"
    
    def validation(products: List[Dict[str, Any]]):
        """
        Validate a list of products.
        :param products: List of product dictionaries to validate.
        :raises ValueError: If validation fails for any product.
        """
        for product in products:
            name = product.get("name")
            price = product.get("price")
            description = product.get("description")

            if not name or len(name) <= 3 or len(name) > 200:
                raise ValueError("Name must be between 3 and 200 characters")
            
            if price is None or price < 0:
                raise ValueError("Price must be greater than or equal to 0")
            
            if description and len(description) > 1000:
                raise ValueError("Description must be less than 1000 characters")


    def to_dict(self, columns=None):
        """
        Convert model instance to dictionary with selected columns.
        :param columns: List of columns to include in the dictionary.
        :return: Dictionary with selected columns.
        """
        # Default columns to include if none are specified
        if columns is None:
            columns = ["id", "name", "description", "price"]

        result = {}
        
        # Only add attributes to result if they exist in the instance
        for column in columns:
            if hasattr(self, column):
                result[column] = getattr(self, column)

        return result

