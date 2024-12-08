from sqlalchemy.orm import Session
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

    def get_all(self):
        return self.db.query(self.model).all()

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
