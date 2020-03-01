import sqlite3
from db import db

class ItemModel(db.Model):
  __tablename__ = 'items'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80)) #limited to 80 Char
  price = db.Column(db.Float(precision=2)) #2 decial places
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) # linking store id row with an item's store_id, many to one relationship
  store = db.relationship('StoreModel') # join

  def __init__(self, name, price, store_id):
    self.name = name
    self.price = price
    self.store_id = store_id

  def json(self):
    return { 'name': self.name, 'price': self.price }

  @classmethod
  def find_by_name(cls, name):
    # SELECT * FROM items WHERE name=name
    return cls.query.filter_by(name=name).first()

  # upsert 
  def save_to_db(self): 
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
