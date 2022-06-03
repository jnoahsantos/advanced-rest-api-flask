from ma import ma 
from models.item import ItemModel
from models.store import StoreModel

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        dump_only = ("id")
        load_istance = True
        include_fk = True

