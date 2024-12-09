from sqlalchemy.orm import Session, SessionTransaction
from sqlalchemy import or_, and_
from typing import List, Dict, Any, Any, Tuple

class BaseRepository:
    def __init__(self, model, db: Session):
        self.model = model
        self.db = db

    def create(self, objs_in: List[Dict[str, Any]]):
        """
        Receives a list of dictionaries and converts them to model instances
        before adding them to the database.
        """
        try:
            # Convert dictionaries to model instances
            model_instances = [self.model(**obj) for obj in objs_in]

            # Add all model instances to the database
            self.db.add_all(model_instances)
            self.db.flush()  # Ensures data is prepared for commit

            # Refresh instances to get their updated state (e.g., IDs)
            for instance in model_instances:
                self.db.refresh(instance)

            return model_instances
        except Exception as e:
            raise ValueError(f"Error creating objects: {str(e)}")

    def get_all(self, page: int = 1, limit: int = 10, filters: Dict[str, Any] = None, or_filters: Dict[str, Any] = None, columns: list = None, order_by: List[Tuple[str, str]] = None):
        """
        Get all records with pagination, filtering, ordering, and specific column selection support.
        :param page: Page number (default is 1).
        :param limit: Number of records per page (default is 10).
        :param filters: A dictionary of filters (optional, applies AND conditions).
        :param or_filters: A dictionary of OR filters (optional).
        :param columns: List of columns to select (optional).
        :param order_by: A list of tuples specifying column and direction (e.g., [("created_at", "DESC")]).
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

        # Apply order by if specified
        if order_by:
            for column, direction in order_by:
                column_attr = getattr(self.model, column, None)
                if column_attr is not None:
                    if direction.upper() == "DESC":
                        query = query.order_by(column_attr.desc())
                    else:
                        query = query.order_by(column_attr.asc())

        # Pagination logic
        offset = (page - 1) * limit
        records = query.offset(offset).limit(limit).all()

        return records


    def get_by_ids(self, ids: list[str]):
        try:
            if not ids:
                raise ValueError("IDs list cannot be empty.")
            products = self.db.query(self.model).filter(self.model.id.in_(ids)).all()
            
            if not products:
                raise ValueError(f"No products found with IDs: {', '.join(map(str, ids))}")
            
            return products
        except Exception as e:
            raise ValueError(f"An error occurred: {str(e)}")
    
    def get_by_id(self, id: int, fields: List[str] = None):
        query = self.db.query(self.model)
        
        if fields:
            valid_fields = [field for field in fields if hasattr(self.model, field)]
            
            if valid_fields:
                query = query.with_entities(*[getattr(self.model, field) for field in valid_fields])
            else:
                raise ValueError(f"Invalid fields: {', '.join(fields)}")

        return query.filter(self.model.id == id).first()

    def delete(self, ids: List[int]):
        objs = self.get_by_ids(ids)
        if objs:
            for obj in objs:
                self.db.delete(obj)
            self.db.flush()  # Prepares the deletion
            return True
        return False

    def update(self, objs_in: List[Dict[str, Any]]):
        updated_objs = []
        
        for obj_in in objs_in:
            product_id = obj_in.get('id')
            if not product_id:
                continue
            
            obj = self.get_by_id(product_id)
            if obj:
                for key, value in obj_in.items():
                    if key != 'id':
                        setattr(obj, key, value)
                
                self.db.flush()
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

    def commit(self, trx: SessionTransaction):
        """
        Commit the current transaction.
        """
        try:
            trx.commit()
            trx.close()
            self.db.close()
        except Exception as e:
            trx.rollback()
            trx.close()
            self.db.close()
            raise e
    
    def close(self):
        """
        Close the current transaction.
        """
        self.db.close()

    def rollback(self, trx: SessionTransaction):
        """
        Rollback the current transaction.
        """
        trx.rollback()
        trx.close()
        self.db.close()

    def count(self):
        """
        Get the total count of rows in the table.
        """
        return self.db.query(self.model).count()

    def find_by(self, filters: Dict[str, Any] = None, or_filters: Dict[str, Any] = None, columns: List[str] = None):
        """
        Finds records based on provided filters (AND and OR conditions).
        Supports custom column selection.
        :param filters: A dictionary of filters (applies AND conditions).
        :param or_filters: A dictionary of OR filters (optional).
        :param columns: A list of column names to select (optional).
        :return: List of records that match the filters.
        """
        # Start the query
        query = self.db.query(self.model)
        
        # Select specific columns if 'columns' is provided
        if columns:
            # Validate columns exist in the model
            valid_columns = [getattr(self.model, col) for col in columns if hasattr(self.model, col)]
            if not valid_columns:
                raise ValueError(f"Invalid columns specified: {columns}")
            query = query.with_entities(*valid_columns)

        # Apply AND filters
        if filters:
            for field, value in filters.items():
                # Handle range filter (BETWEEN)
                if isinstance(value, dict) and 'min' in value and 'max' in value:
                    query = query.filter(getattr(self.model, field).between(value['min'], value['max']))
                # Handle "greater than" or "less than" comparisons
                elif isinstance(value, tuple) and len(value) == 2:
                    operator, val = value
                    if operator == ">":
                        query = query.filter(getattr(self.model, field) > val)
                    elif operator == "<":
                        query = query.filter(getattr(self.model, field) < val)
                    elif operator == "=":
                        query = query.filter(getattr(self.model, field) == val)
                # Handle string matching with LIKE (case-insensitive)
                elif isinstance(value, str) and "%" in value:
                    query = query.filter(getattr(self.model, field).ilike(value))
                # Exact match
                else:
                    query = query.filter(getattr(self.model, field) == value)

        # Apply OR filters
        if or_filters:
            or_conditions = []
            for field, value in or_filters.items():
                # Handle range filter (BETWEEN)
                if isinstance(value, dict) and 'min' in value and 'max' in value:
                    or_conditions.append(getattr(self.model, field).between(value['min'], value['max']))
                # Handle "greater than" or "less than" comparisons
                elif isinstance(value, tuple) and len(value) == 2:
                    operator, val = value
                    if operator == ">":
                        or_conditions.append(getattr(self.model, field) > val)
                    elif operator == "<":
                        or_conditions.append(getattr(self.model, field) < val)
                    elif operator == "=":
                        or_conditions.append(getattr(self.model, field) == val)
                # Handle string matching with LIKE (case-insensitive)
                elif isinstance(value, str) and "%" in value:
                    or_conditions.append(getattr(self.model, field).ilike(value))
                # Exact match
                else:
                    or_conditions.append(getattr(self.model, field) == value)

            # Apply OR condition to the query
            if or_conditions:
                query = query.filter(or_(*or_conditions))

        # Return all matched records
        return query.all()

