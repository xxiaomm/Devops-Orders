import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import logging
import unittest
from datetime import date, datetime

from urllib.parse import quote_plus
from service import status  # HTTP Status Codes
from service.models import db, ProductModel
from service.routes import app
from product_cart import ProductFactory


logging.disable(logging.CRITICAL)
BASE_URL = "/products"
CONTENT_TYPE_JSON = "application/json"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestProductServer(unittest.TestCase):
    """Product Server Tests"""

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

    def test_index(self):
        """Test the Home Page"""
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def _create_products(self, count):
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            resp = self.app.post(
                BASE_URL, 
                json=test_product.serialize(), 
                content_type=CONTENT_TYPE_JSON,
                
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test product"
            )
            new_product = resp.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products


    def test_get_product_list(self):
        """Get a list of Products"""
        self._create_products(5)
        resp = self.app.get( BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)
        resp = self.app.get("/products/yash", content_type=BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_product(self):
        """Get a single Product"""
        # get the id of a product
        test_product = self._create_products(1)[0]
        resp = self.app.get(
            "/products/{}".format(test_product.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_product.name)

    def test_get_product_not_found(self):
        """Get a Product thats not found"""
        resp = self.app.get("/products/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product(self):
        """Create a new Product"""
        test_product = ProductFactory()
        logging.debug(test_product)
        resp = self.app.post(
            BASE_URL, 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON,       
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_product = resp.get_json()
        

        self.assertEqual(new_product["name"], test_product.name, "Names do not match")
        self.assertEqual(
            new_product["description"], test_product.description, "Descripton does not match"
        )
       
        self.assertEqual(
            new_product["price"], test_product.price, "Price does not match"
        )


        # Check that the location header was correct
        resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_product = resp.get_json()
        if new_product:
            if len(new_product) > 0:
                if 'name' in new_product:
                    self.assertEqual(new_product["name"], test_product.name, "Names do not match")
                if 'description' in new_product:
                    self.assertEqual(
                        new_product["description"], test_product.description, "Descripton does not match"
                    )
                if 'price' in new_product:
                    self.assertEqual(
                        new_product["price"], test_product.price, "Price does not match"
                    )

        test_product.name= ""
        resp = self.app.post(
            BASE_URL, 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        #Test a product name > 100 characters
        test_product.name = 'teststringteststringteststringteststringteststringteststringteststringteststringteststringteststring1'
        resp = self.app.post(
            BASE_URL, 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        
        test_product.name = 'Demo'
        test_product.description= ""
        resp = self.app.post(
            BASE_URL, 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        #Test a product description > 250 characters
        test_product.description = 'teststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststring1'
        resp = self.app.post(
            BASE_URL, 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        test_product.description = "Demo product description"
        test_product.price= "gibberish string"
        resp = self.app.post(
            BASE_URL, 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        
        test_product.price= -100
        resp = self.app.post(
            BASE_URL, 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_on_bad_route(self):
        """Test bad methods and route combination"""
        test_product = ProductFactory()
        logging.debug(test_product)
        resp = self.app.post(
            "/products/0", 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON,       
        )
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    

    def test_update_product(self):
        """Update an existing Product"""
        # create a product to update
        test_product = ProductFactory()
        resp = self.app.post(
            BASE_URL, 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = resp.get_json()
        logging.debug(new_product)
        new_product["description"] = "unknown"
        resp = self.app.put(
            "/products/{}".format(new_product["id"]),
            json=new_product,
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product["description"], "unknown")

        #Test a product name > 100 characters
        new_product["name"] = 'teststringteststringteststringteststringteststringteststringteststringteststringteststringteststring1'
        resp = self.app.put(
            "/products/{}".format(new_product["id"]),
            json=new_product,
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        
        new_product["name"] = 'Demo'
        #Test a product description > 250 characters
        new_product["description"] = 'teststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststringteststring1'
        resp = self.app.put(
            "/products/{}".format(new_product["id"]),
            json=new_product,
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        new_product["description"] = "Demo product description"

        new_product["price"] = "gibberish string"
        resp = self.app.put(
            "/products/{}".format(new_product["id"]),
            json=new_product,
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        new_product["price"] = -100
        resp = self.app.put(
            "/products/{}".format(new_product["id"]),
            json=new_product,
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_disable_product(self):
        """Disable an existing Product"""
        # create a product to update
        test_product = ProductFactory()
        resp = self.app.post(
            BASE_URL, 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # disable the product
        new_product = resp.get_json()
        logging.debug(new_product)
        resp = self.app.put(
            "/products/{}/disable".format(new_product["id"]),
            json=new_product,
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product["is_active"], False)

        #Test a disable incorrent product 
       
        resp = self.app.put(
            "/products/{}/disable".format(-1),
            json=new_product,
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_enable_product(self):
        """Enable an existing Product"""
        # create a product to update
        test_product = ProductFactory()
        resp = self.app.post(
            BASE_URL, 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # disable the product
        new_product = resp.get_json()
        logging.debug(new_product)
        resp = self.app.put(
            "/products/{}/enable".format(new_product["id"]),
            json=new_product,
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product["is_active"], True)


        #Test a disable incorrent product 
       
        resp = self.app.put(
            "/products/{}/enable".format(-1),
            json=new_product,
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)  


    def test_delete_product(self):
        """Delete a Product"""
        test_product = self._create_products(1)[0]
        resp = self.app.delete(
            "{0}/{1}".format('/products', test_product.id), 
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "{0}/{1}".format(BASE_URL, test_product.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        test_product.id = -1

        resp = self.app.delete(
            "{0}/{1}".format('/products', test_product.id), 
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_increament_like_product(self):
        """increase the likes of an existing Product"""
        # create a product to update
        test_product = ProductFactory()
        resp = self.app.post(
            BASE_URL, 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # increase the like
        new_product = resp.get_json()
        logging.debug(new_product)
        new_product["description"] = "unknown"
        resp = self.app.put(
            "/products/{}/like".format(new_product["id"]),
            json=new_product,
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product["like"], 1)

        resp = self.app.put(
            "/products/{}/like".format(-1),
            json=new_product,
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_products_by_name(self):
        """List the products by given name"""
        self._create_products(5)
        resp = self.app.get("/products?name=Flowers")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        print(data)
        for d in data:
            self.assertEqual(d['name'], "Flowers")

    def test_list_products_by_price_range(self):
        """List the products in the given price range"""
        self._create_products(5)
        resp = self.app.get("/products?minimum=10&maximum=20000")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        print(data)
        for d in data:
            self.assertGreaterEqual(d['price'], 10)
            self.assertLessEqual(d['price'], 20000)
    
    def test_no_max_for_price_range(self):
        """No maximum price given for listing products"""
        self._create_products(5)
        resp = self.app.get("/products?minimum=10&maximum=")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_min_for_price_range(self):
        """No minimum price given for listing products"""
        self._create_products(5)
        resp = self.app.get("/products?minimum=&maximum=20000")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_decreament_like_product(self):
        """decrease likes of existing Product"""
        # create a product to update
        test_product = ProductFactory()
        resp = self.app.post(
            BASE_URL, 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # decrease the like
        new_product = resp.get_json()
        logging.debug(new_product)
        new_product["description"] = "unknown"
        resp = self.app.put(
            "/products/{}/dislike".format(new_product["id"]),
            json=new_product,
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product["like"], -1)

        resp = self.app.put(
            "/products/{}/dislike".format(-1),
            json=new_product,
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)  

if __name__ =='__main__':
    unittest.main()