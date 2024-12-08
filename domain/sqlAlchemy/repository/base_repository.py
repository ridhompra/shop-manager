from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Dict, Any

class BaseRepository:
    def __init__(self, model, db: Session):
        self.model = model
        self.db = db

    def create(self, objs_in: List[Any]):
        """
        Receives a list of model instances (already validated by model).
        """
        self.db.add_all(objs_in)
        self.db.flush()  # Ensures data is prepared for commit
        for obj in objs_in:
            self.db.refresh(obj)
        return objs_in


    def get_all(self, page: int = 1, limit: int = 10, filters: Dict[str, Any] = None, or_filters: Dict[str, Any] = None, columns: list = None):
        """
        Get all records with pagination, filtering, and specific column selection support.
        :param page: Page number (default is 1).
        :param limit: Number of records per page (default is 10).
        :param filters: A dictionary of filters (optional, applies AND conditions).
        :param or_filters: A dictionary of OR filters (optional).
        :param columns: List of columns to select (optional).
        :return: Paginated list of records.
        """
        query = self.db.query(self.model)

        # Select specific columns if 'columns' is provided
        if columns:
            query = query.with_entities(*[getattr(self.model, col) for col in columns])

        if filters:
            for field, value in filters.items():
                # Filter for range (BETWEEN)
                if isinstance(value, dict) and 'min' in value and 'max' in value:
                    query = query.filter(getattr(self.model, field).between(value['min'], value['max']))
                # Filter for "greater than" or "less than" comparisons
                elif isinstance(value, tuple) and len(value) == 2:
                    operator, val = value
                    if operator == ">":
                        query = query.filter(getattr(self.model, field) > val)
                    elif operator == "<":
                        query = query.filter(getattr(self.model, field) < val)
                    elif operator == "=":
                        query = query.filter(getattr(self.model, field) == val)
                # Filter for string matching using LIKE (case-insensitive)
                elif isinstance(value, str) and "%" in value:
                    query = query.filter(getattr(self.model, field).ilike(value))  # Case-insensitive LIKE
                # Filter for exact match
                else:
                    query = query.filter(getattr(self.model, field) == value)

        # Apply OR filters (if any)
        if or_filters:
            or_conditions = []
            for field, value in or_filters.items():
                # Filter for range (BETWEEN)
                if isinstance(value, dict) and 'min' in value and 'max' in value:
                    or_conditions.append(getattr(self.model, field).between(value['min'], value['max']))
                # Filter for "greater than" or "less than" comparisons
                elif isinstance(value, tuple) and len(value) == 2:
                    operator, val = value
                    if operator == ">":
                        or_conditions.append(getattr(self.model, field) > val)
                    elif operator == "<":
                        or_conditions.append(getattr(self.model, field) < val)
                    elif operator == "=":
                        or_conditions.append(getattr(self.model, field) == val)
                # Filter for string matching using LIKE (case-insensitive)
                elif isinstance(value, str) and "%" in value:
                    or_conditions.append(getattr(self.model, field).ilike(value))  # Case-insensitive LIKE
                # Filter for exact match
                else:
                    or_conditions.append(getattr(self.model, field) == value)

            # Apply the OR condition to the query
            if or_conditions:
                query = query.filter(or_(*or_conditions))

        offset = (page - 1) * limit

        records = query.offset(offset).limit(limit).all()

        return records



    def get_by_ids(self, ids: list):
        return self.db.query(self.model).filter(self.model.id.in_(ids)).all()
    
    def get_by_id(self, id: int, fields: List[str] = None):
        query = self.db.query(self.model)
        
        if fields:
            query = query.with_entities(*[getattr(self.model, field) for field in fields])
        
        return query.filter(self.model.id == id).first()

    def delete(self, ids: List[int]):
        objs = self.get_by_ids(ids)
        if objs:
            for obj in objs:
                self.db.delete(obj)
            self.db.flush()  # Prepares the deletion
            return True
        return False

    def update(self, ids: List[int], objs_in: List[Dict[str, Any]]):
        updated_objs = []
        for id, obj_in in zip(ids, objs_in):
            obj = self.get_by_id(id)
            if obj:
                for key, value in obj_in.items():
                    setattr(obj, key, value)
                self.db.flush()  # Prepares the updates
                self.db.refresh(obj)
                updated_objs.append(obj)
        return updated_objs if updated_objs else None

    def execute_raw_query(self, query: str, params: Dict[str, Any] = None):
        result = self.db.execute(query, params)
        return result.fetchall()

    def execute_raw_query_modify(self, query: str, params: Dict[str, Any] = None):
        self.db.execute(query, params)
        self.db.flush()  # Prepares the modification

    def begin(self):
        """
        Explicitly begin a transaction.
        """
        return self.db.begin()

    def commit(self):
        """
        Commit the current transaction.
        """
        try:
            self.db.commit()
        except Exception as e:
            self.rollback()
            raise e

    def rollback(self):
        """
        Rollback the current transaction.
        """
        self.db.rollback()

    def close(self):
        """
        Close the current database session.
        """
        self.db.close()

    def count(self):
        """
        Get the total count of rows in the table.
        """
        return self.db.query(self.model).count()
