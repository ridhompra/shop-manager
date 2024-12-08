from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"
    
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

