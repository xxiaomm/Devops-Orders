import factory
from factory.fuzzy import FuzzyChoice
from service.models import ProductModel
import datetime
class ProductFactory(factory.Factory):
	# """ Creates fake products used for testing ""

    id = factory.Sequence(lambda n: n+1)
    name = FuzzyChoice(choices = ["Flowers","Toys", "Wafers", "Toyota", "Macbook Pro"])

    description = FuzzyChoice(choices = ["Good Showpiece", "Toys for children aged 3-5", "Hot Potato Chips with Barbecue sauce","Custom car with great milage", "Refurbished Apple Macbook Pro 13 inches laptop"])
    
    price = FuzzyChoice(choices = [19.99, 8.79, 5.99, 15125.49, 2049.67])
    class Meta:
	    model = ProductModel 

if __name__ == '__main__':
    for _ in range(5):
        product = ProductFactory()
        print(product.serialize())