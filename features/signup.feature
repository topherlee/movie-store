Feature: Signup 
  # Confirm that we sign up to the site

  Scenario: Success for signing up as member
    Given I navigate to the home page
    And I click on sign up 
    When I enter my details and submit
    Then I should be registered and logged in on the homepage

