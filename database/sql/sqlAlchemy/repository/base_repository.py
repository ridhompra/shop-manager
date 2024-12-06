from sqlalchemy.orm import Session

class BaseRepository:
    def __init__(self, model, db: Session):
        self.model = model
        self.db = db

    def create(self, obj_in):
        self.db.add(obj_in)
        self.db.commit()
        self.db.refresh(obj_in)
        return obj_in

    def get_all(self):
        return self.db.query(self.model).all()

    def get_by_id(self, id):
        return self.db.query(self.model).filter(self.model.id == id).first()

    def delete(self, id):
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
