from flask import Flask, render_template, url_for
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import InvalidRequestError

db = SQLAlchemy()
class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass
class ProductModel(db.Model):
    app = None
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Float, nullable = False)
    is_active = db.Column(db.Boolean, unique=False, default=True)
    like = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Task %r>' %self.id

    @staticmethod
    def init_db(app):
        ProductModel.app = app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  

    def save_to_db(new_product):
        try:
            db.session.add(new_product)
            db.session.commit()
        except InvalidRequestError:
            db.session.rollback()
        
    def get_products():
        return ProductModel.query.order_by(ProductModel.creation_date).all()

    def delete_from_db(request):
        
        try:
            db.session.delete(request)
            db.session.commit()
        except Exception:
            db.session.rollback()
            
    def serialize(self):
        return {
            "id": self.id, 
            "name": self.name,
            "description": self.description,
            "creation_date": self.creation_date,
            "price": self.price,
            "is_active": self.is_active,
            "like" : self.like
        }

    def deserialize(self, data):
        try:
            self.name = data["name"]
            self.description = data["description"]
            self.price = data["price"]
            self.id = data["id"]
            self.creation_date = data["creation_date"]
            self.is_active = data['is_active']
            self.like = data["like"]

        except KeyError as error:
            raise DataValidationError(
                "Invalid Product: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid Product: body of request contained bad or no data"
            )
        return self

    @classmethod        
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).all()
        
    @classmethod        
    def find_by_id(cls,id):
        product = cls.query.filter_by(id=id).first()
        return product
    
    @classmethod
    def query_by_price(cls, minimum, maximum):
        return cls.query.filter(cls.price.between(minimum, maximum))    

def init_db(app):
    ProductModel.init_db(app)