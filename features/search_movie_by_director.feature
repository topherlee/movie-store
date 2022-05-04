Feature: Search movie by director's name
  # Confirm that we can look for a movie by the director's name

  Scenario: Success for finding a movie by its director's name
    Given I navigate to the home page
    And I put the director's name in the search bar
    And I click radio button to search by director and submit
    When I press the link to the director's page
    Then I should see the correct movie title on the director's page

