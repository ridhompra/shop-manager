from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List, Dict, Any
from datetime import datetime
from utils.utils import validate_email

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"

    @staticmethod
    def validation(user: Dict[str, Any]):
        """
        Validate a dict of users.
        :param users: dict of user dictionaries to validate.
        :raises ValueError: If validation fails for any user.
        """
        name = user.get("name")
        email = user.get("email")
        password = user.get("password")

        if not name or len(name) <= 3 or len(name) > 200:
            raise ValueError("Name must be between 3 and 200 characters")
        
        if not email or len(email) < 5 or len(email) > 255 or not validate_email(email):
            raise ValueError("Email must be a valid email address and must be between 5 and 255 characters")
        
        if not password or len(password) < 6 or len(password) > 50:
            raise ValueError("Password must be between 6 and 50 characters long")


    def to_dict(self, columns=None):
        """
        Convert model instance to dictionary with selected columns.
        :param columns: List of columns to include in the dictionary.
        :return: Dictionary with selected columns.
        """
        # Default columns to include if none are specified
        if columns is None:
            columns = ["id", "name", "email", "created_at", "updated_at"]

        result = {}
        
        # Only add attributes to result if they exist in the instance
        for column in columns:
            if hasattr(self, column):
                result[column] = getattr(self, column)

        return result

    def set_password(self, password: str):
        """
        Set password for the user.
        :param password: Password string to hash.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Check if the provided password matches the stored password.
        :param password: Password string to check.
        :return: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password, password)
