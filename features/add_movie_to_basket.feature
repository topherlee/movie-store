Feature: Add movie to basket
  # Confirm that we can browse the movie list page, select a movie and add to basket

  Scenario: Success for adding a movie to the basket
    Given I navigate to the movie list page
    When I choose a movie and click on it
    When I click on add to basket
    Then I should see the movie title on the cart page

