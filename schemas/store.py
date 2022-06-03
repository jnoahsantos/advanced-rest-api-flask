from ma import ma 
from models.store import StoreModel
from models.item import ItemModel
from schemas.item import ItemSchema


class StoreSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Neste(ItemSchema, many=True)
    class Meta:
        model = StoreModel
        load_only = ("store",)
        dump_only = ("id")
        load_istance = True
        include_fk = True
