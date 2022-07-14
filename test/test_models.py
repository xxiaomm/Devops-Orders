import os , logging
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
import os
from service.models import ProductModel
from service.models import db, ProductModel
from service.routes import app

logging.disable(logging.CRITICAL)
BASE_URL = "/products"
CONTENT_TYPE_JSON = "application/json"

######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
######################################################################
class TestModels(unittest.TestCase):
    """ Test Cases for Model Class """

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.logger.setLevel(logging.CRITICAL)
        ProductModel.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.app = app.test_client()
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_product_success_model(self):
        test_product = ProductModel(name = "Demo", price = 35, description = "Description")
        self.assertNotEqual(test_product, None)
        self.assertEqual(test_product.name, "Demo")
        self.assertEqual(test_product.price, 35)
        self.assertEqual(test_product.description, "Description")
    
    def test_create_product_failure_model(self):
        self.assertRaises(TypeError, ProductModel(price = 35), True)
        self.assertRaises(TypeError, ProductModel(name = "Demo"), True)
        self.assertRaises(TypeError, ProductModel(), True)
        self.assertRaises(TypeError, ProductModel(price = "Demo"), True)
        self.assertRaises(TypeError, ProductModel(name = 35), True)
    
    def test_get_products_success_model(self):
        total_products = ProductModel.get_products() 

    def test_save_to_db_success(self):
        products_before = len(ProductModel.get_products())
        test_product = ProductModel(name = "Demo", price = 35, description = "Description")
        self.assertEqual(ProductModel.save_to_db(test_product), None)
        self.assertEqual(products_before+1, len(ProductModel.get_products()))    

    def test_save_to_db_failure(self):
        self.assertRaises(TypeError, ProductModel.save_to_db("Demo"), True)

    def test_delete_from_db_success(self):
        products_before = len(ProductModel.get_products())
        test_product = ProductModel(name = "Demo", price = 35, description = "Description")
        self.assertEqual(ProductModel.save_to_db(test_product), None)
        self.assertEqual(products_before+1, len(ProductModel.get_products()))
        self.assertEqual(ProductModel.delete_from_db(test_product), None)
        self.assertEqual(products_before, len(ProductModel.get_products()))


    def test_delete_from_db_failure(self):
        self.assertEqual(ProductModel.delete_from_db(None), None)

    def test_serialize_success(self):
        test_product = ProductModel(name = "Demo", price = 35, description = "Description")
        self.assertEqual(test_product.serialize()['id'], test_product.id)
        
    def test_deserialize_success(self):
        test_product = ProductModel(name = "Demo", price = 35, description = "Description")
        data = test_product.serialize()
        prev_id = test_product.id
        test_product.deserialize(data)
        self.assertEqual(test_product.id, prev_id)

    def test_sucess_find_product_by_id_model(self):
        test_product = ProductModel(name = "Demo", price = 35, description = "Description")
        self.assertEqual(ProductModel.save_to_db(test_product), None)
        self.assertNotEqual(ProductModel.find_by_name("Demo"), None)

    def test_find_by_id_success(self):
        test_product = ProductModel(name = "Demo", price = 35, description = "Description")
        self.assertEqual(ProductModel.save_to_db(test_product), None)
        self.assertEqual(ProductModel.find_by_id(test_product.id).id, test_product.id)

    def test_find_by_name_success(self):
        test_product = ProductModel(name = "Demo_Name", price = 35, description = "Description")
        self.assertEqual(ProductModel.save_to_db(test_product), None)
        products = ProductModel.find_by_name(test_product.name)
        for product in products:
            self.assertEqual(product.name, test_product.name)
    

if __name__ == '__main__':
    unittest.main()