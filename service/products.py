from flask import Flask
from service.models import ProductModel
from . import app
class ProductService():

    def index_page():
        products = ProductModel.query.order_by(ProductModel.creation_date).all()
        return products

    def create_product(product_name, product_price, product_description):
        new_product = ProductModel(name = product_name, price = product_price, description = product_description)
        ProductModel.save_to_db(new_product)
        return ProductModel.serialize(new_product)   
    
    def get_all_products():
        products = ProductModel.get_products()
        results = [ProductModel.serialize(product) for product in products]
        return results
    
    def delete_product( id):
        product_to_delete = ProductModel.find_by_id(id)
        if product_to_delete is  None :
            return None
        else :
            ProductModel.delete_from_db(product_to_delete)
            return product_to_delete
            
    def find_product_by_id(id):
        product = ProductModel.find_by_id(id)
        if product is None:
            return None
        return ProductModel.serialize(product)

    def find_product_by_name(name):
        products = ProductModel.find_by_name(name)
        results = [ProductModel.serialize(product) for product in products]
        return results

    def update_product(id, name , price, description):
        
        if type(id) != type(-1):
            id = -1
        product_to_update = ProductModel.find_by_id(id)
        if id < 0:
            return None
        if name != "":
            product_to_update.name = name
        if price !="" and float(price)>=0:
            product_to_update.price = price
        if description!="":
            product_to_update.description = description
        
        ProductModel.save_to_db(product_to_update)
        return ProductModel.serialize(product_to_update)


    def enable_product(id):
        product_to_update = ProductModel.find_by_id(id)
        
        if product_to_update is None:
            return None

        product_to_update.is_active = True
        ProductModel.save_to_db(product_to_update)
        return ProductModel.serialize(product_to_update)
        
        


    def disable_product(id):
        product_to_update = ProductModel.find_by_id(id)
        
        if product_to_update is None:
            return None

        product_to_update.is_active = False
        ProductModel.save_to_db(product_to_update)
        return ProductModel.serialize(product_to_update)

    def query_by_price(minimum, maximum):
        products = ProductModel.query_by_price(minimum, maximum)
        results = [ProductModel.serialize(product) for product in products]
        return results
    
    def increament_product_like(id):
        product_to_update = ProductModel.find_by_id(id)
        product_to_update.like=product_to_update.like+1
        ProductModel.save_to_db(product_to_update)
        return ProductModel.serialize(product_to_update)
    
    def decreament_product_like(id):
        product_to_update = ProductModel.find_by_id(id)
        product_to_update.like=product_to_update.like-1
        ProductModel.save_to_db(product_to_update)
        return ProductModel.serialize(product_to_update)
