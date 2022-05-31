from code.models.item import ItemJSON
from db import db
from typing import Dict, List, Union
from models.item import ItemJSON

storeJSON = Dict[str, Union[int, str, List[ItemJSON]]]
class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True)

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name: str):
        self.name = name

    def json(self) -> storeJSON:
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.json() for item in self.items.all()]
        }

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_all(cls) -> List:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()