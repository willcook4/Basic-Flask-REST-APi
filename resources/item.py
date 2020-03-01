# sys for debugging
# import sys

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
  # NOTE it is not self.parser, parser belongs to the class not an instance of the clas
  parser = reqparse.RequestParser()
  # We only define price as a parser argument
  # so a user can only set the price of an item:
  parser.add_argument('price', 
    type=float,
    required=True,
    help="This field cannot be left blank")
  
  parser.add_argument('store_id', 
    type=int,
    required=True,
    help="Every item needs a store id")

  # @jwt_required(), decorator means the jwt rquest token must be vaild and provided to use this method
  @jwt_required()
  def get(self, name):
    item = ItemModel.find_by_name(name)
    if item:
      return item.json()
    return {'message': 'Item not found'}, 404

  @jwt_required()
  def post(self, name):
    # if name is found (not None), already exists
    if ItemModel.find_by_name(name):
      return { 'message': f"An item with name {name} already exists" }, 400
    
    data = Item.parser.parse_args()

    item = ItemModel(name, **data)
    
    try:
      item.save_to_db()
    except:
      return {'message': 'An error occurred inserting the item'}, 500
    return item.json(), 201

  @jwt_required()
  def delete(self, name):
    item = ItemModel.find_by_name(name)
    if item:
      item.delete_from_db()
    
    return { 'message': 'Item deleted' } 

  @jwt_required()
  def put(self, name):
    data = Item.parser.parse_args()

    item = ItemModel.find_by_name(name)
    
    if item is None:
      item = ItemModel(name, **data)
    else:
      try:
        item.price = data['price']
      except:
        return {'message': 'an error occured inserting the item'}, 500
    
    item.save_to_db()
    return item.json()

class ItemList(Resource):
  def get(self):
    return { 'items': [item.json() for item in ItemModel.query.all()] }
