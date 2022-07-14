Feature: The product store service back-end
    As a Developer in Products team
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        |      name        |                  description                    |  price   |  
        |     Flowers      |                Good Showpiece                   |  19.99   |
        |      Toys        |            Toys for children aged 3-5           |  8.79    |
        |     Wafers       |        Hot Potato Chips with Barbecue sauce     |  5.99    |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Products REST API Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Burger King"
    And I set the "Description" to "Very good food"
    And I set the "Price" to "4.99"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Description" field should be empty
    And the "Price" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Burger King" in the "Name" field
    And I should see "Very good food" in the "Description" field
    And I should see "4.99" in the "Price" field

Scenario: List all products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "Flowers" in the results
    And I should see "Toys" in the results
    And I should see "Wafers" in the results
    And I should not see "Olives" in the results

Scenario: Search all products with name Toys
    When I visit the "Home Page"
    And I set the "Name" to "Toys"
    And I press the "Search" button
    Then I should see "Toys" in the results
    And I should not see "Flowers" in the results
    And I should not see "Olive" in the results

Scenario: Search all products within given price range
    When I visit the "Home Page"
    And I set the "Minimum Price" to "4.00"
    And I set the "Maximum Price" to "10.00"
    And I press the "Search" button
    Then I should see "Toys" in the results
    And I should see "Wafer" in the results
    And I should not see "Flowers" in the results

Scenario: Delete all products with name Toys
    When I visit the "Home Page"
    And I set the "Name" to "Fevicol"
    And I set the "Description" to "strong adhesive"
    And I set the "Price" to "2.99"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Description" field should be empty
    And the "Price" field should be empty
    When I paste the "Id" field
    And I press the "Delete" button
    Then I should not see "Fevicol" in the results

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "Wafers"
    And I press the "Search" button
    Then I should see "Wafers" in the "Name" field
    And I should see "5.99" in the "Price" field
    When I change "Name" to "cycle"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "cycle" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "cycle" in the results
    Then I should not see "Wafers" in the results

Scenario: Retreive a product
    When I visit the "Home Page"
    And I set the "Name" to "Flowers"
    And I press the "Search" button
    Then I should see "Flowers" in the "Name" field
    And I should see "19.99" in the "Price" field
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Flowers" in the "Name" field
    And I should see "Good Showpiece" in the "Description" field
    And I should see "19.99" in the "Price" field


Scenario: Action endpoint for disabling a product
    When I visit the "Home Page"
    And I set the "Name" to "Flowers"
    And I press the "Search" button
    Then I should see "Flowers" in the "Name" field
    And I should see "19.99" in the "Price" field
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Disable" button
    Then I should see the message "Product has been Disabled!"

