
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel



class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('store_id', type=int, required=True,
                        help="Every item need a store id!")

    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item["name"] == name:
        #         return item
        # returns a filter object
        # item = next(filter(lambda x: x["name"] == name, items), None)
        # next gives first item matched returned by this could return additional if found
        # next can raise an error if no item found - we could return None if not found
        # return {"item": item}, 200 if item else 404
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404



    @jwt_required()
    def post(self, name):
        # geting the json payload
        # setting force=True - means that you do not want the Contet-Type header
        # will look and set it appropriately
        # silent=True - doesn't give an error but instead returns None
        # ensure we are adding only unique items
        # if next(filter(lambda item: item["name"] == name, items), None):
        #     return {"message": "An item with {} already exists".format(name)}, 400
        # data = request.get_json()
        if ItemModel.find_by_name(name):
            return {"message": "An item with name {} already exists".format(name)}, 404
        data = Item.parser.parse_args()

        # item = {"name": name, "price": data["price"]}
        item = ItemModel(name, data["price"], data["store_id"])
        # items.append(item)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item deleted"}

    @jwt_required()
    def put(self, name):

        data = Item.parser.parse_args()

        # item = next(filter(lambda item: item["name"] == name, items), None)
        item = ItemModel.find_by_name(name)

        if item is None:
            # item = {"name": name, "price": data["price"]}
            # items.append(item)
            item =  ItemModel(name, data["price"], data["store_id"])
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
        #list(map(lambda x: x.json(), ItemModel.query.all()))
