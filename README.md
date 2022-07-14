# products

[![TDD Tests](https://github.com/products-devops-fall-21/products/actions/workflows/tdd-tests.yml/badge.svg)](https://github.com/products-devops-fall-21/products/actions/workflows/tdd-tests.yml)
[![BDD Tests](https://github.com/products-devops-fall-21/products/actions/workflows/bdd-tests.yml/badge.svg)](https://github.com/products-devops-fall-21/products/actions/workflows/bdd-tests.yml)
[![codecov](https://codecov.io/gh/products-devops-fall-21/products/branch/main/graph/badge.svg?token=B6SCHVQSB5)](https://codecov.io/gh/products-devops-fall-21/products)

### Setting up the development environment
Install [Git](http://git-scm.com/downloads) for using bash commands.
To setup the development environment, we use [Vagrant](https://www.vagrantup.com/downloads) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads). The recommended code editor is [Visual Studio Code](https://code.visualstudio.com/).

The Vagrantfile installs all of the needed software to run the service. You can clone this github repository and follow the given commands to start running the service:
 
```bash
git clone https://github.com/products-devops-fall-21/products.git  

cd products     

#to set up the environment variables
cp dot-env .env

#bring up the vm
vagrant up 

#open a shell inside the vm
vagrant ssh 

cd /vagrant

honcho start


[---------------------------------------------------------
    Can also use to run same step:
    python run.py
---------------------------------------------------------]
#At this point the website will be live

#exit out of the vm shell back to your host computer
exit 

#shutdown the vm to return later with vagrant up
vagrant halt 
```



search [0.0.0.0:8080](http://0.0.0.0:8080) on browser to access the website and find the URL for accessing '/products' page.

### The Database for products has following columns:
| Column | Type | Description
| :--- | :--- | :--- |
| id | Integer | ID (automatically given by database) 
| name | String | Name of the product
| description | String | Description of product
| creation_date | DateTime | Creation date and time of product
| price | Float | Price of product
| is_active | Boolean | Status of product (disabled if false)
| like  | Integer | Likes on product

### API Documentation

 |                 URL                 | HTTP Method |                         Description                          | HTTP Return Code |
| :---------------------------------: | :---------: | :----------------------------------------------------------: | :---------------:|
|              /           |   **GET**   |              The Name of Rest API service, the version and URL to list all products             |  HTTP_200_OK |
|              /products              |   **GET**   |              Returns a list all of the products              | HTTP_200_OK |
|           /products/{id}            |   **GET**   |             Returns the product with a given id in JSON format             | HTTP_200_OK |
|              /products?minimum={min_price}&maximum={max_price}              |   **GET**   |              Returns a list all of the products whose price lay within minimum and maximum range             | HTTP_200_OK |
|              /products?name={name}             |   **GET**   |              Returns a list all of the products whose name matches the given name             | HTTP_200_OK |
|              /products              |  **POST**   | creates a new product with ID and creation date auto assigned by the Database and adds it to the products list | HTTP_201_CREATED |
|           /products/{id}            |   **PUT**   | updates the product with given id with the credentials specified in the request |  HTTP_200_OK |
|              /products/{id}/disable              |   **PUT**   |              Disables status of product (sets is_active to false) & sends appropriate notification              | HTTP_200_OK |
|              /products/{id}/enable              |   **PUT**   |              Re-enables status of product (sets is_active to true) & sends appropriate notification              | HTTP_200_OK |
|              /products/{id}/like              |   **PUT**   |             Increments the like attribute of product by 1              | HTTP_200_OK |
|              /products/{id}/dislike              |   **PUT**   |             Decrements the like attribute of product by 1              | HTTP_200_OK |
|           /products/{id}            | **DELETE**  |           deletes a product record from the database           | HTTP_204_NO_CONTENT |

### Testing
#### TDD
Use the following commands to run the test cases:

Mac: 
```
nosetests
```
Windows: 
```
nosetests --exe
```

As of now we are able to receive 95% test coverage.

#### BDD
Use the following command to run the behave tests:
[After doing ```honcho start``` in one terminal, write this command in another terminal]-
```
behave
```

### Cloud URLs
1. The URL of your service running on IBM Cloud in dev:
https://nyu-product-service-fall2103.us-south.cf.appdomain.cloud
2. The URL of your service running on IBM Cloud in prod:
https://nyu-product-service-fall2103-production.us-south.cf.appdomain.cloud

### Swagger
API Documentation added and can be accessed using above URLs/apidocs

###  Continuous Delivery Pipeline
Setted up in IBM Cloud, but have to run pipeline manually. Need to start press 'play' button on Build stage to start running the pipeline. All 4 stages- Build, Deploy, Test and Prod working.