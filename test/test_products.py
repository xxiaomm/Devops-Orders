import os , logging
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
from service.products import ProductService
from service.models import db, ProductModel
from service.routes import app

logging.disable(logging.CRITICAL)
BASE_URL = "/products"
CONTENT_TYPE_JSON = "application/json"
######################################################################
#  <your resource name>   P R O D U C T S   T E S T   C A S E S
######################################################################
class TestProducts(unittest.TestCase):
    """ Test Cases for Product Class """

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

    def test_index_page_success(self):
        self.assertNotEqual(ProductService.index_page(), None)
    
    def test_get_all_products_success(self):
        self.assertNotEqual(ProductService.get_all_products(), "")  
    
    def test_create_product_success(self):
        ProductService.create_product("Demo", 35, "Demo Description")        

    def test_success_find_product_by_id(self):
        data = ProductService.create_product("Demo", 35, "Description")
        self.assertEqual(len(ProductService.find_product_by_id(data['id']))>0, True) 

    def test_success_find_product_by_name(self):
        data = ProductService.create_product("Demo_Name", 35, "Description")
        self.assertEqual(len(ProductService.find_product_by_name(data['name']))>0, True)      
        
    def test_failure_find_product_by_id(self):
        self.assertEqual(ProductService.find_product_by_id(-1), None)

    def test_failure_find_product_by_name(self):
        self.assertEqual(len(ProductService.find_product_by_name(-1))==0, True)

    def test_update_product_success(self):
        data = ProductService.create_product("Demo", 35, "Description")
        self.assertEqual(len(data)>0, True)
        self.assertEqual(len(ProductService.update_product(data['id'], "Demo1", 351, "Description1"))>0, True)
        
    def test_update_product_failure(self):
        self.assertEqual(ProductService.update_product("Demo", "Demo", "Demo","Demo"), None)
        self.assertEqual(ProductService.update_product(-1, -1, -1,-1), None)

    def test_increament_like_product_success(self):
        data = ProductService.create_product("Demo", 35, "Description")
        self.assertEqual(len(data)>0, True)
        self.assertEqual(len(ProductService.increament_product_like(data['id']))>0, True)
    
    def test_decreament_like_product_success(self):
        data = ProductService.create_product("Demo", 35, "Description")
        self.assertEqual(len(data)>0, True)
        self.assertEqual(len(ProductService.decreament_product_like(data['id']))>0, True)
    
    
    def test_delete_product_success(self):
        data = ProductService.create_product("Demo", 35, "Description")
        self.assertEqual(len(data)>0, True)
        prev_len = len(ProductModel.get_products())
        ProductService.delete_product(data['id'])
        self.assertEqual(prev_len-1, len(ProductModel.get_products()))


    def test_disable_product_success(self):
        data = ProductService.create_product("Demo", 35, "Description")
        self.assertEqual(len(data)>0, True)
        self.assertEqual(len(ProductService.disable_product(data['id']))>0, True)
        
    def test_disable_product_failure(self):
        self.assertEqual(ProductService.disable_product(-1), None)

    def test_enable_product_success(self):
        data = ProductService.create_product("Demo", 35, "Description")
        self.assertEqual(len(data)>0, True)
        self.assertEqual(len(ProductService.enable_product(data['id']))>0, True)
        
    def test_enable_product_failure(self):
        self.assertEqual(ProductService.enable_product(-1), None)

if __name__ == '__main__':
    unittest.main()